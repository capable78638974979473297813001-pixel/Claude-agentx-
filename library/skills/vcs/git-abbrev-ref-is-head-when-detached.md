---
id: git-abbrev-ref-is-head-when-detached
area: vcs
topic: git
task: detect-detached-head
title: git rev-parse --abbrev-ref HEAD prints HEAD when detached
description: Use when a deploy script treats the branch name HEAD as a real branch after checkout of a tag or a raw commit.
triggers:
  - detached HEAD abbrev-ref
  - rev-parse prints HEAD
  - symbolic-ref detached
  - branch name is HEAD
aliases:
  - git
  - detached
  - rev-parse
related:
  - git-describe-fails-on-shallow-clone
  - github-actions-unquoted-run-script
sources:
  - https://git-scm.com/docs/git-rev-parse
commands:
  - python3 library/examples/git-abbrev-ref-is-head-when-detached/check.py
---

# git rev-parse --abbrev-ref HEAD prints HEAD when detached

`git rev-parse --abbrev-ref HEAD` prints the branch name when HEAD is a branch. When HEAD is detached it prints the string `HEAD`. A script that deploys `origin/$name` will look for a branch named `HEAD`. The rev-parse manual describes `--abbrev-ref`.

`git symbolic-ref -q HEAD` exits non-zero when HEAD is not a symbolic ref to a branch. The correct helper returns `None` in that case. Check the exit status; do not parse the word `HEAD` out of abbrev-ref and then special-case the string.

Create the test repo with `git init -b main` so the attached case has a stable branch name. `git checkout --detach` is the setup that makes abbrev-ref print `HEAD`.

## Incorrect

```python file=library/examples/git-abbrev-ref-is-head-when-detached/incorrect.py
import subprocess


def branch_name(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
```

## Correct

```python file=library/examples/git-abbrev-ref-is-head-when-detached/correct.py
import subprocess


def branch_name(repo):
    completed = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "-q", "HEAD"],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()
```

## Verify

Run `python3 library/examples/git-abbrev-ref-is-head-when-detached/check.py`.

## Sources

- https://git-scm.com/docs/git-rev-parse
