#!/usr/bin/env python3
"""Run: python3 scripts/test_knowledge_links.py"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_knowledge_links as checker

HEADER = ("| ID | Type | Title | Status | Sources | Related | Superseded by | Proposed by / date | Curator approval |\n"
          "|---|---|---|---|---|---|---|---|---|\n")
TRACE_HEADER = ("| Req ID | Requirement (as written) | Source citation | Citation status | Requirement status |\n"
                "|---|---|---|---|---|\n")


class KnowledgeLinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "knowledge").mkdir()
        (self.root / "decisions").mkdir()
        (self.root / "decisions" / "ADR-0001.md").write_text("# ADR\nline 2\n", encoding="utf-8")
        (self.root / "meetings" / "sessions" / "m-2026-01").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, rows="", trace=None):
        (self.root / "knowledge" / "INDEX.md").write_text("# Index\n\n" + HEADER + rows, encoding="utf-8")
        if trace is not None:
            (self.root / "docs" / "agent-ops").mkdir(parents=True, exist_ok=True)
            (self.root / "docs" / "agent-ops" / "TRACE_MATRIX.md").write_text(TRACE_HEADER + trace, encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = checker.main(["--root", str(self.root)])
        return code, out.getvalue()

    def test_valid_rows_pass(self):
        rows = ("| K-0001 | DECISION | Use modular monolith | APPROVED | [ADR-0001](../decisions/ADR-0001.md#L2); meeting:m-2026-01 | K-0002 | — | lead 2026-10-01 | Hai 2026-10-02 |\n"
                "| K-0002 | LESSON | Debate needs ballots | PROPOSED | [ADR-0001](../decisions/ADR-0001.md) | K-0001 | — | secretary 2026-10-03 | — |\n")
        code, out = self.run_check(rows)
        self.assertEqual(code, 0, out)
        self.assertNotIn("WARN unindexed", out)

    def test_broken_link_and_line_anchor_fail(self):
        rows = ("| K-0001 | DECISION | A | PROPOSED | [missing](../decisions/NOPE.md) | — | — | a 2026-10-01 | — |\n"
                "| K-0002 | DECISION | B | PROPOSED | [ADR](../decisions/ADR-0001.md#L99) | — | — | a 2026-10-01 | — |\n")
        code, out = self.run_check(rows)
        self.assertEqual(code, 1)
        self.assertIn("broken link", out)
        self.assertIn("beyond end", out)

    def test_approval_rules(self):
        rows = ("| K-0001 | DECISION | A | APPROVED | [ADR](../decisions/ADR-0001.md) | — | — | a 2026-10-01 | — |\n"
                "| K-0002 | DECISION | B | PROPOSED | [ADR](../decisions/ADR-0001.md) | — | — | a 2026-10-01 | Hai 2026-10-02 |\n")
        code, out = self.run_check(rows)
        self.assertEqual(code, 1)
        self.assertIn("requires curator approval", out)
        self.assertIn("must not carry a curator approval", out)

    def test_superseded_needs_existing_successor(self):
        rows = "| K-0001 | DECISION | A | SUPERSEDED | [ADR](../decisions/ADR-0001.md) | — | K-0009 | a 2026-10-01 | Hai 2026-10-02 |\n"
        code, out = self.run_check(rows)
        self.assertEqual(code, 1)
        self.assertIn("Superseded by", out)

    def test_missing_source_unknown_meeting_and_secret_fail(self):
        rows = ("| K-0001 | LESSON | No source | PROPOSED | told in chat | — | — | a 2026-10-01 | — |\n"
                "| K-0002 | LESSON | Bad meeting | PROPOSED | meeting:not-real | — | — | a 2026-10-01 | — |\n"
                "| K-0003 | CONSTRAINT | api_key=abcd1234secret | PROPOSED | [ADR](../decisions/ADR-0001.md) | — | — | a 2026-10-01 | — |\n")
        code, out = self.run_check(rows)
        self.assertEqual(code, 1)
        self.assertIn("needs at least one tracked source", out)
        self.assertIn("meeting:not-real", out)
        self.assertIn("secret-like", out)

    def test_bad_vocabulary_duplicate_id_and_relative_date_fail(self):
        rows = ("| K-0001 | IDEA | A | DONE | [ADR](../decisions/ADR-0001.md) | — | — | a last week | — |\n"
                "| K-0001 | DECISION | B | PROPOSED | [ADR](../decisions/ADR-0001.md) | — | — | a 2026-10-01 | — |\n")
        code, out = self.run_check(rows)
        self.assertEqual(code, 1)
        for text in ("type must be", "status must be", "duplicate ID", "absolute YYYY-MM-DD"):
            self.assertIn(text, out)

    def test_unindexed_adr_warns(self):
        code, out = self.run_check("")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN unindexed record: decisions/ADR-0001.md", out)

    def test_trace_matrix_rules(self):
        trace = ("| R1 | Users export CSV | [ADR](../../decisions/ADR-0001.md#L1) | VERIFIED | APPROVED |\n"
                 "| R2 | Dark mode | — | NO SOURCE | APPROVED |\n"
                 "| R3 | Audit log | — | VERIFIED | PROPOSED |\n"
                 "| R4 | SSO | [doc](../../missing.md) | MAYBE | PROPOSED |\n")
        code, out = self.run_check("", trace=trace)
        self.assertEqual(code, 1)
        self.assertIn("R2: NO SOURCE cannot be APPROVED", out)
        self.assertIn("R3: VERIFIED needs a source citation", out)
        self.assertIn("R4: citation status must be", out)
        self.assertIn("broken link", out)
        self.assertNotIn("R1:", out)

    def test_assumption_accepted_needs_human_owner(self):
        # Reproduces the tbagri-web pilot: the agent accepted its own assumption (R6).
        (self.root / ".claude" / "agents").mkdir(parents=True)
        (self.root / ".claude" / "agents" / "security-reviewer.md").write_text("x", encoding="utf-8")
        trace = ("| R1 | Fail closed | — | NO SOURCE | ASSUMPTION-ACCEPTED |\n"
                 "| R2 | Fail closed | accepted by owner: Claude (pilot session) 2026-10-29 | NO SOURCE | ASSUMPTION-ACCEPTED |\n"
                 "| R3 | Fail closed | owner said yes | NO SOURCE | ASSUMPTION-ACCEPTED |\n"
                 "| R4 | Fail closed | accepted by owner: Hai 2026-10-30 | NO SOURCE | ASSUMPTION-ACCEPTED |\n"
                 "| R5 | Fail closed | accepted by owner: security-reviewer 2026-10-30 | NO SOURCE | ASSUMPTION-ACCEPTED |\n")
        code, out = self.run_check("", trace=trace)
        self.assertEqual(code, 1)
        self.assertIn("R1: ASSUMPTION-ACCEPTED needs 'accepted by owner", out)
        self.assertIn("R2: ASSUMPTION-ACCEPTED by 'Claude (pilot session)', an agent", out)
        self.assertIn("R3: ASSUMPTION-ACCEPTED needs 'accepted by owner", out)
        self.assertIn("R5: ASSUMPTION-ACCEPTED by 'security-reviewer', an agent", out)
        self.assertNotIn("R4:", out)

    def test_dangling_record_path_warns(self):
        # Reproduces the pilot: records named a closeout that did not exist yet.
        (self.root / "reports").mkdir()
        (self.root / "reports" / "sl-1-readiness.md").write_text(
            "See `reports/sl-1-closeout.md` and `decisions/ADR-0001.md#L2`.\n"
            "Pattern `reports/<slice>-closeout.md` and ```\n`reports/in-code.md`\n```\n", encoding="utf-8")
        code, out = self.run_check("| K-0001 | DECISION | A | PROPOSED | [ADR](../decisions/ADR-0001.md) | — | — | a 2026-10-01 | — |\n")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN reports/sl-1-readiness.md: names `reports/sl-1-closeout.md`, which does not exist", out)
        self.assertNotIn("ADR-0001.md`, which", out)
        self.assertNotIn("<slice>", out)
        self.assertNotIn("in-code", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
