#!/usr/bin/env python3
"""Blind batch generation: tasks x {geno,python,javascript} via Groq."""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# Allow running as script: python3 harness/blind_batch.py
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "harness") not in sys.path:
    sys.path.insert(0, str(ROOT / "harness"))

from generate import (  # noqa: E402
    DEFAULT_MODEL,
    EXPECTED_FILES,
    LANGUAGES,
    generate,
)

TASKS_DIR = ROOT / "tasks"
SOLUTIONS_BLIND = ROOT / "solutions-blind"
RESULTS = ROOT / "results"


def list_tasks() -> list[dict]:
    tasks = []
    for path in sorted(TASKS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        task_id = data.get("id") or path.stem
        prompt = data.get("prompt") or ""
        if not prompt:
            raise ValueError(f"task {path.name} missing prompt")
        tasks.append({"id": task_id, "prompt": prompt, "title": data.get("title", task_id)})
    return tasks


def write_files(dest: Path, files: dict[str, str]) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for name, contents in files.items():
        # Only allow basename writes (no path traversal)
        safe = Path(name).name
        target = dest / safe
        if not contents.endswith("\n"):
            contents += "\n"
        target.write_text(contents, encoding="utf-8")
        written.append(safe)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description="Blind Groq batch generation for geno-arena")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--solutions-root", default=str(SOLUTIONS_BLIND))
    ap.add_argument("--batch-id", default="batch-002")
    ap.add_argument("--languages", nargs="+", default=list(LANGUAGES), choices=list(LANGUAGES))
    ap.add_argument("--tasks", nargs="*", default=None, help="optional task id filter")
    ap.add_argument("--dry-run", action="store_true", help="list work without calling API")
    args = ap.parse_args()

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        print("GROQ_API_KEY is not set; no API calls made.", file=sys.stderr)
        print("export GROQ_API_KEY=... then re-run.", file=sys.stderr)
        return 2

    solutions_root = Path(args.solutions_root)
    if not solutions_root.is_absolute():
        solutions_root = ROOT / solutions_root
    tasks = list_tasks()
    if args.tasks:
        want = set(args.tasks)
        tasks = [t for t in tasks if t["id"] in want]
    if not tasks:
        print("no tasks found", file=sys.stderr)
        return 1

    RESULTS.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    run_log = []
    errors = 0

    for task in tasks:
        for lang in args.languages:
            task_id = task["id"]
            dest = solutions_root / lang / task_id
            entry = {"task_id": task_id, "language": lang, "ok": False, "files": [], "error": None}
            print(f"[{lang}] {task_id} ...", flush=True)
            if args.dry_run:
                entry["ok"] = True
                entry["files"] = list(EXPECTED_FILES[lang])
                entry["error"] = "dry-run"
                run_log.append(entry)
                continue
            try:
                files = generate(task["prompt"], lang, model=args.model)
                written = write_files(dest, files)
                missing = [f for f in EXPECTED_FILES[lang] if f not in written]
                entry["files"] = written
                if missing:
                    entry["error"] = f"missing expected files: {missing}"
                    entry["ok"] = False
                    errors += 1
                    print(f"  WARN missing {missing}", flush=True)
                else:
                    entry["ok"] = True
                    print(f"  wrote {written}", flush=True)
            except Exception as exc:  # noqa: BLE001 — record per-cell failure
                errors += 1
                entry["error"] = str(exc)
                # Never leak key material in logs
                if "GROQ_API_KEY" in entry["error"] or "gsk_" in entry["error"]:
                    entry["error"] = "generation failed (details redacted)"
                print(f"  ERROR: {entry['error']}", flush=True)
                traceback.print_exc()
            run_log.append(entry)

    meta = {
        "batch_id": args.batch_id,
        "generated_at": generated_at,
        "model": args.model,
        "note": "blind",
        "agent_note": "blind",
        "solutions_root": str(solutions_root.relative_to(ROOT)) if solutions_root.is_relative_to(ROOT) else str(solutions_root),
        "languages": list(args.languages),
        "task_count": len(tasks),
        "cells": len(run_log),
        "ok_count": sum(1 for e in run_log if e["ok"]),
        "error_count": errors,
        "dry_run": bool(args.dry_run),
    }
    meta_path = RESULTS / f"{args.batch_id}-meta.json"
    payload = {"meta": meta, "run_log": run_log}
    meta_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {meta_path}")
    print(f"ok={meta['ok_count']} errors={errors} cells={meta['cells']}")
    if errors and not args.dry_run:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

