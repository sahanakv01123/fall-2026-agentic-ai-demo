# File Explanations

Legend for **Type**: **Standard** means widely adopted across tools.
**Platform-specific** means one product defines it. **Convention** means an optional
community practice.

| File | Type | Demo reads it? |
|------|------|----------------|
| README.md | Standard (GitHub) | No |
| AGENTS.md | Standard (open, multi-tool) | No |
| CLAUDE.md | Platform-specific (Claude Code) | No |
| SOUL.md | Convention | No |
| TOOLS.md | Convention / documentation | No |
| MEMORY.md | Convention | No |
| SKILL.md | Agent Skills format (Claude Code, Codex, others) | No |
| appointment-reviewer.md | Platform-specific (Claude Code) | No |
| .claude/settings.json | Platform-specific (Claude Code) | No |
| .mcp.json | Platform-specific file for the MCP standard | No |
| manifest.json | Illustrative | No |
| .env.example | Standard practice | No |
| .gitignore | Standard (Git) | No (Git reads it) |
| config/config.yaml | Project-specific | **Yes** |
| data/*.json | Project-specific | **Yes** |
| src/*.py, tests/*.py | Code | **They are the demo** |

---

## README.md
- **What is it?** The front page of the repository.
- **Who reads it?** Humans and GitHub (shown on the repository page).
- **When is it useful?** For first contact, setup, and navigation.
- **Type:** Standard.
- **Demo reads it?** No.
```markdown
## Quick start
python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."
```

## AGENTS.md
- **What is it?** A "README for AI agents" containing build commands, coding rules, and restrictions.
- **Who reads it?** OpenAI Codex (automatically) and many other coding agents. Claude Code
  reads it here because `CLAUDE.md` contains `@AGENTS.md`.
- **When is it useful?** When you want one set of rules shared by every AI tool.
- **Type:** Open standard (agents.md).
- **Demo reads it?** No.
```markdown
## Hard restrictions
- Never add real patient information.
- Never auto-confirm a booking.
```

## CLAUDE.md
- **What is it?** Claude Code's project memory file. It is loaded into context at every session start.
- **Who reads it?** Claude Code.
- **When is it useful?** For Claude-specific workflow, such as which skill or subagent to use.
- **Type:** Platform-specific.
- **Demo reads it?** No.
```markdown
@AGENTS.md
2. After preparing a booking request, delegate to the appointment-reviewer subagent.
```

## SOUL.md
- **What is it?** A personality and values description: tone, values, and boundaries.
- **Who reads it?** Only frameworks or apps that choose to load it into the system prompt.
- **When is it useful?** For user-facing assistants where consistent voice matters.
- **Type:** Optional convention, not a universal standard.
- **Demo reads it?** No.
```markdown
- Privacy-conscious: I share only what is needed for scheduling.
```

## TOOLS.md
- **What is it?** Documentation of each tool's name, inputs, outputs, and errors.
- **Who reads it?** Humans, and agents when they open it. Real LLMs receive tool details as
  JSON schemas through the API, not from this file.
- **When is it useful?** For onboarding and for keeping tool behavior documented.
- **Type:** Convention / documentation.
- **Demo reads it?** No. The demo calls the Python functions directly.
```markdown
## 3. create_booking_request
Output: status is always PENDING_HUMAN_APPROVAL.
```

## MEMORY.md
- **What is it?** Example notes an agent might keep between sessions.
- **Who reads it?** Only an application that loads it and writes updates back.
- **When is it useful?** When building agents that should remember preferences.
- **Type:** Convention. **A file alone is not memory.**
- **Demo reads it?** No.
```markdown
- 2026-10-15: Always recommend the earliest available slot first.
```

## SKILL.md (`.claude/skills/...` and `.agents/skills/...`)
- **What is it?** A reusable procedure with YAML frontmatter (`name`, `description`) and
  step-by-step Markdown instructions. At first only the `description` is seen. The full
  body loads when the agent decides that the skill is relevant.
- **Who reads it?** Claude Code (`.claude/skills/`) and Codex (`.agents/skills/`).
- **When is it useful?** For repeatable multi-step tasks with rules.
- **Type:** Agent Skills format, supported by several tools with different folder locations.
- **Demo reads it?** No. Editing a SKILL.md does **not** change `agent.py`.
- **Why two copies?** Each tool looks in its own folder. They must stay identical, and a test checks this.
```markdown
---
name: appointment-scheduling
description: Find, recommend, and prepare (never confirm) hospital appointment booking requests...
---
```

## .claude/agents/appointment-reviewer.md
- **What is it?** A **subagent**: a specialist with its own context window, prompt, and restricted tools.
- **Who reads it?** Claude Code.
- **When is it useful?** For independent review and focused tasks that should not clutter the main conversation.
- **Type:** Platform-specific.
- **Demo reads it?** No.
```markdown
---
name: appointment-reviewer
tools: Read, Grep, Glob
---
```

## .claude/settings.json
- **What is it?** Claude Code permissions and settings that are shared with the team through Git.
- **Who reads it?** Claude Code.
- **When is it useful?** For enforcing least privilege. Claude Code enforces these rules
  itself, not the model.
- **Type:** Platform-specific.
- **Demo reads it?** No.
```json
"deny": ["Read(./.env)", "Bash(rm:*)", "Bash(git push:*)"]
```

## .mcp.json
- **What is it?** A project-level list of MCP servers that Claude Code can start.
- **Who reads it?** Claude Code. It asks the user before enabling project servers.
  Codex configures MCP in its own `config.toml` instead.
- **When is it useful?** For connecting an agent to external tools or data.
- **Type:** Platform-specific file. MCP itself is an open protocol.
- **Demo reads it?** No. **It is a placeholder:** the server it names does not exist.
```json
"hospital-scheduling-PLACEHOLDER": {"command": "python3", "args": ["-m", "placeholder_mcp_server_NOT_IMPLEMENTED"]}
```

## manifest.json
- **What is it?** Illustrative metadata: name, version, capabilities, and safety flags.
- **Who reads it?** Nobody automatically. Some plugin systems use similar manifests with their own schemas.
- **When is it useful?** For teaching what packaged agents declare about themselves.
- **Type:** Illustrative.
- **Demo reads it?** No.

## .env.example
- **What is it?** A template that shows which secrets or settings exist, using placeholder values only.
- **Who reads it?** Humans. They copy it to `.env`, which is git-ignored.
- **Type:** Standard practice.
- **Demo reads it?** No. The demo needs no keys.

## .gitignore
- **What is it?** Tells Git which files never to commit, such as `.env` and `__pycache__/`.
- **Type:** Standard (Git).

## config/config.yaml
- **What is it?** Agent settings: name, specialties, max results, approval rule, and logging.
- **Who reads it?** **`src/agent.py`** through `load_config()`, a tiny parser in the standard library.
- **Demo reads it?** **Yes.** Change `max_results` to `1` and run again to see the effect.
```yaml
search:
  max_results: 3
```

## data/patients.json and data/appointments.json
- **What is it?** Five fictional patients and ten fictional future appointment slots.
- **Who reads it?** **`src/tools.py`**.
- **Demo reads it?** **Yes.** The tools only read these files and never write to them.

## src/agent.py and src/tools.py
- **What is it?** The runnable simulation. `tools.py` contains the actions, and `agent.py`
  contains the loop that decides what to do.
- **Type:** Code. It is deterministic and not an LLM.

## tests/test_agent.py
- **What is it?** Automated checks for search results, the approval requirement, the config,
  and whether the skill copies are synchronized.
- **Run:** `python3 -m unittest discover -s tests -v`
