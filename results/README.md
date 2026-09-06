# results/

Scoreboard outputs from `harness/score.py`. Each batch writes a JSON payload and a
human-readable Markdown table.

## Files

| File | Role |
|------|------|
| `batch-001.json` | Machine-readable scoreboard for **batch-001** (`solutions/`, manual agent) |
| `batch-001.md` | Markdown scoreboard + per-task rows for batch-001 |
| `batch-002.json` | Machine-readable scoreboard for **batch-002** (`solutions-blind/`, agent-blind) |
| `batch-002.md` | Markdown scoreboard + per-task rows for batch-002 |
| `*-meta.json` | Optional; written by `harness/blind_batch.py` (model, timestamp, `"blind"` note). Merged into the next `score.py` run for that `--batch-id`. |

## JSON shape

```json
{
  "meta": {
    "batch_id": "batch-001",
    "generated_at": "<ISO-8601 UTC>",
    "agent_note": "...",
    "geno_bin": "/workspace/geno-venv/bin/geno",
    "geno_version_hint": "0.4.3",
    "js_lane_note": "...",
    "model_family": "...",
    "solutions_root": "..."
  },
  "scoreboard": {
    "geno": { "total": 8, "build_ok": 8, "tests_ok": 8 },
    "python": { "...": "..." },
    "javascript": { "...": "..." }
  },
  "results": [
    {
      "task_id": "001-fizzbuzz",
      "language": "geno",
      "build_ok": true,
      "tests_ok": true,
      "seconds": 0.6,
      "error": null
    }
  ]
}
```

## Regenerating

```bash
# from repo root
make score          # → batch-001.*
make score-blind    # → batch-002.*
make compare        # print build/tests diffs between the two
```

Do not hand-edit the JSON/Markdown; re-run the scorer so `generated_at` and wall times stay honest.
