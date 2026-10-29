#!/usr/bin/env python3
"""Run: python scripts/test_meeting_logger.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import log_team_message as logger


class MeetingLoggerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        (self.root / "CLAUDE.md").write_text("# test", encoding="utf-8")
        manifest = self.root / "meetings"
        manifest.mkdir()
        (manifest / "CURRENT_MEETING.json").write_text(json.dumps({"meeting_id":"test-meeting-01","active":True}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sendmessage_is_logged_to_active_meeting(self):
        payload = {"hook_event_name":"PostToolUse","tool_name":"SendMessage","tool_use_id":"msg-1","teammate_name":"architect","tool_input":{"recipient":"reviewer","message":"Please challenge option A."}}
        path = logger.handle_payload(payload, self.root)
        self.assertIsNotNone(path)
        event = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(event["meeting_id"], "test-meeting-01")
        self.assertEqual(event["recipient"], "reviewer")
        self.assertIn("challenge option A", event["message_text"])

    def test_non_message_tool_is_ignored(self):
        payload = {"hook_event_name":"PostToolUse","tool_name":"Read","tool_input":{"file_path":"README.md"}}
        self.assertIsNone(logger.handle_payload(payload, self.root))

    def test_secrets_are_redacted(self):
        event = logger.normalized_event({"hook_event_name":"PostToolUse","tool_name":"SendMessage","tool_input":{"message":"api_key=abcdef123456 and Bearer abcdefghijklmnop"}}, "test-meeting-01", True)
        self.assertNotIn("abcdef123456", json.dumps(event))
        self.assertIn("[REDACTED]", json.dumps(event))

    def test_unsafe_meeting_id_uses_unassigned(self):
        (self.root / "meetings" / "CURRENT_MEETING.json").write_text(json.dumps({"meeting_id":"../outside","active":True}), encoding="utf-8")
        payload = {"hook_event_name":"TaskCreated","task_id":"t1","task_subject":"Review ADR"}
        path = logger.handle_payload(payload, self.root)
        self.assertIsNotNone(path)
        self.assertIn("unassigned", str(path))
        self.assertTrue(path.name.endswith(".json"))

    def test_task_metadata_is_recorded(self):
        payload = {"hook_event_name":"TaskCreated","task_id":"task-1","task_subject":"Review ADR"}
        path = logger.handle_payload(payload, self.root)
        saved = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(saved["metadata"]["task_subject"], "Review ADR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
