---
name: skill-router
description: Search this repo as one skill library. Route a question to a few matching skills, or abstain and reason without a skill when the match is weak. Use when choosing skills, when the user asks what skills exist, or before applying a verified coding note.
---

# Skill router

The library is one catalog. Do not load every skill into context. Ask the router, open the few it returns, and stop there.

```bash
python3 tools/skillforge.py route "the exact error or question" --k 5
python3 tools/skillforge.py browse --area frontend
python3 tools/skillforge.py show react-19-ref-as-prop
python3 tools/skillforge.py stats
```

`search` is an alias of `route`.

## How a match is chosen

The index is layered: area, then topic, then task. Tokens from the query hit triggers, aliases, titles, and bodies. `route` prints `confident: true` and up to `--k` skills, or `confident: false` and `fallback: reason without a skill`.

Abstain when the query is vague (`help me code`, `fix the bug`), when nothing overlaps, when the best score is under the floor, or when two unrelated skills score about the same. In that case write the code from ordinary knowledge. Do not pull a skill just to have one.

## What is in the catalog

- `library/skills/<area>/<id>.md` — verified notes. Each one has a command that prints `incorrect: observed` and `correct: ok`.
- `.claude/skills/*/SKILL.md` — curated tax notes and general engineering notes. Tax was kept and not expanded.
- `forge/lenses/` and `forge/domains/` — reference styles and domain background. The router does not return them.

Related skills are listed in each verified note's frontmatter. A form plus an API plus a database is several ids, not one blended file. Open the ones the router returns that the task actually touches.

## Fallback

If `confident` is false, ignore the library for that step. If it is true, read the skill, apply the cited behavior, and run the skill's command or your own check. A skill that does not match the error message you have is the wrong skill even when the router ranked it.
