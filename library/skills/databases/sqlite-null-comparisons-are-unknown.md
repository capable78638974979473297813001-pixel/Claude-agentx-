---
id: sqlite-null-comparisons-are-unknown
area: databases
topic: sqlite
task: include-null-in-filter
title: name != 'Ada' does not return the row whose name is NULL
description: Use when a filter meant to exclude one name also drops rows with a null name, and the missing row has no SQL error.
triggers:
  - NULL comparison unknown
  - name != Ada misses null
  - IS NULL or not equal
  - three-valued logic
aliases:
  - sqlite
  - null
  - sql
related:
  - sqlite-foreign-keys-require-pragma
  - sql-fstring-interpolates-untrusted-input
sources:
  - https://www.sqlite.org/nulls.html
commands:
  - python3 library/examples/sqlite-null-comparisons-are-unknown/check.py
---

# name != 'Ada' does not return the row whose name is NULL

SQLite's NULL handling page: a comparison with NULL is not true. `name != 'Ada'` is unknown for the row whose name is NULL, so the row is filtered out. With rows (1, 'Ada'), (2, 'Grace'), (3, NULL), the query returns only id 2.

`name != 'Ada' OR name IS NULL` returns ids 2 and 3. `IS NOT` is the operator that treats NULL as a value; `!=` is not.

The same unknown result applies to `=`, `<`, and `IN` when the column is NULL. `NOT IN` with a NULL in the list is a separate trap that can filter out every row. This skill is the `!=` case: add `OR column IS NULL` when nulls belong in the "not this value" set.

## Incorrect

```python file=library/examples/sqlite-null-comparisons-are-unknown/incorrect.py
import sqlite3


def missing_names(connection):
    return list(connection.execute("select id from people where name != 'Ada'"))
```

## Correct

```python file=library/examples/sqlite-null-comparisons-are-unknown/correct.py
import sqlite3


def missing_names(connection):
    return list(
        connection.execute("select id from people where name != 'Ada' or name is null")
    )
```

## Verify

Run `python3 library/examples/sqlite-null-comparisons-are-unknown/check.py`.

## Sources

- https://www.sqlite.org/nulls.html
