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

The glossary defines a generator iterator as the object a generator function returns. It yields until exhaustion. `list(gen)` pulls every value. A second `list(gen)` on that same object is `[]`. Nothing in the iterator resets it.

Returning a list produces a new sequence each call, and the same list object can be iterated twice. If the caller needs two passes, return a list or have them call the generator function again to get a new iterator. Re-calling the function re-runs the body, which matters if the body reads a changing database.

A generator expression `(n for n in rows)` has the same one-pass behavior. `len()` on that object raises `TypeError` because a generator has no length. Call the generator function again when you need a second pass, or return a list.

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
