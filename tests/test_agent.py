"""Automated tests. Run from the repository root:

    python3 -m unittest discover -s tests -v
"""

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src import tools
from src.agent import load_config, parse_request, run_agent

ROOT = Path(__file__).resolve().parent.parent


def quiet_run(patient_id, request, config):
    with redirect_stdout(io.StringIO()):
        return run_agent(patient_id, request, config)


class TestSearch(unittest.TestCase):
    def test_cardiology_on_monday_returns_only_available_slots(self):
        ids = [s["appointment_id"] for s in tools.search_appointments("cardiology", weekday="monday")]
        self.assertEqual(ids, ["A001", "A003"])  # A002 is booked, so it is excluded

    def test_search_by_exact_date(self):
        ids = [s["appointment_id"] for s in tools.search_appointments("orthopedics", on_date="2026-11-04")]
        self.assertEqual(ids, ["A007"])

    def test_max_results_is_respected(self):
        self.assertEqual(len(tools.search_appointments("cardiology", max_results=1)), 1)

    def test_unknown_specialty_returns_nothing(self):
        self.assertEqual(tools.search_appointments("neurology"), [])

    def test_get_patient(self):
        self.assertEqual(tools.get_patient("P001")["name"], "John Smith")
        self.assertIsNone(tools.get_patient("P999"))


class TestApprovalRequirement(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_booking_request_is_never_confirmed(self):
        booking = tools.create_booking_request("P001", "A001")
        self.assertEqual(booking["status"], "PENDING_HUMAN_APPROVAL")
        self.assertTrue(booking["requires_human_approval"])

    def test_unavailable_slot_cannot_be_requested(self):
        with self.assertRaises(ValueError):
            tools.create_booking_request("P001", "A002")

    def test_agent_stops_for_approval(self):
        result = quiet_run("P001", "Find me a cardiology appointment on Monday.", self.config)
        self.assertEqual(result["status"], "PENDING_HUMAN_APPROVAL")
        self.assertEqual(result["booking_request"]["appointment_id"], "A001")

    def test_approval_still_required_if_config_disables_it(self):
        self.config["safety"]["require_human_approval"] = False
        with self.assertLogs(level="WARNING"):
            result = quiet_run("P001", "cardiology on Monday", self.config)
        self.assertEqual(result["status"], "PENDING_HUMAN_APPROVAL")

    def test_missing_specialty_asks_for_more_info(self):
        self.assertEqual(quiet_run("P001", "I need a doctor", self.config)["status"], "NEED_MORE_INFO")


class TestConfigAndFiles(unittest.TestCase):
    def test_config_values(self):
        config = load_config()
        self.assertTrue(config["safety"]["require_human_approval"])
        self.assertEqual(config["search"]["max_results"], 3)
        self.assertIn("cardiology", config["specialties"])

    def test_parse_request(self):
        intent = parse_request("Find me a cardiology appointment on Monday.", ["cardiology"])
        self.assertEqual(intent, {"specialty": "cardiology", "weekday": "monday", "date": None})

    def test_skill_copies_are_synchronized(self):
        claude_copy = ROOT / ".claude/skills/appointment-scheduling/SKILL.md"
        codex_copy = ROOT / ".agents/skills/appointment-scheduling/SKILL.md"
        self.assertEqual(claude_copy.read_text(), codex_copy.read_text(),
                         "Edit both SKILL.md copies together.")


if __name__ == "__main__":
    unittest.main()
