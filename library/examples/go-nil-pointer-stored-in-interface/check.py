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
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr)
    return completed.stdout.strip()


bad = run("incorrect.go")
if bad != "typed-nil":
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = run("correct.go")
if good != "nil":
    raise SystemExit(good)
print("correct: ok", good)
