# 30-Minute Classroom Demonstration

**Goal:** students can name each agent file, say who reads it, and explain the difference
between *instructions* and *enforced code*.

**Setup before class:** clone the repository, open it in VS Code, and run the tests once.
Turn on hidden files: `Cmd+Shift+.` in Finder, or use `ls -la`.

| Time | Step |
|------|------|
| 0-3 | 1. Introduce the repository |
| 3-8 | 2. AGENTS.md and CLAUDE.md |
| 8-12 | 3. SKILL.md |
| 12-16 | 4. SOUL.md vs TOOLS.md vs MEMORY.md |
| 16-19 | 5. .mcp.json and settings.json |
| 19-22 | 6. Run the Python example |
| 22-25 | 7. Modify appointment data |
| 25-27 | 8. Run the automated tests |
| 27-30 | 9. Discussion questions |

---

## 1. Introduce the repository (3 min)
- Scenario: a fictional hospital wants an agent that finds appointments but **never books without a human**.
- Show the tree: `ls -la` at the root.
- Key message: *Some files are read by AI tools, some by the program, and some only by humans.*
  Show the "Which files actually affect behavior?" table in `README.md`.

## 2. AGENTS.md and CLAUDE.md (5 min)
- Open `AGENTS.md`: commands, coding standards, and **hard restrictions**.
- Open `CLAUDE.md`: point out `@AGENTS.md`, which **imports** the shared rules so they are written once.
- Ask: *Why not put everything in CLAUDE.md?* Codex and other tools would not see it.

## 3. Explain SKILL.md (4 min)
- Open `.claude/skills/appointment-scheduling/SKILL.md`.
- The frontmatter `description` is what the agent sees first. The body loads only when needed.
- Open `.agents/skills/appointment-scheduling/SKILL.md`. It is identical. Explain why there are two copies.
- Open `patient-summary/SKILL.md` and note its "no diagnosis" rule.
- Stress: **editing a SKILL.md does not change `agent.py`.**

## 4. Compare SOUL.md, TOOLS.md, MEMORY.md (4 min)
| File | Answers the question | Loaded automatically? |
|------|----------------------|------------------------|
| SOUL.md | *Who* is the agent? (tone, values) | No. Optional convention |
| TOOLS.md | *What* can it do? (inputs and outputs) | No. Documentation |
| MEMORY.md | *What* does it remember? | No. Only an app can make it persistent |

## 5. .mcp.json and settings.json (3 min)
- `.claude/settings.json`: `allow` lets commands run without asking, `ask` requires
  confirmation, and `deny` blocks the action. Claude Code enforces these rules, not the model.
- `.mcp.json`: shows *how to start* a server named `...PLACEHOLDER`. It is **only configuration**.
  No server exists, so nothing would connect.

## 6. Run the Python example (3 min)
```bash
python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."
```
Walk through steps [1] to [5]. Point out **step 5: STOP - human approval required.**
Then try:
```bash
python3 -m src.agent --patient P003 "Any orthopedics slot on 2026-11-04?"
python3 -m src.agent --patient P002 "I need a doctor"        # asks for a specialty
```

## 7. Modify appointment data (3 min)
- In `data/appointments.json`, change **A001** to `"available": false`.
- Run the cardiology request again. The recommendation is now **A003**.
- Optional: in `config/config.yaml`, set `max_results: 1` and run again.
- Ask: *Which file changed the behavior: the data, or the SKILL.md?* The answer is the data.

## 8. Run the automated tests (2 min)
```bash
python3 -m unittest discover -s tests -v
```
- With A001 still unavailable, several tests (for example `test_cardiology_on_monday...` and
  `test_agent_stops_for_approval`) **fail**. Tests catch unintended changes.
- Undo the change (`git checkout -- data/ config/` or edit back) and run the tests again.
  All tests pass.

## 9. Discussion questions (3 min)

1. **Q:** If we delete `SOUL.md`, does the Python demo behave differently?
   **A:** No. The demo never reads it. Only an app that loads `SOUL.md` into a prompt would change.

2. **Q:** What is the difference between a skill and a tool?
   **A:** A tool is an action, such as `search_appointments`. A skill is a written
   procedure that tells the agent which tools to use, in what order, and with what rules.

3. **Q:** `AGENTS.md` says "never auto-confirm". Why do we also enforce it in code and tests?
   **A:** Instructions guide an LLM but can be ignored or misread. Code and tests
   *guarantee* the behavior.

4. **Q:** Does adding a server to `.mcp.json` give the agent a new tool?
   **A:** Only if a real MCP server exists at that command and the user approves it. The
   JSON is just a startup recipe.

5. **Q:** Why are there two copies of `appointment-scheduling/SKILL.md`, and what is the risk?
   **A:** Claude Code reads `.claude/skills/` and Codex reads `.agents/skills/`. The risk is
   that they drift apart, which is why a test compares them.
