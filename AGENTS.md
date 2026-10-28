# AGENTS.md

Instructions for **any AI coding agent** working in this repository. OpenAI Codex reads
this file automatically, and many other agent tools support it too. Claude Code reads
`CLAUDE.md`, which imports this file.

## Project overview

`hospital-agent-demo` is a **teaching repository**. It contains a small, deterministic
Python simulation of a hospital appointment scheduling agent. All data is fictional.

## Setup and commands

- Python 3.11+ and the standard library only. Do **not** add dependencies.
- Run the demo: `python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."`
- Run the tests: `python3 -m unittest discover -s tests -v`

## Coding standards

- Keep functions short and readable. Students will read this code.
- Use type hints on public functions.
- New tools go in `src/tools.py` and must be documented in `TOOLS.md`.
- Keep `src/agent.py` deterministic. Do not add LLM calls to the core demo.

## Testing expectations

- Every change must keep `python3 -m unittest discover -s tests -v` passing.
- Add a test for every new tool or rule.
- The test that checks the human-approval requirement must never be removed or weakened.

## Hard restrictions

- **Never add real patient information** (real names linked to health data, real
  medical record numbers, diagnoses, or insurance data). Use fictional IDs like `P006`.
- **Never auto-confirm a booking.** The status of a booking request must remain
  `PENDING_HUMAN_APPROVAL`.
- Never commit secrets. Use `.env.example` with placeholders only.
- Do not connect to real hospital systems, EHRs, or external APIs.

## Skills

Reusable step-by-step procedures live in `.agents/skills/` (Codex) and `.claude/skills/`
(Claude Code). The `appointment-scheduling` skill exists in both places and must stay
identical.
