import importlib.util
import pathlib
import sqlite3

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def connection():
    db = sqlite3.connect(":memory:")
    db.execute("create table orders(id integer primary key, user_id integer)")
    db.executemany(
        "insert into orders(user_id) values (?)",
        [(1,), (1,), (2,), (3,)],
    )
    return db


def count(sql_log, fn):
    db = connection()
    db.set_trace_callback(sql_log.append)
    fn(db)
    return len(sql_log)


users = [1, 2, 3]
bad_log = []
bad_n = count(bad_log, lambda db: load("incorrect").load_orders(db, users))
if bad_n != 3:
    raise SystemExit(bad_n)
print("incorrect: observed", bad_n)

good_log = []
good_n = count(good_log, lambda db: load("correct").load_orders(db, users))
if good_n != 1:
    raise SystemExit(good_n)
print("correct: ok", good_n)
