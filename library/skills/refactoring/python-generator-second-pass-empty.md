---
id: python-generator-second-pass-empty
area: refactoring
topic: python
task: reuse-a-sequence
title: A generator iterator is empty the second time you iterate it
description: Use when the first list(gen) has the rows and the second list(gen) is [] after a refactor that replaced a list with yield.
triggers:
  - generator second iteration empty
  - list(gen) then empty
  - generator iterator exhausted
  - yield consumed
aliases:
  - python
  - generator
  - iterator
related:
  - python-closure-late-binding
  - python-warnings-stacklevel
sources:
  - https://docs.python.org/3/glossary.html#term-generator-iterator
commands:
  - python3 library/examples/python-generator-second-pass-empty/check.py
---

# A generator iterator is empty the second time you iterate it

The glossary defines a generator iterator as the object a generator function returns. `rows()` in `incorrect.py` yields `"a"` then `"b"`. `list(gen)` on that object is `['a', 'b']`. A second `list(gen)` on the same object is `[]`. The check raises `SystemExit` unless both of those lists match.

`correct.py` returns `["a", "b"]`. `list()` on that object twice is `['a', 'b']` both times. The check loads each file with `importlib` from the example directory and prints `incorrect: observed []` for the exhausted iterator.

The second pass is an empty list, not an exception. The iterator does not refill itself. A caller that keeps the object from the first `rows()` call and iterates it again sees no rows.

## Incorrect

```python file=library/examples/python-generator-second-pass-empty/incorrect.py
def rows():
    yield "a"
    yield "b"
```

## Correct

```python file=library/examples/python-generator-second-pass-empty/correct.py
def rows():
    return ["a", "b"]
```

## Verify

Run `python3 library/examples/python-generator-second-pass-empty/check.py`.

## Sources

- https://docs.python.org/3/glossary.html#term-generator-iterator
