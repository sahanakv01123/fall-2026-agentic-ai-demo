# MEMORY.md

> **Important:** this file does **not** give an agent persistent memory by itself.
> Memory only "persists" if an application **loads** this file into the model's context
> at the start of a session **and writes** new notes back to it. Claude Code and Codex
> do not load `MEMORY.md` automatically. (Claude Code's own memory uses `CLAUDE.md` and
> its built-in memory features.) The Python demo does not read this file.
>
> Everything below is fictional and shows what such notes typically look like.

---

## Project preferences (established in earlier sessions)

- 2026-10-12: The team prefers **tables** over long paragraphs when listing slots.
- 2026-10-14: Show at most **3** slots. This matches `search.max_results` in `config/config.yaml`.
- 2026-10-15: Always recommend the **earliest** available slot first.
- 2026-10-20: Dates use ISO format `YYYY-MM-DD`. Times use 24-hour `HH:MM`.

## Decisions

- Booking requests always end with status `PENDING_HUMAN_APPROVAL`. This was agreed with
  the (fictional) scheduling office.
- `appointment-reviewer` subagent runs after every booking request.

## Lessons learned

- A slot with `"available": false` must never be offered. A test covers this.
- Patient P004 is a child (fictional). Pediatrics requests should mention a guardian.

## Open questions

- Should Saturday clinics be added to `appointments.json`?
