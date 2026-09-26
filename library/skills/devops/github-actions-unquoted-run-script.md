---
id: github-actions-unquoted-run-script
area: devops
topic: github-actions
task: quote-untrusted-run-input
title: Interpolating untrusted text into a run script executes it as shell
description: Use when a workflow builds echo {message} from an issue title and the title contains a semicolon and a second command.
triggers:
  - github actions script injection
  - untrusted input in run
  - echo message PWNED
  - quote env in run step
aliases:
  - github-actions
  - shell
  - injection
related:
  - git-describe-fails-on-shallow-clone
  - sql-fstring-interpolates-untrusted-input
sources:
  - https://docs.github.com/en/actions/reference/security/secure-use#understanding-the-risk-of-script-injections
commands:
  - python3 library/examples/github-actions-unquoted-run-script/check.py
---

# Interpolating untrusted text into a run script executes it as shell

GitHub Actions substitutes `${{ }}` expressions into the shell script before the shell parses it. The secure-use page calls this script injection. Building `echo {message}` with message `hello; echo PWNED` produces the script `echo hello; echo PWNED`, and bash runs `PWNED` as its own command.

An environment variable does not reparse `;` on expansion. `echo $MSG` with that same string prints one line, `hello; echo PWNED`. The injection is the substitution into the script source, not the unquoted expansion of a variable. The fix in this check is to emit `echo "$MSG"` and pass the text as the environment variable, so the semicolon stays data.

Do not paste `github.event.issue.title`, pull request bodies, or commit messages into `run:`. Put them in `env:` and quote the expansion.

## Incorrect

```python file=library/examples/github-actions-unquoted-run-script/incorrect.py
def render(message):
    return f"echo {message}\n"
```

## Correct

```python file=library/examples/github-actions-unquoted-run-script/correct.py
def render(_message):
    return 'echo "$MSG"\n'
```

## Verify

Run `python3 library/examples/github-actions-unquoted-run-script/check.py`.

## Sources

- https://docs.github.com/en/actions/reference/security/secure-use#understanding-the-risk-of-script-injections
