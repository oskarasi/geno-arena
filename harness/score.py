#!/usr/bin/env python3
"""Score geno-arena solutions across geno / python / javascript lanes."""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENO_BIN = Path("/workspace/geno-venv/bin/geno")
TASKS_DIR = ROOT / "tasks"
SOLUTIONS = ROOT / "solutions"
RESULTS = ROOT / "results"

LANES = ("geno", "python", "javascript")


@dataclass
class LaneResult:
    task_id: str
    language: str
    build_ok: bool
    tests_ok: bool
    seconds: float
    error: str | None = None


def _run(cmd: list[str], cwd: Path | None = None, timeout: float = 120.0) -> tuple[int, str, float]:
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.perf_counter() - t0
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip(), elapsed
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - t0
        return 124, f"timeout after {timeout}s: {exc}", elapsed
    except FileNotFoundError as exc:
        elapsed = time.perf_counter() - t0
        return 127, str(exc), elapsed


def _snip(text: str, limit: int = 400) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def score_geno(task_id: str) -> LaneResult:
    path = SOLUTIONS / "geno" / task_id
    if not path.exists():
        return LaneResult(task_id, "geno", False, False, 0.0, "missing solution dir")
    geno = str(GENO_BIN if GENO_BIN.exists() else "geno")

    # build/check: geno test implies parse+typecheck; also try geno run
    code_t, out_t, sec_t = _run([geno, "test", str(path)], cwd=path)
    main = path / "Main.geno"
    code_r, out_r, sec_r = _run([geno, "run", str(main)], cwd=path)
    seconds = round(sec_t + sec_r, 4)
    build_ok = code_t != 127 and "Parser" not in out_t and "CompileError" not in out_r
    # Prefer explicit: tests pass if geno test exit 0; build if test+run both 0 or run returns output
    tests_ok = code_t == 0
    build_ok = code_t == 0 and code_r == 0
    err = None
    if not build_ok or not tests_ok:
        err = _snip(out_t if code_t != 0 else out_r)
    return LaneResult(task_id, "geno", build_ok, tests_ok, seconds, err)


def score_python(task_id: str) -> LaneResult:
    path = SOLUTIONS / "python" / task_id
    test_py = path / "solution_test.py"
    sol = path / "solution.py"
    if not sol.exists():
        return LaneResult(task_id, "python", False, False, 0.0, "missing solution.py")
    # syntax/build
    code_b, out_b, sec_b = _run(["python3", "-m", "py_compile", str(sol), str(test_py)], cwd=path)
    if code_b != 0:
        return LaneResult(task_id, "python", False, False, round(sec_b, 4), _snip(out_b))
    code_t, out_t, sec_t = _run(["python3", str(test_py)], cwd=path)
    seconds = round(sec_b + sec_t, 4)
    tests_ok = code_t == 0
    err = None if tests_ok else _snip(out_t)
    return LaneResult(task_id, "python", True, tests_ok, seconds, err)


def score_javascript(task_id: str) -> LaneResult:
    path = SOLUTIONS / "javascript" / task_id
    sol = path / "solution.mjs"
    test = path / "solution.test.mjs"
    if not sol.exists():
        return LaneResult(task_id, "javascript", False, False, 0.0, "missing solution.mjs")
    # syntax check via node --check
    code_b, out_b, sec_b = _run(["node", "--check", str(sol)], cwd=path)
    if code_b != 0:
        return LaneResult(task_id, "javascript", False, False, round(sec_b, 4), _snip(out_b))
    code_t, out_t, sec_t = _run(["node", "--test", str(test)], cwd=path)
    seconds = round(sec_b + sec_t, 4)
    tests_ok = code_t == 0
    err = None if tests_ok else _snip(out_t)
    return LaneResult(task_id, "javascript", True, tests_ok, seconds, err)


SCORERS = {
    "geno": score_geno,
    "python": score_python,
    "javascript": score_javascript,
}


def list_tasks() -> list[str]:
    return sorted(p.stem for p in TASKS_DIR.glob("*.json"))


def scoreboard(results: list[LaneResult]) -> dict[str, dict[str, int]]:
    board: dict[str, dict[str, int]] = {}
    for lang in LANES:
        lane = [r for r in results if r.language == lang]
        board[lang] = {
            "total": len(lane),
            "build_ok": sum(1 for r in lane if r.build_ok),
            "tests_ok": sum(1 for r in lane if r.tests_ok),
        }
    return board


def render_md(batch_id: str, results: list[LaneResult], board: dict, meta: dict) -> str:
    lines = [
        f"# {batch_id}",
        "",
        f"- Generated: {meta['generated_at']}",
        f"- Agent note: {meta['agent_note']}",
        f"- Geno binary: `{meta['geno_bin']}`",
        f"- JS lane: `{meta['js_lane_note']}`",
        "",
        "## Scoreboard (tests_ok / total)",
        "",
        "| Language | build_ok | tests_ok | total |",
        "|---|---:|---:|---:|",
    ]
    for lang in LANES:
        b = board[lang]
        lines.append(f"| {lang} | {b['build_ok']} | {b['tests_ok']} | {b['total']} |")
    lines += ["", "## Per-task results", "", "| Task | Language | build_ok | tests_ok | seconds | error |",
              "|---|---|---|---|---:|---|"]
    for r in results:
        err = (r.error or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {r.task_id} | {r.language} | {r.build_ok} | {r.tests_ok} | {r.seconds:.4f} | {err} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    tasks = list_tasks()
    results: list[LaneResult] = []
    for task_id in tasks:
        for lang in LANES:
            results.append(SCORERS[lang](task_id))

    board = scoreboard(results)
    meta = {
        "batch_id": "batch-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_note": "manual agent solutions by Programmer / Cursor agent, single-pass",
        "geno_bin": str(GENO_BIN if GENO_BIN.exists() else "geno"),
        "geno_version_hint": "0.4.3",
        "js_lane_note": "javascript (.mjs + node:test); TypeScript toolchain unavailable in box (npx tsc path error)",
        "model_family": "manual agent solutions by Programmer / Cursor agent, single-pass",
    }
    payload = {
        "meta": meta,
        "scoreboard": board,
        "results": [asdict(r) for r in results],
    }
    json_path = RESULTS / "batch-001.json"
    md_path = RESULTS / "batch-001.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n")
    md_path.write_text(render_md("batch-001", results, board, meta))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    for lang, b in board.items():
        print(f"  {lang}: tests_ok {b['tests_ok']}/{b['total']} (build_ok {b['build_ok']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
