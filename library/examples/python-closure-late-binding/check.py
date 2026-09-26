import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = [fn() for fn in load("incorrect").multipliers(3)]
if bad != [2, 2, 2]:
    raise SystemExit(f"unexpected late binding result {bad}")
print("incorrect: observed", bad)

good = [fn() for fn in load("correct").multipliers(3)]
if good != [0, 1, 2]:
    raise SystemExit(f"unexpected bound result {good}")
print("correct: ok", good)
