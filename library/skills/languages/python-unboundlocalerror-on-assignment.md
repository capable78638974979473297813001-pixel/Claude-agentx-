---
id: python-unboundlocalerror-on-assignment
area: languages
topic: python
task: bind-name-before-read
title: Assigning to count makes it local, so the earlier print raises UnboundLocalError
description: Use when Python says cannot access local variable 'count' where it is not associated with a value, even though count exists on the module.
triggers:
  - UnboundLocalError count
  - cannot access local variable
  - local variable is not associated with a value
  - global count assignment
aliases:
  - python
  - unboundlocal
  - scoping
related:
  - python-closure-late-binding
  - python-exception-context-chaining
sources:
  - https://docs.python.org/3/reference/executionmodel.html#binding-of-names
commands:
  - python3 library/examples/python-unboundlocalerror-on-assignment/check.py
---

# Assigning to count makes it local, so the earlier print raises UnboundLocalError

Python decides that `count` is local to `label` because the function assigns to it. The assignment is `count = count + 1`, which is after `print(count)`. At the print, the local is not bound yet, so Python 3.12 raises `UnboundLocalError: cannot access local variable 'count' where it is not associated with a value`. The module-level `count = 0` is not consulted.

A parameter named `count` is already bound, so the same print would not raise. That is why a test that passes `count` in as an argument never sees this error.

`global count` makes the assignment target the module name. `label()` then returns 1. Use `global` only when the function is supposed to mutate the module. Otherwise pass the number in and return the next value.

## Incorrect

```python file=library/examples/python-unboundlocalerror-on-assignment/incorrect.py
count = 0


def label():
    print(count)
    count = count + 1
    return count
```

## Correct

```python file=library/examples/python-unboundlocalerror-on-assignment/correct.py
count = 0


def label():
    global count
    print(count)
    count = count + 1
    return count
```

## Verify

Run `python3 library/examples/python-unboundlocalerror-on-assignment/check.py`.

## Sources

- https://docs.python.org/3/reference/executionmodel.html#binding-of-names
