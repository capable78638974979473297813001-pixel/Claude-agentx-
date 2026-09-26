---
id: python-exception-context-chaining
area: debugging
topic: python
task: chain-exception-cause
title: raise X from exc sets __cause__; a bare raise inside except sets __context__
description: Use when a log shows 'During handling of the above exception' and __cause__ is None, or you need the original ValueError attached as the cause.
triggers:
  - exception __context__ __cause__
  - raise from
  - During handling of the above exception
  - implicit exception chaining
aliases:
  - python
  - exceptions
  - traceback
related:
  - python-warnings-stacklevel
  - python-unboundlocalerror-on-assignment
sources:
  - https://docs.python.org/3/library/exceptions.html#exception-context
commands:
  - python3 library/examples/python-exception-context-chaining/check.py
---

# raise X from exc sets __cause__; a bare raise inside except sets __context__

Raising `RuntimeError` inside `except ValueError` attaches the `ValueError` as `__context__` and leaves `__cause__` as `None`. The traceback printer then says the new error happened "During handling of the above exception". The exceptions docs describe this implicit chain.

`raise RuntimeError from exc` sets `__cause__` to that `ValueError`. The printer says "The above exception was the direct cause". `__suppress_context__` is also set, so the implicit context is not the line you read first.

Use `raise NewError(...) from exc` when the new error is the one callers should catch and the original is the reason. Use `raise NewError(...) from None` only when the original context is noise you have deliberately dropped.

## Incorrect

```python file=library/examples/python-exception-context-chaining/incorrect.py
def convert(raw):
    try:
        int(raw)
    except ValueError:
        raise RuntimeError("bad token")
```

## Correct

```python file=library/examples/python-exception-context-chaining/correct.py
def convert(raw):
    try:
        int(raw)
    except ValueError as exc:
        raise RuntimeError("bad token") from exc
```

## Verify

Run `python3 library/examples/python-exception-context-chaining/check.py`.

## Sources

- https://docs.python.org/3/library/exceptions.html#exception-context
