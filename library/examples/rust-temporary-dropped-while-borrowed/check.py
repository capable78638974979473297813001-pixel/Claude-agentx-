import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).parent


def rustc(source, output):
    return subprocess.run(
        ["rustc", str(source), "-o", str(output)],
        check=False,
        text=True,
        capture_output=True,
    )


with tempfile.TemporaryDirectory() as tmp:
    bad = rustc(root / "incorrect.rs", pathlib.Path(tmp) / "bad")
    if bad.returncode == 0:
        raise SystemExit("incorrect.rs compiled")
    if "error[E0716]" not in bad.stderr:
        raise SystemExit(bad.stderr)
    print("incorrect: observed")
    print(bad.stderr.splitlines()[0])

    binary = pathlib.Path(tmp) / "ok"
    good = rustc(root / "correct.rs", binary)
    if good.returncode != 0:
        raise SystemExit(good.stderr)
    out = subprocess.check_output([binary], text=True).strip()
    if out != "hi":
        raise SystemExit(out)
    print("correct: ok", out)
