import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


try:
    load("incorrect").convert("nope")
except RuntimeError as exc:
    if not isinstance(exc.__context__, ValueError):
        raise SystemExit("missing implicit context")
    if exc.__cause__ is not None:
        raise SystemExit("implicit context was stored as __cause__")
    print("incorrect: observed")
    print(type(exc.__context__).__name__)
else:
    raise SystemExit("incorrect did not raise")

try:
    load("correct").convert("nope")
except RuntimeError as exc:
    if exc.__cause__ is not exc.__context__:
        raise SystemExit("explicit cause was not linked")
    if not isinstance(exc.__cause__, ValueError):
        raise SystemExit(type(exc.__cause__))
    print("correct: ok")
else:
    raise SystemExit("correct did not raise")
