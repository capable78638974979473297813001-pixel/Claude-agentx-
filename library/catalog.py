"""Layered index: area, then topic, then task."""

from __future__ import annotations

from collections import defaultdict

from library.model import Skill


def skill_tree(skills: list[Skill]) -> dict:
    tree: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for skill in skills:
        tree[skill.area][skill.topic].append(
            {
                "id": skill.id,
                "task": skill.task,
                "title": skill.title,
                "kind": skill.kind,
            }
        )
    return {
        area: {
            topic: sorted(entries, key=lambda item: item["id"])
            for topic, entries in sorted(topics.items())
        }
        for area, topics in sorted(tree.items())
    }


def area_counts(skills: list[Skill], *, kind: str | None = None) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for skill in skills:
        if kind is not None and skill.kind != kind:
            continue
        counts[skill.area] += 1
    return dict(sorted(counts.items()))
