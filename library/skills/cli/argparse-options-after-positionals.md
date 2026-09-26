---
id: argparse-options-after-positionals
area: cli
topic: python
task: pass-options-after-double-dash
title: argparse nargs='*' rejects an unknown --flag unless the user passes --
description: Use when a CLI exits 2 with unrecognized arguments: --flag after a positional that was meant to accept extra options.
triggers:
  - unrecognized arguments: --flag
  - argparse SystemExit 2
  - nargs star double dash
  - arguments containing -
aliases:
  - python
  - argparse
  - cli
related:
  - node-http-client-hangs-without-end
  - github-actions-unquoted-run-script
sources:
  - https://docs.python.org/3/library/argparse.html#arguments-containing
commands:
  - python3 library/examples/argparse-options-after-positionals/check.py
---

# argparse nargs='*' rejects an unknown --flag unless the user passes --

The argparse page "Arguments containing `-`" says optional arguments start with `-`, and `--` ends option processing. A positional with `nargs='*'` still treats `--flag` as an optional it does not know. `parse_args(['run', '--flag'])` raises `SystemExit` with code 2 and the message `unrecognized arguments: --flag`.

`parse_args(['run', '--', '--flag'])` puts `['--flag']` in the positional. The check expects `SystemExit` code `2` for the first argv and that list for the second.

## Incorrect

```python file=library/examples/argparse-options-after-positionals/incorrect.py
import argparse


def parse(argv):
    parser = argparse.ArgumentParser(prog="tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("cmd")
    parser.add_argument("args", nargs="*")
    return parser.parse_args(argv)
```

## Correct

```python file=library/examples/argparse-options-after-positionals/correct.py
import argparse


def command_line(cmd, child_args):
    return [cmd, "--", *child_args]


def parse(argv):
    parser = argparse.ArgumentParser(prog="tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("cmd")
    parser.add_argument("args", nargs="*")
    return parser.parse_args(argv)
```

## Verify

Run `python3 library/examples/argparse-options-after-positionals/check.py`.

## Sources

- https://docs.python.org/3/library/argparse.html#arguments-containing
