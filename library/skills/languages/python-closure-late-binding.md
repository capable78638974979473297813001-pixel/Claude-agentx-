---
id: python-closure-late-binding
area: languages
topic: python
task: capture-loop-value
title: A lambda in a loop reads i after the loop, unless the default binds it
description: Use when a list of lambdas created in a for-loop all return the last index instead of the index from their iteration.
triggers:
  - lambda loop late binding
  - closures all return 2
  - lambda i=i
  - default argument captures loop
aliases:
  - python
  - closure
  - lambda
related:
  - python-unboundlocalerror-on-assignment
  - python-generator-second-pass-empty
sources:
  - https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
commands:
  - python3 library/examples/python-closure-late-binding/check.py
---

# A lambda in a loop reads i after the loop, unless the default binds it

A function body looks up free variables when it runs, not when the `lambda` is created. The programming FAQ states that lambdas in a loop share the variable. After `for i in range(3)`, every `lambda: i` returns 2, so the list is `[2, 2, 2]`.

Default arguments are evaluated at definition. `lambda i=i: i` stores the integer from that iteration. The list is `[0, 1, 2]`.

The same lookup applies to a `def` nested in the loop, not only to `lambda`. A default of a mutable object is a different trap (one list shared by all calls). Here the default is the loop integer, which is the binding you want.

## Incorrect

```python file=library/examples/python-closure-late-binding/incorrect.py
def multipliers(count):
    funcs = []
    for i in range(count):
        funcs.append(lambda: i)
    return funcs
```

## Correct

```python file=library/examples/python-closure-late-binding/correct.py
def multipliers(count):
    funcs = []
    for i in range(count):
        funcs.append(lambda i=i: i)
    return funcs
```

## Verify

Run `python3 library/examples/python-closure-late-binding/check.py`.

## Sources

- https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
