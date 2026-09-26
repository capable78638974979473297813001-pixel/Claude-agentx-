# Skill library

One catalog an AI can search. Verified coding notes live in `library/skills/`. Curated tax notes and general engineering notes live in `.claude/skills/`. The router returns a few matches or tells you to reason without a skill.

```bash
python3 tools/skillforge.py route "the error message or question" --k 5
python3 tools/skillforge.py show react-19-ref-as-prop
python3 tools/skillforge.py browse --area frontend
python3 tools/skillforge.py stats
```

`search` is an alias of `route`.

## How an AI should use it

1. **Search.** Put the concrete error, flag, or behavior in the query. `route` looks up an inverted index layered by area, then topic, then task.
2. **Route.** A confident result lists up to `--k` skills (default 5). Open those files. Follow `related` when the task crosses areas (a form, an API, auth, a database).
3. **Fall back.** If the router prints `confident: false` and `fallback: reason without a skill`, do not pull a skill. Answer from ordinary knowledge. Vague prompts (`help me code`, `fix the bug`) and close races between unrelated low scores abstain. Two strong matches in different areas are returned together.

Lenses in `forge/lenses/` and domain notes in `forge/domains/` are reference material. The router does not search them.

## What is verified

Each file under `library/skills/<area>/<id>.md` has incorrect and correct code, a command, and at least one official source URL. `python3 tools/skillforge.py validate` checks the schema, banned filler, near-duplicate bodies, source URLs, and runs every example. An example passes only when it prints both `incorrect: observed` and `correct: ok`.

The verified count is whatever `stats` prints. Quality rules outrank filling the catalog toward 10,000. Notes that could not be executed in this environment were not added.

Verified areas are frontend, backend, APIs, languages, debugging, databases, DevOps, testing, security, performance, mobile, CLIs, architecture, refactoring, documentation, and version control. Frontend topics include frameworks, components, state, CSS, accessibility, forms, routing, testing queries, build tooling, and layout performance. `python3 tools/skillforge.py browse --area frontend` lists them.

Tax skills were kept as one section and were not expanded. Money in those notes is decimal or integer minor units. Rates and thresholds come from a cited source or stay `UNVERIFIED`.

## Layout

| Path | What |
|---|---|
| `library/skills/` | Verified coding skills |
| `library/examples/` | Programs the validator runs |
| `library/router.py` | Index and abstaining router |
| `.claude/skills/` | Curated tax and engineering notes |
| `forge/lenses/` | General working styles, not routed |
| `forge/domains/` | Domain background, not routed |
| `eval/` | 50-task benchmark and the old-skill snapshot |
| `catalog/index.json` | Generated area → topic → task index |

## Checks

```bash
python3 -m unittest discover -s tools -v
python3 tools/skillforge.py validate
python3 eval/harness.py dry-run
```

Node dependencies for the browser and framework examples install with `npm ci --prefix library`. See `eval/README.md` for the benchmark. The dry run does not call a model and does not invent pass rates.
