"""Load verified skills and the kept curated skills into one catalog."""

from __future__ import annotations

import re
from pathlib import Path

from library.model import Skill
from library.textutil import tokenize

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "library" / "skills"
CURATED_DIR = ROOT / ".claude" / "skills"

VERIFIED_AREAS = (
    "frontend",
    "backend",
    "apis",
    "languages",
    "debugging",
    "databases",
    "devops",
    "testing",
    "security",
    "performance",
    "mobile",
    "cli",
    "architecture",
    "refactoring",
    "docs",
    "vcs",
)

_LIST_KEYS = {"triggers", "aliases", "related", "sources", "commands"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    data: dict = {}
    current: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            item = line.split("- ", 1)[1].strip()
            if current is None:
                raise ValueError(f"list item without a key: {line}")
            data.setdefault(current, []).append(item)
            continue
        if ":" not in line:
            raise ValueError(f"bad frontmatter line: {line}")
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"')
        if value == "":
            data[key] = []
            current = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [part.strip() for part in inner.split(",") if part.strip()] if inner else []
            current = None
        else:
            data[key] = value
            current = None
    return data, body


def _as_tuple(value) -> tuple[str, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return (str(value),)


def load_verified(root: Path | None = None) -> list[Skill]:
    base = (root or ROOT) / "library" / "skills"
    skills: list[Skill] = []
    if not base.exists():
        return skills
    for path in sorted(base.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        skill_id = str(meta.get("id") or path.stem)
        area = str(meta.get("area") or path.parent.name)
        topic = str(meta.get("topic") or "")
        task = str(meta.get("task") or "")
        title = str(meta.get("title") or skill_id)
        description = str(meta.get("description") or "")
        triggers = _as_tuple(meta.get("triggers"))
        aliases = _as_tuple(meta.get("aliases"))
        search = " ".join(
            [skill_id, title, description, topic, task, " ".join(triggers), " ".join(aliases), body]
        )
        skills.append(
            Skill(
                id=skill_id,
                name=skill_id,
                area=area,
                topic=topic,
                task=task,
                title=title,
                description=description,
                body=body,
                path=str(path.relative_to(root or ROOT)),
                kind="verified",
                triggers=triggers,
                aliases=aliases,
                related=_as_tuple(meta.get("related")),
                sources=_as_tuple(meta.get("sources")),
                commands=_as_tuple(meta.get("commands")),
                search_text=search,
            )
        )
    return skills


def _curated_area(name: str) -> str:
    if name.startswith("tax-"):
        return "tax"
    return "engineering"


def load_curated(root: Path | None = None) -> list[Skill]:
    base = (root or ROOT) / ".claude" / "skills"
    skills: list[Skill] = []
    if not base.exists():
        return skills
    for path in sorted(base.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        name = str(meta.get("name") or path.parent.name)
        description = str(meta.get("description") or "")
        area = _curated_area(name)
        topic = "tax" if area == "tax" else "general"
        aliases = tuple(dict.fromkeys(tokenize(name.replace("-", " "))))
        search = " ".join([name, description, body])
        skills.append(
            Skill(
                id=name,
                name=name,
                area=area,
                topic=topic,
                task=name,
                title=name,
                description=description,
                body=body,
                path=str(path.relative_to(root or ROOT)),
                kind="curated",
                triggers=(),
                aliases=aliases,
                related=(),
                sources=(),
                commands=(),
                search_text=search,
            )
        )
    return skills


def load_library(root: Path | None = None) -> list[Skill]:
    return load_verified(root) + load_curated(root)


def by_id(skills: list[Skill]) -> dict[str, Skill]:
    return {skill.id: skill for skill in skills}
