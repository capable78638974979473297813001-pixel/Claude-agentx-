import importlib.util
import pathlib

root = pathlib.Path(__file__).parent
rows = [
    {"id": 2, "created": "2024-01-01"},
    {"id": 1, "created": "2024-01-01"},
    {"id": 3, "created": "2024-01-02"},
]


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def walk(module):
    first = module.page(rows, 1, None)
    cursor = (first[0]["created"], first[0]["id"])
    second = module.page(rows, 1, cursor)
    return [first[0]["id"], second[0]["id"]]


bad = walk(load("incorrect"))
if bad != [1, 3]:
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = walk(load("correct"))
if good != [1, 2]:
    raise SystemExit(good)
print("correct: ok", good)
