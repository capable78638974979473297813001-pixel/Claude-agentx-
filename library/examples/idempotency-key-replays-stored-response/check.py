import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(post):
    calls = {"n": 0}

    def handler():
        calls["n"] += 1
        return {"id": calls["n"]}

    store = {}
    first = post(store, "abc", handler)
    second = post(store, "abc", handler)
    return calls["n"], first, second


bad_calls, bad_first, bad_second = run(load("incorrect").post)
if bad_calls != 2 or bad_first == bad_second:
    raise SystemExit((bad_calls, bad_first, bad_second))
print("incorrect: observed", bad_calls, bad_second["id"])

good_calls, good_first, good_second = run(load("correct").post)
if good_calls != 1 or good_first != good_second:
    raise SystemExit((good_calls, good_first, good_second))
print("correct: ok", good_calls)
