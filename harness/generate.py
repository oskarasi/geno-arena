#!/usr/bin/env python3
"""Blind LLM generation via Groq (OpenAI-compatible Chat Completions API)."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_MD = ROOT / "AGENTS.md"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "llama-3.3-70b-versatile"

LANGUAGES = ("geno", "python", "javascript")

EXPECTED_FILES: dict[str, tuple[str, ...]] = {
    "geno": ("Main.geno", "geno.toml"),
    "python": ("solution.py", "solution_test.py"),
    "javascript": ("solution.mjs", "solution.test.mjs"),
}


def _load_agents_md() -> str:
    if AGENTS_MD.exists():
        return AGENTS_MD.read_text(encoding="utf-8")
    return (
        "Geno pitfalls: examples on every non-@untested function; named args for "
        "arity >= 3; end if/while/match/func; no top-level let; capability-free main()."
    )


def _read_prompt_file(name: str) -> str:
    path = PROMPTS_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _system_prompt(language: str) -> str:
    files = ", ".join(EXPECTED_FILES[language])
    common = _read_prompt_file("common.txt").format(files=files)
    if not common:
        common = (
            "Return ONLY solution files as JSON map or fenced blocks.\n"
            f"Emit exactly these files: {files}.\n"
        )
    lang_extra = _read_prompt_file(f"{language}.txt")
    parts = [common, "", lang_extra]
    if language == "geno":
        parts += ["", "=== AGENTS.md (Geno pitfalls) ===", _load_agents_md(), "=== end AGENTS.md ==="]
    return "\n".join(p for p in parts if p is not None).strip() + "\n"


def _user_prompt(prompt: str, language: str) -> str:
    files = ", ".join(EXPECTED_FILES[language])
    return (
        f"Task prompt:\n{prompt.strip()}\n\n"
        f"Implement this in {language}. Emit files: {files}.\n"
    )

_FENCE_RE = re.compile(
    r"```([^\n`]*)\n(.*?)```",
    re.DOTALL,
)


def _normalize_name(name: str, language: str) -> str | None:
    name = name.strip().lstrip("./").replace("\\", "/")
    base = Path(name).name
    expected = EXPECTED_FILES[language]
    for exp in expected:
        if name == exp or base == exp:
            return exp
    aliases = {
        "geno": {"main.geno": "Main.geno", "lib.geno": "Main.geno"},
        "python": {
            "test_solution.py": "solution_test.py",
            "tests.py": "solution_test.py",
            "main.py": "solution.py",
        },
        "javascript": {
            "solution.js": "solution.mjs",
            "solution.test.js": "solution.test.mjs",
            "test.mjs": "solution.test.mjs",
            "solution_test.mjs": "solution.test.mjs",
        },
    }
    low = base.lower()
    return aliases.get(language, {}).get(low)


def _parse_json_map(text: str, language: str) -> dict[str, str] | None:
    text = text.strip()
    m = re.match(r"^```(?:json)?\s*\n(.*?)```\s*$", text, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    blob = text[start : end + 1]
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    out: dict[str, str] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            continue
        norm = _normalize_name(k, language)
        if norm:
            out[norm] = v
    return out or None


def _parse_fenced(text: str, language: str) -> dict[str, str]:
    out: dict[str, str] = {}
    header_re = re.compile(
        r"(?:^|\n)(?:#{1,3}\s*|File:\s*|Filename:\s*)([\w./-]+\.(?:geno|toml|py|mjs|js))\s*\n",
        re.IGNORECASE,
    )
    for m in _FENCE_RE.finditer(text):
        info = (m.group(1) or "").strip()
        body = m.group(2)
        fname = None
        if info:
            for tok in reversed(info.split()):
                cand = _normalize_name(tok, language)
                if cand:
                    fname = cand
                    break
            if fname is None:
                cand = _normalize_name(info, language)
                if cand:
                    fname = cand
        if fname is None:
            preceding = text[: m.start()]
            hm = None
            for hm in header_re.finditer(preceding):
                pass
            if hm is not None and hm.end() >= len(preceding) - 2:
                fname = _normalize_name(hm.group(1), language)
        if fname is None:
            tag = info.split()[0].lower() if info else ""
            tag_map = {
                "geno": "Main.geno" if language == "geno" else None,
                "toml": "geno.toml" if language == "geno" else None,
                "python": "solution.py" if language == "python" else None,
                "py": "solution.py" if language == "python" else None,
                "javascript": "solution.mjs" if language == "javascript" else None,
                "js": "solution.mjs" if language == "javascript" else None,
            }
            fname = tag_map.get(tag)
        if fname:
            contents = body if body.endswith('\n') else body + '\n'
            out[fname] = contents
    return out


def parse_model_output(text: str, language: str) -> dict[str, str]:
    """Parse model output into filename -> contents."""
    if language not in EXPECTED_FILES:
        raise ValueError(f"unsupported language: {language}")
    files = _parse_json_map(text, language)
    if not files:
        files = _parse_fenced(text, language)
    if not files:
        primary = EXPECTED_FILES[language][0]
        stripped = text.strip()
        if stripped and "```" not in stripped:
            files = {primary: stripped + ("" if stripped.endswith("\n") else "\n")}
    cleaned: dict[str, str] = {}
    for name, contents in (files or {}).items():
        if not contents.endswith("\n"):
            contents += "\n"
        cleaned[name] = contents
    return cleaned


def _snip_err(text: str, limit: int = 300) -> str:
    text = text.strip()
    text = re.sub(r"gsk_[A-Za-z0-9]+", "[REDACTED]", text)
    text = re.sub(r"Bearer\s+\S+", "Bearer [REDACTED]", text)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _chat_completion(*, api_key: str, model: str, system: str, user: str) -> str:
    url = f"{GROQ_BASE_URL.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "geno-arena-harness/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Groq HTTP {exc.code}: {_snip_err(err_body)}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Groq network error: {exc.reason}") from None
    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"unexpected Groq response shape: {type(body).__name__}") from exc


def generate(prompt: str, language: str, *, model: str = DEFAULT_MODEL) -> dict[str, str]:
    """Generate solution files for one task x language via Groq.

    Returns filename -> contents. Raises RuntimeError if GROQ_API_KEY is missing
    or the API call / parse fails badly. Does not print the API key.
    """
    language = language.lower().strip()
    if language not in EXPECTED_FILES:
        raise ValueError(f"unsupported language: {language!r}; expected one of {LANGUAGES}")

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set; export it before running blind generation "
            "(no API call was made)."
        )

    system = _system_prompt(language)
    user = _user_prompt(prompt, language)
    raw = _chat_completion(api_key=api_key, model=model, system=system, user=user)
    files = parse_model_output(raw, language)
    if not files:
        raise RuntimeError(
            f"model returned no parseable files for {language}; "
            f"expected {list(EXPECTED_FILES[language])}"
        )
    return files


def dry_call(model: str = DEFAULT_MODEL) -> str:
    """Tiny connectivity check: one short completion. Returns model text."""
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")
    return _chat_completion(
        api_key=api_key,
        model=model,
        system="Reply with exactly: pong",
        user="ping",
    )


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Groq generate helper / dry-call")
    ap.add_argument("--dry-call", action="store_true", help="one tiny completion")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--language", choices=LANGUAGES)
    ap.add_argument("--prompt", default="")
    args = ap.parse_args()
    if args.dry_call:
        print(dry_call(args.model))
    elif args.language and args.prompt:
        out = generate(args.prompt, args.language, model=args.model)
        for name, contents in out.items():
            print(f"=== {name} ({len(contents)} bytes) ===")
            print(contents)
    else:
        ap.error("use --dry-call or --language + --prompt")

