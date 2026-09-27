---
id: idempotency-key-replays-stored-response
area: apis
topic: http
task: replay-idempotent-post
title: An idempotency key must replay the stored response, not run the handler again
description: Use when a retried POST with the same Idempotency-Key creates a second row or returns a new id.
triggers:
  - Idempotency-Key second POST
  - replay stored response
  - duplicate create on retry
  - idempotency store
aliases:
  - http
  - idempotency
  - post
related:
  - if-match-rejects-stale-update
  - sqlite-foreign-keys-require-pragma
sources:
  - https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-06
commands:
  - python3 library/examples/idempotency-key-replays-stored-response/check.py
---

# An idempotency key must replay the stored response, not run the handler again

A retry of a POST is a second HTTP request. The handler with no store runs twice (`calls == 2`) and returns a new id on the second call. The Idempotency-Key header draft says the server saves the first response and replays it for the same key.

The store keyed by that header runs the handler once. The second call returns the stored body, and the id does not become `2`.

## Incorrect

```python file=library/examples/idempotency-key-replays-stored-response/incorrect.py
def post(store, key, handler):
    return handler()
```

## Correct

```python file=library/examples/idempotency-key-replays-stored-response/correct.py
def post(store, key, handler):
    if key in store:
        return store[key]
    body = handler()
    store[key] = body
    return body
```

## Verify

Run `python3 library/examples/idempotency-key-replays-stored-response/check.py`.

## Sources

- https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-06
