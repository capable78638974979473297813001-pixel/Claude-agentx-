import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad_row = {"name": "a", "version": 1}
bad = load("incorrect")
if bad.update(bad_row, "b", 1) != 200 or bad.update(bad_row, "c", 1) != 200:
    raise SystemExit("stale write was rejected")
if bad_row["version"] != 3 or bad_row["name"] != "c":
    raise SystemExit(bad_row)
print("incorrect: observed", bad_row["version"])

good_row = {"name": "a", "version": 1}
good = load("correct")
if good.update(good_row, "b", 1) != 200:
    raise SystemExit("fresh write failed")
status = good.update(good_row, "c", 1)
if status != 412 or good_row["name"] != "b" or good_row["version"] != 2:
    raise SystemExit((status, good_row))
print("correct: ok", status)
