---
name: patient-summary
description: Create a short administrative (non-clinical) summary of a fictional patient from data/patients.json. Use when a user asks "who is P003", wants a patient overview before scheduling, or needs contact preferences.
---

# Patient Summary Skill

## Steps

1. **Get the patient ID.** If the user gave a name, look it up in `data/patients.json`
   and confirm the ID with the user.

2. **Retrieve the record.** Use `get_patient(patient_id)` from `src/tools.py`.
   If the ID is unknown, say so and stop.

3. **Write the administrative summary** using exactly this template:

   ```
   Patient summary (administrative only)
   - Name / ID:          John Smith (P001)
   - Date of birth:      1980-04-12
   - Preferred contact:  phone (555-0101)
   - Preferred time:     morning
   - Language:           English
   ```

4. **Add a scheduling hint** based on preferred time, for example
   "Prefers morning slots - offer 09:00 options first."

## Rules

- **No diagnosis, no medical advice, no guesses about health conditions.**
  The data contains no medical information, and you must not invent any.
- If asked a medical question, reply: *"I can help with scheduling only.
  Please ask a clinician."*
- Share only the fields listed in the template.
- All patients are fictional. Never add or request real patient information.
