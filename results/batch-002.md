# batch-002

- Generated: 2026-09-05T19:45:47.414969+00:00
- Agent note: Programmer/Cursor agent blind single-pass (no external API; Groq signup failed); did not consult solutions/
- Model = "Programmer/Cursor agent blind single-pass (no external API; Groq signup failed)"
- Blind: did not consult solutions/ or batch-001 solution content; implemented from tasks/ + AGENTS.md + harness/score.py only.
- Geno binary: `/workspace/geno-venv/bin/geno`
- JS lane: `javascript (.mjs + node:test); TypeScript toolchain unavailable in box (npx tsc path error)`

## Scoreboard (tests_ok / total)

| Language | build_ok | tests_ok | total |
|---|---:|---:|---:|
| geno | 8 | 8 | 8 |
| python | 8 | 8 | 8 |
| javascript | 8 | 8 | 8 |

## Per-task results

| Task | Language | build_ok | tests_ok | seconds | error |
|---|---|---|---|---:|---|
| 001-fizzbuzz | geno | True | True | 0.6442 |  |
| 001-fizzbuzz | python | True | True | 0.0403 |  |
| 001-fizzbuzz | javascript | True | True | 0.3571 |  |
| 002-roman | geno | True | True | 0.9829 |  |
| 002-roman | python | True | True | 0.0487 |  |
| 002-roman | javascript | True | True | 0.3443 |  |
| 003-luhn | geno | True | True | 0.7062 |  |
| 003-luhn | python | True | True | 0.0408 |  |
| 003-luhn | javascript | True | True | 0.3532 |  |
| 004-anagram | geno | True | True | 0.6948 |  |
| 004-anagram | python | True | True | 0.0463 |  |
| 004-anagram | javascript | True | True | 0.3460 |  |
| 005-rle | geno | True | True | 0.7205 |  |
| 005-rle | python | True | True | 0.0433 |  |
| 005-rle | javascript | True | True | 0.3317 |  |
| 006-binary-search | geno | True | True | 0.6259 |  |
| 006-binary-search | python | True | True | 0.0400 |  |
| 006-binary-search | javascript | True | True | 0.3437 |  |
| 007-caesar | geno | True | True | 0.7494 |  |
| 007-caesar | python | True | True | 0.0404 |  |
| 007-caesar | javascript | True | True | 0.3320 |  |
| 008-levenshtein | geno | True | True | 0.7293 |  |
| 008-levenshtein | python | True | True | 0.0394 |  |
| 008-levenshtein | javascript | True | True | 0.3292 |  |
