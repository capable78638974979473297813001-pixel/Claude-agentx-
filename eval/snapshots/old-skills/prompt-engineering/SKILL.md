---
name: prompt-engineering
description: Write prompts for subagents and LLM features - self-contained context, clear role, explicit deliverable and format, examples, constraints, and verification steps. Use when spawning swarm agents or building prompts into an application.
---

# Prompt engineering (for agents you spawn)

A subagent starts cold. Its prompt must contain:

- **Role and goal**: who it is on the team and the overall goal.
- **Context**: files to read first (the board, skill files), key decisions.
- **Ownership**: which paths it may edit; how to request other changes.
- **Deliverable**: exact files/interfaces and the format of its final message.
- **Proof**: the command that must pass.
- **Stop conditions**: when to stop and report a blocker instead of guessing.

Prefer concrete examples over adjectives. One task per agent. If you'd need
to explain it twice, write the explanation into the board instead.
