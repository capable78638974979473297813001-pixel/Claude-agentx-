import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).parent


def run(class_name):
    with tempfile.TemporaryDirectory() as tmp:
        compiled = subprocess.run(
            ["javac", "--release", "21", "-d", tmp, str(root / f"{class_name}.java")],
            check=False,
            text=True,
            capture_output=True,
        )
        if compiled.returncode != 0:
            raise SystemExit(compiled.stderr)
        completed = subprocess.run(
            ["java", "-cp", tmp, class_name],
            check=False,
            text=True,
            capture_output=True,
        )
        if completed.returncode != 0:
            raise SystemExit(completed.stderr)
        return completed.stdout.strip()


bad = run("Incorrect")
if bad != "npe":
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = run("Correct")
if good != "missing":
    raise SystemExit(good)
print("correct: ok", good)
