---
id: path-join-allows-traversal
area: security
topic: python
task: contain-joined-path
title: normpath(join(root, user)).startswith(root) accepts uploads-evil
description: Use when a filename of ../uploads-evil/x.txt passes a startswith check against the uploads directory.
triggers:
  - path traversal startswith
  - uploads-evil
  - os.path.commonpath
  - normpath join escape
aliases:
  - python
  - path
  - traversal
related:
  - sql-fstring-interpolates-untrusted-input
  - node-http-client-hangs-without-end
sources:
  - https://docs.python.org/3/library/os.path.html#os.path.commonpath
commands:
  - python3 library/examples/path-join-allows-traversal/check.py
---

# normpath(join(root, user)).startswith(root) accepts uploads-evil

`os.path.normpath(os.path.join(uploads, "../uploads-evil/x.txt"))` lands in a sibling directory named `uploads-evil`. `str.startswith(uploads_root)` is true because the string `uploads-evil` begins with the string `uploads`. The file is outside the root and the check says it is inside.

`os.path.commonpath` of the realpaths returns the parent of both directories, not the uploads root. The docs define `commonpath` as the longest common sub-path. Compare that result to the real uploads root and reject the join when they differ.

`Path.resolve()` plus `relative_to` raises `ValueError` when the target escapes. String prefix checks do not. Also reject absolute user input before `join`, because `join(root, "/etc/passwd")` discards `root` on POSIX.

## Incorrect

```python file=library/examples/path-join-allows-traversal/incorrect.py
import os


def resolve(root, user_path):
    return os.path.normpath(os.path.join(root, user_path))


def is_inside(root, candidate):
    return os.path.normpath(candidate).startswith(os.path.normpath(root))
```

## Correct

```python file=library/examples/path-join-allows-traversal/correct.py
import os


def resolve(root, user_path):
    root_real = os.path.realpath(root)
    candidate = os.path.realpath(os.path.join(root, user_path))
    if os.path.commonpath([root_real, candidate]) != root_real:
        raise ValueError("path escapes root")
    return candidate
```

## Verify

Run `python3 library/examples/path-join-allows-traversal/check.py`.

## Sources

- https://docs.python.org/3/library/os.path.html#os.path.commonpath
