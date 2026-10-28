# CLAUDE.md

Claude Code loads this file automatically when it starts in this folder.

@AGENTS.md

The line above imports `AGENTS.md`, so shared rules are written once and used by both
Claude Code and Codex. The sections below are specific to Claude Code.

## About this project

A fictional hospital appointment scheduling agent, used to teach how agent files fit
together. `src/agent.py` is a deterministic simulation, **not** an LLM.

## How to run

```bash
python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."
python3 -m unittest discover -s tests -v
```

## Where things are

| What | Location |
|------|----------|
| Skills | `.claude/skills/appointment-scheduling/`, `.claude/skills/patient-summary/` |
| Subagent | `.claude/agents/appointment-reviewer.md` |
| Permissions | `.claude/settings.json` |
| MCP (placeholder only) | `.mcp.json` |
| Tools reference | `TOOLS.md` |
| Fictional data | `data/` |

## Claude-specific workflow

1. For scheduling requests, use the **appointment-scheduling** skill.
2. After preparing a booking request, delegate to the **appointment-reviewer** subagent.
3. Finish by asking the human to approve. Never say "booked" or "confirmed".
4. If you edit `.claude/skills/appointment-scheduling/SKILL.md`, copy the same change to
   `.agents/skills/appointment-scheduling/SKILL.md`.
