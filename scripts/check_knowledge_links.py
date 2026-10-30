#!/usr/bin/env python3
"""Dependency-free link and citation checker for Orcasus records.

Checks:
- knowledge/INDEX.md rows: columns, IDs, allowed values, dates, curator approval,
  successors, tracked source links and secret-like content (S10).
- TRACE_MATRIX.md files: citation status vocabulary, resolvable repo-relative
  citations, no unaccepted uncited requirement in approved scope, and
  ASSUMPTION-ACCEPTED only with a named human owner and date (S3).
- Relative markdown links in the repository's documentation resolve.
- Repository paths quoted in backticks in lifecycle records (docs/agent-ops,
  reports, decisions, projects, evidence) exist; a missing one is a warning,
  because a record may name an output that is still planned (S9).

A resolving link proves the source exists, not that it says what the record
claims; content checks stay with the human reviewer or curator.
Run: python3 scripts/check_knowledge_links.py [--root PATH]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from log_team_message import SECRET_PATTERNS  # noqa: E402

INDEX_COLUMNS = ["ID", "Type", "Title", "Status", "Sources", "Related", "Superseded by",
                 "Proposed by / date", "Curator approval"]
TYPES = {"DECISION", "CONSTRAINT", "LESSON", "ANCHOR", "PROCESS", "GLOSSARY"}
STATUSES = {"PROPOSED", "APPROVED", "SUPERSEDED", "RETIRED"}
CITATION_STATUSES = {"VERIFIED", "PARAPHRASE-OK", "MISMATCH", "UNVERIFIABLE", "NO SOURCE"}
REQUIREMENT_STATUSES = {"PROPOSED", "APPROVED", "REJECTED", "ASSUMPTION-ACCEPTED"}
ID_RE = re.compile(r"^K-\d{4}$")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
APPROVAL_RE = re.compile(r"^\S.*\s\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MEETING_RE = re.compile(r"\bmeeting:([A-Za-z0-9][A-Za-z0-9._-]{0,100})")
SHA_RE = re.compile(r"(?<![0-9a-f/])\b[0-9a-f]{7,40}\b")
DOC_GLOBS = ["*.md", "docs/**/*.md", "templates/**/*.md", "knowledge/**/*.md", ".claude/**/*.md",
             "skills/**/*.md", "meetings/README.md", "projects/**/*.md", "decisions/**/*.md", "reports/**/*.md"]
EMPTY = {"", "—", "-"}
OWNER_ACCEPT_RE = re.compile(r"accepted by owner:\s*(?P<name>[^|;]*?\S)\s+(?P<date>\d{4}-\d{2}-\d{2})\b", re.I)
AGENT_NAMES = {"claude", "agent", "assistant", "ai", "lead", "orchestrator", "main agent", "subagent"}
RECORD_GLOBS = ["docs/agent-ops/**/*.md", "reports/**/*.md", "decisions/**/*.md", "projects/**/*.md", "evidence/**/*.md"]
RECORD_PATH_RE = re.compile(r"`((?:docs|reports|decisions|projects|knowledge|meetings|evidence|templates|scripts)/[^`\s]*)`")


class Report:
    def __init__(self):
        self.passed, self.warnings, self.errors = [], [], []

    def ok(self, msg):
        self.passed.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def fail(self, msg):
        self.errors.append(msg)


def parse_table(lines, header_first_cell):
    """Return (header, rows) of the first markdown table whose header starts with header_first_cell."""
    for i, line in enumerate(lines):
        cells = split_row(line)
        if cells and cells[0] == header_first_cell and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            rows = []
            for row_line in lines[i + 2:]:
                if not row_line.strip().startswith("|"):
                    break
                rows.append(split_row(row_line))
            return cells, rows
    return None, []


def split_row(line):
    line = line.strip()
    if not line.startswith("|"):
        return []
    return [cell.strip() for cell in line.strip("|").split("|")]


def has_secret(text):
    return any(pattern.search(text) for pattern, _ in SECRET_PATTERNS)


def check_target(target, base_dir, root, where, report):
    """Validate one link target relative to base_dir. Returns True when it resolves or is external."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):  # http:, https:, mailto: ...
        return True
    path_part, _, anchor = target.partition("#")
    if not path_part:
        return True  # same-document anchor
    resolved = (base_dir / path_part).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        report.fail(f"{where}: link leaves the repository: {target}")
        return False
    if not resolved.exists():
        report.fail(f"{where}: broken link: {target}")
        return False
    line_anchor = re.fullmatch(r"L(\d+)(?:-L(\d+))?", anchor)
    if line_anchor and resolved.is_file():
        last = int(line_anchor.group(2) or line_anchor.group(1))
        count = len(resolved.read_text(encoding="utf-8", errors="replace").splitlines())
        if last > count:
            report.fail(f"{where}: line anchor #{anchor} beyond end of {path_part} ({count} lines)")
            return False
    return True


def check_meetings(text, root, where, report):
    ok = True
    for meeting_id in MEETING_RE.findall(text):
        if not (root / "meetings" / "sessions" / meeting_id).is_dir():
            report.fail(f"{where}: meeting:{meeting_id} has no meetings/sessions/{meeting_id}/ record")
            ok = False
    return ok


def check_shas(text, root, where, report):
    for sha in SHA_RE.findall(text):
        try:
            result = subprocess.run(["git", "-C", str(root), "cat-file", "-e", sha + "^{commit}"],
                                    capture_output=True, timeout=10)
        except (OSError, subprocess.SubprocessError):
            report.warn(f"{where}: could not verify commit {sha} (git unavailable)")
            continue
        if result.returncode != 0:
            report.warn(f"{where}: commit {sha} not found in this clone (shallow clone or wrong SHA)")


def has_source(text):
    return bool(LINK_RE.search(text) or MEETING_RE.search(text) or re.search(r"https?://", text) or SHA_RE.search(text))


def check_index(root, report):
    index = root / "knowledge" / "INDEX.md"
    if not index.is_file():
        report.fail("knowledge/INDEX.md missing")
        return ""
    lines = index.read_text(encoding="utf-8").splitlines()
    header, rows = parse_table(lines, "ID")
    if header != INDEX_COLUMNS:
        report.fail("knowledge/INDEX.md header must be: | " + " | ".join(INDEX_COLUMNS) + " |")
        return ""
    report.ok("knowledge index header")
    entries, ids = [], set()
    for row in rows:
        if len(row) != len(INDEX_COLUMNS):
            report.fail(f"knowledge/INDEX.md: row has {len(row)} cells, expected {len(INDEX_COLUMNS)}: {row[:1]}")
            continue
        entry = dict(zip(INDEX_COLUMNS, row))
        if not ID_RE.match(entry["ID"]):
            report.fail(f"knowledge {entry['ID']}: ID must look like K-0001")
        if entry["ID"] in ids:
            report.fail(f"knowledge {entry['ID']}: duplicate ID")
        ids.add(entry["ID"])
        entries.append(entry)
    for entry in entries:
        where = f"knowledge {entry['ID']}"
        if entry["Type"] not in TYPES:
            report.fail(f"{where}: type must be one of {sorted(TYPES)}")
        if entry["Status"] not in STATUSES:
            report.fail(f"{where}: status must be one of {sorted(STATUSES)}")
        if not entry["Title"]:
            report.fail(f"{where}: empty title")
        if not DATE_RE.search(entry["Proposed by / date"]):
            report.fail(f"{where}: 'Proposed by / date' needs an absolute YYYY-MM-DD date")
        approval = entry["Curator approval"]
        if entry["Status"] in {"APPROVED", "SUPERSEDED", "RETIRED"} and not APPROVAL_RE.match(approval):
            report.fail(f"{where}: {entry['Status']} requires curator approval as '<name> YYYY-MM-DD'")
        if entry["Status"] == "PROPOSED" and approval not in EMPTY:
            report.fail(f"{where}: PROPOSED entries must not carry a curator approval")
        successor = entry["Superseded by"]
        if entry["Status"] == "SUPERSEDED":
            if successor not in ids:
                report.fail(f"{where}: SUPERSEDED requires 'Superseded by' to name an existing entry")
        elif successor not in EMPTY:
            report.fail(f"{where}: only SUPERSEDED entries may name a successor")
        for related in [r.strip() for r in entry["Related"].split(";") if r.strip() not in EMPTY]:
            if related not in ids:
                report.fail(f"{where}: related entry {related} does not exist")
        sources = entry["Sources"]
        if not has_source(sources):
            report.fail(f"{where}: needs at least one tracked source (link, meeting:<id>, commit SHA or URL)")
        for target in LINK_RE.findall(sources):
            check_target(target, index.parent, root, where, report)
        check_meetings(sources, root, where, report)
        check_shas(sources, root, where, report)
        if has_secret(" ".join(entry.values())):
            report.fail(f"{where}: secret-like value; remove it and rotate the secret if it was real")
    report.ok(f"knowledge index rows checked: {len(entries)}")
    return index.read_text(encoding="utf-8")


def check_unindexed(root, index_text, report):
    candidates = [p for p in (root / "decisions").glob("*.md")] + list((root / "reports").glob("*-closeout.md"))
    for path in sorted(candidates):
        rel = path.relative_to(root).as_posix()
        if rel not in index_text and path.name not in index_text:
            report.warn(f"unindexed record: {rel} (index it or note why not)")


def check_owner_acceptance(text, agents, where, report):
    """Only a named human owner may accept an assumption (retro P1, tbagri-web pilot 2026-10-29)."""
    match = OWNER_ACCEPT_RE.search(text)
    if not match:
        report.fail(f"{where}: ASSUMPTION-ACCEPTED needs 'accepted by owner: <name> YYYY-MM-DD'; only the owner may accept an assumption")
        return
    name = match.group("name").strip().lower()
    if name in agents or name.split()[0] in AGENT_NAMES:
        report.fail(f"{where}: ASSUMPTION-ACCEPTED by '{match.group('name')}', an agent; only the human owner may accept an assumption")


def check_trace_matrices(root, report):
    agents = AGENT_NAMES | {p.stem.lower() for p in (root / ".claude" / "agents").glob("*.md")}
    files = [root / "docs" / "agent-ops" / "TRACE_MATRIX.md"] + sorted((root / "projects").glob("*/TRACE_MATRIX.md"))
    for path in [p for p in files if p.is_file()]:
        rel = path.relative_to(root).as_posix()
        header, rows = parse_table(path.read_text(encoding="utf-8").splitlines(), "Req ID")
        if not header:
            report.fail(f"{rel}: no requirements table with a 'Req ID' column")
            continue
        col = {name: i for i, name in enumerate(header)}
        needed = ["Source citation", "Citation status", "Requirement status"]
        if any(name not in col for name in needed):
            report.fail(f"{rel}: requirements table needs columns {needed}")
            continue
        for row in rows:
            if not row or row[0] in EMPTY or len(row) != len(header):
                continue
            where = f"{rel} {row[0]}"
            citation, status, req_status = (row[col[n]] for n in needed)
            if status not in CITATION_STATUSES:
                report.fail(f"{where}: citation status must be one of {sorted(CITATION_STATUSES)}")
            if req_status not in REQUIREMENT_STATUSES:
                report.fail(f"{where}: requirement status must be one of {sorted(REQUIREMENT_STATUSES)}")
            if status in {"VERIFIED", "PARAPHRASE-OK"} and not has_source(citation):
                report.fail(f"{where}: {status} needs a source citation")
            if status in {"MISMATCH", "UNVERIFIABLE", "NO SOURCE"} and req_status == "APPROVED":
                report.fail(f"{where}: {status} cannot be APPROVED; resolve it with the owner, who may accept it as ASSUMPTION-ACCEPTED")
            if req_status == "ASSUMPTION-ACCEPTED":
                check_owner_acceptance(" | ".join(row), agents, where, report)
            for target in LINK_RE.findall(citation):
                check_target(target, path.parent, root, where, report)
            check_meetings(citation, root, where, report)
        report.ok(f"trace matrix checked: {rel}")


def check_docs(root, report):
    seen = set()
    count = 0
    for pattern in DOC_GLOBS:
        for path in root.glob(pattern):
            if path in seen or not path.is_file() or "/events/" in path.as_posix():
                continue
            seen.add(path)
            text = path.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore code blocks
            text = re.sub(r"`[^`\n]*`", "", text)  # ignore inline code examples
            for target in LINK_RE.findall(text):
                count += 1
                check_target(target, path.parent, root, path.relative_to(root).as_posix(), report)
    report.ok(f"documentation links checked: {count} in {len(seen)} files")


def check_record_paths(root, report):
    """Warn when a lifecycle record names a repository path that does not exist (retro P4)."""
    seen, count = set(), 0
    for pattern in RECORD_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            rel = path.relative_to(root).as_posix()
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8", errors="replace"), flags=re.S)
            for target in RECORD_PATH_RE.findall(text):
                if any(ch in target for ch in "<>*{}…") or "..." in target:
                    continue  # placeholder or pattern, not a concrete path
                target = re.sub(r"(#.*|:\d+(-\d+)?)$", "", target)
                count += 1
                if not (root / target).exists():
                    report.warn(f"{rel}: names `{target}`, which does not exist (write it, or mark it as planned without backticks)")
    report.ok(f"record paths checked: {count} in {len(seen)} records")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    report = Report()
    index_text = check_index(root, report)
    check_unindexed(root, index_text, report)
    check_trace_matrices(root, report)
    check_docs(root, report)
    check_record_paths(root, report)
    print("Orcasus knowledge and citation link check")
    for item in report.passed:
        print("PASS", item)
    for item in report.warnings:
        print("WARN", item)
    for item in report.errors:
        print("FAIL", item)
    print(f"Summary: {len(report.passed)} passed, {len(report.warnings)} warnings, {len(report.errors)} failed")
    print("A resolving link proves the source exists, not that it supports the claim; a human checks content.")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
