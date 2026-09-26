import importlib.util
import pathlib
import warnings

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def caller(fn):
    return fn()


def filename_of(fn):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        caller(fn)
    if len(caught) != 1:
        raise SystemExit(f"expected 1 warning, got {len(caught)}")
    return pathlib.Path(caught[0].filename).name


bad_name = filename_of(load("incorrect").library_call)
if bad_name != "incorrect.py":
    raise SystemExit(f"stacklevel=1 pointed at {bad_name}")
print("incorrect: observed", bad_name)

good_name = filename_of(load("correct").library_call)
if good_name != "check.py":
    raise SystemExit(f"stacklevel=2 pointed at {good_name}")
print("correct: ok", good_name)
