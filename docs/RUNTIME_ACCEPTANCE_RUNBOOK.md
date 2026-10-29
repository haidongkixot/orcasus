# Runtime Acceptance Runbook — Agent Teams, hooks and Team Secretary

Agent Teams only spawn teammates in an **interactive** Claude Code session; `claude -p` and the Agent SDK do not. This runbook is the repeatable, evidence-producing version of [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md) sections B, C and H. Run it on each operating system you support (macOS, Windows with Git Bash, Linux) in a non-production copy of the repository.

Time: about 20–30 minutes. Cost: one lead and 2–3 teammates for a short discussion; the token use shows in Claude Code.

## 1. Before the session

1. Pull the latest `main` and run the package checks:
   `python3 scripts/validate_bundle.py` and `sh scripts/hooks/run_python.sh --check` (Windows: in Git Bash).
2. Optional, headless only: `python3 scripts/live_evals/hook_probe.py` records whether the SendMessage hook fires in `claude -p`. Keep its JSON with the evidence; it does not replace the steps below.
3. Make sure `meetings/HOOK_ERRORS.log` does not exist or is empty, so new errors are attributable to this run.

## 2. In the interactive session

1. Start `claude` in the repository root. **Record** the first lines: the SessionStart line must read `Orcasus hook runtime: OK (...)`.
2. Ask the lead:
   > Run /meeting-record. Open meeting `RA-<yyyy-mm-dd>-<os>` with decision question "Which of two logging formats should the sample app use: JSON lines or plain text?" Start the team-secretary first, then spawn two voters using the domain-architect and devil-advocate agent types. Each voter sends one proposal and one critique to the other and to the secretary with SendMessage, then one FINAL_BALLOT to the secretary. The secretary writes MINUTES.md, DISCUSSION_LOG.md, VOTE_REGISTER.md, DECISION_SUMMARY.md, ACTION_ITEMS.md and COVERAGE_REPORT.md and lists every message it received in DISCUSSION_LOG.md. Do not edit any other file.
3. Wait until the secretary reports. Confirm in the agent panel that the teammates really exist (not subagents).
4. **Before closing the session**, in a second terminal run:

   ```
   python3 scripts/runtime_acceptance/collect_evidence.py --meeting-id RA-<yyyy-mm-dd>-<os> --expected-messages <number of messages listed in DISCUSSION_LOG.md>
   ```

   The team directory under `~/.claude/teams/` is removed when the session ends, so collect first.
5. Ask the lead to shut the teammates down and set the meeting manifest inactive.

## 3. Record the result

- The collector writes `evidence/runtime/<date>-<os>/RUNTIME_ACCEPTANCE.md` with counts, coverage, gaps and SHA-256 hashes; it copies no message bodies or session IDs.
- **CAPTURE VERIFIED** requires at least two real senders, complete events (sender, recipient, text), coverage 1.0, no hook errors and all six Secretary records. Anything less is PARTIAL; no events is NOT VERIFIED. Do not edit the verdict by hand.
- Commit the report (and the meeting's Secretary records if they contain no sensitive content). Raw event files stay gitignored.
- Update the runtime row for that OS in [EVIDENCE.md](EVIDENCE.md) with the date, status and report path.

## If it fails

- SessionStart shows WARNING: install Python 3.8+ or set `ORCASUS_PYTHON`, start a new session and rerun.
- No teammates spawn: confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is active and that you are not in `-p` mode; report the limitation instead of simulating a team.
- Events missing but no hook errors: record PARTIAL, attach the Claude Code version, and open an issue with the collector report.
