import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect")
try:
    bad.parse(["run", "--flag"])
except SystemExit as exc:
    if exc.code != 2:
        raise SystemExit(f"expected exit 2, got {exc.code}")
    print("incorrect: observed", exc.code)
else:
    raise SystemExit("unrecognized --flag was accepted")

good = load("correct")
parsed = good.parse(good.command_line("run", ["--flag"]))
if parsed.cmd != "run" or parsed.args != ["--flag"]:
    raise SystemExit(parsed)
print("correct: ok", parsed.args)
