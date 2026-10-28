# TOOLS.md

Human- and agent-readable documentation for the tools in `src/tools.py`.

> **Who reads this?** Humans, and AI coding agents when they open it or when `CLAUDE.md`
> or `AGENTS.md` points to it. The Python demo **does not** read this file. It calls the
> functions directly. In a real LLM agent, this same information would be sent to the
> model as **tool schemas** (name, description, and JSON input schema). See the example
> at the end of this file.

All tools are **read-only**. They never change files in `data/`.

---

## 1. `search_appointments`

Find **available** appointment slots.

| Input | Type | Required | Example |
|-------|------|----------|---------|
| `specialty` | string | yes | `"cardiology"` |
| `on_date` | string `YYYY-MM-DD` | no | `"2026-11-02"` |
| `weekday` | string | no | `"monday"` |
| `max_results` | integer | no (default 5) | `3` |

**Output:** a list of slots sorted by date and time. Booked slots are excluded.

```json
[{"appointment_id": "A001", "date": "2026-11-02", "time": "09:00",
  "specialty": "cardiology", "doctor": "Dr. Elena Ruiz", "available": true}]
```

## 2. `get_patient`

Look up a fictional patient's administrative record.

| Input | Type | Required | Example |
|-------|------|----------|---------|
| `patient_id` | string | yes | `"P001"` |

**Output:** a patient object, or `None` if the ID is unknown.

```json
{"patient_id": "P001", "name": "John Smith", "date_of_birth": "1980-04-12",
 "phone": "555-0101", "preferred_contact": "phone", "preferred_time": "morning",
 "language": "English"}
```

## 3. `create_booking_request`

Prepare a booking **request** for human approval. **It never confirms a booking.**

| Input | Type | Required | Example |
|-------|------|----------|---------|
| `patient_id` | string | yes | `"P001"` |
| `appointment_id` | string | yes | `"A001"` |

**Output:** a request whose status is always `PENDING_HUMAN_APPROVAL`.

```json
{"patient_id": "P001", "patient_name": "John Smith", "appointment_id": "A001",
 "specialty": "cardiology", "date": "2026-11-02", "time": "09:00",
 "doctor": "Dr. Elena Ruiz", "status": "PENDING_HUMAN_APPROVAL",
 "requires_human_approval": true}
```

**Errors:** raises `ValueError` if the patient is unknown or the slot is unavailable.

---

## How a real LLM would see a tool

```json
{
  "name": "search_appointments",
  "description": "Find available hospital appointment slots by specialty and optional date or weekday.",
  "input_schema": {
    "type": "object",
    "properties": {
      "specialty":   {"type": "string"},
      "on_date":     {"type": "string", "description": "YYYY-MM-DD"},
      "weekday":     {"type": "string"},
      "max_results": {"type": "integer"}
    },
    "required": ["specialty"]
  }
}
```
