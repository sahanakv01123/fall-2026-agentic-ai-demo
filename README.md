# hospital-agent-demo

A small teaching repository that explains the **files used by agentic AI systems**
(Claude Code, OpenAI Codex, and other agent frameworks), using one simple example:
a **Hospital Appointment Scheduling AI Agent**.

> **Not a real medical system.** All patients, doctors, and appointments are fictional.
> The Python program is a **deterministic educational simulation**, not an LLM. It never
> confirms a booking. It always stops and asks a human for approval.

## What the example agent does

1. Answers questions about available appointments.
2. Searches appointments by specialty and date.
3. Recommends an available slot.
4. Prepares a booking request.
5. **Stops and asks a human for approval.** It never confirms a booking.

## Quick start

Requires **Python 3.11+**. There are no dependencies to install.

```bash
cd hospital-agent-demo
python3 --version                      # 3.11 or newer

# Run the agent
python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."

# Interactive mode (it will prompt you)
python3 -m src.agent --patient P002

# Run the tests
python3 -m unittest discover -s tests -v
```

Expected output (shortened):

```
=== Hospital Appointment Assistant - Maple Grove General Hospital (fictional) ===
[1] Understand the request
    Patient:   John Smith (P001)
    Specialty: cardiology | Day: monday
[2] Tool call: search_appointments(specialty='cardiology', ..., weekday='monday', max_results=3)
[3] Available slots
    A001  2026-11-02 (Monday)  09:00  Dr. Elena Ruiz
    A003  2026-11-02 (Monday)  14:00  Dr. Marcus Lee
[4] Recommendation: A001 - the earliest available slot.
[5] STOP - human approval required.
    Status: PENDING_HUMAN_APPROVAL. Nothing has been booked.
```

## The files at a glance

| File | Purpose | Read by |
|------|---------|---------|
| `README.md` | Explains the project to humans | Humans, GitHub |
| `AGENTS.md` | Repository rules for **any** coding agent | Codex (automatic), many other agents |
| `CLAUDE.md` | Claude Code project instructions (imports `AGENTS.md`) | Claude Code (automatic) |
| `SOUL.md` | Agent personality (optional convention) | Only apps that choose to load it |
| `TOOLS.md` | Documents tool inputs and outputs | Humans, agents when they open it |
| `MEMORY.md` | Example persistent notes | Only apps that load and update it |
| `.claude/skills/*/SKILL.md` | Step-by-step skills | Claude Code (automatic) |
| `.agents/skills/*/SKILL.md` | Same skill, for Codex | Codex (automatic) |
| `.claude/agents/appointment-reviewer.md` | Subagent definition | Claude Code (automatic) |
| `.claude/settings.json` | Permissions (allow / ask / deny) | Claude Code (automatic) |
| `.mcp.json` | MCP server config (**placeholder**) | Claude Code (asks before enabling) |
| `manifest.json` | Illustrative metadata | Not recognized by most frameworks |
| `.env.example` | Template for secrets (placeholders only) | Humans |
| `config/config.yaml` | Agent settings | **The Python demo** |
| `data/*.json` | Fictional patients and appointments | **The Python demo** |
| `src/agent.py`, `src/tools.py` | The runnable simulation | Python |
| `tests/test_agent.py` | Automated tests | `unittest` |

### Which files actually affect behavior?

| Consumer | Files it loads automatically |
|----------|------------------------------|
| **This Python demo** | `config/config.yaml`, `data/patients.json`, `data/appointments.json`. **No Markdown.** |
| **Claude Code** | `CLAUDE.md` (and `AGENTS.md` through `@AGENTS.md`), `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`, `.mcp.json` |
| **OpenAI Codex** | `AGENTS.md`, `.agents/skills/` |
| **Nobody, automatically** | `SOUL.md`, `TOOLS.md`, `MEMORY.md`, `manifest.json`. These are conventions or documentation. |

Creating or editing a `SKILL.md` **does not change the Python program**. Skills
change how an **AI agent** (Claude Code or Codex) behaves when it works in this
repository.

### Why are there two `appointment-scheduling/SKILL.md` files?

Claude Code looks in `.claude/skills/`, and Codex looks in `.agents/skills/`. To show
both tools, the same skill is copied into both folders. **They must stay identical.**
A test (`test_skill_copies_are_synchronized`) fails if they drift apart.

## Navigating the repository

1. Start with [docs/FILE_EXPLANATIONS.md](docs/FILE_EXPLANATIONS.md), which explains every file.
2. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for diagrams and key distinctions.
3. Teach with [docs/CLASSROOM_DEMO.md](docs/CLASSROOM_DEMO.md), a 30-minute lesson plan.

```
hospital-agent-demo/
├── README.md  AGENTS.md  CLAUDE.md  SOUL.md  TOOLS.md  MEMORY.md
├── .env.example  .gitignore  .mcp.json  manifest.json
├── .claude/   settings.json, agents/, skills/      <- Claude Code
├── .agents/   skills/                              <- Codex
├── config/    config.yaml                          <- read by the demo
├── data/      patients.json, appointments.json     <- read by the demo
├── src/       agent.py, tools.py                   <- the simulation
├── tests/     test_agent.py
└── docs/      FILE_EXPLANATIONS.md, ARCHITECTURE.md, CLASSROOM_DEMO.md
```

Hidden folders (`.claude/`, `.agents/`) are hidden in Finder by default. Press
`Cmd+Shift+.` on macOS or use `ls -la`.

## Safety rules built into this repo

- Fictional data only. See `AGENTS.md`.
- No automatic confirmation. This is enforced in code and covered by tests.
- No real API keys. `.env` is git-ignored.
- `.claude/settings.json` denies destructive commands (`rm`, `curl`, `git push`) and reading `.env`.

## License

MIT. Free to use for teaching.
