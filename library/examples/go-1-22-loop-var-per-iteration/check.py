import pathlib
import subprocess

root = pathlib.Path(__file__).parent


def run(directory):
    completed = subprocess.run(
        ["go", "run", "."],
        cwd=root / directory,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr)
    return completed.stdout.strip()


old = run("old")
if old != "3 3 3":
    raise SystemExit(f"go 1.21 semantics changed: {old}")
print("incorrect: observed", old)

new = run("new")
if new != "0 1 2":
    raise SystemExit(f"go 1.22 semantics changed: {new}")
print("correct: ok", new)
