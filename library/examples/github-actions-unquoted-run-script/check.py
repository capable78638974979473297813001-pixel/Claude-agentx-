import importlib.util
import os
import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(script, message):
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "run.sh"
        path.write_text(script, encoding="utf-8")
        env = os.environ.copy()
        env["MSG"] = message
        return subprocess.run(
            ["bash", str(path)],
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )


message = "hello; echo PWNED"
bad = run(load("incorrect").render(message), message)
if "PWNED" not in bad.stdout.splitlines():
    raise SystemExit(bad.stdout)
print("incorrect: observed", "PWNED")

good = run(load("correct").render(message), message)
if good.stdout.strip() != message:
    raise SystemExit(repr(good.stdout))
print("correct: ok")
