#!/usr/bin/env python3
"""Calibrate the LLM judge against human labels.

1. sample: export a blind labeling sheet (CSV) of judged assertions; the judge's
   verdicts are not shown. The owner fills human_label with PASS or FAIL.
2. score: compare human labels with judge verdicts and record agreement, the
   false-PASS rate and Cohen's kappa. The judge is TRUSTED only when
   n >= MIN_ITEMS, agreement >= MIN_AGREEMENT and false-PASS <= MAX_FALSE_PASS.

  python3 scripts/live_evals/calibrate.py sample evidence/live-evals/run-<id> [...] --n 60
  python3 scripts/live_evals/calibrate.py score evidence/live-evals/calibration/<date>-labels.csv evidence/live-evals/run-<id> [...]
"""
from __future__ import annotations

import argparse
import csv
import random
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EVIDENCE_DIR, ROOT, iter_attempts, write_json  # noqa: E402

MIN_ITEMS = 30
MIN_AGREEMENT = 0.80
MAX_FALSE_PASS = 0.05
COLUMNS = ["item_id", "run_id", "skill", "case_id", "attempt", "assertion", "evidence_dir", "human_label", "human_note"]


def judged_items(run_dirs):
    items = []
    for path, verdict in iter_attempts(run_dirs):
        for assertion in verdict.get("assertions", []):
            if assertion.get("judge"):
                items.append({"run_id": verdict["run_id"], "skill": verdict["skill"], "case_id": verdict["case_id"],
                              "attempt": verdict["attempt"], "assertion": assertion["text"],
                              "evidence_dir": rel(path.parent), "judge_verdict": assertion["verdict"],
                              "judge": assertion["judge"]})
    return items


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def key(item) -> tuple:
    return (item["run_id"], item["skill"], item["case_id"], str(item["attempt"]), item["assertion"])


def sample(run_dirs, n: int, seed: int, out: Path) -> int:
    items = judged_items(run_dirs)
    if not items:
        print("No judged assertions found; run judge.py first.", file=sys.stderr)
        return 1
    chosen = random.Random(seed).sample(items, min(n, len(items)))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for i, item in enumerate(chosen, 1):
            row = {k: item.get(k, "") for k in COLUMNS}
            row.update({"item_id": f"C{i:03d}", "human_label": "", "human_note": ""})
            writer.writerow(row)
    print(f"Wrote {len(chosen)} items to {out}. Open each evidence_dir (final.redacted.txt, diff.redacted.patch, "
          "tool_calls.json), set human_label to PASS or FAIL without looking at the judge verdict, then run score.")
    return 0


def metrics(pairs) -> dict:
    """pairs: list of (human PASS/FAIL, judge PASS/FAIL/UNCLEAR). UNCLEAR counts as disagreement (and as FAIL for kappa)."""
    n = len(pairs)
    if not n:
        return {"n": 0, "agreement": None, "false_pass_rate": None, "kappa": None}
    agree = sum(h == j for h, j in pairs)
    human_fail = [j for h, j in pairs if h == "FAIL"]
    false_pass = sum(j == "PASS" for j in human_fail)
    jb = ["PASS" if j == "PASS" else "FAIL" for _, j in pairs]
    hb = [h for h, _ in pairs]
    po = sum(a == b for a, b in zip(hb, jb)) / n
    ph, pj = hb.count("PASS") / n, jb.count("PASS") / n
    pe = ph * pj + (1 - ph) * (1 - pj)
    kappa = 1.0 if pe == 1 and po == 1 else (0.0 if pe == 1 else (po - pe) / (1 - pe))
    return {"n": n, "agreement": round(agree / n, 4),
            "false_pass_rate": round(false_pass / len(human_fail), 4) if human_fail else 0.0,
            "kappa": round(kappa, 4), "unclear": sum(j == "UNCLEAR" for _, j in pairs),
            "human_fail": len(human_fail)}


def score(labels: Path, run_dirs, out: Path | None) -> int:
    judged = {key(i): i for i in judged_items(run_dirs)}
    pairs, missing, judges = [], [], set()
    with labels.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            label = (row.get("human_label") or "").strip().upper()
            if label not in ("PASS", "FAIL"):
                continue
            item = judged.get(key(row))
            if not item:
                missing.append(row["item_id"])
                continue
            pairs.append((label, item["judge_verdict"]))
            judges.add((item["judge"].get("model"), item["judge"].get("rubric_hash")))
    result = metrics(pairs)
    reasons = []
    if result["n"] < MIN_ITEMS:
        reasons.append(f"only {result['n']} labeled items (need {MIN_ITEMS})")
    if result["agreement"] is not None and result["agreement"] < MIN_AGREEMENT:
        reasons.append(f"agreement {result['agreement']} < {MIN_AGREEMENT}")
    if result["false_pass_rate"] is not None and result["false_pass_rate"] > MAX_FALSE_PASS:
        reasons.append(f"false-PASS rate {result['false_pass_rate']} > {MAX_FALSE_PASS}")
    if len(judges) > 1:
        reasons.append("labels mix several judge models or rubrics; calibrate one judge configuration at a time")
    model, rubric = next(iter(judges)) if len(judges) == 1 else (None, None)
    record = {"date": date.today().isoformat(), "labels_file": rel(labels), "judge_model": model,
              "rubric_hash": rubric, **result, "thresholds": {"min_items": MIN_ITEMS, "min_agreement": MIN_AGREEMENT,
                                                               "max_false_pass": MAX_FALSE_PASS},
              "trusted": not reasons and result["n"] > 0, "reasons_not_trusted": reasons,
              "unmatched_label_rows": missing}
    out = out or labels.with_name(labels.stem.replace("-labels", "") + "-calibration.json")
    write_json(out, record)
    print(f"Calibration: n={result['n']} agreement={result['agreement']} false_pass={result['false_pass_rate']} "
          f"kappa={result['kappa']} -> {'TRUSTED' if record['trusted'] else 'NOT TRUSTED'}")
    for reason in reasons:
        print("  -", reason)
    print(f"Wrote {out}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Calibrate the LLM judge against human labels.")
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("sample")
    s.add_argument("run_dirs", nargs="+")
    s.add_argument("--n", type=int, default=60)
    s.add_argument("--seed", type=int, default=7)
    s.add_argument("--out", default=str(EVIDENCE_DIR / "calibration" / f"{date.today().isoformat()}-labels.csv"))
    c = sub.add_parser("score")
    c.add_argument("labels")
    c.add_argument("run_dirs", nargs="+")
    c.add_argument("--out")
    args = parser.parse_args(argv)
    if args.command == "sample":
        return sample(args.run_dirs, args.n, args.seed, Path(args.out))
    return score(Path(args.labels), args.run_dirs, Path(args.out) if args.out else None)


if __name__ == "__main__":
    raise SystemExit(main())
