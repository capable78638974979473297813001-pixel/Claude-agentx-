---
id: if-match-rejects-stale-update
area: apis
topic: http
task: reject-stale-if-match
title: A second update with a stale version must return 412
description: Use when two clients PUT the same row and the slower write overwrites the faster one, or version climbs past the client's If-Match.
triggers:
  - If-Match 412
  - lost update version
  - stale client_version
  - conditional update
aliases:
  - http
  - etag
  - if-match
related:
  - idempotency-key-replays-stored-response
  - transactional-outbox-commit-with-row
sources:
  - https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match
commands:
  - python3 library/examples/if-match-rejects-stale-update/check.py
---

# A second update with a stale version must return 412

RFC 9110 `If-Match` tells the origin to apply the request only when the current representation matches the validator the client sent. An update that ignores `client_version` applies version 1 twice: the row ends at version 3 with name `c`.

The check that compares `client_version` to the stored version applies the first update (name `b`, version 2) and returns 412 on the second call. The name stays `b`.

Compare against the version you read in the same statement that writes, `UPDATE ... WHERE id = ? AND version = ?`, and treat a zero rowcount as 412. A check-then-write in two statements still loses if another request commits between them.

## Incorrect

```python file=library/examples/if-match-rejects-stale-update/incorrect.py
def update(row, new_name, client_version):
    row["name"] = new_name
    row["version"] += 1
    return 200
```

## Correct

```python file=library/examples/if-match-rejects-stale-update/correct.py
def update(row, new_name, client_version):
    if row["version"] != client_version:
        return 412
    row["name"] = new_name
    row["version"] += 1
    return 200
```

## Verify

Run `python3 library/examples/if-match-rejects-stale-update/check.py`.

## Sources

- https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match
