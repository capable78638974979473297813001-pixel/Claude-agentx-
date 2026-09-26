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
    connection.execute("create table users(id integer primary key, name text)")
    connection.execute("insert into users(name) values ('Ada')")
    return connection


payload = "' OR '1'='1"
bad = load("incorrect").find_user(database(), payload)
if [row[0] for row in bad] != [1]:
    raise SystemExit(bad)
print("incorrect: observed", bad)

good = load("correct").find_user(database(), payload)
if good != []:
    raise SystemExit(good)
print("correct: ok", good)
