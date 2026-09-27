import importlib.util
import pathlib
import sqlite3

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect").connect()
enabled = bad.execute("PRAGMA foreign_keys").fetchone()[0]
orphans = bad.execute("select count(*) from child where parent_id = 99").fetchone()[0]
if enabled != 0 or orphans != 1:
    raise SystemExit((enabled, orphans))
print("incorrect: observed", f"foreign_keys={enabled}", f"orphans={orphans}")

good = load("correct").connect()
if good.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
    raise SystemExit("pragma did not stick")
try:
    good.execute("insert into child(parent_id) values (99)")
except sqlite3.IntegrityError as exc:
    print("correct: ok", exc)
else:
    raise SystemExit("orphan insert was accepted")
