import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect").rows()
first = list(bad)
second = list(bad)
if first != ["a", "b"] or second != []:
    raise SystemExit((first, second))
print("incorrect: observed", second)

good = load("correct").rows()
if list(good) != ["a", "b"] or list(good) != ["a", "b"]:
    raise SystemExit("list result was not reusable")
print("correct: ok")
