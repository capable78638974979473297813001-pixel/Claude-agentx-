---
id: transactional-outbox-commit-with-row
area: architecture
topic: transactions
task: commit-outbox-with-order
title: The outbox row has to commit in the same transaction as the order
description: Use when an order row exists and the outbox is empty because the process raised after commit and before the outbox insert.
triggers:
  - transactional outbox
  - orders 1 outbox 0
  - rollback before commit
  - commit then raise
aliases:
  - sqlite
  - outbox
  - transactions
related:
  - idempotency-key-replays-stored-response
  - sqlite-foreign-keys-require-pragma
sources:
  - https://docs.python.org/3/library/sqlite3.html#transaction-control
commands:
  - python3 library/examples/transactional-outbox-commit-with-row/check.py
---

# The outbox row has to commit in the same transaction as the order

sqlite3 transaction control commits when you `commit()`. An insert into `orders`, a `commit()`, and then a raise before the outbox insert leaves `orders` at 1 and `outbox` at 0.

Insert both rows, then raise, and `rollback()` in the handler. Both counts stay 0. The check calls `place(..., True)` on each version and counts the rows after the `RuntimeError`.

## Incorrect

```python file=library/examples/transactional-outbox-commit-with-row/incorrect.py
def place(connection, should_fail):
    connection.execute("insert into orders(id) values (1)")
    connection.commit()
    if should_fail:
        raise RuntimeError("publisher down")
    connection.execute("insert into outbox(order_id) values (1)")
    connection.commit()
```

## Correct

```python file=library/examples/transactional-outbox-commit-with-row/correct.py
def place(connection, should_fail):
    try:
        connection.execute("insert into orders(id) values (1)")
        connection.execute("insert into outbox(order_id) values (1)")
        if should_fail:
            raise RuntimeError("publisher down")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
```

## Verify

Run `python3 library/examples/transactional-outbox-commit-with-row/check.py`.

## Sources

- https://docs.python.org/3/library/sqlite3.html#transaction-control
