---
name: appointment-scheduling
description: Find, recommend, and prepare (never confirm) hospital appointment booking requests using the fictional data in this repository. Use when a user asks to find, schedule, or book an appointment by specialty, date, or weekday.
---

# Appointment Scheduling Skill

> **Two synchronized copies exist:**
> `.claude/skills/appointment-scheduling/SKILL.md` (read by Claude Code) and
> `.agents/skills/appointment-scheduling/SKILL.md` (read by OpenAI Codex).
> Edit both together. `tests/test_agent.py` fails if they differ.

## When to use

- "Find me a cardiology appointment on Monday."
- "What dermatology slots are open on 2026-11-03?"
- "Book P002 with orthopedics this week."

## Steps

1. **Understand the request.**
   Identify the patient ID, the specialty, and the date or weekday.
   Valid specialties are listed in `config/config.yaml`.
   If the specialty or patient ID is missing, ask the user before continuing.

2. **Confirm the patient exists.**
   Use `get_patient(patient_id)` from `src/tools.py` (see `TOOLS.md`).
   If it returns nothing, stop and ask for a valid ID (P001-P005).

3. **Search available slots.**
   Use `search_appointments(specialty, on_date, weekday, max_results)`, or run:

   ```bash
   python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."
   ```

4. **Recommend an appointment.**
   Recommend the earliest slot. Show up to 3 options in a table:

   | ID | Date | Time | Doctor |
   |----|------|------|--------|

5. **Prepare the booking request.**
   Use `create_booking_request(patient_id, appointment_id)`.
   The status must be `PENDING_HUMAN_APPROVAL`.

6. **Ask for human approval.**
   End with: *"This is a booking request only. A staff member must approve it before it is confirmed."*

## Rules

- Never say an appointment is "booked" or "confirmed".
- Never edit `data/appointments.json` to mark a slot as taken.
- Use only the fictional patients in `data/patients.json`.
- Do not give medical advice. You are scheduling only.
