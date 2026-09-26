---
name: skill-router
description: Find and pick the right skills for a task from this repo's catalog - search core skills, lenses, and domain packs, and forge blended skills. Use when you or a swarm agent need to choose skills, when the user asks "what skills do you have", or before spawning agents.
---

# Skill router

```bash
python3 tools/skillforge.py stats              # counts
python3 tools/skillforge.py list               # every atom, lens, domain
python3 tools/skillforge.py search "<words>"   # ranked matches
python3 tools/skillforge.py show <name>        # print one
python3 tools/skillforge.py compose <atom>... --lens <l> --domain <d> [--out path]
```

## Picking

1. Name the deliverable and the riskiest part of it.
2. Pick one **craft** atom for the deliverable (e.g. `tax-progressive-brackets`).
3. Add one atom that covers the riskiest part (e.g. `tax-money-math`,
   `security-review-lite`).
4. Add a **domain** pack if the facts of a field matter.
5. Add a **lens** for how to think: `builder` for speed, `adversarial` for
   reviewers, `claude-careful` for ambiguous specs, `gpt-code-interpreter`
   when every number should be checked by running code.

Three to four atoms is the ceiling. Past that the guidance dilutes.
