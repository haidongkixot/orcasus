#!/usr/bin/env python3
"""Run: python3 scripts/runtime_acceptance/test_collect_evidence.py"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_evidence as ce  # noqa: E402


class CollectEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.home = Path(self.tmp.name) / "claude"
        self.session = self.root / "meetings" / "sessions" / "m1"
        (self.session / "events").mkdir(parents=True)
        team = self.home / "teams" / "session-abc12345"
        team.mkdir(parents=True)
        (team / "config.json").write_text(json.dumps({"members": [
            {"name": "team-lead", "agentType": "team-lead", "sessionId": "secret-session"},
            {"name": "architect", "agentType": "domain-architect"},
            {"name": "skeptic", "agentType": "devil-advocate"}]}))
        tasks = self.home / "tasks" / "session-abc12345"
        tasks.mkdir(parents=True)
        (tasks / "1.json").write_text("{}")

    def tearDown(self):
        self.tmp.cleanup()

    def add_message(self, i, sender, text="proposal", recipient="team-secretary"):
        (self.session / "events" / f"{i:03d}.json").write_text(json.dumps({
            "hook_event_name": "PostToolUse", "tool_name": "SendMessage", "teammate_name": sender,
            "recipient": recipient, "message_text": text}))

    def add_records(self):
        for name in ce.SECRETARY_FILES:
            (self.session / name).write_text("# record\n")

    def run_collect(self, expected):
        out = Path(self.tmp.name) / "report.md"
        with contextlib.redirect_stdout(io.StringIO()):
            ce.main(["--meeting-id", "m1", "--expected-messages", str(expected), "--root", str(self.root),
                     "--claude-home", str(self.home), "--out", str(out)])
        return out.read_text()

    def test_verified_when_complete(self):
        self.add_message(1, "architect")
        self.add_message(2, "skeptic", "FINAL_BALLOT\nchoice: A")
        self.add_records()
        report = self.run_collect(2)
        self.assertIn("Capture status: CAPTURE VERIFIED", report)
        self.assertIn("architect, skeptic", report)
        self.assertIn("| Events carrying FINAL_BALLOT | 1 |", report)
        self.assertIn("team-lead, architect, skeptic", report)
        self.assertNotIn("secret-session", report)
        self.assertNotIn("FINAL_BALLOT\nchoice", report)

    def test_partial_on_low_coverage_hook_errors_and_missing_records(self):
        self.add_message(1, "architect")
        self.add_message(2, "skeptic")
        (self.root / "meetings" / "HOOK_ERRORS.log").write_text("2026-11-01T10:00:00Z\tlog_team_message.py\tno python\n")
        report = self.run_collect(4)
        self.assertIn("Capture status: PARTIAL", report)
        self.assertIn("coverage 0.5 < 1.0", report)
        self.assertIn("HOOK_ERRORS.log", report)
        self.assertIn("Secretary records missing", report)

    def test_single_sender_is_partial_and_no_events_not_verified(self):
        self.add_message(1, "architect")
        self.add_records()
        self.assertIn("only 1 distinct sender", self.run_collect(1))
        for path in (self.session / "events").glob("*.json"):
            path.unlink()
        self.assertIn("Capture status: NOT VERIFIED", self.run_collect(1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
