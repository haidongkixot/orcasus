#!/usr/bin/env python3
"""Best-effort, privacy-conscious Claude Code Agent Team event logger.

Reads one hook JSON payload from stdin. Records observable SendMessage input
and selected task lifecycle metadata. Does not record tool responses, unrelated
tool calls or hidden model reasoning. Secret redaction is best-effort.
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECRET_KEY = re.compile(r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|authorization|private[_-]?key|client[_-]?secret)")
SECRET_PATTERNS = [
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"), "Bearer [REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"), "[REDACTED_API_KEY]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    (re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret)\s*[:=]\s*(['\"]?)[^\s,;\"']{4,}\2"), r"\1=[REDACTED]"),
]
ALLOWED_TASK_EVENTS = {"TaskCreated", "TaskCompleted", "TeammateIdle"}


def redact_text(value: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def redact_object(value: Any, key: str = "") -> Any:
    if SECRET_KEY.search(key):
        return "[REDACTED]"
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, dict):
        return {str(k): redact_object(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_object(v, key) for v in value]
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return redact_text(str(value))


def find_project_root(payload: dict[str, Any]) -> Path:
    configured = os.environ.get("CLAUDE_PROJECT_DIR")
    if configured:
        candidate = Path(configured)
        if candidate.is_dir():
            return candidate.resolve()
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and Path(cwd).is_dir():
        return Path(cwd).resolve()
    return Path(__file__).resolve().parents[1]


def read_meeting_id(root: Path) -> tuple[str, bool]:
    manifest = root / "meetings" / "CURRENT_MEETING.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "UNASSIGNED-" + datetime.now(timezone.utc).strftime("%Y%m%d"), False
    meeting_id = data.get("meeting_id")
    active = data.get("active") is True
    if not isinstance(meeting_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,100}", meeting_id):
        return "UNASSIGNED-" + datetime.now(timezone.utc).strftime("%Y%m%d"), False
    if not active:
        return "UNASSIGNED-" + datetime.now(timezone.utc).strftime("%Y%m%d"), False
    return meeting_id, True


def event_is_loggable(payload: dict[str, Any]) -> bool:
    event_name = payload.get("hook_event_name")
    if event_name == "PostToolUse":
        return payload.get("tool_name") == "SendMessage"
    return event_name in ALLOWED_TASK_EVENTS


def extract_message_text(tool_input: dict[str, Any]) -> str | None:
    for key in ("message", "content", "text", "body", "summary"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return redact_text(value)
        if isinstance(value, dict):
            for nested_key in ("text", "content", "body", "message"):
                nested = value.get(nested_key)
                if isinstance(nested, str):
                    return redact_text(nested)
            return json.dumps(redact_object(value), ensure_ascii=False, sort_keys=True)
    return None


def normalized_event(payload: dict[str, Any], meeting_id: str, meeting_active: bool) -> dict[str, Any]:
    event_name = str(payload.get("hook_event_name", "UNKNOWN"))
    event: dict[str, Any] = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "event_id": str(payload.get("tool_use_id") or uuid.uuid4()),
        "meeting_id": meeting_id,
        "meeting_manifest_active": meeting_active,
        "hook_event_name": event_name,
        "session_id": payload.get("session_id"),
        "agent_id": payload.get("agent_id"),
        "agent_type": payload.get("agent_type"),
        "teammate_name": payload.get("teammate_name"),
        "team_name": payload.get("team_name"),
        "source_note": "Observable hook event only; no hidden reasoning. Secret redaction is best-effort.",
    }
    if event_name == "PostToolUse":
        tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
        event["tool_name"] = "SendMessage"
        event["recipient"] = next((tool_input.get(k) for k in ("recipient", "to", "target", "teammate_name") if tool_input.get(k) is not None), None)
        event["message_text"] = extract_message_text(tool_input)
        event["tool_input_redacted"] = redact_object(tool_input)
    else:
        keys = ("task_id", "task_subject", "task_description", "teammate_name", "team_name")
        event["metadata"] = redact_object({k: payload.get(k) for k in keys if payload.get(k) is not None})
    return event


def handle_payload(payload: dict[str, Any], root: Path | None = None) -> Path | None:
    if not event_is_loggable(payload):
        return None
    root = root or find_project_root(payload)
    meeting_id, meeting_active = read_meeting_id(root)
    session_dir = root / "meetings" / "sessions" / meeting_id if meeting_active else root / "meetings" / "unassigned" / meeting_id
    events_dir = session_dir / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    event = normalized_event(payload, meeting_id, meeting_active)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    safe_event_id = re.sub(r"[^A-Za-z0-9._-]", "_", event["event_id"])[:80]
    destination = events_dir / f"{timestamp}-{safe_event_id}.json"
    counter = 1
    while True:
        try:
            with destination.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(event, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            return destination
        except FileExistsError:
            destination = events_dir / f"{timestamp}-{safe_event_id}-{counter}.json"
            counter += 1


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        handle_payload(payload)
        return 0
    except Exception as exc:
        print(f"[orcasus logger warning] Could not record hook event: {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
