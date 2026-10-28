"""Hospital Appointment Agent - a DETERMINISTIC educational simulation, NOT an LLM.

It follows the same loop a real AI agent follows, using simple keyword matching:
    understand the request -> call tools -> recommend -> STOP for human approval

Files this program reads:
    config/config.yaml, data/patients.json, data/appointments.json
Files it does NOT read (they are for AI coding agents and humans):
    AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, MEMORY.md, every SKILL.md,
    .mcp.json, .claude/settings.json, manifest.json

Run:
    python3 -m src.agent --patient P001 "Find me a cardiology appointment on Monday."
"""

import argparse
import json
import logging
import re
from pathlib import Path

from src import tools

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def _value(text: str):
    text = text.strip().strip('"')
    if text.lower() in ("true", "false"):
        return text.lower() == "true"
    return int(text) if text.isdigit() else text


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Tiny reader for config.yaml (the standard library has no YAML parser).

    Supports only top-level sections containing "key: value" pairs or "- item" lists.
    """
    config, section = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            section = line.rstrip(":")
            config[section] = {}
        elif line.strip().startswith("- "):
            if not isinstance(config[section], list):
                config[section] = []
            config[section].append(_value(line.strip()[2:]))
        else:
            key, value = line.strip().split(":", 1)
            config[section][key] = _value(value)
    return config


def parse_request(text: str, specialties: list[str]) -> dict:
    """'Understand' the request with keyword matching (an LLM would do this step in a real agent)."""
    lower = text.lower()
    found_date = re.search(r"\d{4}-\d{2}-\d{2}", text)
    return {
        "specialty": next((s for s in specialties if s in lower), None),
        "weekday": next((d for d in tools.WEEKDAYS if d in lower), None),
        "date": found_date.group() if found_date else None,
    }


def run_agent(patient_id: str, request: str, config: dict) -> dict:
    """Run one request through the agent loop. Never confirms a booking."""
    if not config["safety"]["require_human_approval"]:
        logging.warning("require_human_approval is false in config.yaml; this demo requires approval anyway.")

    print("\n[1] Understand the request")
    print(f'    Request:   "{request}"')
    patient = tools.get_patient(patient_id)
    if patient is None:
        print(f"    Unknown patient ID: {patient_id}")
        return {"status": "UNKNOWN_PATIENT"}
    intent = parse_request(request, config["specialties"])
    print(f"    Patient:   {patient['name']} ({patient_id})")
    print(f"    Specialty: {intent['specialty']} | Day: {intent['date'] or intent['weekday'] or 'any'}")
    if intent["specialty"] is None:
        print("    Please name a specialty: " + ", ".join(config["specialties"]))
        return {"status": "NEED_MORE_INFO"}

    max_results = config["search"]["max_results"]
    print(
        f"\n[2] Tool call: search_appointments(specialty={intent['specialty']!r}, "
        f"on_date={intent['date']!r}, weekday={intent['weekday']!r}, max_results={max_results})"
    )
    slots = tools.search_appointments(intent["specialty"], intent["date"], intent["weekday"], max_results)
    if not slots:
        print("    No available slots match. Try another day.")
        return {"status": "NO_SLOTS", "slots": []}

    print("\n[3] Available slots")
    for s in slots:
        print(f"    {s['appointment_id']}  {s['date']} ({tools.weekday_name(s['date']).title()})  {s['time']}  {s['doctor']}")

    choice = slots[0]
    print(f"\n[4] Recommendation: {choice['appointment_id']} - the earliest available slot.")
    print(f"    Tool call: create_booking_request(patient_id={patient_id!r}, appointment_id={choice['appointment_id']!r})")
    booking = tools.create_booking_request(patient_id, choice["appointment_id"])
    print("    " + json.dumps(booking, indent=2).replace("\n", "\n    "))

    print("\n[5] STOP - human approval required.")
    print("    Status: PENDING_HUMAN_APPROVAL. Nothing has been booked.")
    print("    A staff member must review and confirm this request in the scheduling system.")
    return {"status": booking["status"], "slots": slots, "booking_request": booking}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Hospital appointment agent (educational simulation).")
    parser.add_argument("request", nargs="?", help='e.g. "Find me a cardiology appointment on Monday."')
    parser.add_argument("--patient", default="P001", help="Fictional patient ID (P001-P005)")
    args = parser.parse_args(argv)

    config = load_config()
    logging.basicConfig(level=config["logging"]["level"], format=config["logging"]["format"])

    print(f"=== {config['agent']['name']} - {config['agent']['hospital']} ===")
    print("(Deterministic educational simulation - not an LLM. Fictional data only.)")
    request = args.request or input("What appointment do you need? ")
    run_agent(args.patient, request, config)


if __name__ == "__main__":
    main()
