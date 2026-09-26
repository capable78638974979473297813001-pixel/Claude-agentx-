import importlib.util
import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        text=True,
        capture_output=True,
    )


with tempfile.TemporaryDirectory() as tmp:
    src = pathlib.Path(tmp) / "src"
    src.mkdir()
    git(src, "init", "-q")
    git(src, "config", "user.email", "t@example.com")
    git(src, "config", "user.name", "t")
    (src / "a.txt").write_text("a\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "init")
    git(src, "tag", "-a", "v1.2.3", "-m", "v1.2.3")
    (src / "a.txt").write_text("a\nb\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "second")
    shallow = pathlib.Path(tmp) / "shallow"
    subprocess.run(
        ["git", "clone", "--depth", "1", "--quiet", f"file://{src}", str(shallow)],
        check=True,
        text=True,
        capture_output=True,
    )
    described = load("incorrect").describe(shallow)
    if described.returncode == 0:
        raise SystemExit(described.stdout)
    message = described.stderr.strip()
    if message != "fatal: No names found, cannot describe anything.":
        raise SystemExit(message)
    print("incorrect: observed", message)
    full = load("correct").describe(src)
    if not full.stdout.startswith("v1.2.3-1-g"):
        raise SystemExit(full.stdout)
    print("correct: ok", full.stdout.strip().split("-g")[0])
