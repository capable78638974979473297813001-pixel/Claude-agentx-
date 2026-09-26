import contextlib
import importlib.util
import io
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect")
stderr = io.StringIO()
try:
    with contextlib.redirect_stderr(stderr):
        bad.parse(["run", "--flag"])
except SystemExit as exc:
    message = stderr.getvalue()
    if exc.code != 2 or "unrecognized arguments: --flag" not in message:
        raise SystemExit(f"expected exit 2 and unrecognized arguments, got {exc.code} {message!r}")
    print("incorrect: observed", exc.code)
else:
    raise SystemExit("unrecognized --flag was accepted")

good = load("correct")
parsed = good.parse(good.command_line("run", ["--flag"]))
if parsed.cmd != "run" or parsed.args != ["--flag"]:
    raise SystemExit(parsed)
print("correct: ok", parsed.args)
