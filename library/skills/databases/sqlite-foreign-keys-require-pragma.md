---
id: sqlite-foreign-keys-require-pragma
area: databases
topic: sqlite
task: enable-foreign-keys
title: SQLite foreign keys stay off unless PRAGMA foreign_keys runs outside a transaction
description: Use when an orphan child row inserts successfully, or PRAGMA foreign_keys reports 0 after you thought you enabled it.
triggers:
  - PRAGMA foreign_keys
  - FOREIGN KEY constraint failed
  - sqlite foreign keys default off
  - pragma inside transaction
aliases:
  - sqlite
  - foreign-keys
  - pragma
related:
  - sqlite-null-comparisons-are-unknown
  - transactional-outbox-commit-with-row
sources:
  - https://www.sqlite.org/foreignkeys.html
  - https://www.sqlite.org/pragma.html#pragma_foreign_keys
commands:
  - python3 library/examples/sqlite-foreign-keys-require-pragma/check.py
---

# SQLite foreign keys stay off unless PRAGMA foreign_keys runs outside a transaction

SQLite leaves foreign key enforcement off. `PRAGMA foreign_keys` reads 0 on a new connection. The foreign keys page says you must enable it per connection, and the pragma page says changing `foreign_keys` while a transaction is open does nothing.

Python's `sqlite3` module opens a transaction on the first DML statement. Creating the parent row and then executing `PRAGMA foreign_keys = ON` leaves the pragma at 0. The child insert with `parent_id` 99 succeeds, and a count of orphans is 1.

Set `connection.isolation_level = None` (autocommit, documented under sqlite3 transaction control) and run `PRAGMA foreign_keys = ON` before any DDL or DML. The same orphan insert then raises `IntegrityError: FOREIGN KEY constraint failed`. The check reads the pragma on that connection.

## Incorrect

```python file=library/examples/sqlite-foreign-keys-require-pragma/incorrect.py
import sqlite3


def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table parent(id integer primary key)")
    connection.execute(
        "create table child(id integer primary key, parent_id integer references parent(id))"
    )
    connection.execute("insert into parent(id) values (1)")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("insert into child(parent_id) values (99)")
    return connection
```

## Correct

```python file=library/examples/sqlite-foreign-keys-require-pragma/correct.py
import sqlite3


def connect():
    connection = sqlite3.connect(":memory:")
    connection.isolation_level = None
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("create table parent(id integer primary key)")
    connection.execute(
        "create table child(id integer primary key, parent_id integer references parent(id))"
    )
    return connection
```

## Verify

Run `python3 library/examples/sqlite-foreign-keys-require-pragma/check.py`.

## Sources

- https://www.sqlite.org/foreignkeys.html
- https://www.sqlite.org/pragma.html#pragma_foreign_keys
