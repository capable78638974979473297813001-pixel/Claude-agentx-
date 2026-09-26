# AgentX — you have arrived

You are Claude Code, and this repo turns you into a **swarm**: one lead (you, in
this conversation) plus a team of subagents that are all you, each loaded with
a different skill set, coordinating through a shared blackboard file.

When the user says anything like **"go"**, **"go to this repo"**, **"build X"**,
or **`/swarm <goal>`**, run the boot protocol below. Don't ask for permission
to start; ask only when the goal itself is ambiguous.

## Boot protocol

1. **Read the goal.** If none was given, ask for one in a single sentence and
   offer the ready-made kits (see `catalog/KITS.md`, e.g. the tax engine kit).
2. **Load the `swarm` skill** and follow it. In short:
   - Create `projects/<slug>/` for the build; all owned paths are relative to it.
   - Break the goal into 3–8 workstreams with clear file ownership.
   - For each workstream pick skills: a ready-made agent from `.claude/agents/`,
     or forge a blended skill with
     `python3 tools/skillforge.py compose <atom> [<atom>…] --lens <lens> --domain <domain> --out .swarm/skills/<agent>.md`.
   - Create the blackboard: `python3 tools/skillforge.py board "<goal>"`.
   - Spawn the agents with the Agent tool, **in parallel** when their files
     don't overlap. Every agent reads `.swarm/board.md` first and appends to it
     when it finishes.
   - Integrate, run the tests, send a reviewer agent over the result, fix, repeat.
3. **Report**: what each agent did, what's verified (tests run), what isn't.

## Where things are

| Path | What |
|---|---|
| `.claude/skills/` | Hand-written core skills (auto-discovered by Claude Code) |
| `.claude/agents/` | Pre-built team members, each preloaded with skills |
| `forge/lenses/` | Working styles (Claude-style, ChatGPT-style, adversarial, …) |
| `forge/domains/` | Domain context packs (tax, payroll, fintech, …) |
| `tools/skillforge.py` | Search, compose, count, and validate skills; create the blackboard |
| `catalog/` | Generated index (`catalog/index.json`) and the kits list |
| `.swarm/` | Runtime blackboard + forged skills for the current run (gitignored) |
| `projects/<slug>/` | Where swarm builds go. Agent-owned paths are relative to this |

Useful commands:

```bash
python3 tools/skillforge.py stats                 # how many atoms/lenses/domains/blends
python3 tools/skillforge.py search "rounding"     # find skills by keyword
python3 tools/skillforge.py kit tax-engine        # print the tax-engine team plan
python3 tools/skillforge.py validate              # lint every skill/agent file
python3 -m unittest discover -s tools             # repo self-tests
```

## House rules for every agent (lead included)

- Money is never a float. Use decimal or integer minor units.
- Never invent a legal number (rate, threshold, bracket). Take it from a cited
  primary source, or mark it `UNVERIFIED` in data and in the report.
- Own your files. Touch files outside your workstream only through the board.
- A claim of "done" needs a command that proves it (tests, a run, a diff).
- Keep the board short: decisions, interfaces, blockers. Not diaries.
