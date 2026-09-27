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
    repo = pathlib.Path(tmp)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "init")
    git(repo, "checkout", "--detach", "HEAD")
    name = load("incorrect").branch_name(repo)
    if name != "HEAD":
        raise SystemExit(name)
    print("incorrect: observed", name)
    symbolic = load("correct").branch_name(repo)
    if symbolic is not None:
        raise SystemExit(symbolic)
    print("correct: ok", "detached")
