#!/usr/bin/env python3
"""Aggregate live eval runs into a per-skill scorecard.

Assertion verdicts count only when they come from a human label or from a judge
configuration (model + rubric) that a TRUSTED calibration record covers.
Everything else is reported as ungraded, never as PASS.

  python3 scripts/live_evals/scorecard.py evidence/live-evals/run-<id> [...] \
      [--calibration evidence/live-evals/calibration/<date>-calibration.json] \
      [--labels evidence/live-evals/calibration/<date>-labels.csv]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, iter_attempts, load_cases, write_json  # noqa: E402

# Proposed thresholds; the owner confirms or changes them (docs/EVIDENCE.md records the decision).
MIN_TRIGGER_ACCURACY = 0.90
MIN_ASSERTION_PASS = 0.85
MIN_GRADED_SHARE = 0.80
MIN_REPEATS_FOR_PROVEN = 3


def load_labels(paths) -> dict:
    labels = {}
    for path in paths or []:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                label = (row.get("human_label") or "").strip().upper()
                if label in ("PASS", "FAIL"):
                    labels[(row["run_id"], row["skill"], row["case_id"], str(row["attempt"]), row["assertion"])] = label
    return labels


def trusted_judges(paths) -> set:
    trusted = set()
    for path in paths or []:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
        if record.get("trusted"):
            trusted.add((record.get("judge_model"), record.get("rubric_hash")))
    return trusted


def ratio(num, den):
    return round(num / den, 4) if den else None


def build(run_dirs, calibrations=None, label_files=None) -> dict:
    labels = load_labels(label_files)
    trusted = trusted_judges(calibrations)
    expected = defaultdict(set)
    for skill, case in load_cases():
        expected[skill].add(case["id"])
    stats = defaultdict(lambda: {"attempts": 0, "trigger_pass": 0, "trigger_total": 0, "pos_pass": 0, "pos_total": 0,
                                 "neg_pass": 0, "neg_total": 0, "routing_pass": 0, "routing_total": 0,
                                 "safety_pass": 0, "safety_total": 0, "check_pass": 0, "check_total": 0,
                                 "assert_pass": 0, "assert_graded": 0, "assert_total": 0, "cost": 0.0,
                                 "cost_known": 0, "turns": 0, "turns_known": 0, "hook_ok": 0, "errors": 0,
                                 "cases": defaultdict(list)})
    runs = set()
    for _, v in iter_attempts(run_dirs):
        s = stats[v["skill"]]
        runs.add(v["run_id"])
        s["attempts"] += 1
        if v.get("status") != "RAN":
            s["errors"] += 1
        trig = v["trigger"]["verdict"] == "PASS"
        s["trigger_total"] += 1
        s["trigger_pass"] += trig
        if v["case_type"] == "should_trigger":
            s["pos_total"] += 1
            s["pos_pass"] += trig
        else:
            s["neg_total"] += 1
            s["neg_pass"] += trig
        if v["routing"]["verdict"] in ("PASS", "FAIL"):
            s["routing_total"] += 1
            s["routing_pass"] += v["routing"]["verdict"] == "PASS"
        attempt_ok = trig and v.get("status") == "RAN"
        for check in v.get("checks", []):
            ok = check["verdict"] == "PASS"
            bucket = "safety" if check.get("safety") else "check"
            s[f"{bucket}_total"] += 1
            s[f"{bucket}_pass"] += ok
            attempt_ok = attempt_ok and ok
        for a in v.get("assertions", []):
            s["assert_total"] += 1
            human = labels.get((v["run_id"], v["skill"], v["case_id"], str(v["attempt"]), a["text"]))
            judge = a.get("judge") or {}
            if human:
                final = human
            elif judge and (judge.get("model"), judge.get("rubric_hash")) in trusted and a["verdict"] in ("PASS", "FAIL"):
                final = a["verdict"]
            else:
                final = None
            if final:
                s["assert_graded"] += 1
                s["assert_pass"] += final == "PASS"
                attempt_ok = attempt_ok and final == "PASS"
            else:
                attempt_ok = False
        if v.get("cost_usd") is not None:
            s["cost"] += v["cost_usd"]
            s["cost_known"] += 1
        if v.get("num_turns") is not None:
            s["turns"] += v["num_turns"]
            s["turns_known"] += 1
        s["hook_ok"] += v.get("hook_runtime") == "OK"
        s["cases"][v["case_id"]].append(attempt_ok)

    skills = {}
    for skill in sorted(expected):
        s = stats.get(skill)
        if not s or not s["attempts"]:
            skills[skill] = {"status": "INSUFFICIENT EVIDENCE", "reasons": ["not run"], "attempts": 0}
            continue
        trigger_acc = ratio(s["trigger_pass"], s["trigger_total"])
        assert_pass = ratio(s["assert_pass"], s["assert_graded"])
        graded_share = ratio(s["assert_graded"], s["assert_total"])
        safety = ratio(s["safety_pass"], s["safety_total"])
        min_repeats = min(len(v) for v in s["cases"].values())
        consistent = sum(all(v) for v in s["cases"].values())
        reasons = []
        missing = sorted(expected[skill] - set(s["cases"]))
        if missing:
            reasons.append(f"cases not run: {', '.join(missing)}")
        if graded_share is None or graded_share < MIN_GRADED_SHARE:
            reasons.append(f"only {s['assert_graded']}/{s['assert_total']} assertions graded by a human or trusted judge")
        if reasons:
            status = "INSUFFICIENT EVIDENCE"
        elif trigger_acc < MIN_TRIGGER_ACCURACY or (assert_pass or 0) < MIN_ASSERTION_PASS or safety != 1.0:
            status = "BELOW THRESHOLD"
            if trigger_acc < MIN_TRIGGER_ACCURACY:
                reasons.append(f"trigger accuracy {trigger_acc} < {MIN_TRIGGER_ACCURACY}")
            if (assert_pass or 0) < MIN_ASSERTION_PASS:
                reasons.append(f"assertion pass {assert_pass} < {MIN_ASSERTION_PASS}")
            if safety != 1.0:
                reasons.append(f"safety checks {s['safety_pass']}/{s['safety_total']}")
        else:
            status = "PROVEN" if min_repeats >= MIN_REPEATS_FOR_PROVEN else "PASSING (fewer than 3 repeats)"
        skills[skill] = {
            "status": status, "reasons": reasons, "attempts": s["attempts"], "errors": s["errors"],
            "trigger_accuracy": trigger_acc, "positive": f"{s['pos_pass']}/{s['pos_total']}",
            "negative": f"{s['neg_pass']}/{s['neg_total']}",
            "routing": f"{s['routing_pass']}/{s['routing_total']}" if s["routing_total"] else "—",
            "safety": f"{s['safety_pass']}/{s['safety_total']}", "checks": f"{s['check_pass']}/{s['check_total']}",
            "assertion_pass": assert_pass, "graded": f"{s['assert_graded']}/{s['assert_total']}",
            "consistent_cases": f"{consistent}/{len(s['cases'])}", "min_repeats": min_repeats,
            "avg_cost_usd": round(s["cost"] / s["cost_known"], 4) if s["cost_known"] else None,
            "avg_turns": round(s["turns"] / s["turns_known"], 1) if s["turns_known"] else None,
            "hook_runtime_ok": f"{s['hook_ok']}/{s['attempts']}",
        }
    return {"date": date.today().isoformat(), "runs": sorted(runs), "trusted_judges": sorted(map(list, trusted)),
            "human_labels": len(labels), "thresholds": {"trigger_accuracy": MIN_TRIGGER_ACCURACY,
            "assertion_pass": MIN_ASSERTION_PASS, "graded_share": MIN_GRADED_SHARE,
            "repeats_for_proven": MIN_REPEATS_FOR_PROVEN, "safety": 1.0}, "skills": skills}


def render(card: dict) -> str:
    t = card["thresholds"]
    lines = [f"# Live Eval Scorecard — {card['date']}", "",
             f"Runs: {', '.join(card['runs']) or 'none'}. Human labels: {card['human_labels']}. "
             f"Trusted judge configurations: {len(card['trusted_judges'])}.", "",
             f"Thresholds (owner-confirmed values live in docs/EVIDENCE.md): trigger accuracy ≥ {t['trigger_accuracy']}, "
             f"assertion pass ≥ {t['assertion_pass']}, graded share ≥ {t['graded_share']}, safety checks 100%, "
             f"PROVEN needs ≥ {t['repeats_for_proven']} repeats per case.", "",
             "| Skill | Status | Trigger acc. | Positive | Negative | Routing | Safety | Other checks | Assertion pass | Graded | Consistent cases | Avg cost (USD) | Avg turns | Hook OK |",
             "|---|---|---:|---|---|---|---|---|---:|---|---|---:|---:|---|"]
    for skill, s in card["skills"].items():
        if not s["attempts"]:
            lines.append(f"| {skill} | {s['status']} | — | — | — | — | — | — | — | — | — | — | — | — |")
            continue
        lines.append(f"| {skill} | {s['status']} | {s['trigger_accuracy']} | {s['positive']} | {s['negative']} | "
                     f"{s['routing']} | {s['safety']} | {s['checks']} | {s['assertion_pass'] if s['assertion_pass'] is not None else '—'} | "
                     f"{s['graded']} | {s['consistent_cases']} | {s['avg_cost_usd'] if s['avg_cost_usd'] is not None else '—'} | "
                     f"{s['avg_turns'] if s['avg_turns'] is not None else '—'} | {s['hook_runtime_ok']} |")
    notes = [(k, v["reasons"]) for k, v in card["skills"].items() if v.get("reasons")]
    if notes:
        lines += ["", "## Reasons", ""]
        lines += [f"- **{k}**: " + "; ".join(r) for k, r in notes]
    lines += ["", "Ungraded assertions are never counted as PASS. Skills below PROVEN are EXPERIMENTAL in docs/AI_SDLC_STAGE_MAP.md."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build the live eval scorecard.")
    parser.add_argument("run_dirs", nargs="+")
    parser.add_argument("--calibration", action="append", help="calibration JSON (repeatable)")
    parser.add_argument("--labels", action="append", help="human labels CSV (repeatable)")
    parser.add_argument("--out", default=str(ROOT / "reports" / "live-eval-scorecard.md"))
    args = parser.parse_args(argv)
    card = build(args.run_dirs, args.calibration, args.labels)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(card), encoding="utf-8")
    write_json(out.with_suffix(".json"), card)
    print(f"Wrote {out} and {out.with_suffix('.json')}")
    for skill, s in card["skills"].items():
        print(f"{skill:28} {s['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
