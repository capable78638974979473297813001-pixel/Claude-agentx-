#!/usr/bin/env python3
"""skillforge: search, mix, and validate the AgentX skill library.

Atoms   = hand-written skills in .claude/skills/<name>/SKILL.md
Lenses  = working styles in forge/lenses/<name>.md
Domains = domain packs in forge/domains/<name>.md
Agents  = team members in .claude/agents/<name>.md

A *blend* is 1-3 atoms, optionally viewed through one lens and one domain.
`compose` materializes a blend as a single skill file a swarm agent can read.

Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
AGENTS_DIR = ROOT / ".claude" / "agents"
LENSES_DIR = ROOT / "forge" / "lenses"
DOMAINS_DIR = ROOT / "forge" / "domains"
KITS_FILE = ROOT / "catalog" / "kits.json"
INDEX_FILE = ROOT / "catalog" / "index.json"
SWARM_DIR = ROOT / ".swarm"

MAX_ATOMS = 3
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass
class Entry:
    kind: str  # atom | lens | domain | agent
    name: str
    description: str
    body: str
    path: Path
    meta: dict[str, str] = field(default_factory=dict)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    body = text[end + 4:].lstrip("\n")
    return meta, body


def _load(kind: str, paths: list[Path]) -> list[Entry]:
    entries = []
    for path in sorted(paths):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        name = meta.get("name") or (path.parent.name if kind == "atom" else path.stem)
        entries.append(Entry(kind, name, meta.get("description", ""), body, path, meta))
    return entries


def load_all() -> dict[str, list[Entry]]:
    return {
        "atom": _load("atom", list(SKILLS_DIR.glob("*/SKILL.md"))),
        "lens": _load("lens", list(LENSES_DIR.glob("*.md"))),
        "domain": _load("domain", list(DOMAINS_DIR.glob("*.md"))),
        "agent": _load("agent", list(AGENTS_DIR.glob("*.md"))),
    }


def by_name(entries: list[Entry]) -> dict[str, Entry]:
    return {e.name: e for e in entries}


def blend_count(atoms: int, lenses: int, domains: int, max_atoms: int = MAX_ATOMS) -> int:
    """Distinct blends: 1..max_atoms atoms x (no lens | one lens) x (no domain | one domain)."""
    atom_sets = sum(math.comb(atoms, k) for k in range(1, max_atoms + 1))
    return atom_sets * (lenses + 1) * (domains + 1)


# ---------------------------------------------------------------- commands

def cmd_stats(lib, args) -> int:
    a, l, d, g = (len(lib[k]) for k in ("atom", "lens", "domain", "agent"))
    print(f"atoms (core skills)  {a}")
    print(f"lenses               {l}")
    print(f"domain packs         {d}")
    print(f"agents               {g}")
    print(f"blends               {blend_count(a, l, d):,}  "
          f"(1-{MAX_ATOMS} atoms x optional lens x optional domain)")
    return 0


def cmd_list(lib, args) -> int:
    kinds = [args.kind] if args.kind else ["atom", "lens", "domain", "agent"]
    for kind in kinds:
        print(f"\n# {kind}s")
        for e in lib[kind]:
            print(f"  {e.name:34} {e.description[:90]}")
    return 0


def _tokens(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower())


def search(lib, query: str, limit: int = 15) -> list[tuple[float, Entry]]:
    terms = _tokens(query)
    results = []
    for kind in ("atom", "lens", "domain", "agent"):
        for e in lib[kind]:
            name, desc, body = (" ".join(_tokens(x)) for x in (e.name, e.description, e.body))
            score = 0.0
            for t in terms:
                score += 5 * name.count(t) + 2 * desc.count(t) + 0.25 * min(body.count(t), 8)
            if score:
                results.append((score, e))
    results.sort(key=lambda r: (-r[0], r[1].name))
    return results[:limit]


def cmd_search(lib, args) -> int:
    hits = search(lib, " ".join(args.query), args.limit)
    if not hits:
        print("no matches")
        return 1
    for score, e in hits:
        print(f"{score:6.1f}  {e.kind:6} {e.name:34} {e.description[:80]}")
    return 0


def cmd_show(lib, args) -> int:
    for kind in ("atom", "lens", "domain", "agent"):
        e = by_name(lib[kind]).get(args.name)
        if e:
            print(e.path.read_text(encoding="utf-8"))
            return 0
    print(f"unknown: {args.name}", file=sys.stderr)
    return 1


def demote_headings(text: str) -> str:
    """Push markdown headings down one level, leaving fenced code untouched."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"#+ ", line):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)


def compose(lib, atom_names: list[str], lens: str | None, domain: str | None,
            name: str | None = None) -> str:
    atoms_by, lenses_by, domains_by = (by_name(lib[k]) for k in ("atom", "lens", "domain"))
    if not 1 <= len(atom_names) <= MAX_ATOMS:
        raise ValueError(f"pick 1-{MAX_ATOMS} atoms (got {len(atom_names)})")
    if len(set(atom_names)) != len(atom_names):
        raise ValueError("duplicate atoms")
    missing = [a for a in atom_names if a not in atoms_by]
    if missing:
        raise ValueError(f"unknown atom(s): {', '.join(missing)}")
    if lens and lens not in lenses_by:
        raise ValueError(f"unknown lens: {lens}")
    if domain and domain not in domains_by:
        raise ValueError(f"unknown domain: {domain}")

    atoms = [atoms_by[a] for a in atom_names]
    parts = [*atom_names, *(p for p in (lens, domain) if p)]
    blend_name = name or "blend-" + "--".join(parts)
    desc = "Forged blend of " + " + ".join(atom_names)
    if lens:
        desc += f", through the {lens} lens"
    if domain:
        desc += f", in the {domain} domain"

    out = [
        "---",
        f"name: {blend_name}",
        f"description: {desc}.",
        "---",
        "",
        f"# {blend_name}",
        "",
        "## How to use this blend",
        "",
        f"- **Primary craft**: `{atom_names[0]}`. Build with it.",
    ]
    for a in atom_names[1:]:
        out.append(f"- **Mixed in**: `{a}`. Apply it wherever it touches the primary craft;"
                   " if the two conflict, the stricter rule wins.")
    if lens:
        out.append(f"- **Lens**: `{lens}`. It decides *how* you work, not *what* is true.")
    if domain:
        out.append(f"- **Domain**: `{domain}`. Facts to respect; verify specifics at the source.")
    out.append("")
    if lens:
        e = lenses_by[lens]
        out += [f"## Lens: {lens}", "", f"_{e.description}_", "", e.body.strip(), ""]
    if domain:
        e = domains_by[domain]
        out += [f"## Domain: {domain}", "", f"_{e.description}_", "", e.body.strip(), ""]
    for i, e in enumerate(atoms, 1):
        out += [f"## Atom {i}: {e.name}", "", f"_{e.description}_", "", demote_headings(e.body.strip()), ""]
    return "\n".join(out).rstrip() + "\n"


def cmd_compose(lib, args) -> int:
    try:
        text = compose(lib, args.atoms, args.lens, args.domain, args.name)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.as_skill:
        meta, _ = parse_frontmatter(text)
        dest = SKILLS_DIR / meta["name"] / "SKILL.md"
    else:
        dest = Path(args.out) if args.out else None
    if dest:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        print(f"wrote {dest}")
    else:
        sys.stdout.write(text)
    return 0


BOARD_TEMPLATE = """# Swarm board

**Goal:** {goal}
**Started:** {started}
**Done means:** <command that proves it>

## Plan
| Agent | Skills / blend | Owns | Delivers |
|---|---|---|---|

## Interfaces
<!-- signatures, schemas, file paths. Prefix entries with your agent name. -->

## Decisions
<!-- "agent: decision (why)". Assumptions go here as decisions. -->

## Blockers
<!-- "agent -> owner: what you need". -->

## Handoffs
<!-- Each agent appends "### <agent-name>": built / command + result / open questions / UNVERIFIED. -->

## Verification
<!-- Lead fills in: commands run at integration and their results. -->
"""


def cmd_board(lib, args) -> int:
    SWARM_DIR.mkdir(exist_ok=True)
    (SWARM_DIR / "skills").mkdir(exist_ok=True)
    board = SWARM_DIR / "board.md"
    if board.exists() and not args.force:
        print(f"{board.relative_to(ROOT)} exists (use --force to reset)", file=sys.stderr)
        return 1
    started = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    board.write_text(BOARD_TEMPLATE.format(goal=" ".join(args.goal), started=started), encoding="utf-8")
    print(f"wrote {board.relative_to(ROOT)}")
    return 0


def load_kits() -> dict:
    return json.loads(KITS_FILE.read_text(encoding="utf-8"))


def cmd_kit(lib, args) -> int:
    kits = load_kits()
    if not args.name:
        for name, kit in kits.items():
            print(f"{name:20} {kit['summary']}")
        return 0
    kit = kits.get(args.name)
    if not kit:
        print(f"unknown kit: {args.name} (have: {', '.join(kits)})", file=sys.stderr)
        return 1
    agents = by_name(lib["agent"])
    print(f"# Kit: {args.name}\n\n{kit['summary']}\n")
    for phase in kit["phases"]:
        mode = "parallel" if phase.get("parallel") else "sequential"
        print(f"## {phase['name']} ({mode})")
        for member in phase["members"]:
            agent = agents.get(member["agent"])
            skills = agent.meta.get("skills", "") if agent else ""
            blend = member.get("blend")
            extra = ""
            if blend:
                extra = f"  + blend: {' '.join(blend['atoms'])}"
                extra += f" --lens {blend['lens']}" if blend.get("lens") else ""
                extra += f" --domain {blend['domain']}" if blend.get("domain") else ""
            print(f"- {member['agent']}: {member['task']}")
            print(f"    owns: {member['owns']}")
            if skills:
                print(f"    skills: {skills}")
            if extra:
                print(f"   {extra}")
        print()
    return 0


def validate(lib) -> list[str]:
    errors = []
    atom_names = {e.name for e in lib["atom"]}
    for kind in ("atom", "lens", "domain", "agent"):
        seen = set()
        for e in lib[kind]:
            where = e.path.relative_to(ROOT)
            if not e.meta:
                errors.append(f"{where}: missing frontmatter")
                continue
            if not NAME_RE.match(e.name):
                errors.append(f"{where}: bad name {e.name!r}")
            if e.name in seen:
                errors.append(f"{where}: duplicate {kind} name {e.name}")
            seen.add(e.name)
            if len(e.description) < 20:
                errors.append(f"{where}: description too short")
            if kind == "atom" and e.path.parent.name != e.name:
                errors.append(f"{where}: directory name must equal skill name {e.name}")
            if kind in ("lens", "domain") and e.path.stem != e.name:
                errors.append(f"{where}: file name must equal name {e.name}")
            if not e.body.strip():
                errors.append(f"{where}: empty body")
            if kind == "agent":
                for s in (x.strip() for x in e.meta.get("skills", "").split(",") if x.strip()):
                    if s not in atom_names:
                        errors.append(f"{where}: unknown skill {s}")
    if KITS_FILE.exists():
        agent_names = {e.name for e in lib["agent"]}
        lens_names = {e.name for e in lib["lens"]}
        domain_names = {e.name for e in lib["domain"]}
        for kit_name, kit in load_kits().items():
            for phase in kit["phases"]:
                for m in phase["members"]:
                    if m["agent"] not in agent_names:
                        errors.append(f"kit {kit_name}: unknown agent {m['agent']}")
                    blend = m.get("blend") or {}
                    for a in blend.get("atoms", []):
                        if a not in atom_names:
                            errors.append(f"kit {kit_name}: unknown atom {a}")
                    if blend.get("lens") and blend["lens"] not in lens_names:
                        errors.append(f"kit {kit_name}: unknown lens {blend['lens']}")
                    if blend.get("domain") and blend["domain"] not in domain_names:
                        errors.append(f"kit {kit_name}: unknown domain {blend['domain']}")
    return errors


def cmd_validate(lib, args) -> int:
    errors = validate(lib)
    for err in errors:
        print(err)
    total = sum(len(v) for v in lib.values())
    print(f"{'FAIL' if errors else 'OK'}: {total} files checked, {len(errors)} problem(s)")
    return 1 if errors else 0


def build_index(lib) -> dict:
    a, l, d = (len(lib[k]) for k in ("atom", "lens", "domain"))
    return {
        "counts": {"atoms": a, "lenses": l, "domains": d, "agents": len(lib["agent"]),
                   "blends": blend_count(a, l, d)},
        **{kind + "s": [{"name": e.name, "description": e.description,
                         "path": str(e.path.relative_to(ROOT)),
                         **({"skills": e.meta.get("skills", "")} if kind == "agent" else {})}
                        for e in lib[kind]]
           for kind in ("atom", "lens", "domain", "agent")},
    }


def cmd_index(lib, args) -> int:
    INDEX_FILE.parent.mkdir(exist_ok=True)
    INDEX_FILE.write_text(json.dumps(build_index(lib), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {INDEX_FILE.relative_to(ROOT)}")
    return 0


def cmd_banner(lib, args) -> int:
    a, l, d, g = (len(lib[k]) for k in ("atom", "lens", "domain", "agent"))
    print(f"AgentX loaded: {a} core skills, {l} lenses, {d} domain packs, {g} agents, "
          f"{blend_count(a, l, d):,} possible blends. "
          "Say 'go <goal>' or '/swarm <goal>' to split into a team; "
          "'/tax-engine-kit' launches the tax engine team. See CLAUDE.md.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="skillforge", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats", help="count atoms, lenses, domains, agents, blends")
    sp = sub.add_parser("list", help="list entries")
    sp.add_argument("--kind", choices=["atom", "lens", "domain", "agent"])
    sp = sub.add_parser("search", help="keyword search")
    sp.add_argument("query", nargs="+")
    sp.add_argument("--limit", type=int, default=15)
    sp = sub.add_parser("show", help="print one entry")
    sp.add_argument("name")
    sp = sub.add_parser("compose", help="forge a blended skill")
    sp.add_argument("atoms", nargs="+")
    sp.add_argument("--lens")
    sp.add_argument("--domain")
    sp.add_argument("--name", help="skill name (default derived from parts)")
    sp.add_argument("--out", help="write to this path instead of stdout")
    sp.add_argument("--as-skill", action="store_true",
                    help="write into .claude/skills/<name>/ so Claude Code discovers it")
    sp = sub.add_parser("board", help="create .swarm/board.md for a goal")
    sp.add_argument("goal", nargs="+")
    sp.add_argument("--force", action="store_true")
    sp = sub.add_parser("kit", help="list kits or print a kit's team plan")
    sp.add_argument("name", nargs="?")
    sub.add_parser("validate", help="lint every skill, lens, domain, agent, and kit")
    sub.add_parser("index", help="regenerate catalog/index.json")
    sub.add_parser("banner", help="one-line summary (used by the SessionStart hook)")
    args = p.parse_args(argv)
    lib = load_all()
    return globals()[f"cmd_{args.cmd}"](lib, args)


if __name__ == "__main__":
    sys.exit(main())
