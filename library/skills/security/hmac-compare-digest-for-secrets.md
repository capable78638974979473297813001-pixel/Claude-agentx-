---
id: hmac-compare-digest-for-secrets
area: security
topic: python
task: compare-mac-bytes
title: hmac.compare_digest rejects a str against bytes and returns False for a different length
description: Use when compare_digest raises TypeError: a bytes-like object is required, not 'str', or a token check uses ==.
triggers:
  - compare_digest TypeError str
  - hmac timing
  - bytes-like object is required
  - compare digest length
aliases:
  - python
  - hmac
  - compare_digest
related:
  - sql-fstring-interpolates-untrusted-input
  - if-match-rejects-stale-update
sources:
  - https://docs.python.org/3/library/hmac.html#hmac.compare_digest
commands:
  - python3 library/examples/hmac-compare-digest-for-secrets/check.py
---

# hmac.compare_digest rejects a str against bytes and returns False for a different length

`hmac.compare_digest` requires both arguments to be the same type, either `bytes` or `str`. `hmac.compare_digest(b"secret", "secret")` raises `TypeError: a bytes-like object is required, not 'str'`. The hmac docs state that mixed types throw.

Different lengths return `False` without raising. That includes a truncated MAC. Encode both sides with the same encoding, or hex-decode both, before comparing.

This check does not measure a timing gap between `==` and `compare_digest`. The function exists so the comparison does not return early on the first differing byte; do not invent a benchmark number for that. `==` on the raw token is the comparison to replace, after the types match.

## Incorrect

```python file=library/examples/hmac-compare-digest-for-secrets/incorrect.py
def tokens_match(left, right):
    return left == right
```

## Correct

```python file=library/examples/hmac-compare-digest-for-secrets/correct.py
import hmac


def tokens_match(left, right):
    if isinstance(left, str):
        left = left.encode("utf-8")
    if isinstance(right, str):
        right = right.encode("utf-8")
    return hmac.compare_digest(left, right)
```

## Verify

Run `python3 library/examples/hmac-compare-digest-for-secrets/check.py`.

## Sources

- https://docs.python.org/3/library/hmac.html#hmac.compare_digest
