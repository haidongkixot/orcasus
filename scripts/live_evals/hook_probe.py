#!/usr/bin/env python3
"""Probe whether Orcasus logger hooks fire in a real headless Claude Code session.

Agent Teams do not spawn teammates in `claude -p`, but a named subagent can still
receive SendMessage. This probe activates a meeting in a scratch copy of the
sample app, asks Claude to message a named subagent, and reports which hook
events the logger actually recorded. The result is evidence either way; it does
not replace the interactive runtime acceptance run (docs/RUNTIME_ACCEPTANCE_RUNBOOK.md).

  python3 scripts/live_evals/hook_probe.py [--model MODEL] [--budget 1.0]
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EVIDENCE_DIR, parse_stream, redact_text, write_json  # noqa: E402
from run_live_evals import claude_version, prepare_workspace  # noqa: E402

TOKEN = "orcasus-hook-probe"
PROMPT = (f"This is an Orcasus hook probe; do not do any other work. Use the Agent tool to start a subagent named "
          f"probe-listener whose only job is to reply 'ready'. Then use SendMessage to send the exact text "
          f"'{TOKEN}' to probe-listener. Then stop and report which tools you used.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model")
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--budget", type=float, default=1.0)
    parser.add_argument("--out", default=str(EVIDENCE_DIR / "hook-probe"))
    args = parser.parse_args(argv)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    with tempfile.TemporaryDirectory(prefix="orcasus-probe-") as tmp:
        ws = Path(tmp) / "project"
        prepare_workspace(ws)
        manifest = {"meeting_id": "hook-probe", "active": True, "participants": [], "voters": []}
        (ws / "meetings" / "CURRENT_MEETING.json").write_text(json.dumps(manifest), encoding="utf-8")
        cmd = [args.claude_bin, "-p", PROMPT, "--output-format", "stream-json", "--verbose", "--max-turns", "10",
               "--setting-sources", "project", "--no-session-persistence", "--permission-mode", "dontAsk",
               "--allowedTools", "Agent", "SendMessage", "--max-budget-usd", str(args.budget)]
        if args.model:
            cmd += ["--model", args.model]
        proc = subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
        summary = parse_stream(proc.stdout)
        events = []
        for path in sorted((ws / "meetings").glob("*/*/events/*.json")):
            event = json.loads(path.read_text(encoding="utf-8"))
            events.append({"hook_event_name": event.get("hook_event_name"), "tool_name": event.get("tool_name"),
                           "recipient": event.get("recipient"), "meeting_id": event.get("meeting_id"),
                           "contains_token": TOKEN in json.dumps(event)})
        hook_errors = (ws / "meetings" / "HOOK_ERRORS.log").read_text(encoding="utf-8") \
            if (ws / "meetings" / "HOOK_ERRORS.log").is_file() else ""
    sent = summary["tools_used"].get("SendMessage", 0)
    logged = sum(e["hook_event_name"] == "PostToolUse" and e["contains_token"] for e in events)
    if not sent:
        result = "INCONCLUSIVE: Claude did not call SendMessage"
    elif logged:
        result = "PASS: SendMessage PostToolUse hook recorded the probe message in headless mode"
    else:
        result = "FAIL: SendMessage was called but no logger event was recorded"
    record = {"date_utc": stamp, "claude_version": claude_version(args.claude_bin),
              "platform": f"{platform.system()} {platform.release()}", "exit_code": proc.returncode,
              "hook_runtime": summary["hook_runtime"], "tools_used": summary["tools_used"],
              "send_message_calls": sent, "events": events, "hook_errors": redact_text(hook_errors),
              "cost_usd": summary["cost_usd"], "result": result}
    out = Path(args.out) / f"{stamp}-{platform.system().lower()}.json"
    write_json(out, record)
    print(result)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
