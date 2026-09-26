# AgentX

A skill library plus orchestration layer for **Claude Code**. When you open
Claude Code in this repo, it becomes a swarm: the main conversation acts as
lead and splits the work across subagents. Every subagent is the same model
with a different skill loadout, and they coordinate through a shared
blackboard file.

```
you: go build a tax engine
         │
   lead (this conversation) ── reads CLAUDE.md, loads the `swarm` skill
         │   writes .swarm/board.md  (plan · interfaces · decisions · handoffs)
         ├── tax-architect           spine: money, trace, facts, ruleset schema
         ├── tax-rules-researcher    cited ruleset data  ─┐
         ├── tax-calc-engineer       brackets, phase-outs, credits   │ parallel
         ├── tax-test-oracle         golden + property + differential tests
         ├── tax-api-builder         compute / explain / diff / CLI ─┘
         ├── tax-auditor             audit pass
         └── swarm-reviewer          final review, shared blind spots
```

## Use it

1. Start Claude Code in this repo (CLI: `claude` in the repo; web: start a
   session on this repository).
2. The session-start hook prints what's loaded.
3. Say one of:
   - `go build a tax calculation engine`, or `/tax-engine-kit`
   - `/swarm <any goal>`
   - `what skills do you have for payroll?`

Builds go in `projects/<slug>/`, so the framework files stay clean.

## What's inside

| | Count | Where |
|---|---|---|
| Core skills (atoms) | 35 | `.claude/skills/*/SKILL.md` |
| Lenses (working styles, including Claude-style and ChatGPT-style) | 17 | `forge/lenses/` |
| Domain packs | 23 | `forge/domains/` |
| Agents | 10 | `.claude/agents/` |
| Possible blends | 3,099,600 | made on demand by `tools/skillforge.py compose` |

A **blend** is 1–3 core skills combined, with an optional lens and an optional
domain pack, e.g.:

```bash
python3 tools/skillforge.py compose tax-money-math tax-progressive-brackets \
    --lens adversarial --domain us-federal-income-tax --out .swarm/skills/bracket-engineer.md
```

The blend count is combinatorial. The written expertise lives in the 35 core
skills, 17 lenses, and 23 domain packs; a blend combines them into one brief
for a single agent. It adds no knowledge beyond its parts.

### Tax engine skill pack

`tax-engine-architecture`, `tax-money-math`, `tax-rules-as-data`,
`tax-progressive-brackets`, `tax-phaseouts-and-limits`, `tax-credits-engine`,
`tax-filing-status-and-household`, `tax-jurisdiction-modeling`,
`tax-sales-and-vat`, `tax-payroll-withholding`, `tax-golden-test-vectors`,
`tax-explainability-audit-trail`, `tax-source-research`,
`tax-api-and-scenarios`, and the launcher `tax-engine-kit`.

Kits: `tax-engine`, `vat-engine`, `payroll-engine`
(`python3 tools/skillforge.py kit <name>`).

### General skills

`swarm`, `skill-router`, `code-review-rigorous`, `test-driven-development`,
`debugging-scientific-method`, `spec-writing`, `api-design`, `data-modeling`,
`refactoring-safe`, `python-engineering`, `typescript-engineering`,
`security-review-lite`, `performance-profiling`, `adversarial-red-team`,
`verify-before-claiming`, `research-synthesis`, `prompt-engineering`,
`docs-writer`, `data-analysis-with-code`, `iterative-canvas-editing`.

## skillforge CLI

```bash
python3 tools/skillforge.py stats|list|search|show|compose|board|kit|validate|index|banner
python3 -m unittest discover -s tools
```

## Adding a skill

1. `mkdir .claude/skills/<name>` and write `SKILL.md` with `name` and
   `description` frontmatter. The description decides when Claude uses it, so
   say what it does and when to use it.
2. `python3 tools/skillforge.py validate && python3 tools/skillforge.py index`.

## Notes

- The skills are original. They are written in the style of Claude and ChatGPT
  workflows, not copied from either product.
- The tax skills tell agents never to enter a legal number from memory as
  verified. Rates and thresholds come from cited primary sources or get marked
  `UNVERIFIED`. An engine built here is software, not tax advice.
