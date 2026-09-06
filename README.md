# geno-arena

Adversarial LLM **coding arena**: the same language-agnostic task prompts implemented in
**Geno**, **Python**, and **JavaScript**, then scored by a shared harness.

**Repo:** https://github.com/oskarasi/geno-arena  
**Geno:** [geno-lang](https://github.com/davidiach/geno-lang) **0.4.3**

## What this proves / does not prove

**Proves (v0):**

- A reproducible layout for multi-language coding tasks with machine-checkable tests.
- That one agent family can implement the same 8 prompts in Geno, Python, and JS such that
  all lanes pass the harness (batch-001).
- That a second, agent-blind pass (batch-002) can also clear the harness without consulting
  `solutions/`.
- The harness is ready to score future generated solutions the same way (including Groq).

**Does not prove:**

- Multi-model or multi-vendor LLM comparison — batch-001 is manual; batch-002 is
  agent-blind (Groq path exists but was not used for the checked-in scoreboard).
- Latency, token cost, or naturalness rankings — only build/test pass-fail and wall seconds.

## Batches: batch-001 vs batch-002

| | **batch-001** | **batch-002** |
|---|---|---|
| Solutions tree | `solutions/` | `solutions-blind/` |
| How produced | Manual agent solutions (Programmer / Cursor), single-pass | Agent-blind single-pass from `tasks/` + `AGENTS.md` only (did **not** consult `solutions/`) |
| Scorer | `python3 harness/score.py` (defaults) | `python3 harness/score.py --solutions-root solutions-blind --batch-id batch-002` |
| Results | `results/batch-001.{json,md}` | `results/batch-002.{json,md}` |
| Blind? | No | Yes (agent-blind; Groq API optional — see below) |

### Scoreboard snapshot

**batch-001** (manual):

| Language   | build_ok | tests_ok | total |
|------------|---------:|---------:|------:|
| geno       |        8 |        8 |     8 |
| python     |        8 |        8 |     8 |
| javascript |        8 |        8 |     8 |

**batch-002** (agent-blind):

| Language   | build_ok | tests_ok | total |
|------------|---------:|---------:|------:|
| geno       |        8 |        8 |     8 |
| python     |        8 |        8 |     8 |
| javascript |        8 |        8 |     8 |

Full detail: `results/batch-001.md`, `results/batch-002.md`. Diff: `python3 harness/compare_batches.py`.

### JavaScript vs TypeScript

The TypeScript compiler was unavailable in the build box. The third lane is plain ES modules
with the Node test runner under `solutions/javascript` (and `solutions-blind/javascript`).
Swap in TypeScript later by adding a compile step to the harness when `tsc` is present.

## Two generation paths

### 1. Agent-blind path (what batch-002 used)

An agent implements each task from `tasks/*.json` + `AGENTS.md` (+ optionally
`harness/score.py` for layout expectations) **without reading** `solutions/`.
Write under `solutions-blind/`, then score with `--solutions-root solutions-blind
--batch-id batch-002`.

### 2. Groq path (optional API generation)

`harness/blind_batch.py` calls the OpenAI-compatible Groq Chat Completions API via
`harness/generate.py`. Default model: `llama-3.3-70b-versatile`. Solutions land under
`solutions-blind/` (never overwrites `solutions/`).

```bash
export GROQ_API_KEY=...
python3 harness/blind_batch.py
# or: make blind-generate
python3 harness/score.py --solutions-root solutions-blind --batch-id batch-002
# or: make score-blind
```

If `GROQ_API_KEY` is missing, `blind_batch.py` exits without calling the API.
Optional flags: `--model`, `--languages`, `--tasks`, `--dry-run`.
Connectivity check: `python3 harness/generate.py --dry-call`.

`blind_batch.py` writes `results/<batch-id>-meta.json` (model, timestamp, note `"blind"`).
The scorer merges that meta when present.

## Layout

```text
geno-arena/
  tasks/                 # language-agnostic prompts (JSON)
  solutions/             # batch-001 (manual)
    geno|python|javascript/<task-id>/
  solutions-blind/       # batch-002 (blind / Groq)
  harness/
    score.py             # multi-lane scorer
    compare_batches.py   # diff two result JSON files
    blind_batch.py       # Groq generation driver
    generate.py          # Groq HTTP + prompt assembly
    prompts/             # per-language prompt snippets
    run_task.sh          # thin wrapper → score.py
  results/               # scoreboard JSON + Markdown
  AGENTS.md              # Geno pitfalls for solution authors
  Makefile               # score / score-blind shortcuts
```

## Scoring: `harness/score.py` CLI

Scores every task × {geno, python, javascript} under a solutions root and writes
`results/<batch-id>.{json,md}`.

```bash
# batch-001 (defaults: --solutions-root solutions --batch-id batch-001)
python3 harness/score.py
# or
make score
# or
harness/run_task.sh

# batch-002 / blind tree
python3 harness/score.py --solutions-root solutions-blind --batch-id batch-002
make score-blind

# custom note / model family in meta
python3 harness/score.py \
  --solutions-root solutions-blind \
  --batch-id batch-002 \
  --agent-note "blind" \
  --model-family "llama-3.3-70b-versatile"

# compare two checked-in scoreboards
python3 harness/compare_batches.py
python3 harness/compare_batches.py --a results/batch-001.json --b results/batch-002.json
```

| Flag | Default | Meaning |
|------|---------|---------|
| `--solutions-root` | `solutions` | Root with `geno/`, `python/`, `javascript/` trees |
| `--batch-id` | `batch-001` | Output stem under `results/` |
| `--agent-note` | manual-agent note | Recorded in batch meta (`agent_note`) |
| `--model-family` | same as agent-note | Model family string in meta |

Per lane:

- **geno** — `geno test` + `geno run` (uses `/workspace/geno-venv/bin/geno` when present)
- **python** — `py_compile` + `solution_test.py`
- **javascript** — `node --check` + `node --test`

Requirements: Python 3, Node.js 18+, Geno 0.4.x on `PATH` or the geno-venv binary.
Blind Groq generation additionally needs `GROQ_API_KEY` (stdlib HTTP only; no extra pip packages).

## Makefile targets

```bash
make score          # score solutions/ → results/batch-001.*
make score-blind    # score solutions-blind/ → results/batch-002.*
make compare        # diff batch-001 vs batch-002 scoreboards
make blind-generate # Groq generation into solutions-blind/ (needs GROQ_API_KEY)
```

## How to add a task

1. Add `tasks/<id>.json` with `id`, `title`, and `prompt`.
2. Implement matching folders under `solutions/{geno,python,javascript}/<id>/`.
3. Re-run `make score` (and optionally a blind tree + `make score-blind`).

## Tasks (batch-001 / batch-002)

| ID | Title |
|----|-------|
| 001-fizzbuzz | FizzBuzz |
| 002-roman | Roman Numerals |
| 003-luhn | Luhn Checksum |
| 004-anagram | Anagram Checker |
| 005-rle | Run-Length Encoding |
| 006-binary-search | Binary Search |
| 007-caesar | Caesar Cipher |
| 008-levenshtein | Levenshtein Distance |

## License

Apache-2.0 (see LICENSE).
