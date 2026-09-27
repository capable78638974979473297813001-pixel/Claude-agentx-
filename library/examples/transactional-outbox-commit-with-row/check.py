import importlib.util
import pathlib
import sqlite3

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fresh():
    db = sqlite3.connect(":memory:")
    db.execute("create table orders(id integer primary key)")
    db.execute("create table outbox(order_id integer)")
    return db


bad = fresh()
try:
    load("incorrect").place(bad, True)
except RuntimeError:
    pass
else:
    raise SystemExit("incorrect path did not fail")
orders = bad.execute("select count(*) from orders").fetchone()[0]
outbox = bad.execute("select count(*) from outbox").fetchone()[0]
if orders != 1 or outbox != 0:
    raise SystemExit((orders, outbox))
print("incorrect: observed", f"orders={orders}", f"outbox={outbox}")

good = fresh()
try:
    load("correct").place(good, True)
except RuntimeError:
    pass
else:
    raise SystemExit("correct path did not fail")
if good.execute("select count(*) from orders").fetchone()[0] != 0:
    raise SystemExit("order survived rollback")
if good.execute("select count(*) from outbox").fetchone()[0] != 0:
    raise SystemExit("outbox survived rollback")
print("correct: ok")
