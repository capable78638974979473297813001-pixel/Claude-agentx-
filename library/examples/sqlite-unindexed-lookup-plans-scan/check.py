import importlib.util
import pathlib
import sqlite3

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plan(setup):
    connection = sqlite3.connect(":memory:")
    setup(connection)
    connection.executemany(
        "insert into events(user_id) values (?)",
        [(1,), (1,), (2,)],
    )
    rows = connection.execute(
        "explain query plan select id from events where user_id = 1"
    ).fetchall()
    return " | ".join(str(row[-1]) for row in rows)


bad = plan(load("incorrect").create)
if "SCAN" not in bad:
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = plan(load("correct").create)
if "SEARCH" not in good or "events_user_id" not in good:
    raise SystemExit(good)
print("correct: ok", good)
