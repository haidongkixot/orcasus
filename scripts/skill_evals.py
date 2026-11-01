#!/usr/bin/env python3
"""Validate skill eval files and export a grading sheet for live runs.

Each skill keeps trigger and behavior cases in .claude/skills/<name>/evals/evals.json.
This script does not call a model: CI validates the cases; a person or a separate
authorized session runs the prompts in Claude Code and grades the assertions.

Run:
  python3 scripts/skill_evals.py validate
  python3 scripts/skill_evals.py sheet [--skill NAME] [--out reports/skill-eval-sheet.md]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_TYPES = {"should_trigger": True, "should_not_trigger": False}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,80}$")
MIN_CASES = 3


def skill_names(root: Path) -> list[str]:
    return sorted(p.parent.name for p in (root / ".claude" / "skills").glob("*/SKILL.md"))


CHECK_KEYS = {"files_created", "files_unchanged", "forbidden_tools", "max_turns"}


def validate_checks(checks, where: str) -> list[str]:
    """Deterministic checks the live runner applies to a run (see scripts/live_evals/)."""
    if not isinstance(checks, dict):
        return [f"{where}: checks must be an object"]
    errors = [f"{where}: unknown check '{key}'" for key in checks if key not in CHECK_KEYS]
    for key in ("files_created", "files_unchanged", "forbidden_tools"):
        value = checks.get(key)
        if value is not None and (not isinstance(value, list) or not value
                                  or not all(isinstance(v, str) and v.strip() for v in value)):
            errors.append(f"{where}: checks.{key} must be a non-empty list of strings")
    turns = checks.get("max_turns")
    if turns is not None and (not isinstance(turns, int) or not 1 <= turns <= 100):
        errors.append(f"{where}: checks.max_turns must be an integer from 1 to 100")
    return errors


def validate_file(path: Path, skill: str, known_skills: set[str]) -> list[str]:
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{skill}: evals.json unreadable: {exc}"]
    if data.get("skill") != skill:
        errors.append(f"{skill}: evals.json 'skill' must be '{skill}'")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        errors.append(f"{skill}: evals.json needs a description")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < MIN_CASES:
        return errors + [f"{skill}: needs at least {MIN_CASES} cases"]
    seen, types = set(), set()
    for i, case in enumerate(cases):
        where = f"{skill} case {case.get('id', i)}"
        case_id = case.get("id")
        if not isinstance(case_id, str) or not ID_RE.match(case_id):
            errors.append(f"{where}: id must be lowercase-kebab-case")
        elif case_id in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(case_id)
        case_type = case.get("type")
        if case_type not in CASE_TYPES:
            errors.append(f"{where}: type must be one of {sorted(CASE_TYPES)}")
            continue
        types.add(case_type)
        if not isinstance(case.get("prompt"), str) or len(case["prompt"].strip()) < 10:
            errors.append(f"{where}: prompt must be a realistic request")
        expect = case.get("expect", {})
        if expect.get("triggers") is not CASE_TYPES[case_type]:
            errors.append(f"{where}: expect.triggers must be {str(CASE_TYPES[case_type]).lower()} for {case_type}")
        assertions = expect.get("assertions")
        if not isinstance(assertions, list) or not assertions or not all(isinstance(a, str) and a.strip() for a in assertions):
            errors.append(f"{where}: expect.assertions must be a non-empty list of strings")
        routes_to = case.get("routes_to")
        if routes_to is not None:
            if case_type != "should_not_trigger":
                errors.append(f"{where}: routes_to is only for should_not_trigger cases")
            elif routes_to not in known_skills:
                errors.append(f"{where}: routes_to names unknown skill '{routes_to}'")
        if "checks" in case:
            errors.extend(validate_checks(case["checks"], where))
    for case_type in CASE_TYPES:
        if case_type not in types:
            errors.append(f"{skill}: needs at least one {case_type} case")
    return errors


def validate(root: Path = ROOT) -> tuple[list[str], list[str]]:
    passed, errors = [], []
    names = skill_names(root)
    known = set(names)
    for skill in names:
        path = root / ".claude" / "skills" / skill / "evals" / "evals.json"
        if not path.is_file():
            errors.append(f"{skill}: missing evals/evals.json")
            continue
        file_errors = validate_file(path, skill, known)
        if file_errors:
            errors.extend(file_errors)
        else:
            count = len(json.loads(path.read_text(encoding="utf-8"))["cases"])
            passed.append(f"evals valid: {skill} ({count} cases)")
    return passed, errors


def sheet(root: Path, only: str | None) -> str:
    lines = [f"# Skill Eval Grading Sheet — {date.today().isoformat()}", "",
             "Run each prompt in a fresh Claude Code session in a non-production copy of the repository.",
             "Record whether the expected skill was selected and grade each assertion PASS, FAIL or NOT RUN.",
             "Do not mark a case PASS without the session transcript or output as evidence.", ""]
    for skill in skill_names(root):
        if only and skill != only:
            continue
        data = json.loads((root / ".claude" / "skills" / skill / "evals" / "evals.json").read_text(encoding="utf-8"))
        lines += [f"## {skill}", "", data["description"], ""]
        for case in data["cases"]:
            expected = "should trigger" if case["type"] == "should_trigger" else "should NOT trigger"
            if case.get("routes_to"):
                expected += f" (expected skill: {case['routes_to']})"
            lines += [f"### {case['id']} — {expected}", "", "> " + case["prompt"], "",
                      "| Assertion | Result | Evidence |", "|---|---|---|"]
            lines += [f"| {a} | NOT RUN | |" for a in case["expect"]["assertions"]]
            lines += ["", "- Skill selected: ", ""]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate skill evals or export a grading sheet.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sheet_parser = sub.add_parser("sheet")
    sheet_parser.add_argument("--skill")
    sheet_parser.add_argument("--out")
    args = parser.parse_args(argv)
    if args.command == "validate":
        passed, errors = validate()
        for item in passed:
            print("PASS", item)
        for item in errors:
            print("FAIL", item)
        print(f"Summary: {len(passed)} passed, {len(errors)} failed")
        print("Valid eval files are not eval results; run the grading sheet in a live session to measure behavior.")
        return 1 if errors else 0
    if args.skill and args.skill not in skill_names(ROOT):
        print(f"Unknown skill: {args.skill}", file=sys.stderr)
        return 1
    text = sheet(ROOT, args.skill)
    if args.out:
        out = (ROOT / args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
