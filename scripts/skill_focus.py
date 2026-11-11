#!/usr/bin/env python3
"""Skill admission and focus checks for the Orcasus core (CLAUDE.md, "Skill admission and focus").

Every skill description is loaded into every session, so the core stays small:
- at most MAX_CORE_SKILLS skills in .claude/skills/;
- at most MAX_DESCRIPTION_CHARS description characters in total;
- each skill is named in docs/AI_SDLC_STAGE_MAP.md;
- each description says when NOT to use the skill ("Do NOT use"), so neighbours stay apart.

The limits are owner-set; change them here, with an intake record.
Run: python3 scripts/skill_focus.py [--root PATH]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MAX_CORE_SKILLS = 20
MAX_DESCRIPTION_CHARS = 9000
BOUNDARY = "Do NOT use"
STAGE_MAP = Path("docs") / "AI_SDLC_STAGE_MAP.md"


def descriptions(root: Path) -> dict[str, str]:
    """Map skill directory name -> description from SKILL.md frontmatter."""
    found = {}
    for path in sorted((root / ".claude" / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("\n---\n", 1)[0]
        match = re.search(r"(?m)^description:[ ]*(.+)$", frontmatter)
        found[path.parent.name] = match.group(1).strip().strip('"\'') if match else ""
    return found


def check(root: Path) -> tuple[list[str], list[str]]:
    passed, errors = [], []
    found = descriptions(root)
    total = sum(len(d) for d in found.values())
    if len(found) <= MAX_CORE_SKILLS:
        passed.append(f"core skills: {len(found)} of at most {MAX_CORE_SKILLS}")
    else:
        errors.append(f"core skills: {len(found)} exceeds {MAX_CORE_SKILLS}; merge or move one to an optional pack")
    if total <= MAX_DESCRIPTION_CHARS:
        passed.append(f"skill descriptions: {total} of at most {MAX_DESCRIPTION_CHARS} characters")
    else:
        errors.append(f"skill descriptions: {total} characters exceed {MAX_DESCRIPTION_CHARS}; shorten or remove a skill")
    stage_map = root / STAGE_MAP
    map_text = stage_map.read_text(encoding="utf-8") if stage_map.is_file() else ""
    for name, description in found.items():
        if f"`{name}`" not in map_text:
            errors.append(f"{name}: not named in {STAGE_MAP.as_posix()}; give it a lifecycle stage")
        if BOUNDARY not in description:
            errors.append(f"{name}: description has no '{BOUNDARY} ...' boundary naming a neighbouring skill")
    if not any(e.startswith(tuple(found)) for e in errors):
        passed.append(f"every skill has a stage-map entry and a '{BOUNDARY}' boundary")
    return passed, errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args(argv)
    passed, errors = check(Path(args.root))
    for item in passed:
        print("PASS", item)
    for item in errors:
        print("FAIL", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
