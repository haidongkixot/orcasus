#!/usr/bin/env python3
"""Dependency-free static validator for the integrated Orcasus package."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "CLAUDE.md", "VERSION", "INITIALIZE_AGENTS.md",
    ".claude/settings.json", ".gitignore", "CHANGELOG.md",
    "docs/TEAM_OPERATING_MODEL.md", "docs/DEBATE_PROTOCOL.md",
    "docs/MEETING_RECORDING_PROTOCOL.md", "docs/PLATFORM_REFERENCE_ARCHITECTURE.md",
    "docs/UX_NORTH_STAR.md", "docs/ACCEPTANCE_TESTS.md",
    "docs/USER_GUIDE_VI.md", "docs/RESEARCH_AND_DECISIONS.md",
    "docs/ADR_TEMPLATE.md", "docs/PRD_TEMPLATE.md", "docs/MEETING_MINUTES_TEMPLATE.md",
    "docs/DEFINITION_OF_DONE.md",
    ".claude/skills/project-discovery/SKILL.md",
    ".claude/skills/efficient-testing/SKILL.md",
    ".claude/skills/team-debate/SKILL.md",
    ".claude/skills/meeting-record/SKILL.md",
    ".claude/skills/platform-discovery/SKILL.md",
    ".claude/skills/root-cause-debate/SKILL.md",
    ".claude/skills/vertical-slice-delivery/SKILL.md",
    ".claude/skills/design-quality-gate/SKILL.md",
    ".claude/skills/delivery-readiness/SKILL.md",
    "skills/project-discovery/SKILL.md", "skills/efficient-testing/SKILL.md",
    "scripts/log_team_message.py", "scripts/test_meeting_logger.py",
    "scripts/validate_bundle.py", "meetings/CURRENT_MEETING.json", "meetings/README.md",
    "templates/READINESS_MATRIX_TEMPLATE.md", "templates/TEST_PLAN_TEMPLATE.md",
]
passed, errors = [], []

for rel in REQUIRED:
    if (ROOT / rel).is_file():
        passed.append("PASS required file: " + rel)
    else:
        errors.append("Missing required file: " + rel)

try:
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    passed.append("PASS settings JSON parses")
    if settings.get("env", {}).get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1":
        passed.append("PASS Agent Teams explicitly enabled")
    else:
        errors.append("Agent Teams switch missing")
    hooks = settings.get("hooks", {})
    post = json.dumps(hooks.get("PostToolUse", []))
    if "SendMessage" in post and "log_team_message.py" in post:
        passed.append("PASS SendMessage logger hook configured")
    else:
        errors.append("SendMessage logger hook missing")
    for event in ("TaskCreated", "TaskCompleted", "TeammateIdle"):
        if event in hooks and "log_team_message.py" in json.dumps(hooks[event]):
            passed.append("PASS lifecycle hook: " + event)
        else:
            errors.append("Missing logger hook: " + event)
    deny = settings.get("permissions", {}).get("deny", [])
    if any("Read(./.env)" in item for item in deny):
        passed.append("PASS env secret guard")
    else:
        errors.append("Missing secret-file permission guard")
except Exception as exc:
    errors.append("Invalid settings JSON: " + str(exc))

agents_dir = ROOT / ".claude/agents"
agents = sorted(agents_dir.glob("*.md")) if agents_dir.exists() else []
agent_names = set()
for path in agents:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        errors.append("Invalid agent frontmatter: " + str(path.relative_to(ROOT)))
        continue
    frontmatter = text.split("\n---\n", 1)[0]
    match = re.search(r"(?m)^name:[ ]*([a-z0-9-]+)[ ]*$", frontmatter)
    desc = re.search(r"(?m)^description:[ ]*.+$", frontmatter)
    if not match or not desc or not text.split("\n---\n", 1)[1].strip():
        errors.append("Invalid agent metadata/body: " + str(path.relative_to(ROOT)))
        continue
    if match.group(1) in agent_names:
        errors.append("Duplicate agent name: " + match.group(1))
    agent_names.add(match.group(1))
if len(agent_names) == 15 and "team-secretary" in agent_names:
    passed.append("PASS 15 unique agent roles incl. Team Secretary")
else:
    errors.append("Expected 15 unique roles incl. Team Secretary; found " + str(len(agent_names)))

skills_dir = ROOT / ".claude/skills"
skills = sorted(skills_dir.rglob("SKILL.md")) if skills_dir.exists() else []
skill_names = set()
for path in skills:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        errors.append("Invalid skill frontmatter: " + str(path.relative_to(ROOT)))
        continue
    frontmatter = text.split("\n---\n", 1)[0]
    match = re.search(r"(?m)^name:[ ]*([a-z0-9-]+)[ ]*$", frontmatter)
    desc = re.search(r"(?m)^description:[ ]*.+$", frontmatter)
    if not match or not desc or not text.split("\n---\n", 1)[1].strip():
        errors.append("Invalid skill metadata/body: " + str(path.relative_to(ROOT)))
        continue
    if match.group(1) in skill_names:
        errors.append("Duplicate skill name: " + match.group(1))
    skill_names.add(match.group(1))
if len(skill_names) == 9:
    passed.append("PASS 9 unique workflow skills")
else:
    errors.append("Expected 9 skills; found " + str(len(skill_names)))

for name in ("project-discovery", "efficient-testing"):
    runtime = ROOT / ".claude/skills" / name / "SKILL.md"
    mirror = ROOT / "skills" / name / "SKILL.md"
    if runtime.exists() and mirror.exists() and runtime.read_bytes() == mirror.read_bytes():
        passed.append("PASS root/library skill mirror: " + name)
    else:
        errors.append("Skill mirror missing or differs: " + name)

testing = ROOT / ".claude/skills/efficient-testing/SKILL.md"
if testing.exists():
    body = testing.read_text(encoding="utf-8").lower()
    for term in ("screenshot budget = 0", "trace budget = 0", "video budget = 0", "image-generation"):
        if term in body:
            passed.append("PASS zero-capture policy: " + term)
        else:
            errors.append("Efficient Testing missing policy: " + term)

discovery = ROOT / ".claude/skills/project-discovery/SKILL.md"
if discovery.exists():
    body = discovery.read_text(encoding="utf-8").lower()
    for term in ("unknown", "owner", "readiness record", "never silently"):
        if term in body:
            passed.append("PASS discovery gate: " + term)
        else:
            errors.append("Project Discovery missing policy: " + term)

try:
    manifest = json.loads((ROOT / "meetings/CURRENT_MEETING.json").read_text(encoding="utf-8"))
    if manifest.get("active") is False:
        passed.append("PASS meeting manifest starts inactive")
    else:
        errors.append("Meeting manifest must start inactive")
except Exception as exc:
    errors.append("Meeting manifest invalid: " + str(exc))

print("Orcasus integrated Agent Team static validation")
for item in passed:
    print(item)
for item in errors:
    print("FAIL", item)
print("Summary: " + str(len(passed)) + " passed, " + str(len(errors)) + " failed")
print("Static checks do not prove runtime teammate messaging, hook firing, permissions enforcement, product UX or production readiness.")
sys.exit(1 if errors else 0)
