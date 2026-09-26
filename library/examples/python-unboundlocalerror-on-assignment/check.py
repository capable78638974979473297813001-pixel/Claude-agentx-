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
    bad.label()
except UnboundLocalError as exc:
    text = str(exc)
    if "cannot access local variable 'count'" not in text:
        raise SystemExit(text)
    print("incorrect: observed")
    print(text)
else:
    raise SystemExit("incorrect function did not raise")

good = load("correct")
if good.label() != 1:
    raise SystemExit("correct function returned the wrong value")
print("correct: ok")
