"""Remaining benchmark tasks. Imported by eval.taskset."""

from eval.taskset import CHROME, LOAD, node, py, task

GO_LOOP = """package main

import "fmt"

func main() {
	ptrs := []*int{}
	for i := 0; i < 3; i++ {
		ptrs = append(ptrs, &i)
	}
	fmt.Println(*ptrs[0], *ptrs[1], *ptrs[2])
}
"""

MORE = [
    py(
        "sql-placeholder-and-null",
        "cross",
        "SQLite name != 'Ada' drops the NULL row, and f-string name = '{payload}' with payload quote OR 1=1 returns Ada. Use a ? placeholder and OR name IS NULL.",
        ["sql-fstring-interpolates-untrusted-input", "sqlite-null-comparisons-are-unknown"],
        """def find_ids(connection, payload):
    return connection.execute(f"select id from people where name = '{payload}'").fetchall()

def rows_not_named(connection, name):
    return connection.execute(f"select id from people where name != '{name}'").fetchall()
""",
        """def find_ids(connection, payload):
    return connection.execute("select id from people where name = ?", (payload,)).fetchall()

def rows_not_named(connection, name):
    return connection.execute(
        "select id from people where name != ? or name is null",
        (name,),
    ).fetchall()
""",
        LOAD + """
import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("create table people(id integer, name text)")
connection.executemany("insert into people values (?, ?)", [(1, "Ada"), (2, "Grace"), (3, None)])
if answer.find_ids(connection, "' OR '1'='1"):
    raise SystemExit("injected")
ids = [row[0] for row in answer.rows_not_named(connection, "Ada")]
if ids != [2, 3]:
    raise SystemExit(ids)
""",
    ),
    py(
        "retry-post-and-stale-version",
        "cross",
        "Idempotency-Key retry must replay the stored response so the handler runs once. A second update with client_version 1 must return 412 and keep name b at version 2. If-Match.",
        ["idempotency-key-replays-stored-response", "if-match-rejects-stale-update"],
        """def post(store, key, handler):
    return handler()

def update(row, client_version, name):
    row["name"] = name
    row["version"] += 1
    return 200
""",
        """def post(store, key, handler):
    if key in store:
        return store[key]
    body = handler()
    store[key] = body
    return body

def update(row, client_version, name):
    if client_version != row["version"]:
        return 412
    row["name"] = name
    row["version"] += 1
    return 200
""",
        LOAD + """
calls = {"n": 0}
def handler():
    calls["n"] += 1
    return {"id": calls["n"]}
store = {}
first = answer.post(store, "k", handler)
second = answer.post(store, "k", handler)
if calls["n"] != 1 or first != second:
    raise SystemExit((calls, first, second))
row = {"name": "a", "version": 1}
if answer.update(row, 1, "b") != 200:
    raise SystemExit(row)
status = answer.update(row, 1, "c")
if status != 412 or row["name"] != "b" or row["version"] != 2:
    raise SystemExit((status, row))
""",
    ),
    py(
        "outbox-and-foreign-key",
        "cross",
        "PRAGMA foreign_keys is a no-op inside an open transaction, so parent_id 99 inserts. Committing the order before the outbox insert leaves orders 1 and outbox 0 when the process raises. Enable the pragma before DDL and roll both inserts back.",
        ["sqlite-foreign-keys-require-pragma", "transactional-outbox-commit-with-row"],
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table parent(id integer primary key)")
    connection.execute("create table child(id integer primary key, parent_id integer references parent(id))")
    connection.execute("insert into parent values (1)")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def place(connection, fail):
    connection.execute("insert into orders(id) values (1)")
    connection.commit()
    if fail:
        raise RuntimeError("boom")
    connection.execute("insert into outbox(id) values (1)")
    connection.commit()
""",
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.isolation_level = None
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("create table parent(id integer primary key)")
    connection.execute("create table child(id integer primary key, parent_id integer references parent(id))")
    connection.execute("insert into parent values (1)")
    return connection

def place(connection, fail):
    connection.execute("begin")
    try:
        connection.execute("insert into orders(id) values (1)")
        connection.execute("insert into outbox(id) values (1)")
        if fail:
            raise RuntimeError("boom")
        connection.execute("commit")
    except Exception:
        connection.execute("rollback")
        raise
""",
        LOAD + """
connection = answer.connect()
try:
    connection.execute("insert into child(parent_id) values (99)")
    raise SystemExit("orphan inserted")
except Exception as exc:
    if "FOREIGN KEY" not in str(exc) and "orphan" in str(exc):
        raise
connection.execute("create table orders(id integer)")
connection.execute("create table outbox(id integer)")
try:
    answer.place(connection, True)
except RuntimeError:
    pass
orders = connection.execute("select count(*) from orders").fetchone()[0]
outbox = connection.execute("select count(*) from outbox").fetchone()[0]
if orders != 0 or outbox != 0:
    raise SystemExit((orders, outbox))
""",
    ),
    py(
        "page-ties-and-one-query",
        "cross",
        "A created-only keyset cursor returns ids 1 then 3 and skips id 2 sharing 2024-01-01. Tuple (created, id) returns 1 then 2. Loading three users with one SELECT each is N+1; use one IN (?,?,?) query.",
        ["cursor-page-needs-unique-tie-break", "n-plus-one-query-per-row"],
        """def first_two(rows):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    cursor = ""
    found = []
    for row in ordered:
        if row["created"] > cursor:
            found.append(row["id"])
            cursor = row["created"]
        if len(found) == 2:
            break
    return found

def load_orders(connection, user_ids):
    found = []
    for user_id in user_ids:
        found.extend(connection.execute("select id from orders where user_id = ?", (user_id,)).fetchall())
    return found
""",
        """def first_two(rows):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    cursor = ("", -1)
    found = []
    for row in ordered:
        if (row["created"], row["id"]) > cursor:
            found.append(row["id"])
            cursor = (row["created"], row["id"])
        if len(found) == 2:
            break
    return found

def load_orders(connection, user_ids):
    marks = ",".join("?" for _ in user_ids)
    return connection.execute(
        f"select id from orders where user_id in ({marks})",
        tuple(user_ids),
    ).fetchall()
""",
        LOAD + """
import sqlite3
rows = [
    {"id": 1, "created": "2024-01-01"},
    {"id": 2, "created": "2024-01-01"},
    {"id": 3, "created": "2024-01-02"},
]
if answer.first_two(rows) != [1, 2]:
    raise SystemExit(answer.first_two(rows))
connection = sqlite3.connect(":memory:")
connection.execute("create table orders(id integer, user_id integer)")
connection.executemany("insert into orders values (?, ?)", [(1, 10), (2, 11), (3, 12)])
trace = []
connection.set_trace_callback(trace.append)
found = answer.load_orders(connection, [10, 11, 12])
selects = [sql for sql in trace if sql.lower().startswith("select")]
if len(selects) != 1 or sorted(row[0] for row in found) != [1, 2, 3]:
    raise SystemExit((selects, found))
""",
    ),
    py(
        "shallow-describe-and-detached-head",
        "cross",
        "git clone --depth 1 then git describe --tags writes fatal: No names found, cannot describe anything. rev-parse --abbrev-ref HEAD prints HEAD when detached. Unshallow and use symbolic-ref -q so detached HEAD is None.",
        ["git-describe-fails-on-shallow-clone", "git-abbrev-ref-is-head-when-detached"],
        """import subprocess

def label(repo):
    return subprocess.run(["git", "-C", str(repo), "describe", "--tags"], check=False, text=True, capture_output=True)

def branch_name(repo):
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        check=True, text=True, capture_output=True,
    )
    return completed.stdout.strip()
""",
        """import subprocess

def label(repo):
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--unshallow", "origin"],
        check=False, text=True, capture_output=True,
    )
    return subprocess.run(
        ["git", "-C", str(repo), "describe", "--tags"],
        check=False, text=True, capture_output=True,
    )

def branch_name(repo):
    completed = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "-q", "HEAD"],
        check=False, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()
""",
        LOAD + r"""
import pathlib, subprocess, tempfile

def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True, capture_output=True)

with tempfile.TemporaryDirectory() as tmp:
    src = pathlib.Path(tmp) / "src"
    src.mkdir()
    git(src, "init", "-q", "-b", "main")
    git(src, "config", "user.email", "t@example.com")
    git(src, "config", "user.name", "t")
    (src / "a.txt").write_text("a\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "init")
    git(src, "tag", "-a", "v1.2.3", "-m", "v1.2.3")
    (src / "a.txt").write_text("b\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "second")
    shallow = pathlib.Path(tmp) / "shallow"
    subprocess.run(["git", "clone", "--depth", "1", "--quiet", f"file://{src}", str(shallow)], check=True)
    described = answer.label(shallow)
    if described.returncode != 0 or not described.stdout.startswith("v1.2.3"):
        raise SystemExit((described.returncode, described.stdout, described.stderr))
    git(shallow, "checkout", "--detach", "HEAD")
    if answer.branch_name(shallow) is not None:
        raise SystemExit(repr(answer.branch_name(shallow)))
""",
        timeout=40,
    ),
    task(
        "go-1-22-loop-variable",
        "languages",
        "Taking the address of i in for i := 0; i < 3; i++ prints 3 3 3 under go 1.21 and 0 1 2 under go 1.22. The go line in go.mod selects the loop variable rule.",
        ["go-1-22-loop-var-per-iteration"],
        ["python3", "check.py"],
        "check.py",
        {"main.go": GO_LOOP, "go.mod": "module example.com/loopold\n\ngo 1.21\n"},
        {"main.go": GO_LOOP, "go.mod": "module example.com/loopnew\n\ngo 1.22\n"},
        """import subprocess
completed = subprocess.run(["go", "run", "."], check=False, text=True, capture_output=True)
if completed.returncode != 0:
    raise SystemExit(completed.stderr)
if completed.stdout.strip() != "0 1 2":
    raise SystemExit(completed.stdout)
""",
        timeout=60,
    ),
    py(
        "python-unbound-local-count",
        "languages",
        "UnboundLocalError: cannot access local variable 'count' where it is not associated with a value. Assigning to count makes it local even though the module set count = 0. Declare global count.",
        ["python-unboundlocalerror-on-assignment"],
        """count = 0
def label():
    print(count)
    count = count + 1
    return count
""",
        """count = 0
def label():
    global count
    print(count)
    count = count + 1
    return count
""",
        LOAD + """
if answer.label() != 1:
    raise SystemExit("label")
""",
    ),
    py(
        "python-lambda-defaults",
        "languages",
        "Lambdas created in a for-loop all return 2. The Python FAQ says the free variable is read when the lambda runs. lambda i=i: i returns 0, 1, 2.",
        ["python-closure-late-binding"],
        """def make():
    return [lambda: i for i in range(3)]
""",
        """def make():
    return [lambda i=i: i for i in range(3)]
""",
        LOAD + """
if [fn() for fn in answer.make()] != [0, 1, 2]:
    raise SystemExit([fn() for fn in answer.make()])
""",
    ),
    node(
        "javascript-numeric-sort",
        "languages",
        "Array.prototype.sort with no compare function orders [10, 2, 1] as 1,10,2 because it compares UTF-16 strings. A numeric compare returns 1,2,10.",
        ["javascript-array-sort-lexicographic"],
        {"answer.mjs": """export function sortNumbers(values) {
  return values.sort();
}
"""},
        {"answer.mjs": """export function sortNumbers(values) {
  return values.slice().sort((a, b) => a - b);
}
"""},
        """import { pathToFileURL } from "node:url";
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const original = [10, 2, 1];
const sorted = answer.sortNumbers(original);
if (sorted.join(",") !== "1,2,10") throw new Error(sorted.join(","));
if (original.join(",") !== "10,2,1") throw new Error("mutated " + original.join(","));
""",
    ),
    task(
        "rust-let-temporary",
        "languages",
        "rustc error E0716 temporary value dropped while borrowed on value.unwrap().as_str(). Bind the String in a let before borrowing it.",
        ["rust-temporary-dropped-while-borrowed"],
        ["python3", "check.py"],
        "check.py",
        {"answer.rs": """fn main() {
    let value = Some("hi".to_string());
    let borrowed = value.unwrap().as_str();
    println!("{borrowed}");
}
"""},
        {"answer.rs": """fn main() {
    let value = Some("hi".to_string());
    let owned = value.unwrap();
    let borrowed = owned.as_str();
    println!("{borrowed}");
}
"""},
        """import subprocess
compiled = subprocess.run(["rustc", "answer.rs", "-o", "answer.bin"], text=True, capture_output=True)
if compiled.returncode != 0:
    raise SystemExit(compiled.stderr)
ran = subprocess.run(["./answer.bin"], check=True, text=True, capture_output=True)
if ran.stdout.strip() != "hi":
    raise SystemExit(ran.stdout)
""",
        timeout=60,
    ),
    task(
        "java-switch-case-null",
        "languages",
        "Java 21 pattern switch throws NullPointerException when the selector is null and there is no case null. JEP 441. case null should print missing, not npe.",
        ["java-21-switch-null-throws"],
        ["python3", "check.py"],
        "check.py",
        {"Answer.java": """public class Answer {
    static String label(String value) {
        return switch (value) {
            case "ok" -> "ok";
            default -> "other";
        };
    }
    public static void main(String[] args) {
        try {
            System.out.println(label(null));
        } catch (NullPointerException ex) {
            System.out.println("npe");
        }
    }
}
"""},
        {"Answer.java": """public class Answer {
    static String label(String value) {
        return switch (value) {
            case null -> "missing";
            case "ok" -> "ok";
            default -> "other";
        };
    }
    public static void main(String[] args) {
        System.out.println(label(null));
    }
}
"""},
        """import subprocess
compiled = subprocess.run(["javac", "--release", "21", "Answer.java"], text=True, capture_output=True)
if compiled.returncode != 0:
    raise SystemExit(compiled.stderr)
ran = subprocess.run(["java", "Answer"], check=True, text=True, capture_output=True)
if ran.stdout.strip() != "missing":
    raise SystemExit(ran.stdout)
""",
        timeout=60,
    ),
    py(
        "keyset-second-page",
        "apis",
        "Page size 1. Rows id 1 and id 2 share created 2024-01-01, id 3 is the next day. A cursor that keeps only created skips id 2. The second page must be id 2. SQLite row values.",
        ["cursor-page-needs-unique-tie-break"],
        """def second_id(rows):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    first = ordered[0]
    rest = [row for row in ordered if row["created"] > first["created"]]
    return rest[0]["id"]
""",
        """def second_id(rows):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    first = ordered[0]
    rest = [row for row in ordered if (row["created"], row["id"]) > (first["created"], first["id"])]
    return rest[0]["id"]
""",
        LOAD + """
rows = [
    {"id": 2, "created": "2024-01-01"},
    {"id": 1, "created": "2024-01-01"},
    {"id": 3, "created": "2024-01-02"},
]
if answer.second_id(rows) != 2:
    raise SystemExit(answer.second_id(rows))
""",
    ),
    py(
        "idempotency-replays-body",
        "apis",
        "A retried POST with the same Idempotency-Key runs the handler twice and returns a new id. Store the first response and replay it. The draft idempotency-key header.",
        ["idempotency-key-replays-stored-response"],
        """def post(store, key, handler):
    return handler()
""",
        """def post(store, key, handler):
    if key in store:
        return store[key]
    body = handler()
    store[key] = body
    return body
""",
        LOAD + """
seq = {"n": 0}
def handler():
    seq["n"] += 1
    return {"id": seq["n"]}
store = {}
a = answer.post(store, "same", handler)
b = answer.post(store, "same", handler)
c = answer.post(store, "other", handler)
if seq["n"] != 2 or a != b or c["id"] != 2:
    raise SystemExit((seq, a, b, c))
""",
    ),
    py(
        "if-match-412",
        "apis",
        "Two updates that ignore If-Match apply client_version 1 twice and the row ends at version 3 name c. The second call must return 412 and leave name b version 2. RFC 9110 If-Match.",
        ["if-match-rejects-stale-update"],
        """def update(row, client_version, name):
    row["name"] = name
    row["version"] += 1
    return 200
""",
        """def update(row, client_version, name):
    if row["version"] != client_version:
        return 412
    row["name"] = name
    row["version"] += 1
    return 200
""",
        LOAD + """
row = {"name": "a", "version": 1}
answer.update(row, 1, "b")
status = answer.update(row, 1, "c")
if status != 412 or row != {"name": "b", "version": 2}:
    raise SystemExit((status, row))
""",
    ),
    py(
        "cursor-does-not-skip-tie",
        "apis",
        "created > cursor skips the other row with the same timestamp. After returning id 1, the next id with page size 1 must be 2, not 3. Include id in the comparison.",
        ["cursor-page-needs-unique-tie-break"],
        """def next_id(rows, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    for row in ordered:
        if row["created"] > cursor[0]:
            return row["id"]
    raise RuntimeError("empty")
""",
        """def next_id(rows, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    for row in ordered:
        if (row["created"], row["id"]) > cursor:
            return row["id"]
    raise RuntimeError("empty")
""",
        LOAD + """
rows = [
    {"id": 1, "created": "2024-01-01"},
    {"id": 2, "created": "2024-01-01"},
    {"id": 3, "created": "2024-01-02"},
]
if answer.next_id(rows, ("2024-01-01", 1)) != 2:
    raise SystemExit(answer.next_id(rows, ("2024-01-01", 1)))
""",
    ),
    py(
        "sqlite-pragma-before-ddl",
        "databases",
        "PRAGMA foreign_keys reads 0 on a new SQLite connection. Setting it after inserting the parent is a no-op and the child parent_id 99 inserts. isolation_level None, pragma ON, then DDL. IntegrityError FOREIGN KEY constraint failed.",
        ["sqlite-foreign-keys-require-pragma"],
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table parent(id integer primary key)")
    connection.execute("create table child(id integer primary key, parent_id integer references parent(id))")
    connection.execute("insert into parent values (1)")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
""",
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.isolation_level = None
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("create table parent(id integer primary key)")
    connection.execute("create table child(id integer primary key, parent_id integer references parent(id))")
    connection.execute("insert into parent values (1)")
    return connection
""",
        LOAD + """
connection = answer.connect()
try:
    connection.execute("insert into child(parent_id) values (99)")
except Exception as exc:
    if "FOREIGN KEY" not in str(exc):
        raise SystemExit(exc)
else:
    raise SystemExit("orphan inserted")
""",
    ),
    py(
        "sqlite-null-not-equal",
        "databases",
        "name != 'Ada' returns only id 2. The NULL name is unknown, not different. SQLite nulls. Add OR name IS NULL so ids are 2 and 3.",
        ["sqlite-null-comparisons-are-unknown"],
        """def rows_not_named(connection, name):
    return connection.execute("select id from people where name != ?", (name,)).fetchall()
""",
        """def rows_not_named(connection, name):
    return connection.execute(
        "select id from people where name != ? or name is null",
        (name,),
    ).fetchall()
""",
        LOAD + """
import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("create table people(id integer, name text)")
connection.executemany("insert into people values (?, ?)", [(1, "Ada"), (2, "Grace"), (3, None)])
ids = [row[0] for row in answer.rows_not_named(connection, "Ada")]
if ids != [2, 3]:
    raise SystemExit(ids)
""",
    ),
    py(
        "sqlite-index-search-plan",
        "databases",
        "EXPLAIN QUERY PLAN for user_id = ? says SCAN events until CREATE INDEX events_user_id. The indexed plan contains SEARCH and events_user_id, with the word COVERING between USING and INDEX.",
        ["sqlite-unindexed-lookup-plans-scan"],
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table events(id integer, user_id integer)")
    connection.execute("insert into events values (1, 7)")
    return connection
""",
        """import sqlite3

def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table events(id integer, user_id integer)")
    connection.execute("create index events_user_id on events(user_id)")
    connection.execute("insert into events values (1, 7)")
    return connection
""",
        LOAD + """
connection = answer.connect()
plan = " ".join(str(row) for row in connection.execute("explain query plan select id from events where user_id = ?", (7,)))
if "SEARCH" not in plan or "events_user_id" not in plan:
    raise SystemExit(plan)
""",
    ),
    py(
        "path-commonpath-not-prefix",
        "security",
        "normpath(join(uploads, '../uploads-evil/x.txt')).startswith(uploads) is true because uploads-evil startswith uploads. os.path.commonpath of the realpaths is the parent, not the uploads root.",
        ["path-join-allows-traversal"],
        """import os

def inside(root, user_path):
    candidate = os.path.normpath(os.path.join(root, user_path))
    return candidate.startswith(os.path.normpath(root))
""",
        """import os

def inside(root, user_path):
    root_real = os.path.realpath(root)
    candidate = os.path.realpath(os.path.normpath(os.path.join(root, user_path)))
    try:
        return os.path.commonpath([root_real, candidate]) == root_real
    except ValueError:
        return False
""",
        LOAD + """
import pathlib, tempfile
with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp) / "uploads"
    evil = pathlib.Path(tmp) / "uploads-evil"
    root.mkdir()
    evil.mkdir()
    if answer.inside(str(root), "../uploads-evil/x.txt"):
        raise SystemExit("escaped")
    if not answer.inside(str(root), "ok.txt"):
        raise SystemExit("rejected child")
""",
    ),
    py(
        "hmac-bytes-compare-digest",
        "security",
        "hmac.compare_digest(b'secret', 'secret') raises TypeError: a bytes-like object is required, not 'str'. Different lengths return False. Do not use == for the MAC.",
        ["hmac-compare-digest-for-secrets"],
        """def same(left, right):
    return left == right
""",
        """import hmac

def same(left, right):
    return hmac.compare_digest(left, right)
""",
        LOAD + """
try:
    answer.same(b"secret", "secret")
except TypeError as exc:
    if "bytes-like object is required" not in str(exc):
        raise SystemExit(exc)
else:
    raise SystemExit("mixed types compared")
if answer.same(b"secret", b"secre"):
    raise SystemExit("prefix")
if not answer.same(b"secret", b"secret"):
    raise SystemExit("equal")
""",
    ),
    py(
        "sql-bind-untrusted-name",
        "security",
        "f-string SQL name = '{payload}' with payload ' OR '1'='1 returns the Ada row. sqlite3 placeholders: WHERE name = ? returns an empty list.",
        ["sql-fstring-interpolates-untrusted-input"],
        """def find_ids(connection, payload):
    return connection.execute(f"select id from people where name = '{payload}'").fetchall()
""",
        """def find_ids(connection, payload):
    return connection.execute("select id from people where name = ?", (payload,)).fetchall()
""",
        LOAD + """
import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("create table people(id integer, name text)")
connection.execute("insert into people values (1, 'Ada')")
if answer.find_ids(connection, "' OR '1'='1"):
    raise SystemExit("injected")
""",
    ),
    task(
        "go-shutdown-returns",
        "backend",
        "http.Server.Shutdown waits until the handler returns. A handler that sleeps 1s with a 150ms shutdown timeout prints blocked. Close an explicit stop channel before Shutdown so the process prints returned.",
        ["go-http-shutdown-blocks-on-handler"],
        ["python3", "check.py"],
        "check.py",
        {"go.mod": "module example.com/shutdown\n\ngo 1.22\n", "main.go": """package main

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"time"
)

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		panic(err)
	}
	server := &http.Server{
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			time.Sleep(time.Second)
			w.WriteHeader(http.StatusNoContent)
		}),
	}
	go server.Serve(ln)
	go http.Get("http://" + ln.Addr().String())
	time.Sleep(30 * time.Millisecond)
	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()
	err = server.Shutdown(ctx)
	if err == nil {
		fmt.Println("returned")
		return
	}
	fmt.Println("blocked")
}
"""},
        {"go.mod": "module example.com/shutdown\n\ngo 1.22\n", "main.go": """package main

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"time"
)

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		panic(err)
	}
	stop := make(chan struct{})
	server := &http.Server{
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			select {
			case <-stop:
				return
			case <-time.After(time.Second):
				w.WriteHeader(http.StatusNoContent)
			}
		}),
	}
	go server.Serve(ln)
	go http.Get("http://" + ln.Addr().String())
	time.Sleep(30 * time.Millisecond)
	close(stop)
	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()
	err = server.Shutdown(ctx)
	if err != nil {
		fmt.Println("blocked")
		return
	}
	fmt.Println("returned")
}
"""},
        """import subprocess
completed = subprocess.run(["go", "run", "."], check=False, text=True, capture_output=True, timeout=20)
if completed.stdout.strip() != "returned":
    raise SystemExit(completed.stdout + completed.stderr)
""",
        timeout=40,
    ),
    node(
        "node-request-must-end",
        "backend",
        "A Node http.request that write()s JSON and never calls end() stays open. The server answers on the request end event. The client resolves timeout after 200ms unless end() is called. Destroy emits ECONNRESET unless error is handled.",
        ["node-http-client-hangs-without-end"],
        {"answer.mjs": """import http from "node:http";
export function post(port) {
  return new Promise((resolve) => {
    const request = http.request({ hostname: "127.0.0.1", port, method: "POST" }, (response) => {
      const chunks = [];
      response.on("data", (chunk) => chunks.push(chunk));
      response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    });
    request.on("error", () => {});
    request.setTimeout(200, () => {
      request.destroy();
      resolve("timeout");
    });
    request.write("{}");
  });
}
"""},
        {"answer.mjs": """import http from "node:http";
export function post(port) {
  return new Promise((resolve, reject) => {
    const request = http.request({ hostname: "127.0.0.1", port, method: "POST" }, (response) => {
      const chunks = [];
      response.on("data", (chunk) => chunks.push(chunk));
      response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    });
    request.on("error", reject);
    request.write("{}");
    request.end();
  });
}
"""},
        """import http from "node:http";
import { pathToFileURL } from "node:url";
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const server = http.createServer((request, response) => {
  request.on("data", () => {});
  request.on("end", () => response.end("ok"));
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
try {
  const body = await answer.post(server.address().port);
  if (body !== "ok") throw new Error(body);
} finally {
  server.close();
}
""",
        timeout=20,
    ),
    py(
        "exception-cause-is-set",
        "debugging",
        "raise RuntimeError inside except ValueError sets __context__ and leaves __cause__ None. raise RuntimeError from exc sets __cause__ to that ValueError. Python exception context.",
        ["python-exception-context-chaining"],
        """def convert():
    try:
        raise ValueError("bad")
    except ValueError:
        raise RuntimeError("wrapped")
""",
        """def convert():
    try:
        raise ValueError("bad")
    except ValueError as exc:
        raise RuntimeError("wrapped") from exc
""",
        LOAD + """
try:
    answer.convert()
except RuntimeError as exc:
    if not isinstance(exc.__cause__, ValueError):
        raise SystemExit(repr(exc.__cause__))
else:
    raise SystemExit("no error")
""",
    ),
    node(
        "await-rejected-promise",
        "debugging",
        "try { Promise.reject(new Error('nope')) } returns fell-through. The rejection is an unhandledRejection, not a catch. await inside the try returns nope. Node process unhandledRejection.",
        ["node-unhandled-rejection-is-not-thrown"],
        {"answer.mjs": """export async function run() {
  try {
    Promise.reject(new Error("nope"));
    return "fell-through";
  } catch (error) {
    return error.message;
  }
}
"""},
        {"answer.mjs": """export async function run() {
  try {
    await Promise.reject(new Error("nope"));
    return "fell-through";
  } catch (error) {
    return error.message;
  }
}
"""},
        """import { pathToFileURL } from "node:url";
process.on("unhandledRejection", () => {});
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const result = await answer.run();
if (result !== "nope") throw new Error(result);
""",
    ),
    py(
        "quote-actions-run-script",
        "devops",
        "Building echo {message} from hello; echo PWNED runs PWNED as its own shell command. GitHub Actions script injection. Emit echo \"$MSG\" and pass the text in the environment.",
        ["github-actions-unquoted-run-script"],
        """def render(message):
    return f"echo {message}\\n"
""",
        """def render(_message):
    return 'echo "$MSG"\\n'
""",
        LOAD + """
import os, pathlib, subprocess, tempfile
message = "hello; echo PWNED"
script = answer.render(message)
with tempfile.TemporaryDirectory() as tmp:
    path = pathlib.Path(tmp) / "run.sh"
    path.write_text(script, encoding="utf-8")
    env = os.environ.copy()
    env["MSG"] = message
    completed = subprocess.run(["bash", str(path)], check=False, text=True, capture_output=True, env=env)
if completed.stdout.strip() != message:
    raise SystemExit(repr(completed.stdout))
""",
    ),
    py(
        "describe-after-unshallow",
        "devops",
        "git describe --tags on a depth-1 clone fails with fatal: No names found, cannot describe anything. Fetch --unshallow origin so describe prints a name starting with v1.2.3.",
        ["git-describe-fails-on-shallow-clone"],
        """import subprocess

def label(repo):
    return subprocess.run(["git", "-C", str(repo), "describe", "--tags"], check=False, text=True, capture_output=True)
""",
        """import subprocess

def label(repo):
    subprocess.run(["git", "-C", str(repo), "fetch", "--unshallow", "origin"], check=False, text=True, capture_output=True)
    return subprocess.run(["git", "-C", str(repo), "describe", "--tags"], check=False, text=True, capture_output=True)
""",
        LOAD + r"""
import pathlib, subprocess, tempfile

def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True, capture_output=True)

with tempfile.TemporaryDirectory() as tmp:
    src = pathlib.Path(tmp) / "src"
    src.mkdir()
    git(src, "init", "-q", "-b", "main")
    git(src, "config", "user.email", "t@example.com")
    git(src, "config", "user.name", "t")
    (src / "a.txt").write_text("a\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "init")
    git(src, "tag", "-a", "v1.2.3", "-m", "v1.2.3")
    (src / "a.txt").write_text("b\n", encoding="utf-8")
    git(src, "add", "a.txt")
    git(src, "commit", "-q", "-m", "second")
    shallow = pathlib.Path(tmp) / "shallow"
    subprocess.run(["git", "clone", "--depth", "1", "--quiet", f"file://{src}", str(shallow)], check=True)
    described = answer.label(shallow)
    if described.returncode != 0 or not described.stdout.startswith("v1.2.3"):
        raise SystemExit((described.returncode, described.stdout, described.stderr))
""",
        timeout=40,
    ),
    node(
        "mock-timers-need-tick",
        "testing",
        "node:test mock.timers.enable({ apis: ['setTimeout'] }) does not fire a 5000ms timer until mock.timers.tick(5000). The flag stays false if you only enable the mock.",
        ["node-mock-timers-do-not-advance-alone"],
        {"answer.mjs": """export function advance() {}
"""},
        {"answer.mjs": """import { mock } from "node:test";
export function advance() {
  mock.timers.tick(5000);
}
"""},
        """import { mock } from "node:test";
import { pathToFileURL } from "node:url";
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
mock.timers.enable({ apis: ["setTimeout"] });
let flag = false;
setTimeout(() => {
  flag = true;
}, 5000);
answer.advance();
if (!flag) throw new Error("timer did not run");
""",
    ),
    node(
        "mock-timers-partial-tick",
        "testing",
        "mock.timers.tick(1000) does not run a callback scheduled for 5000ms. tick advances the mocked clock by the amount you pass. Node mock.timers.tick.",
        ["node-mock-timers-do-not-advance-alone"],
        {"answer.mjs": """import { mock } from "node:test";
export function advance(ms) {
  mock.timers.tick(5000);
}
"""},
        {"answer.mjs": """import { mock } from "node:test";
export function advance(ms) {
  mock.timers.tick(ms);
}
"""},
        """import { mock } from "node:test";
import { pathToFileURL } from "node:url";
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
mock.timers.enable({ apis: ["setTimeout"] });
let flag = false;
setTimeout(() => {
  flag = true;
}, 5000);
answer.advance(1000);
if (flag) throw new Error("fired early");
""",
    ),
    py(
        "detached-head-is-not-a-branch",
        "vcs",
        "git rev-parse --abbrev-ref HEAD prints HEAD on a detached checkout. git symbolic-ref -q HEAD exits non-zero. The helper must return None, not the string HEAD.",
        ["git-abbrev-ref-is-head-when-detached"],
        """import subprocess

def branch_name(repo):
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        check=True, text=True, capture_output=True,
    )
    return completed.stdout.strip()
""",
        """import subprocess

def branch_name(repo):
    completed = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "-q", "HEAD"],
        check=False, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()
""",
        LOAD + r"""
import pathlib, subprocess, tempfile

def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True, capture_output=True)

with tempfile.TemporaryDirectory() as tmp:
    repo = pathlib.Path(tmp)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "init")
    git(repo, "checkout", "--detach", "HEAD")
    if answer.branch_name(repo) is not None:
        raise SystemExit(repr(answer.branch_name(repo)))
""",
    ),
    py(
        "argparse-double-dash",
        "cli",
        "argparse nargs='*' exits 2 with unrecognized arguments: --flag when the user passes run --flag. Arguments containing -. Insert -- so the positional receives ['--flag'].",
        ["argparse-options-after-positionals"],
        """import argparse

def forward(argv):
    parser = argparse.ArgumentParser(prog="tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("cmd")
    parser.add_argument("args", nargs="*")
    return parser.parse_args(argv).args
""",
        """import argparse

def forward(argv):
    parser = argparse.ArgumentParser(prog="tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("cmd")
    parser.add_argument("args", nargs="*")
    if argv and argv[0] != "--" and "--" not in argv:
        argv = [argv[0], "--", *argv[1:]]
    return parser.parse_args(argv).args
""",
        LOAD + """
try:
    args = answer.forward(["run", "--flag"])
except SystemExit as exc:
    raise SystemExit(f"parser exited {exc.code}")
if args != ["--flag"]:
    raise SystemExit(args)
""",
    ),
    py(
        "outbox-rolls-back-both",
        "architecture",
        "Insert the order, commit, then raise before the outbox insert: orders is 1 and outbox is 0. Insert both, then roll back when the operation fails. sqlite3 transaction control.",
        ["transactional-outbox-commit-with-row"],
        """def place(connection, fail):
    connection.execute("insert into orders(id) values (1)")
    connection.commit()
    if fail:
        raise RuntimeError("boom")
    connection.execute("insert into outbox(id) values (1)")
    connection.commit()
""",
        """def place(connection, fail):
    try:
        connection.execute("insert into orders(id) values (1)")
        connection.execute("insert into outbox(id) values (1)")
        if fail:
            raise RuntimeError("boom")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
""",
        LOAD + """
import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("create table orders(id integer)")
connection.execute("create table outbox(id integer)")
try:
    answer.place(connection, True)
except RuntimeError:
    pass
orders = connection.execute("select count(*) from orders").fetchone()[0]
outbox = connection.execute("select count(*) from outbox").fetchone()[0]
if orders != 0 or outbox != 0:
    raise SystemExit((orders, outbox))
""",
    ),
    py(
        "generator-second-pass",
        "refactoring",
        "list() on a generator iterator is empty the second time. The glossary calls that object a generator iterator. Return a list when the caller iterates twice.",
        ["python-generator-second-pass-empty"],
        """def values():
    for item in (1, 2):
        yield item
""",
        """def values():
    return [1, 2]
""",
        LOAD + """
seq = answer.values()
if list(seq) != [1, 2] or list(seq) != [1, 2]:
    raise SystemExit("not reusable")
""",
    ),
    py(
        "warning-stacklevel-caller",
        "docs",
        "warnings.warn stacklevel=1 names the helper file. stacklevel=2 names the caller. The warning filename must be check.py, not answer.py.",
        ["python-warnings-stacklevel"],
        """import warnings

def deprecated():
    warnings.warn("old entry point", DeprecationWarning, stacklevel=1)
""",
        """import warnings

def deprecated():
    warnings.warn("old entry point", DeprecationWarning, stacklevel=2)
""",
        LOAD + """
import pathlib, warnings
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    answer.deprecated()
if not caught:
    raise SystemExit("no warning")
if pathlib.Path(caught[0].filename).name != "check.py":
    raise SystemExit(caught[0].filename)
""",
    ),
    py(
        "one-query-for-users",
        "performance",
        "Three per-user SELECT statements show up in the sqlite3 trace. Build WHERE user_id IN (?,?,?) from len(user_ids) so the trace contains one select. sqlite3 placeholders.",
        ["n-plus-one-query-per-row"],
        """def load_orders(connection, user_ids):
    found = []
    for user_id in user_ids:
        found.extend(connection.execute("select id from orders where user_id = ?", (user_id,)).fetchall())
    return found
""",
        """def load_orders(connection, user_ids):
    marks = ",".join("?" for _ in user_ids)
    return connection.execute(
        f"select id from orders where user_id in ({marks})",
        tuple(user_ids),
    ).fetchall()
""",
        LOAD + """
import sqlite3
connection = sqlite3.connect(":memory:")
connection.execute("create table orders(id integer, user_id integer)")
connection.executemany("insert into orders values (?, ?)", [(1, 10), (2, 11), (3, 12)])
trace = []
connection.set_trace_callback(trace.append)
found = answer.load_orders(connection, [10, 11, 12])
selects = [sql for sql in trace if sql.lower().startswith("select")]
if len(selects) != 1 or len(found) != 3:
    raise SystemExit((selects, found))
""",
    ),
    node(
        "safe-area-max-with-env",
        "mobile",
        "env(safe-area-inset-top, 12px) computes padding-top 0px in this Chrome because the variable exists and is 0. The fallback applies only when the variable is undefined. Use max(12px, env(safe-area-inset-top)) so padding-top is 12px. css-env-1 safe-area-insets.",
        ["mobile-safe-area-fallback-only-if-undefined"],
        {"answer.html": """<style>
  #pad { padding-top: env(safe-area-inset-top, 12px); }
</style>
<div id="pad"></div>
"""},
        {"answer.html": """<style>
  #pad { padding-top: max(12px, env(safe-area-inset-top)); }
</style>
<div id="pad"></div>
"""},
        CHROME + """
await withPage(async (page) => {
  await setHtmlFile(page, "answer.html");
  const pad = await page.$eval("#pad", (el) => getComputedStyle(el).paddingTop);
  if (pad !== "12px") throw new Error(pad);
});
""",
        timeout=40,
    ),
]
