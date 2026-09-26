---
name: python-engineering
description: Modern Python conventions - project layout, typing, dataclasses, Decimal, pathlib, pytest, packaging with pyproject, and stdlib-first dependencies. Use when writing or reviewing Python code in this repo or projects it builds.
---

# Python engineering

- Python 3.11+. `pyproject.toml`; `src/` or flat package, pick one and stay.
- Type hints on public functions; `from __future__ import annotations` is fine.
- `@dataclass(frozen=True, slots=True)` for value objects.
- `decimal.Decimal` from strings for money; `pathlib.Path` for files.
- No mutable default arguments. No bare `except:`.
- pytest: plain asserts, fixtures for setup, `parametrize` for tables,
  `hypothesis` for properties when available.
- Stdlib first; add a dependency only when it removes real code.
- `python -m package` entry point via `__main__.py`; argparse for CLIs.
- Run: `python -m pytest -q` before claiming done.
