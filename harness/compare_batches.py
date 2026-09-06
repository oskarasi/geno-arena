#!/usr/bin/env python3
"""Diff two geno-arena scoreboard JSON files (default: batch-001 vs batch-002)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANES = ("geno", "python", "javascript")


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "results" not in data or "scoreboard" not in data:
        raise SystemExit(f"not a scoreboard JSON: {path}")
    return data


def index_results(results: list[dict]) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    for r in results:
        out[(r["task_id"], r["language"])] = r
    return out


def fmt_bool(v: bool) -> str:
    return "ok" if v else "FAIL"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compare two geno-arena batch scoreboards (build_ok / tests_ok / seconds)"
    )
    ap.add_argument(
        "--a",
        default=str(ROOT / "results" / "batch-001.json"),
        help="first scoreboard JSON (default: results/batch-001.json)",
    )
    ap.add_argument(
        "--b",
        default=str(ROOT / "results" / "batch-002.json"),
        help="second scoreboard JSON (default: results/batch-002.json)",
    )
    ap.add_argument(
        "--seconds-epsilon",
        type=float,
        default=0.05,
        help="ignore wall-time deltas smaller than this (default: 0.05s)",
    )
    args = ap.parse_args()

    path_a = Path(args.a)
    path_b = Path(args.b)
    if not path_a.is_absolute():
        path_a = (ROOT / path_a).resolve()
    if not path_b.is_absolute():
        path_b = (ROOT / path_b).resolve()

    a = load(path_a)
    b = load(path_b)
    meta_a = a.get("meta") or {}
    meta_b = b.get("meta") or {}
    id_a = meta_a.get("batch_id", path_a.stem)
    id_b = meta_b.get("batch_id", path_b.stem)

    print(f"Comparing {id_a} ({path_a.name}) vs {id_b} ({path_b.name})")
    print(f"  A note: {meta_a.get('agent_note', '?')}")
    print(f"  B note: {meta_b.get('agent_note', '?')}")
    print()

    print("## Scoreboard")
    print()
    print("| Language | A build | A tests | B build | B tests | delta tests |")
    print("|---|---:|---:|---:|---:|---:|")
    board_a = a["scoreboard"]
    board_b = b["scoreboard"]
    for lang in LANES:
        ba = board_a.get(lang, {})
        bb = board_b.get(lang, {})
        ta = ba.get("tests_ok", 0)
        tb = bb.get("tests_ok", 0)
        delta = tb - ta
        sign = f"+{delta}" if delta > 0 else str(delta)
        print(
            f"| {lang} | {ba.get('build_ok', 0)}/{ba.get('total', 0)} | "
            f"{ta}/{ba.get('total', 0)} | {bb.get('build_ok', 0)}/{bb.get('total', 0)} | "
            f"{tb}/{bb.get('total', 0)} | {sign} |"
        )
    print()

    idx_a = index_results(a["results"])
    idx_b = index_results(b["results"])
    keys = sorted(set(idx_a) | set(idx_b))

    regressions: list[str] = []
    improvements: list[str] = []
    missing: list[str] = []
    time_deltas: list[tuple[str, str, float, float, float]] = []

    for task_id, lang in keys:
        ra = idx_a.get((task_id, lang))
        rb = idx_b.get((task_id, lang))
        label = f"{task_id}/{lang}"
        if ra is None:
            missing.append(f"  only in B: {label}")
            continue
        if rb is None:
            missing.append(f"  only in A: {label}")
            continue

        a_ok = bool(ra.get("tests_ok"))
        b_ok = bool(rb.get("tests_ok"))
        a_build = bool(ra.get("build_ok"))
        b_build = bool(rb.get("build_ok"))
        if a_ok and not b_ok:
            regressions.append(
                f"  REGRESS {label}: tests {fmt_bool(a_ok)} → {fmt_bool(b_ok)}"
                + (f" ({rb.get('error')})" if rb.get("error") else "")
            )
        elif (not a_ok) and b_ok:
            improvements.append(f"  IMPROVE {label}: tests {fmt_bool(a_ok)} → {fmt_bool(b_ok)}")
        elif a_build != b_build:
            regressions.append(
                f"  BUILD   {label}: build {fmt_bool(a_build)} → {fmt_bool(b_build)}"
            )

        sa = float(ra.get("seconds") or 0.0)
        sb = float(rb.get("seconds") or 0.0)
        delta_s = sb - sa
        if abs(delta_s) >= args.seconds_epsilon:
            time_deltas.append((task_id, lang, sa, sb, delta_s))

    print("## Pass/fail deltas")
    print()
    if not regressions and not improvements and not missing:
        print("No build/tests differences across tasks × languages.")
    else:
        for line in regressions:
            print(line)
        for line in improvements:
            print(line)
        for line in missing:
            print(line)
    print()

    print(f"## Wall time deltas (|Δ| ≥ {args.seconds_epsilon}s)")
    print()
    if not time_deltas:
        print("None.")
    else:
        print("| Task | Language | A s | B s | Δ s |")
        print("|---|---|---:|---:|---:|")
        for task_id, lang, sa, sb, delta_s in sorted(
            time_deltas, key=lambda t: abs(t[4]), reverse=True
        ):
            print(f"| {task_id} | {lang} | {sa:.4f} | {sb:.4f} | {delta_s:+.4f} |")
    print()
    return 1 if regressions else 0


if __name__ == "__main__":
    raise SystemExit(main())
