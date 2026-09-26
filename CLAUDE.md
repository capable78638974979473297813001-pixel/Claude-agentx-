# Skill library

Search this repo as one library. Do not load every skill, and do not spawn a team of agents.

## Search, route, fall back

1. Run `python3 tools/skillforge.py route "<question>" --k 5`.
2. If the output says `confident: true`, read the listed skills with `python3 tools/skillforge.py show <id>`. Use `related` ids when the task needs more than one area.
3. If the output says `confident: false` and `fallback: reason without a skill`, stop looking in the catalog and answer from ordinary knowledge.

`browse --area <name>` lists topics before you route. `stats` prints the verified and curated counts.

Verified skills are `library/skills/<area>/<id>.md`. Curated tax and engineering notes are `.claude/skills/*/SKILL.md`. Tax notes stay as they are; do not add jurisdictions or years to them. `forge/lenses/` and `forge/domains/` are not skills.

## Where things are

| Path | What |
|---|---|
| `library/skills/` | Verified coding skills, one file each |
| `library/examples/` | Runnable incorrect and correct programs |
| `tools/skillforge.py` | `stats`, `list`, `show`, `route`, `browse`, `validate`, `index`, `banner` |
| `.claude/skills/` | Curated tax section and engineering notes |
| `eval/` | Benchmark tasks, harness, old skill snapshot |
| `catalog/index.json` | Generated layered index |

```bash
python3 tools/skillforge.py route "foreign key pragma"
python3 tools/skillforge.py validate
python3 -m unittest discover -s tools
python3 eval/harness.py dry-run
```

## House rules

- Money is never a float. Use decimal or integer minor units.
- Never invent a legal number (rate, threshold, bracket). Take it from a cited primary source, or mark it `UNVERIFIED`.
- A claim of "done" needs a command that proves it.
- Do not add a verified skill whose example you have not run. Do not paste filler to get past the duplicate check.
