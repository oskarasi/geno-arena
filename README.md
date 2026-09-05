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

- Multi-model or multi-vendor LLM comparison — **no external LLM API is called yet**.
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

From the repo root, run the Python scorer in harness/score.py or the thin shell wrapper harness/run_task.sh.

Requirements: Python 3, Node.js 18+, Geno 0.4.x on PATH or the geno-venv binary.

## How to add a task

Add a task JSON under tasks/, implement matching folders under solutions for each language, then re-run the scorer.

## Plugging in an external LLM later

Keep scoring unchanged; only generation is new. Provide a generate(prompt, language) helper that returns filename-to-contents for one language, write those files into the solutions tree, then run the scorer. Log model metadata into the batch JSON.

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
