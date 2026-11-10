#!/usr/bin/env python3
"""Run: python3 scripts/test_skill_focus.py"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_focus  # noqa: E402

GOOD = "Does one thing. Do NOT use for the other thing (other-skill)."


class SkillFocusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, name, description=GOOD, in_map=True):
        path = self.root / ".claude" / "skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(f"---\nname: {name}\ndescription: \"{description}\"\n---\n\nBody.\n", encoding="utf-8")
        if in_map:
            with (self.root / "docs" / "AI_SDLC_STAGE_MAP.md").open("a", encoding="utf-8") as handle:
                handle.write(f"| S1 | `{name}` |\n")

    def test_focused_core_passes(self):
        self.add("alpha")
        self.add("beta")
        passed, errors = skill_focus.check(self.root)
        self.assertEqual(errors, [])
        self.assertIn("core skills: 2 of at most 20", passed)

    def test_missing_boundary_and_stage_fail(self):
        self.add("alpha", description="Does one thing.")
        self.add("beta", in_map=False)
        _, errors = skill_focus.check(self.root)
        self.assertTrue(any(e.startswith("alpha: description has no 'Do NOT use") for e in errors), errors)
        self.assertTrue(any(e.startswith("beta: not named in docs/AI_SDLC_STAGE_MAP.md") for e in errors), errors)

    def test_cap_and_budget_fail(self):
        with mock.patch.object(skill_focus, "MAX_CORE_SKILLS", 1), \
                mock.patch.object(skill_focus, "MAX_DESCRIPTION_CHARS", 2 * len(GOOD) - 1):
            self.add("alpha")
            self.add("beta")
            _, errors = skill_focus.check(self.root)
        self.assertTrue(any("exceeds 1" in e for e in errors), errors)
        self.assertTrue(any("characters exceed" in e for e in errors), errors)

    def test_repository_passes(self):
        passed, errors = skill_focus.check(Path(__file__).resolve().parents[1])
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
