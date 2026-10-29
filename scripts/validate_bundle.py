#!/usr/bin/env python3
"""Dependency-free static validator for the integrated Orcasus package."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import skill_evals  # noqa: E402

SKILLS = {
    "change-intake", "project-discovery", "platform-discovery", "requirements-traceability",
    "team-debate", "meeting-record", "backlog-slicing", "efficient-testing",
    "vertical-slice-delivery", "root-cause-debate", "design-quality-gate", "delivery-readiness",
    "closeout-report", "governance-audit", "process-retro", "knowledge-curation",
}
AGENTS = {
    "product-manager", "product-analyst", "domain-architect", "product-designer", "ux-researcher",
    "frontend-engineer", "backend-engineer", "mobile-engineer", "integration-engineer",
    "data-platform-engineer", "qa-automation-engineer", "security-reviewer", "performance-reviewer",
    "devil-advocate", "team-secretary", "governance-auditor", "knowledge-steward",
}
REQUIRED = [
    "README.md", "CLAUDE.md", "VERSION", "INITIALIZE_AGENTS.md",
    ".claude/settings.json", ".gitignore", "CHANGELOG.md",
    "docs/TEAM_OPERATING_MODEL.md", "docs/DEBATE_PROTOCOL.md",
    "docs/MEETING_RECORDING_PROTOCOL.md", "docs/PLATFORM_REFERENCE_ARCHITECTURE.md",
    "docs/UX_NORTH_STAR.md", "docs/ACCEPTANCE_TESTS.md", "docs/AI_SDLC_STAGE_MAP.md",
    "docs/USER_GUIDE_VI.md", "docs/RESEARCH_AND_DECISIONS.md", "docs/STATIC_VALIDATION_RESULTS.md",
    "docs/ADR_TEMPLATE.md", "docs/PRD_TEMPLATE.md", "docs/MEETING_MINUTES_TEMPLATE.md",
    "docs/DEFINITION_OF_DONE.md",
    "skills/project-discovery/SKILL.md", "skills/efficient-testing/SKILL.md",
    "scripts/log_team_message.py", "scripts/test_meeting_logger.py",
    "scripts/hooks/run_python.sh", "scripts/test_hook_launcher.py",
    "scripts/check_knowledge_links.py", "scripts/test_knowledge_links.py", "scripts/skill_evals.py",
    "scripts/validate_bundle.py", "meetings/CURRENT_MEETING.json", "meetings/README.md",
    "knowledge/INDEX.md", "knowledge/README.md", ".github/workflows/validate.yml",
    "templates/READINESS_MATRIX_TEMPLATE.md", "templates/TEST_PLAN_TEMPLATE.md",
    "templates/INTAKE_RECORD_TEMPLATE.md", "templates/TRACE_MATRIX_TEMPLATE.md",
    "templates/BACKLOG_TEMPLATE.md", "templates/CLOSEOUT_TEMPLATE.md",
    "templates/GOVERNANCE_AUDIT_TEMPLATE.md", "templates/RETRO_TEMPLATE.md",
]
REQUIRED += [f".claude/skills/{name}/SKILL.md" for name in sorted(SKILLS)]
REQUIRED += [f".claude/agents/{name}.md" for name in sorted(AGENTS)]
LAUNCHER = "scripts/hooks/run_python.sh"
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
    if LAUNCHER in json.dumps(hooks.get("SessionStart", [])) and "--check" in json.dumps(hooks.get("SessionStart", [])):
        passed.append("PASS SessionStart hook runtime check configured")
    else:
        errors.append("SessionStart hook must run " + LAUNCHER + " --check")
    portable = True
    for event, groups in hooks.items():
        for group in groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                first = command.split()[0] if command.split() else ""
                if first in ("python", "python3", "py") or LAUNCHER not in command:
                    errors.append(f"Hook {event} must call Python through {LAUNCHER}, not '{command}'")
                    portable = False
    if portable:
        passed.append("PASS every hook uses the portable Python launcher")
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
    if match.group(1) != path.stem:
        errors.append(f"Agent name '{match.group(1)}' must match file name {path.name}")
if agent_names == AGENTS:
    passed.append(f"PASS {len(AGENTS)} unique agent roles match the expected roster")
else:
    errors.append(f"Agent roster mismatch; missing {sorted(AGENTS - agent_names)}, unexpected {sorted(agent_names - AGENTS)}")

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
    if match.group(1) != path.parent.name:
        errors.append(f"Skill name '{match.group(1)}' must match its directory {path.parent.name}")
    description = desc.group(0).split(":", 1)[1].strip().strip('"\'')
    if len(description) > 1024:
        errors.append(f"Skill description over 1024 characters: {match.group(1)}")
if skill_names == SKILLS:
    passed.append(f"PASS {len(SKILLS)} unique workflow skills match the expected set")
else:
    errors.append(f"Skill set mismatch; missing {sorted(SKILLS - skill_names)}, unexpected {sorted(skill_names - SKILLS)}")

eval_passed, eval_errors = skill_evals.validate(ROOT)
passed.extend("PASS " + item for item in eval_passed)
errors.extend(eval_errors)

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
