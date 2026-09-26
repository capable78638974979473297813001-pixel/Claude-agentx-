---
id: sql-fstring-interpolates-untrusted-input
area: security
topic: python
task: bind-sql-parameters
title: An f-string SQL predicate runs the quote the caller sent
description: Use when a name filter built with an f-string returns every row for a payload that closes the quote.
triggers:
  - SQL injection f-string
  - OR 1=1
  - sqlite placeholder question mark
  - untrusted input in query
aliases:
  - python
  - sql
  - injection
related:
  - sqlite-null-comparisons-are-unknown
  - hmac-compare-digest-for-secrets
sources:
  - https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
commands:
  - python3 library/examples/sql-fstring-interpolates-untrusted-input/check.py
---

# An f-string SQL predicate runs the quote the caller sent

`f"SELECT id FROM people WHERE name = '{payload}'"` with `payload` equal to `' OR '1'='1` is one statement whose predicate is true for every row. The query returns the Ada row. sqlite3's placeholder section says to use `?` and a parameter sequence instead of formatting values into the string.

`WHERE name = ?` with `(payload,)` returns `[]`. The quote characters stay inside the bound value. They are not SQL syntax. The payload in the check is `' OR '1'='1`.

## Incorrect

```python file=library/examples/sql-fstring-interpolates-untrusted-input/incorrect.py
def find_user(connection, name):
    return list(connection.execute(f"select id from users where name = '{name}'"))
```

## Correct

```python file=library/examples/sql-fstring-interpolates-untrusted-input/correct.py
def find_user(connection, name):
    return list(connection.execute("select id from users where name = ?", (name,)))
```

## Verify

Run `python3 library/examples/sql-fstring-interpolates-untrusted-input/check.py`.

## Sources

- https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
