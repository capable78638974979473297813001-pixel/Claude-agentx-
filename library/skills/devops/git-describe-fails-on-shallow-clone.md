---
id: git-describe-fails-on-shallow-clone
area: devops
topic: git
task: fetch-tags-before-describe
title: git describe --tags fails on a depth-1 clone with no names found
description: Use when CI prints fatal: No names found, cannot describe anything after a shallow clone of a tagged repo.
triggers:
  - No names found, cannot describe anything
  - git describe shallow clone
  - depth 1 missing tag
  - v1.2.3-1-g
aliases:
  - git
  - describe
  - ci
related:
  - git-abbrev-ref-is-head-when-detached
  - github-actions-unquoted-run-script
sources:
  - https://git-scm.com/docs/git-describe
commands:
  - python3 library/examples/git-describe-fails-on-shallow-clone/check.py
---

# git describe --tags fails on a depth-1 clone with no names found

`git describe` needs a tag it can walk to. The man page says it finds the most recent tag reachable from a commit. `git clone --depth 1` of a repo whose tag `v1.2.3` sits on the first commit, with HEAD one commit later, does not transfer that tag. `git describe --tags` then writes exactly `fatal: No names found, cannot describe anything.` on stderr and exits non-zero.

A full clone of the same repo prints a stdout line that starts with `v1.2.3-1-g`. The `-1-` is one commit after the tag, and `g` plus the abbreviated hash follows.

`actions/checkout` with `fetch-depth: 1` is this clone. Set `fetch-depth: 0`, or fetch the tags you describe, before calling `git describe`. `describe` on a shallow clone that happens to include the tag still works; the failure is the missing tag, not the command spelling.

## Incorrect

```python file=library/examples/git-describe-fails-on-shallow-clone/incorrect.py
import subprocess


def describe(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "describe", "--tags"],
        check=False,
        text=True,
        capture_output=True,
    )
```

## Correct

```python file=library/examples/git-describe-fails-on-shallow-clone/correct.py
import subprocess


def describe(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "describe", "--tags"],
        check=True,
        text=True,
        capture_output=True,
    )
```

## Verify

Run `python3 library/examples/git-describe-fails-on-shallow-clone/check.py`.

## Sources

- https://git-scm.com/docs/git-describe
