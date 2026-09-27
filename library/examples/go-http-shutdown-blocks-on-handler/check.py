import pathlib
import subprocess

root = pathlib.Path(__file__).parent


def run(filename):
    completed = subprocess.run(
        ["go", "run", filename],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
        timeout=10,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr or completed.stdout)
    return completed.stdout.strip()


bad = run("incorrect.go")
if bad != "blocked":
    raise SystemExit(f"incorrect shutdown result: {bad}")
print("incorrect: observed", bad)

good = run("correct.go")
if good != "returned":
    raise SystemExit(f"correct shutdown result: {good}")
print("correct: ok", good)
