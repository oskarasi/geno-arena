"""Anagram checker ignoring case and spaces."""

def _signature(text: str) -> str:
    normalized = "".join(ch for ch in text.lower() if ch != " ")
    return "".join(sorted(normalized))


def is_anagram(a: str, b: str) -> bool:
    return _signature(a) == _signature(b)
