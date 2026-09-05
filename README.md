# geno-arena

Adversarial LLM **coding arena**: the same language-agnostic task prompts implemented in **Geno**, **Python**, and **JavaScript**, then scored by a shared harness.

**Repo:** https://github.com/oskarasi/geno-arena
**Geno:** [geno-lang](https://github.com/geno-lang/geno) **0.4.3**

## What this proves / does not prove

**Proves (v0):**

- A reproducible layout for multi-language coding tasks with machine-checkable tests.
- That one agent family can implement the same 8 prompts in Geno, Python, and JS such that all lanes pass the harness (see batch-001).
- The harness is ready to score future generated solutions the same way.

**Does not prove:**

- Multi-model or multi-vendor LLM comparison — batch-001 is still manual; Groq blind batch is optional via `harness/blind_batch.py`.
- Batch-001 solutions are **manual agent solutions by Programmer / Cursor agent, single-pass** (same model family / workflow), not blind independent model runs.
- Latency, token cost, or naturalness rankings — only build/test pass-fail and wall seconds.

## Batch-001 scoreboard

| Language   | build_ok | tests_ok | total |
|------------|---------:|---------:|------:|
| geno       |        8 |        8 |     8 |
| python     |        8 |        8 |     8 |
| javascript |        8 |        8 |     8 |

Full detail: results/batch-001.md and results/batch-001.json.
### JavaScript vs TypeScript

The TypeScript compiler was unavailable in the build box. The third lane is plain ES modules with node test runner under solutions/javascript. Swap in TypeScript later by adding a compile step to the harness when the compiler is present.

## Layout

tasks JSON files, solutions for geno python and javascript, harness score script, results batch files, AGENTS.md for Geno pitfalls.

## How to run

From the repo root:

```bash
python3 harness/score.py
# or
harness/run_task.sh
```

Score an alternate solutions tree (e.g. blind batch):

```bash
python3 harness/score.py --solutions-root solutions-blind --batch-id batch-002
```

Requirements: Python 3, Node.js 18+, Geno 0.4.x on PATH or the geno-venv binary.
Blind generation additionally needs `GROQ_API_KEY` (stdlib HTTP only; no extra pip packages).

## How to add a task

Add a task JSON under tasks/, implement matching folders under solutions for each language, then re-run the scorer.

## Blind batch via Groq (batch-002)

Generation uses the OpenAI-compatible Groq Chat Completions API (`harness/generate.py`).
Default model: `llama-3.3-70b-versatile`. Solutions are written under `solutions-blind/`
(never overwrites `solutions/`).

```bash
export GROQ_API_KEY=...
python3 harness/blind_batch.py
python3 harness/score.py --solutions-root solutions-blind --batch-id batch-002
```

If `GROQ_API_KEY` is missing, `blind_batch.py` exits without calling the API.
Optional flags: `--model`, `--languages`, `--tasks`, `--dry-run`.
Connectivity check: `python3 harness/generate.py --dry-call`.

`blind_batch.py` writes `results/batch-002-meta.json` (model, timestamp, note `"blind"`).
The scorer merges that meta when present.

## Tasks (batch-001)

001-fizzbuzz FizzBuzz
002-roman Roman Numerals
003-luhn Luhn Checksum
004-anagram Anagram Checker
005-rle Run-Length Encoding
006-binary-search Binary Search
007-caesar Caesar Cipher
008-levenshtein Levenshtein Distance

## License

Apache-2.0 (see LICENSE).
