---
id: cursor-page-needs-unique-tie-break
area: apis
topic: pagination
task: keyset-with-unique-column
title: A keyset cursor on created alone skips rows that share the timestamp
description: Use when page 2 of a created_at cursor jumps over a row that has the same timestamp as the last row of page 1.
triggers:
  - keyset pagination skips tie
  - created_at cursor duplicate
  - tuple comparison created id
  - page size 1 misses id 2
aliases:
  - pagination
  - cursor
  - sql
related:
  - react-index-key-sticks-dom-state
  - sqlite-null-comparisons-are-unknown
sources:
  - https://www.sqlite.org/rowvalue.html
commands:
  - python3 library/examples/cursor-page-needs-unique-tie-break/check.py
---

# A keyset cursor on created alone skips rows that share the timestamp

Rows with ids 2 and 1 share `created = 2024-01-01`. Id 3 is the next day. With page size 1, a cursor that keeps only `created` and asks for `created > ?` returns pages `[1, 3]`. Id 2 is never emitted: it is not greater than the timestamp of id 1, and it is not the row already returned.

A tuple comparison `(created, id) > (?, ?)` returns `[1, 2]`. SQLite row values document that comparison. The tie-break column has to be unique and present in the sort, or two rows with the same timestamp collapse into one page boundary.

Sorting in Python with a stable sort and then using OFFSET does not reproduce this skip. The bug is the strict greater-than on a non-unique column. Include the primary key in both the ORDER BY and the cursor predicate.

## Incorrect

```python file=library/examples/cursor-page-needs-unique-tie-break/incorrect.py
def page(rows, limit, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    if cursor is None:
        return ordered[:limit]
    created, _row_id = cursor
    return [row for row in ordered if row["created"] > created][:limit]
```

## Correct

```python file=library/examples/cursor-page-needs-unique-tie-break/correct.py
def page(rows, limit, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    if cursor is None:
        return ordered[:limit]
    return [row for row in ordered if (row["created"], row["id"]) > cursor][:limit]
```

## Verify

Run `python3 library/examples/cursor-page-needs-unique-tie-break/check.py`.

## Sources

- https://www.sqlite.org/rowvalue.html
