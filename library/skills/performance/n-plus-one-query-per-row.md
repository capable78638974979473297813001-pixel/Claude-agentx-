---
id: n-plus-one-query-per-row
area: performance
topic: sql
task: batch-the-lookup
title: One query per user is N round trips; one IN list is a single query
description: Use when a trace shows one SELECT per user id and the count equals the page size.
triggers:
  - N+1 query
  - SELECT per user id
  - IN clause placeholders
  - query count equals row count
aliases:
  - sql
  - n-plus-one
  - sqlite
related:
  - sqlite-unindexed-lookup-plans-scan
  - cursor-page-needs-unique-tie-break
sources:
  - https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
commands:
  - python3 library/examples/n-plus-one-query-per-row/check.py
---

# One query per user is N round trips; one IN list is a single query

Loading three users and then selecting each user's events inside the loop records 3 statements. The number of statements grows with the page. That is the N+1 shape: 1 query for the parents plus N queries for the children, and here the trace is counting the N child queries.

One statement, `WHERE user_id IN (?,?,?)`, records a single execution. Build the placeholder list from `len(user_ids)`, not by interpolating the ids into the SQL text. The sqlite3 placeholder docs require a `?` per bound value. The check's trace length is `3` for the loop and `1` for the `IN` list.

## Incorrect

```python file=library/examples/n-plus-one-query-per-row/incorrect.py
def load_orders(connection, user_ids):
    orders = []
    for user_id in user_ids:
        orders.extend(
            connection.execute(
                "select id from orders where user_id = ?",
                (user_id,),
            ).fetchall()
        )
    return orders
```

## Correct

```python file=library/examples/n-plus-one-query-per-row/correct.py
def load_orders(connection, user_ids):
    marks = ",".join("?" for _ in user_ids)
    return connection.execute(
        f"select id from orders where user_id in ({marks})",
        tuple(user_ids),
    ).fetchall()
```

## Verify

Run `python3 library/examples/n-plus-one-query-per-row/check.py`.

## Sources

- https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
