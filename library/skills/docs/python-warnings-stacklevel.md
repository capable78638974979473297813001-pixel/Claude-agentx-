---
id: python-warnings-stacklevel
area: docs
topic: python
task: attribute-warning-to-caller
title: warnings.warn stacklevel=1 names the helper; stacklevel=2 names the caller
description: Use when a deprecation warning points at your wrapper file instead of the application line that called it.
triggers:
  - warnings.warn stacklevel
  - stacklevel 2 filename
  - deprecation warning points at library
  - incorrect.py vs check.py
aliases:
  - python
  - warnings
  - stacklevel
related:
  - python-exception-context-chaining
  - python-generator-second-pass-empty
sources:
  - https://docs.python.org/3/library/warnings.html#warnings.warn
commands:
  - python3 library/examples/python-warnings-stacklevel/check.py
---

# warnings.warn stacklevel=1 names the helper; stacklevel=2 names the caller

`warnings.warn` records the filename `stacklevel` frames above the `warn` call. The default is 1, the line that called `warn`. A helper in `incorrect.py` that warns with `stacklevel=1` attributes the warning to `incorrect.py`. Callers then think the library file is the code they must change.

`stacklevel=2` attributes it to the caller. In this check the caller lives in `check.py`, and the warning filename is `check.py`. The warnings docs say stacklevel is how far up the stack the warning refers to. The check compares those two filenames and does not call `warn` through another wrapper.

## Incorrect

```python file=library/examples/python-warnings-stacklevel/incorrect.py
import warnings


def library_call():
    warnings.warn("quota exceeded", stacklevel=1)
```

## Correct

```python file=library/examples/python-warnings-stacklevel/correct.py
import warnings


def library_call():
    warnings.warn("quota exceeded", stacklevel=2)
```

## Verify

Run `python3 library/examples/python-warnings-stacklevel/check.py`.

## Sources

- https://docs.python.org/3/library/warnings.html#warnings.warn
