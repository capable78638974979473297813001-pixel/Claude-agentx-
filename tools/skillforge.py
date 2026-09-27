#!/usr/bin/env python3
"""Search and validate the skill library.

Verified skills: library/skills/<area>/<id>.md
Curated notes:   .claude/skills/<name>/SKILL.md  (tax section, plus engineering)

`route` returns a few matches or abstains. An abstention means: reason
without a skill. Lenses and domain notes are not skills and are not routed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from library.catalog import skill_tree  # noqa: E402
from library.load import load_library  # noqa: E402
from library.router import Router, format_route  # noqa: E402
from library.validate import summary, validate_verified  # noqa: E402

LENSES_DIR = ROOT / "forge" / "lenses"
DOMAINS_DIR = ROOT / "forge" / "domains"
INDEX_FILE = ROOT / "catalog" / "index.json"


def _library():
    skills = load_library(ROOT)
    return skills, Router(skills)


def cmd_stats(_args) -> int:
    skills, _router = _library()
    data = summary(skills)
    print(f"verified skills   {data['verified']}")
    print(f"curated skills    {data['curated']}")
    print(f"total             {data['total']}")
    print("verified by area:")
    for area, count in data["verified_by_area"].items():
        print(f"  {area:16} {count}")
    print("curated by area:")
    for area, count in data["curated_by_area"].items():
        print(f"  {area:16} {count}")
    print(f"lenses (not routed)   {len(list(LENSES_DIR.glob('*.md')))}")
    print(f"domain notes (not routed) {len(list(DOMAINS_DIR.glob('*.md')))}")
    return 0


def cmd_list(args) -> int:
    skills, _router = _library()
    for skill in skills:
        if args.area and skill.area != args.area:
            continue
        if args.kind and skill.kind != args.kind:
            continue
        print(f"{skill.kind:9} {skill.area:14} {skill.id}")
    return 0


def cmd_show(args) -> int:
    skills, _router = _library()
    for skill in skills:
        if skill.id == args.id:
            print((ROOT / skill.path).read_text(encoding="utf-8"))
            return 0
    print(f"unknown skill: {args.id}", file=sys.stderr)
    return 1


def cmd_route(args) -> int:
    _skills, router = _library()
    result = router.route(" ".join(args.query), k=args.k)
    print(format_route(result))
    return 0 if result.confident else 2


def cmd_browse(args) -> int:
    skills, router = _library()
    try:
        payload = router.browse(args.area, args.topic)
    except KeyError as exc:
        print(f"unknown: {exc}", file=sys.stderr)
        return 1
    if args.area is None:
        print(json.dumps({"areas": payload, "tree_areas": list(skill_tree(skills))}, indent=2))
        return 0
    print(json.dumps(payload, indent=2))
    return 0


def cmd_validate(args) -> int:
    errors = validate_verified(root=ROOT, run=not args.skip_commands, check_urls=not args.skip_urls)
    for err in errors:
        print(err)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} problem(s)")
    return 1 if errors else 0


def build_index() -> dict:
    skills, _router = _library()
    data = summary(skills)
    return {
        "verified": data["verified"],
        "curated": data["curated"],
        "total": data["total"],
        "verified_by_area": data["verified_by_area"],
        "curated_by_area": data["curated_by_area"],
        "counts_note": (
            "verified is the count of skills whose examples ran. "
            "Curated tax skills were kept and not expanded. "
            "Lenses and domain notes are omitted because the router does not search them."
        ),
        "tree": skill_tree(skills),
        "skills": [
            {
                "id": skill.id,
                "area": skill.area,
                "topic": skill.topic,
                "task": skill.task,
                "title": skill.title,
                "description": skill.description,
                "path": skill.path,
                "kind": skill.kind,
                "related": list(skill.related),
            }
            for skill in skills
        ],
    }


def cmd_index(_args) -> int:
    INDEX_FILE.parent.mkdir(exist_ok=True)
    INDEX_FILE.write_text(json.dumps(build_index(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {INDEX_FILE.relative_to(ROOT)}")
    return 0


def cmd_banner(_args) -> int:
    skills, _router = _library()
    data = summary(skills)
    areas = ", ".join(f"{name} {count}" for name, count in data["verified_by_area"].items())
    print(
        f"Skill library: {data['verified']} verified skills ({areas}). "
        f"{data['curated']} curated notes (tax and engineering, not expanded). "
        "Route with: python3 tools/skillforge.py route \"<question>\". "
        "If the router is not confident, reason without a skill."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skillforge", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats", help="count verified and curated skills")
    list_parser = sub.add_parser("list", help="list skill ids")
    list_parser.add_argument("--area")
    list_parser.add_argument("--kind", choices=["verified", "curated"])
    show_parser = sub.add_parser("show", help="print one skill")
    show_parser.add_argument("id")
    route_parser = sub.add_parser("route", help="route a question or abstain")
    route_parser.add_argument("query", nargs="+")
    route_parser.add_argument("--k", type=int, default=5)
    search_parser = sub.add_parser("search", help="alias of route")
    search_parser.add_argument("query", nargs="+")
    search_parser.add_argument("--k", type=int, default=5)
    browse_parser = sub.add_parser("browse", help="area, then topic, then task")
    browse_parser.add_argument("--area")
    browse_parser.add_argument("--topic")
    validate_parser = sub.add_parser("validate", help="schema, duplicates, sources, and examples")
    validate_parser.add_argument("--skip-commands", action="store_true")
    validate_parser.add_argument("--skip-urls", action="store_true")
    sub.add_parser("index", help="write catalog/index.json")
    sub.add_parser("banner", help="one-line summary for the session hook")
    args = parser.parse_args(argv)
    command = "route" if args.cmd == "search" else args.cmd
    return globals()[f"cmd_{command}"](args)


if __name__ == "__main__":
    sys.exit(main())
