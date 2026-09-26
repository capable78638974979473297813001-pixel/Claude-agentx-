import importlib.util
import pathlib
import sqlite3

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def database():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table people(id integer primary key, name text)")
    connection.executemany(
        "insert into people(name) values (?)",
        [("Ada",), ("Grace",), (None,)],
    )
    return connection


bad = [row[0] for row in load("incorrect").missing_names(database())]
if bad != [2]:
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = [row[0] for row in load("correct").missing_names(database())]
if good != [2, 3]:
    raise SystemExit(good)
print("correct: ok", good)
