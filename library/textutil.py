"""Token and similarity helpers for the skill library."""

from __future__ import annotations

import hashlib
import re

WORD_RE = re.compile(r"[a-z0-9]+(?:[.+#-][a-z0-9]+)*", re.IGNORECASE)
FENCE_RE = re.compile(r"```([^\n]*)\n(.*?)```", re.DOTALL)
SHINGLE_N = 5

BANNED_PHRASES = (
    "lorem ipsum",
    "tbd",
    "todo",
    "fixme",
    "something something",
    "as needed",
    "insert here",
    "click here",
    "placeholder text",
    "various factors",
    "best practices",
    "best practice",
    "it's important",
    "it is important",
    "worth noting",
    "keep in mind",
    "in conclusion",
    "make sure to",
    "you should always",
    "in general",
    "don't forget",
    "do not forget",
    "highly recommended",
    "delve into",
    "as we can see",
    "simply put",
    "key takeaway",
    "in summary",
    "to summarize",
    "when it comes to",
    "bear in mind",
    "needless to say",
    "let's dive",
    "we will explore",
    "this guide covers",
    "in this article",
)

STOPWORDS = frozenset(
    """
    a an the of to in on for and or with from by at as is are was were be
    this that these those it its into over under about than then so if
    when while how what which who your you we our their they them my me
    do does did done make made use used using can should must will just
    please help want need app code bug error issue fix update add handle
    write implement create change working work thing things stuff some any
    not no yes skill skills library using via per each our their into within
    without across around after before during still also only really very
    more most less many much same other another new old good bad
    """.split()
)


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def contains_phrase(haystack: str, phrase: str) -> bool:
    needle = tokenize(phrase)
    if not needle:
        return False
    tokens = tokenize(haystack)
    width = len(needle)
    if width > len(tokens):
        return False
    return any(tokens[i : i + width] == needle for i in range(len(tokens) - width + 1))


def shingles(text: str, n: int = SHINGLE_N) -> set[tuple[str, ...]]:
    tokens = tokenize(text)
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def jaccard(left: set[tuple[str, ...]], right: set[tuple[str, ...]]) -> float:
    if not left and not right:
        return 0.0
    union = len(left | right)
    if union == 0:
        return 0.0
    return len(left & right) / union


def body_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def fences(body: str) -> list[tuple[str, str]]:
    return [(info.strip(), content) for info, content in FENCE_RE.findall(body)]
