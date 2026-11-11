"""Shared helpers for Orcasus live skill evals (run, judge, calibrate, scorecard)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from log_team_message import EMAIL_RE, SECRET_PATTERNS, redact_text  # noqa: E402,F401

EVIDENCE_DIR = ROOT / "evidence" / "live-evals"
# Judge "model" recorded on assertions failed by the deterministic trigger check, without a model call.
AUTO_FAIL_MODEL = "auto:trigger-fail"
FIXTURE_DIR = ROOT / "evals" / "fixtures" / "sample-app"
# Per-case files copied over the fixture before the baseline commit (case "setup": {"overlay": name}).
OVERLAY_DIR = ROOT / "evals" / "fixtures" / "overlays"
HOOK_OK = "Orcasus hook runtime: OK"
HOOK_WARNING = "Orcasus hook runtime: WARNING"


def load_cases(root: Path = ROOT, skills=None, case_ids=None, smoke=False):
    """Return [(skill, case)] in a stable order. Smoke = first trigger and first non-trigger case per skill."""
    selected = []
    for path in sorted((root / ".claude" / "skills").glob("*/evals/evals.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        skill = data["skill"]
        if skills and skill not in skills:
            continue
        cases = data["cases"]
        if case_ids:
            cases = [c for c in cases if c["id"] in case_ids]
        if smoke:
            picked = []
            for case_type in ("should_trigger", "should_not_trigger"):
                first = next((c for c in cases if c["type"] == case_type), None)
                if first:
                    picked.append(first)
            cases = picked
        selected.extend((skill, case) for case in cases)
    return selected


def parse_stream(text: str) -> dict:
    """Summarize Claude Code `--output-format stream-json` output."""
    summary = {"skills_invoked": [], "tool_calls": [], "tools_used": {}, "final_text": "",
               "cost_usd": None, "num_turns": None, "is_error": False, "result_subtype": None,
               "hook_runtime": "NOT SEEN", "events": 0}
    if HOOK_OK in text:
        summary["hook_runtime"] = "OK"
    elif HOOK_WARNING in text:
        summary["hook_runtime"] = "WARNING"
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        summary["events"] += 1
        if event.get("type") == "assistant":
            for block in (event.get("message") or {}).get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name", "")
                tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
                summary["tools_used"][name] = summary["tools_used"].get(name, 0) + 1
                summary["tool_calls"].append({"name": name, "input": short_input(tool_input)})
                if name == "Skill":
                    skill = tool_input.get("skill") or tool_input.get("command") or tool_input.get("name")
                    if isinstance(skill, str):
                        skill = skill.lstrip("/").split()[0] if skill.strip() else skill
                        if skill not in summary["skills_invoked"]:
                            summary["skills_invoked"].append(skill)
        elif event.get("type") == "result":
            summary["final_text"] = event.get("result") or ""
            summary["cost_usd"] = event.get("total_cost_usd")
            summary["num_turns"] = event.get("num_turns")
            summary["is_error"] = bool(event.get("is_error"))
            summary["result_subtype"] = event.get("subtype")
    return summary


def short_input(tool_input: dict, limit: int = 300) -> dict:
    out = {}
    for key, value in tool_input.items():
        if isinstance(value, str):
            out[key] = redact_text(value[:limit])
        elif isinstance(value, (int, float, bool)) or value is None:
            out[key] = value
        else:
            out[key] = redact_text(json.dumps(value)[:limit])
    return out


def glob_to_regex(pattern: str) -> re.Pattern:
    """Glob with `**` (any depth), `*` (one path segment) and `?`."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif pattern[i] == "*":
            out += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(pattern[i])
            i += 1
    return re.compile("^" + out + "$")


def matches(path: str, pattern: str) -> bool:
    return bool(glob_to_regex(pattern).match(path))


def has_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern, _ in SECRET_PATTERNS)


# Nested runs must not see the caller's account identity or session: the 2026-10-30 run copied the
# owner's e-mail into a record (audit F3), and inherited session ids mix the child into the parent.
SESSION_VARS = {"CLAUDE_PROJECT_DIR", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDECODE",
                "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_PID"}
IDENTITY_MARKERS = ("USER_EMAIL", "ACCOUNT_UUID", "ORGANIZATION_UUID")


def child_env(base) -> dict:
    """Environment for a nested `claude -p`: no session ids, no account identity."""
    return {k: v for k, v in base.items()
            if k not in SESSION_VARS and not any(marker in k for marker in IDENTITY_MARKERS)}


def has_personal_data(text: str) -> bool:
    return bool(EMAIL_RE.search(text))


def iter_attempts(run_dirs):
    """Yield (verdict_path, verdict) for every attempt under the given run directories."""
    for run_dir in run_dirs:
        for path in sorted(Path(run_dir).glob("*/*/attempt-*/verdict.json")):
            yield path, json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
