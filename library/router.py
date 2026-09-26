"""Layered lookup and a router that abstains when it is not confident.

Search is an inverted index over titles, triggers, aliases, and skill text.
If the best hit is weak or tied with an unrelated skill, the result is not
confident and the caller should reason without a skill.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from dataclasses import dataclass

from library.model import Skill
from library.textutil import STOPWORDS, contains_phrase, tokenize

# Extra generics that show up in coding questions and should not carry a match.
GENERIC = STOPWORDS | frozenset(
    """
    skill skills library using via per each our their into within without
    across around after before during still also only really very more most
    less many much same other another new old good bad
    """.split()
)

MIN_SCORE = 8.0
MIN_MARGIN = 1.28
MIN_CONTENT_TOKENS = 2
# A close race between unrelated skills is ambiguous when the scores are only
# moderate. Two high scores in different areas mean the question names both
# problems, so return the top few instead of abstaining.
STRONG_SCORE = 40.0


@dataclass(frozen=True)
class RouteHit:
    skill_id: str
    title: str
    area: str
    topic: str
    task: str
    score: float
    matched: tuple[str, ...]


@dataclass(frozen=True)
class RouteResult:
    confident: bool
    reason: str
    hits: tuple[RouteHit, ...]

    def as_dict(self) -> dict:
        return {
            "confident": self.confident,
            "reason": self.reason,
            "fallback": None if self.confident else "reason without a skill",
            "hits": [
                {
                    "id": hit.skill_id,
                    "title": hit.title,
                    "area": hit.area,
                    "topic": hit.topic,
                    "task": hit.task,
                    "score": round(hit.score, 2),
                    "matched": list(hit.matched),
                }
                for hit in self.hits
            ],
        }


class Router:
    def __init__(self, skills: list[Skill]):
        self.skills = {skill.id: skill for skill in skills}
        self._order = [skill.id for skill in skills]
        self._df: dict[str, int] = defaultdict(int)
        self._postings: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self._phrases: list[tuple[str, str]] = []
        n = len(skills)
        for skill in skills:
            weights: dict[str, float] = defaultdict(float)
            for tok in tokenize(skill.topic.replace("-", " ")):
                weights[tok] = max(weights[tok], 4.0)
            for alias in skill.aliases:
                for tok in tokenize(alias):
                    weights[tok] = max(weights[tok], 5.0)
            for tok in tokenize(skill.task.replace("-", " ")):
                weights[tok] = max(weights[tok], 3.0)
            for tok in tokenize(skill.title):
                weights[tok] = max(weights[tok], 1.5)
            for trigger in skill.triggers:
                self._phrases.append((trigger.lower(), skill.id))
                for tok in tokenize(trigger):
                    weights[tok] = max(weights[tok], 2.5)
            for tok in tokenize(skill.description):
                weights[tok] = max(weights[tok], 2.0)
            for tok in tokenize(skill.body):
                weights[tok] = max(weights[tok], 1.0)
            for tok, weight in weights.items():
                if tok in GENERIC or len(tok) < 2:
                    continue
                self._postings[tok].append((skill.id, weight))
                self._df[tok] += 1
        self._idf = {
            tok: math.log((n + 1) / (df + 1)) + 1.0 for tok, df in self._df.items()
        }
        self._n = n

    def browse(self, area: str | None = None, topic: str | None = None) -> dict:
        """Layered index: area, then topic, then task."""
        tree: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
        for skill_id in self._order:
            skill = self.skills[skill_id]
            tree[skill.area][skill.topic].append(skill.task)
        if area is None:
            return {
                name: {"topics": len(topics), "skills": sum(len(v) for v in topics.values())}
                for name, topics in tree.items()
            }
        if area not in tree:
            raise KeyError(area)
        if topic is None:
            return {
                name: {"skills": len(tasks), "tasks": tasks}
                for name, tasks in tree[area].items()
            }
        if topic not in tree[area]:
            raise KeyError(topic)
        return {"area": area, "topic": topic, "tasks": tree[area][topic]}

    def route(self, query: str, k: int = 3) -> RouteResult:
        tokens = [tok for tok in tokenize(query) if tok not in GENERIC and len(tok) > 1]
        unique_tokens = list(dict.fromkeys(tokens))
        phrase_hits: dict[str, list[str]] = defaultdict(list)
        query_lower = query.lower()
        for phrase, skill_id in self._phrases:
            if len(tokenize(phrase)) < 2:
                continue
            if contains_phrase(query_lower, phrase):
                phrase_hits[skill_id].append(phrase)

        if len(unique_tokens) < MIN_CONTENT_TOKENS and not phrase_hits:
            return RouteResult(False, "query is too vague to choose a skill", ())

        scores: dict[str, float] = defaultdict(float)
        matched: dict[str, list[str]] = defaultdict(list)
        for tok in unique_tokens:
            idf = self._idf.get(tok)
            if idf is None:
                continue
            for skill_id, weight in self._postings.get(tok, ()):
                scores[skill_id] += weight * idf
                matched[skill_id].append(tok)
        for skill_id, phrases in phrase_hits.items():
            scores[skill_id] += 9.0 * len(phrases)
            matched[skill_id].extend(phrases)

        if not scores:
            return RouteResult(False, "no skill token overlaps this query", ())

        ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        best_id, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0
        best = self.skills[best_id]

        if best_score < MIN_SCORE:
            return RouteResult(
                False,
                f"best score {best_score:.1f} is below the confidence floor",
                (),
            )

        distinctive = [tok for tok in matched[best_id] if tok not in GENERIC]
        if len(distinctive) < MIN_CONTENT_TOKENS and best_id not in phrase_hits:
            return RouteResult(False, "match uses only generic words", ())

        same_topic_margin = True
        if second_score and best_score < second_score * MIN_MARGIN:
            second = self.skills[ranked[1][0]]
            unrelated = second.topic != best.topic or second.area != best.area
            if unrelated and best_score < STRONG_SCORE:
                same_topic_margin = False
        if not same_topic_margin:
            return RouteResult(
                False,
                "several unrelated skills match about equally; not confident",
                (),
            )

        hits = []
        for skill_id, score in ranked[:k]:
            skill = self.skills[skill_id]
            hits.append(
                RouteHit(
                    skill_id=skill.id,
                    title=skill.title,
                    area=skill.area,
                    topic=skill.topic,
                    task=skill.task,
                    score=score,
                    matched=tuple(dict.fromkeys(matched[skill_id])),
                )
            )
        return RouteResult(True, "top match clears the score floor and the margin", tuple(hits))


def format_route(result: RouteResult) -> str:
    lines = [
        f"confident: {str(result.confident).lower()}",
        f"reason: {result.reason}",
    ]
    if not result.confident:
        lines.append("fallback: reason without a skill")
        return "\n".join(lines)
    for index, hit in enumerate(result.hits, start=1):
        lines.append(
            f"{index}. {hit.skill_id}  {hit.score:.1f}  {hit.title}"
        )
    lines.append("Open one with: python3 tools/skillforge.py show <id>")
    return "\n".join(lines)


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query).strip()
