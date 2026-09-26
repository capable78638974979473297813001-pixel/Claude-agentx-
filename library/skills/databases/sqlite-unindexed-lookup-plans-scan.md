---
id: sqlite-unindexed-lookup-plans-scan
area: databases
topic: sqlite
task: index-the-filtered-column
title: A lookup on user_id scans until an index exists, and the plan says COVERING
description: Use when EXPLAIN QUERY PLAN prints SCAN events for a user_id filter and you expected SEARCH using an index.
triggers:
  - EXPLAIN QUERY PLAN SCAN
  - SEARCH COVERING INDEX
  - unindexed user_id
  - sqlite query plan
aliases:
  - sqlite
  - index
  - explain
related:
  - n-plus-one-query-per-row
  - sqlite-foreign-keys-require-pragma
sources:
  - https://www.sqlite.org/eqp.html
commands:
  - python3 library/examples/sqlite-unindexed-lookup-plans-scan/check.py
---

# A lookup on user_id scans until an index exists, and the plan says COVERING

Without an index, `EXPLAIN QUERY PLAN` for `SELECT ... FROM events WHERE user_id = ?` contains `SCAN events`. SQLite's query plan page describes `SCAN` as a full walk of the table.

After `CREATE INDEX events_user_id ON events(user_id)`, the plan is `SEARCH events USING COVERING INDEX events_user_id (user_id=?)`. A test that looks for the substring `USING INDEX events_user_id` fails because the word `COVERING` sits between `USING` and `INDEX`. Look for `SEARCH` and `events_user_id`.

The word `COVERING` in that plan means this query's selected columns were available from the index. Match `SEARCH` and the index name. `SCAN` is the plan this lookup had before the index existed.

## Incorrect

```python file=library/examples/sqlite-unindexed-lookup-plans-scan/incorrect.py
def create(connection):
    connection.execute("create table events(id integer primary key, user_id integer)")
```

## Correct

```python file=library/examples/sqlite-unindexed-lookup-plans-scan/correct.py
def create(connection):
    connection.execute("create table events(id integer primary key, user_id integer)")
    connection.execute("create index events_user_id on events(user_id)")
```

## Verify

Run `python3 library/examples/sqlite-unindexed-lookup-plans-scan/check.py`.

## Sources

- https://www.sqlite.org/eqp.html
