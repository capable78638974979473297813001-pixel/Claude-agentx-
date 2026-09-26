---
name: swarm
description: Split yourself into a coordinated team of subagents, each loaded with different skills, to build something large. Use when the user says "go", "/swarm <goal>", asks to build a whole system, or asks for agents/a team. Covers decomposition, skill assignment, the shared blackboard, parallel spawning, integration, and review loops.
---

# Swarm: one model, many agents

Every subagent is you with a narrower job and a different skill loadout. That
is the advantage: you share the same judgement, so the contract between agents
can be light. The risk is the same too: every agent will make the same blind
guess, so the skill loadouts and the reviewer exist to break symmetry.

## 1. Decompose

Builds live in `projects/<slug>/` (keep the framework files at the repo
root untouched). Record the project directory on the board; every owned path
is relative to it.

Write the plan into the board before spawning anything:

- **Goal** in one sentence, plus what "done" means as a command
  (e.g. `pytest -q` passes and `python -m engine demo` prints a return).
- **Workstreams**: 3–8, each with an owner, owned paths, inputs it needs, and
  the interface it will publish. Cut along interfaces, not along layers of
  effort. If two streams need the same file, merge them or give one ownership.
- **Order**: what must exist first (usually data schemas and interfaces).
  Run a short "spine" phase for that, then fan out.

## 2. Assign skills (mix them)

For each workstream choose one of:

1. A pre-built agent in `.claude/agents/` (its `skills:` are preloaded).
2. A forged blend:
   ```bash
   python3 tools/skillforge.py search "<keyword>"
   python3 tools/skillforge.py compose tax-money-math tax-progressive-brackets \
       --lens adversarial --domain us-federal-income-tax \
       --out .swarm/skills/bracket-engineer.md
   ```
   Then spawn `swarm-worker` and tell it to read that file first.

Mixing rule of thumb: one **craft** skill (how to build), one **domain** pack
(what is true), one **lens** (how to think). Give at least one agent the
`adversarial` or `auditor` lens so the team doesn't agree with itself.

## 3. Blackboard

`python3 tools/skillforge.py board "<goal>"` creates `.swarm/board.md`.
Sections: Plan, Interfaces, Decisions, Handoffs, Blockers, Verification.
Rules for agents:

- Read the whole board before starting.
- Append only under your own `### <agent-name>` heading in Handoffs, plus
  Interfaces/Decisions/Blockers entries prefixed with your name.
- Publish interfaces (function signatures, data schemas, file paths) *before*
  implementing behind them when others depend on you.

## 4. Spawn

Use the Agent tool. Put independent agents in the **same message** so they run
in parallel. Each prompt must be self-contained (agents start cold):

```
You are <name> on the swarm building: <goal>.
Read .swarm/board.md first, then <skill file if forged>.
Project dir: projects/<slug>/. You own: <paths> (relative to it). Do not edit other paths; request changes under Blockers.
Deliver: <interface/files>. Prove it with: <command>.
When done, append your handoff under "### <name>" in .swarm/board.md:
what you built, the command you ran and its result, open questions.
```

## 5. Integrate and review

- Read every handoff. Run the done-command yourself; don't trust summaries.
- Spawn a reviewer (`swarm-reviewer` or `tax-auditor`) over the full diff.
- Fix or re-dispatch findings. Loop until the done-command passes and the
  reviewer has no blocking findings, or you hit a blocker only the user can
  resolve.

## 6. Report

Per agent: one line on what it produced. Then: verified (with the command),
unverified (and why), and any `UNVERIFIED` legal values still in the data.

## Anti-patterns

- Spawning 20 agents for a 5-file job. Parallelism costs context; each agent
  must own enough work to be worth a cold start.
- Two agents editing the same file.
- Agents "integrating" by reading each other's transcripts. The board and the
  code are the only channels.
- Declaring done because every agent said done.
