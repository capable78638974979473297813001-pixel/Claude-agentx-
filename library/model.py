"""A skill record loaded from markdown, not assembled from fill-in slots."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    area: str
    topic: str
    task: str
    title: str
    description: str
    body: str
    path: str
    kind: str  # verified | curated
    triggers: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    related: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    commands: tuple[str, ...] = ()
    search_text: str = ""
    extra: dict[str, str] = field(default_factory=dict)
