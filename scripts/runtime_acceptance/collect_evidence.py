#!/usr/bin/env python3
"""Collect runtime acceptance evidence for an Agent Teams meeting.

Run on the owner's machine, in the Orcasus project, while the team session is
still open (Claude Code removes ~/.claude/teams/<team>/ when the session ends).
It gathers logger events, hook errors, team membership names, task counts and
Secretary records; computes capture coverage; and writes
evidence/runtime/<date>-<os>/RUNTIME_ACCEPTANCE.md with SHA-256 hashes.
Session IDs, message bodies and secrets are not copied into the report.

  python3 scripts/runtime_acceptance/collect_evidence.py --meeting-id M-2026-11-01-arch \
      --expected-messages 9 [--team session-1a2b3c4d] [--claude-home ~/.claude]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SECRETARY_FILES = ["MINUTES.md", "DISCUSSION_LOG.md", "VOTE_REGISTER.md", "DECISION_SUMMARY.md",
                   "ACTION_ITEMS.md", "COVERAGE_REPORT.md"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def newest_team(claude_home: Path) -> Path | None:
    teams = [p for p in (claude_home / "teams").glob("*") if p.is_dir()] if (claude_home / "teams").is_dir() else []
    return max(teams, key=lambda p: p.stat().st_mtime) if teams else None


def collect(root: Path, meeting_id: str, expected: int | None, claude_home: Path, team: str | None) -> dict:
    session = root / "meetings" / "sessions" / meeting_id
    events = []
    for path in sorted((session / "events").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        events.append({"file": path, "hook": data.get("hook_event_name"), "tool": data.get("tool_name"),
                       "sender": data.get("teammate_name") or data.get("agent_type") or data.get("agent_id"),
                       "recipient": data.get("recipient"), "has_text": bool(data.get("message_text")),
                       "ballot": "FINAL_BALLOT" in (data.get("message_text") or "")})
    messages = [e for e in events if e["hook"] == "PostToolUse" and e["tool"] == "SendMessage"]
    complete = [e for e in messages if e["sender"] and e["recipient"] and e["has_text"]]
    senders = sorted({e["sender"] for e in messages if e["sender"]})
    errors_file = root / "meetings" / "HOOK_ERRORS.log"
    hook_errors = errors_file.read_text(encoding="utf-8").splitlines() if errors_file.is_file() else []
    team_dir = (claude_home / "teams" / team) if team else newest_team(claude_home)
    members = []
    if team_dir and (team_dir / "config.json").is_file():
        config = json.loads((team_dir / "config.json").read_text(encoding="utf-8"))
        members = [{"name": m.get("name"), "agent_type": m.get("agentType") or m.get("agent_type")}
                   for m in config.get("members", [])]
    tasks_dir = claude_home / "tasks" / team_dir.name if team_dir else None
    task_files = sorted(tasks_dir.glob("*.json")) if tasks_dir and tasks_dir.is_dir() else []
    records = {name: session / name for name in SECRETARY_FILES}
    coverage = round(len(messages) / expected, 4) if expected else None

    if not messages:
        status, reasons = "NOT VERIFIED", ["no SendMessage events were recorded"]
    else:
        reasons = []
        if len(senders) < 2:
            reasons.append(f"only {len(senders)} distinct sender(s); need at least 2 real teammates")
        if len(complete) < len(messages):
            reasons.append(f"{len(messages) - len(complete)} message event(s) missing sender, recipient or text")
        if expected is None:
            reasons.append("expected message count not given; coverage unknown")
        elif coverage < 1.0:
            reasons.append(f"coverage {coverage} < 1.0 ({len(messages)}/{expected} messages logged)")
        if hook_errors:
            reasons.append(f"{len(hook_errors)} line(s) in meetings/HOOK_ERRORS.log")
        missing = [n for n, p in records.items() if not p.is_file()]
        if missing:
            reasons.append("Secretary records missing: " + ", ".join(missing))
        status = "CAPTURE VERIFIED" if not reasons else "PARTIAL"
    return {"meeting_id": meeting_id, "status": status, "reasons": reasons, "events": events,
            "event_counts": Counter(e["hook"] for e in events), "messages": len(messages),
            "complete_messages": len(complete), "senders": senders, "ballots": sum(e["ballot"] for e in events),
            "expected": expected, "coverage": coverage, "hook_errors": hook_errors, "team_dir": team_dir,
            "members": members, "task_files": len(task_files), "records": records}


def render(c: dict, root: Path) -> str:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [f"# Runtime Acceptance — meeting {c['meeting_id']}", "",
             f"- Collected (UTC): {now}",
             f"- Platform: {platform.system()} {platform.release()}, Python {platform.python_version()}",
             f"- **Capture status: {c['status']}**", ""]
    if c["reasons"]:
        lines += ["## Gaps", ""] + [f"- {r}" for r in c["reasons"]] + [""]
    lines += ["## Measurements", "",
              "| Measure | Value |", "|---|---|",
              f"| SendMessage events logged | {c['messages']} |",
              f"| Complete message events (sender, recipient, text) | {c['complete_messages']} |",
              f"| Messages expected (from Secretary log) | {c['expected'] if c['expected'] is not None else 'not given'} |",
              f"| Capture coverage | {c['coverage'] if c['coverage'] is not None else 'unknown'} |",
              f"| Distinct senders | {len(c['senders'])}: {', '.join(c['senders']) or '—'} |",
              f"| Events carrying FINAL_BALLOT | {c['ballots']} |",
              f"| Event counts by hook | {', '.join(f'{k}: {v}' for k, v in sorted(c['event_counts'].items(), key=str)) or '—'} |",
              f"| HOOK_ERRORS.log lines | {len(c['hook_errors'])} |",
              f"| Team members (from ~/.claude/teams) | {', '.join(m['name'] or '?' for m in c['members']) or 'not found (collect before the session ends)'} |",
              f"| Task files (from ~/.claude/tasks) | {c['task_files']} |", "",
              "## Evidence files (SHA-256)", "", "| File | SHA-256 |", "|---|---|"]
    for e in c["events"]:
        lines.append(f"| {e['file'].relative_to(root).as_posix()} | {sha256(e['file'])} |")
    for name, path in c["records"].items():
        lines.append(f"| {path.relative_to(root).as_posix()} | {sha256(path) if path.is_file() else 'MISSING'} |")
    lines += ["", "Message bodies, session IDs and secrets are intentionally not copied into this report.",
              "CAPTURE VERIFIED requires ≥ 2 real senders, complete events, coverage 1.0, no hook errors and all Secretary records."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Collect Agent Teams runtime acceptance evidence.")
    parser.add_argument("--meeting-id", required=True)
    parser.add_argument("--expected-messages", type=int, help="messages the Secretary's discussion log lists")
    parser.add_argument("--team", help="team directory name under ~/.claude/teams (default: newest)")
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,100}", args.meeting_id):
        parser.error("unsafe meeting id")
    root = Path(args.root).resolve()
    c = collect(root, args.meeting_id, args.expected_messages, Path(args.claude_home).expanduser(), args.team)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(args.out) if args.out else root / "evidence" / "runtime" / f"{stamp}-{platform.system().lower()}" / "RUNTIME_ACCEPTANCE.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(c, root), encoding="utf-8")
    print(f"Capture status: {c['status']}")
    for reason in c["reasons"]:
        print("  -", reason)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
