# Benchmark

50 coding tasks in `eval/taskset.py` and `eval/taskset_rest.py`. Each task has a starter, a reference solution, a check, and one or more expected skill ids. Frontend is the largest group. Five tasks cross areas and expect more than one skill.

## Dry run (no model)

```bash
python3 eval/harness.py dry-run
```

This checks that every starter fails and every reference solution passes. It also routes each prompt with `--k 5` and writes `eval/dry-run.json`.

`pass_rate` and `tokens` are `null`. Those fields stay null until a model is actually called. `top5_hit_rate.new` is the router only: a hit means every expected skill id is in the top five. An abstention is a miss. `top5_hit_rate.old` searches `eval/snapshots/old-skills/` (the catalog from before this library). `top5_hit_rate.none` is 0 because that arm retrieves nothing.

## Running the real comparison

Do this on a machine that can call a model. Do not fill `pass_rate` from a guess.

For each task, and for each arm:

1. **none** — prompt the model with `task["prompt"]` only. Ask it to write the same filenames the solution uses (`answer.py`, `answer.mjs`, `answer.html`, `main.go`, or `Answer.java`).
2. **old** — search `eval/snapshots/old-skills/*/SKILL.md` with the prompt (the harness function `_old_ids` is the same ranking). Paste the top five skill bodies into the prompt, then ask for the same files.
3. **new** — `python3 tools/skillforge.py route "<prompt>" --k 5`. If `confident` is false, use the prompt alone (same as none). If it is true, paste the shown skill files into the prompt.

Write the model's files into a fresh directory, copy that task's `check`, set `SKILL_REPO` to the repo root, and run the task command (`python3 check.py` or `node check.mjs`). Exit 0 is a pass.

Record, per arm:

- pass rate = passes / 50
- top-five hit rate (retrieval only; the dry run already computes this for old and new)
- wall time and token counts from the model API

The reference solutions are the files under each task's `solution` key. They are the ceiling, not a model result. `npm ci --prefix library` and a Chrome binary on `CHROME_PATH` or `/usr/bin/google-chrome` are required for the frontend checks. Go, rustc, and `javac --release 21` are required for those language tasks.
