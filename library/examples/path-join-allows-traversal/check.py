import importlib.util
import os
import pathlib
import tempfile

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect")
good = load("correct")
with tempfile.TemporaryDirectory() as tmp:
    base = os.path.join(tmp, "uploads")
    os.makedirs(base)
    os.makedirs(os.path.join(tmp, "uploads-evil"))
    user_path = os.path.join("..", "uploads-evil", "x.txt")
    resolved = bad.resolve(base, user_path)
    if not bad.is_inside(base, resolved):
        raise SystemExit(f"prefix check rejected the escape: {resolved}")
    if not resolved.endswith(os.path.join("uploads-evil", "x.txt")):
        raise SystemExit(resolved)
    print("incorrect: observed", os.path.basename(os.path.dirname(resolved)))
    try:
        good.resolve(base, user_path)
    except ValueError as exc:
        print("correct: ok", exc)
    else:
        raise SystemExit("escape was accepted")
