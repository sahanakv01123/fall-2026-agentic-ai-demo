"""Tools the demo agent can call.

Each tool is a plain Python function over fictional JSON files in data/.
TOOLS.md documents these same functions for humans and AI agents.
No tool ever writes to the data files, so nothing is ever really booked.
"""

import json
import logging
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

log = logging.getLogger("tools")


def _load(filename: str) -> list[dict]:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def weekday_name(iso_date: str) -> str:
    """'2026-11-02' -> 'monday'."""
    return WEEKDAYS[date.fromisoformat(iso_date).weekday()]


def get_patient(patient_id: str) -> dict | None:
    """Return the fictional patient record, or None if the ID is unknown."""
    log.info("get_patient(%r)", patient_id)
    for patient in _load("patients.json"):
        if patient["patient_id"] == patient_id:
            return patient
    return None


def search_appointments(
    specialty: str,
    on_date: str | None = None,
    weekday: str | None = None,
    max_results: int = 5,
) -> list[dict]:
    """Return AVAILABLE slots for a specialty, optionally filtered by date or weekday."""
    log.info("search_appointments(%r, on_date=%r, weekday=%r)", specialty, on_date, weekday)
    results = []
    for slot in _load("appointments.json"):
        if not slot["available"]:
            continue
        if slot["specialty"] != specialty.lower():
            continue
        if on_date and slot["date"] != on_date:
            continue
        if weekday and weekday_name(slot["date"]) != weekday.lower():
            continue
        results.append(slot)
    results.sort(key=lambda s: (s["date"], s["time"]))
    return results[:max_results]


def create_booking_request(patient_id: str, appointment_id: str) -> dict:
    """Prepare a booking REQUEST. It is never confirmed here - a human must approve it."""
    log.info("create_booking_request(%r, %r)", patient_id, appointment_id)
    patient = get_patient(patient_id)
    if patient is None:
        raise ValueError(f"Unknown patient ID: {patient_id}")

    slot = next((s for s in _load("appointments.json") if s["appointment_id"] == appointment_id), None)
    if slot is None or not slot["available"]:
        raise ValueError(f"Appointment {appointment_id} does not exist or is not available")

    return {
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "appointment_id": appointment_id,
        "specialty": slot["specialty"],
        "date": slot["date"],
        "time": slot["time"],
        "doctor": slot["doctor"],
        "status": "PENDING_HUMAN_APPROVAL",
        "requires_human_approval": True,
    }
