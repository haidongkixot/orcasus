#!/usr/bin/env python3
"""Run Orcasus skill eval cases against a real Claude Code session, locally.

Each attempt copies the sample-app fixture to a temporary directory, installs the
Orcasus package into it, commits a baseline, runs `claude -p` with the case prompt
and applies the deterministic checks: skill selection, files created/unchanged,
forbidden tools, turn limit and secret-like output. Text assertions stay PENDING
for scripts/live_evals/judge.py.

This spends tokens on the account `claude` is logged in to. Run it on your own
machine, start with --smoke, and set --budget-total.

  python3 scripts/live_evals/run_live_evals.py --smoke --budget-total 5
  python3 scripts/live_evals/run_live_evals.py --skill change-intake --repeats 3
  python3 scripts/live_evals/run_live_evals.py --smoke --dry-run
"""
from __future__ import annotations

import argparse
import os
import platform
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (EVIDENCE_DIR, FIXTURE_DIR, ROOT, has_secret, load_cases, matches,  # noqa: E402
                    parse_stream, redact_text, write_json)

# What a consuming project gets when it installs Orcasus.
INSTALL_PATHS = [".claude", "CLAUDE.md", "templates", "scripts", "knowledge", "docs",
                 "meetings/README.md", "meetings/CURRENT_MEETING.json", ".gitignore", ".gitattributes"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "live_evals", "runtime_acceptance")
DEFAULT_TOOLS = [
    "Read", "Grep", "Glob", "Write", "Edit", "Skill", "Agent", "SendMessage", "TodoWrite",
    "Bash(git status *)", "Bash(git diff *)", "Bash(git log *)", "Bash(git show *)", "Bash(ls *)",
    "Bash(python3 scripts/*)", "Bash(node --test *)", "Bash(npm test *)",
]
DEFAULT_MAX_TURNS = 25


def prepare_workspace(dest: Path, fixture: Path = FIXTURE_DIR, root: Path = ROOT) -> None:
    shutil.copytree(fixture, dest, dirs_exist_ok=True)
    for rel in INSTALL_PATHS:
        src = root / rel
        if src.is_dir():
            shutil.copytree(src, dest / rel, dirs_exist_ok=True, ignore=IGNORE)
        elif src.is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / rel)
    git(dest, "init", "-q")
    git(dest, "add", "-A")
    git(dest, "-c", "user.name=orcasus-eval", "-c", "user.email=eval@example.invalid",
        "commit", "-q", "-m", "baseline")


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def changed_files(workspace: Path) -> dict:
    """Map path -> status code relative to the baseline commit (A=added, M=modified, D=deleted)."""
    out = git(workspace, "status", "--porcelain", "--untracked-files=all")
    files = {}
    for line in out.splitlines():
        code, path = line[:2].strip(), line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files[path.strip('"')] = "A" if code in ("??", "A") else code[:1]
    return files


def build_command(args, case, workspace: Path) -> list[str]:
    max_turns = (case.get("checks") or {}).get("max_turns", args.max_turns)
    cmd = [args.claude_bin, "-p", case["prompt"], "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns), "--setting-sources", "project", "--no-session-persistence",
           "--permission-mode", "dontAsk", "--allowedTools", *args.allowed_tools]
    if args.budget_per_run:
        cmd += ["--max-budget-usd", str(args.budget_per_run)]
    if args.model:
        cmd += ["--model", args.model]
    return cmd


def apply_checks(skill: str, case: dict, summary: dict, files: dict, raw: str) -> dict:
    """Deterministic verdicts for one attempt."""
    invoked = summary["skills_invoked"]
    if case["type"] == "should_trigger":
        trigger = {"verdict": "PASS" if skill in invoked else "FAIL",
                   "detail": f"expected {skill}; invoked {invoked or 'none'}"}
        routing = {"verdict": "NOT APPLICABLE"}
    else:
        trigger = {"verdict": "FAIL" if skill in invoked else "PASS",
                   "detail": f"must not invoke {skill}; invoked {invoked or 'none'}"}
        target = case.get("routes_to")
        routing = ({"verdict": "PASS" if target in invoked else "FAIL", "detail": f"expected {target}"}
                   if target else {"verdict": "NOT APPLICABLE"})
    checks = []
    spec = case.get("checks") or {}
    for pattern in spec.get("files_created", []):
        hit = [p for p, status in files.items() if status in ("A", "M") and matches(p, pattern)]
        checks.append({"name": f"files_created:{pattern}", "safety": False,
                       "verdict": "PASS" if hit else "FAIL", "detail": hit or "no matching file written"})
    for pattern in spec.get("files_unchanged", []):
        hit = [p for p in files if matches(p, pattern)]
        checks.append({"name": f"files_unchanged:{pattern}", "safety": True,
                       "verdict": "FAIL" if hit else "PASS", "detail": hit or "unchanged"})
    for tool in spec.get("forbidden_tools", []):
        used = summary["tools_used"].get(tool, 0)
        checks.append({"name": f"forbidden_tool:{tool}", "safety": True,
                       "verdict": "FAIL" if used else "PASS", "detail": f"used {used} times"})
    checks.append({"name": "no_secret_like_output", "safety": True,
                   "verdict": "FAIL" if has_secret(raw) else "PASS",
                   "detail": "secret-like pattern in transcript" if has_secret(raw) else "none found"})
    return {"trigger": trigger, "routing": routing, "checks": checks}


def run_attempt(args, run_id, skill, case, attempt, out_dir: Path, raw_dir: Path) -> dict:
    verdict = {"run_id": run_id, "skill": skill, "case_id": case["id"], "case_type": case["type"],
               "routes_to": case.get("routes_to"), "attempt": attempt, "prompt": case["prompt"],
               "assertions": [{"text": a, "verdict": "PENDING", "evidence_quote": None, "judge": None}
                              for a in case["expect"]["assertions"]]}
    with tempfile.TemporaryDirectory(prefix="orcasus-eval-") as tmp:
        workspace = Path(tmp) / "project"
        prepare_workspace(workspace)
        cmd = build_command(args, case, workspace)
        env = dict(os.environ)
        env.pop("CLAUDE_PROJECT_DIR", None)
        started = time.monotonic()
        try:
            proc = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True,
                                  timeout=args.timeout, env=env, stdin=subprocess.DEVNULL)
            raw, stderr, status = proc.stdout, proc.stderr, "RAN" if proc.returncode == 0 else "ERROR"
            verdict["exit_code"] = proc.returncode
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr, status = "timeout", "TIMEOUT"
            verdict["exit_code"] = None
        verdict["duration_s"] = round(time.monotonic() - started, 1)
        files = changed_files(workspace)
        diff = git(workspace, "diff", "--no-color") + untracked_text(workspace, files)
    summary = parse_stream(raw)
    verdict.update({"status": status, "skills_invoked": summary["skills_invoked"],
                    "tools_used": summary["tools_used"], "num_turns": summary["num_turns"],
                    "cost_usd": summary["cost_usd"], "result_subtype": summary["result_subtype"],
                    "hook_runtime": summary["hook_runtime"], "files_changed": files})
    verdict.update(apply_checks(skill, case, summary, files, raw))
    if status != "RAN":
        verdict["error"] = redact_text(stderr[-2000:])
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "transcript.jsonl").write_text(raw, encoding="utf-8")
    (raw_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "transcript.redacted.jsonl").write_text(redact_text(raw), encoding="utf-8")
    (out_dir / "diff.redacted.patch").write_text(redact_text(diff), encoding="utf-8")
    (out_dir / "final.redacted.txt").write_text(redact_text(summary["final_text"]), encoding="utf-8")
    write_json(out_dir / "tool_calls.json", summary["tool_calls"])
    write_json(out_dir / "verdict.json", verdict)
    return verdict


def untracked_text(workspace: Path, files: dict, limit: int = 20000) -> str:
    chunks = []
    for path, status in sorted(files.items()):
        if status != "A":
            continue
        target = workspace / path
        if target.is_file() and target.stat().st_size <= limit:
            chunks.append(f"\n--- new file: {path} ---\n" + target.read_text(encoding="utf-8", errors="replace"))
    return "".join(chunks)


def claude_version(bin_name: str) -> str:
    try:
        return subprocess.run([bin_name, "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run Orcasus skill evals against real Claude Code sessions.")
    parser.add_argument("--skill", action="append", help="skill to run (repeatable); default all")
    parser.add_argument("--case", action="append", help="case id to run (repeatable)")
    parser.add_argument("--smoke", action="store_true", help="one trigger and one non-trigger case per skill")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--budget-total", type=float, default=5.0, help="stop when reported spend reaches this (USD)")
    parser.add_argument("--budget-per-run", type=float, default=1.0, help="--max-budget-usd per attempt")
    parser.add_argument("--max-runs", type=int, default=0, help="hard cap on attempts (0 = no cap)")
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    parser.add_argument("--timeout", type=int, default=900, help="seconds per attempt")
    parser.add_argument("--model")
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--allowed-tools", nargs="+", default=DEFAULT_TOOLS)
    parser.add_argument("--out", default=str(EVIDENCE_DIR))
    parser.add_argument("--dry-run", action="store_true", help="list the attempts and the command, run nothing")
    args = parser.parse_args(argv)

    cases = load_cases(skills=args.skill, case_ids=args.case, smoke=args.smoke)
    if not cases:
        print("No eval cases matched.", file=sys.stderr)
        return 1
    planned = [(skill, case, n) for skill, case in cases for n in range(1, args.repeats + 1)]
    if args.max_runs:
        planned = planned[:args.max_runs]
    if args.dry_run:
        for skill, case, n in planned:
            print(f"{skill:28} {case['id']:45} attempt {n}")
        print(f"{len(planned)} attempts planned. Example command:")
        print(" ".join(build_command(args, planned[0][1], Path("."))))
        return 0
    if not shutil.which(args.claude_bin) and not Path(args.claude_bin).is_file():
        print(f"Claude Code CLI not found: {args.claude_bin}", file=sys.stderr)
        return 1

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"run-{stamp}-{secrets.token_hex(3)}"
    out_root = Path(args.out)
    run_dir, raw_root = out_root / run_id, out_root / "raw" / run_id
    meta = {"run_id": run_id, "started_utc": stamp, "claude_version": claude_version(args.claude_bin),
            "model": args.model or "default", "platform": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(), "orcasus_commit": orcasus_commit(),
            "args": {k: v for k, v in vars(args).items() if k != "allowed_tools"},
            "allowed_tools": args.allowed_tools, "planned_attempts": len(planned)}
    write_json(run_dir / "run.json", meta)
    spent, results = 0.0, []
    for index, (skill, case, n) in enumerate(planned, 1):
        if spent >= args.budget_total:
            results.append({"skill": skill, "case_id": case["id"], "attempt": n, "status": "NOT RUN",
                            "reason": "budget-total reached"})
            continue
        print(f"[{index}/{len(planned)}] {skill} / {case['id']} / attempt {n}", flush=True)
        verdict = run_attempt(args, run_id, skill, case, n, run_dir / skill / case["id"] / f"attempt-{n}",
                              raw_root / skill / case["id"] / f"attempt-{n}")
        spent += verdict.get("cost_usd") or 0.0
        print(f"    status={verdict['status']} trigger={verdict['trigger']['verdict']} "
              f"checks={sum(c['verdict'] == 'PASS' for c in verdict['checks'])}/{len(verdict['checks'])} "
              f"cost={verdict.get('cost_usd')} hook={verdict['hook_runtime']}", flush=True)
        results.append({k: verdict.get(k) for k in ("skill", "case_id", "attempt", "status", "cost_usd")})
    meta.update({"finished_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                 "reported_spend_usd": round(spent, 4), "results": results,
                 "not_run": sum(r["status"] == "NOT RUN" for r in results)})
    write_json(run_dir / "run.json", meta)
    print(f"Run {run_id}: {len(results) - meta['not_run']} attempts ran, {meta['not_run']} not run, "
          f"reported spend ${spent:.4f}. Evidence: {run_dir}")
    print("Next: python3 scripts/live_evals/judge.py " + str(run_dir))
    return 0


def orcasus_commit() -> str:
    try:
        sha = git(ROOT, "rev-parse", "HEAD").strip()
        dirty = bool(git(ROOT, "status", "--porcelain").strip())
        return sha + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
