#!/usr/bin/env python3
"""Benchmark harness for the skill library.

`dry-run` does not call a model. It checks that every task fails on its starter
and passes on its reference solution, and it records router top-5 hit rate.
Pass rate and token counts stay null until someone runs a model. See eval/README.md.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.taskset import TASKS  # noqa: E402
from library.load import load_library  # noqa: E402
from library.router import Router  # noqa: E402
from library.textutil import tokenize  # noqa: E402

WORK = ROOT / "eval" / "work"
SNAPSHOT = ROOT / "eval" / "snapshots" / "old-skills"
EXPECTED_AREAS = {
    "frontend": 14,
    "cross": 5,
    "languages": 6,
    "apis": 4,
    "databases": 3,
    "security": 3,
    "backend": 2,
    "debugging": 2,
    "devops": 2,
    "testing": 2,
    "vcs": 1,
    "cli": 1,
    "architecture": 1,
    "refactoring": 1,
    "docs": 1,
    "performance": 1,
    "mobile": 1,
}


def _run(task: dict, variant: str) -> subprocess.CompletedProcess[str]:
    dest = WORK / task["id"] / variant
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    files = task["starter"] if variant == "starter" else task["solution"]
    for name, content in {**files, task["check_name"]: task["check"]}.items():
        text = content if content.endswith("\n") else content + "\n"
        (dest / name).write_text(text, encoding="utf-8")
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["SKILL_REPO"] = str(ROOT)
    return subprocess.run(
        task["command"],
        cwd=dest,
        check=False,
        text=True,
        capture_output=True,
        timeout=task.get("timeout", 60),
        env=env,
    )


def _old_ids(query: str, k: int = 5) -> list[str]:
    terms = [tok for tok in tokenize(query) if len(tok) > 2]
    scored: list[tuple[int, str]] = []
    for path in sorted(SNAPSHOT.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8").lower()
        score = sum(text.count(term) for term in terms)
        if score:
            scored.append((score, path.parent.name))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [name for _score, name in scored[:k]]


def _hit(found: list[str], expected: list[str]) -> bool:
    return all(skill_id in found[:5] for skill_id in expected)


def dry_run() -> dict:
    counts: dict[str, int] = {}
    for task in TASKS:
        counts[task["area"]] = counts.get(task["area"], 0) + 1
    if counts != EXPECTED_AREAS:
        raise SystemExit(f"task area counts {counts} != {EXPECTED_AREAS}")
    if len(TASKS) != 50:
        raise SystemExit(f"expected 50 tasks, found {len(TASKS)}")
    ids = [task["id"] for task in TASKS]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate task id")

    skills = load_library(ROOT)
    router = Router(skills)
    starter_fail = 0
    solution_pass = 0
    failures: list[str] = []
    new_hits = 0
    old_hits = 0
    route_seconds = 0.0
    misses: list[dict] = []
    for task in TASKS:
        starter = _run(task, "starter")
        solution = _run(task, "solution")
        if starter.returncode != 0:
            starter_fail += 1
        else:
            failures.append(f"{task['id']}: starter passed\n{starter.stdout[-400:]}\n{starter.stderr[-400:]}")
        if solution.returncode == 0:
            solution_pass += 1
        else:
            failures.append(
                f"{task['id']}: solution failed ({solution.returncode})\n"
                f"{solution.stdout[-500:]}\n{solution.stderr[-500:]}"
            )
        started = time.perf_counter()
        routed = router.route(task["prompt"], k=5)
        route_seconds += time.perf_counter() - started
        found = [hit.skill_id for hit in routed.hits] if routed.confident else []
        if _hit(found, task["expected_skills"]):
            new_hits += 1
        else:
            misses.append(
                {
                    "id": task["id"],
                    "expected": task["expected_skills"],
                    "confident": routed.confident,
                    "found": found,
                    "reason": routed.reason,
                }
            )
        if _hit(_old_ids(task["prompt"]), task["expected_skills"]):
            old_hits += 1
    report = {
        "model_invoked": False,
        "tasks": len(TASKS),
        "areas": counts,
        "pass_rate": {"none": None, "old": None, "new": None},
        "top5_hit_rate": {
            "none": 0.0,
            "old": old_hits / len(TASKS),
            "new": new_hits / len(TASKS),
        },
        "top5_hits": {"none": 0, "old": old_hits, "new": new_hits},
        "tokens": None,
        "route_seconds": round(route_seconds, 4),
        "dry_run": {
            "starter_failures": starter_fail,
            "solution_passes": solution_pass,
            "ok": starter_fail == len(TASKS) and solution_pass == len(TASKS),
        },
        "router_misses": misses,
        "note": (
            "pass_rate and tokens are null because no model was called. "
            "top5_hit_rate.new is the router only. "
            "A hit requires every expected skill id to appear in the top 5. "
            "An abstention counts as a miss."
        ),
    }
    out = ROOT / "eval" / "dry-run.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("\n".join(failures))
        print(json.dumps({k: report[k] for k in ("dry_run", "top5_hit_rate")}, indent=2))
        return report
    print(json.dumps({k: report[k] for k in ("dry_run", "top5_hit_rate", "route_seconds", "tasks")}, indent=2))
    print(f"wrote {out.relative_to(ROOT)}")
    return report


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    command = args[0] if args else "dry-run"
    if command != "dry-run":
        print("usage: python3 eval/harness.py dry-run", file=sys.stderr)
        return 2
    report = dry_run()
    return 0 if report["dry_run"]["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
