#!/usr/bin/env python3
"""Run: python3 scripts/test_hook_launcher.py"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts" / "hooks" / "run_python.sh"
LOGGER = ROOT / "scripts" / "log_team_message.py"
SH = shutil.which("sh")
PAYLOAD = {"hook_event_name": "PostToolUse", "tool_name": "SendMessage", "tool_use_id": "msg-1",
           "tool_input": {"recipient": "reviewer", "message": "Please challenge option A."}}


@unittest.skipUnless(SH, "POSIX sh is required for the hook launcher")
class HookLauncherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        (self.project / "meetings").mkdir(parents=True)
        (self.project / "meetings" / "CURRENT_MEETING.json").write_text(
            json.dumps({"meeting_id": "launcher-test", "active": True}), encoding="utf-8")
        self.bin = Path(self.tmp.name) / "bin"
        self.bin.mkdir()
        # Only the tools the launcher needs besides Python.
        for tool in ("date", "mkdir", "dirname"):
            os.symlink(shutil.which(tool), self.bin / tool)

    def tearDown(self):
        self.tmp.cleanup()

    def add_stub(self, name):
        """A command that exists on PATH but is not Python, like the Windows Store alias."""
        stub = self.bin / name
        stub.write_text("#!/bin/sh\necho 'Python was not found' >&2\nexit 9009\n", encoding="utf-8")
        stub.chmod(0o755)

    def add_real(self, name):
        os.symlink(sys.executable, self.bin / name)

    def run_launcher(self, *args, stdin=""):
        env = {"PATH": str(self.bin), "CLAUDE_PROJECT_DIR": str(self.project)}
        return subprocess.run([SH, str(LAUNCHER), *args], input=stdin, text=True,
                              capture_output=True, env=env, timeout=30)

    def events(self):
        return sorted((self.project / "meetings" / "sessions" / "launcher-test" / "events").glob("*.json"))

    def test_python3_runs_logger_with_stdin_payload(self):
        self.add_real("python3")
        result = self.run_launcher(str(LOGGER), stdin=json.dumps(PAYLOAD))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.events()), 1)
        event = json.loads(self.events()[0].read_text(encoding="utf-8"))
        self.assertIn("challenge option A", event["message_text"])

    def test_python_only_machine_falls_back(self):
        self.add_real("python")
        result = self.run_launcher(str(LOGGER), stdin=json.dumps(PAYLOAD))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.events()), 1)

    def test_stub_python3_is_skipped(self):
        self.add_stub("python3")
        self.add_real("python")
        result = self.run_launcher(str(LOGGER), stdin=json.dumps(PAYLOAD))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.events()), 1)

    def test_orcasus_python_override_wins(self):
        self.add_stub("python3")
        custom = Path(self.tmp.name) / "custom-python"
        os.symlink(sys.executable, custom)
        env = {"PATH": str(self.bin), "CLAUDE_PROJECT_DIR": str(self.project), "ORCASUS_PYTHON": str(custom)}
        result = subprocess.run([SH, str(LAUNCHER), str(LOGGER)], input=json.dumps(PAYLOAD), text=True,
                                capture_output=True, env=env, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.events()), 1)

    def test_missing_interpreter_fails_loudly_and_is_recorded(self):
        self.add_stub("python3")
        result = self.run_launcher(str(LOGGER), stdin=json.dumps(PAYLOAD))
        self.assertEqual(result.returncode, 1)
        self.assertIn("NOT recorded", result.stderr)
        log = (self.project / "meetings" / "HOOK_ERRORS.log").read_text(encoding="utf-8")
        self.assertIn("log_team_message.py", log)
        self.assertEqual(self.events(), [])

    def test_check_reports_ok_and_warning(self):
        self.add_real("python3")
        ok = self.run_launcher("--check")
        self.assertEqual(ok.returncode, 0)
        self.assertIn("Orcasus hook runtime: OK", ok.stdout)
        (self.bin / "python3").unlink()
        warning = self.run_launcher("--check")
        self.assertEqual(warning.returncode, 0)
        self.assertIn("WARNING", warning.stdout)
        self.assertIn("ORCASUS_PYTHON", warning.stdout)


class HookSettingsTests(unittest.TestCase):
    def test_every_hook_uses_the_launcher(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        commands = [h["command"] for groups in settings["hooks"].values() for g in groups for h in g["hooks"]]
        self.assertTrue(commands)
        for command in commands:
            self.assertIn("scripts/hooks/run_python.sh", command)
            self.assertFalse(command.split()[0] in ("python", "python3", "py"), command)
        self.assertIn("SessionStart", settings["hooks"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
