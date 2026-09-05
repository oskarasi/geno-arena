"""Roman numeral conversion for 1..3999."""

_VALUES = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
_SYMBOLS = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
_MAP = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def to_roman(n: int) -> str:
    if n < 1 or n > 3999:
        raise ValueError("n must be between 1 and 3999")
    remaining = n
    parts: list[str] = []
    for value, symbol in zip(_VALUES, _SYMBOLS):
        while remaining >= value:
            parts.append(symbol)
            remaining -= value
    return "".join(parts)


def from_roman(s: str) -> int:
    if not s:
        raise ValueError("empty roman numeral")
    upper = s.upper()
    total = 0
    i = 0
    while i < len(upper):
        val = _MAP.get(upper[i])
        if val is None:
            raise ValueError("invalid roman numeral")
        if i + 1 < len(upper):
            nxt = _MAP.get(upper[i + 1])
            if nxt is None:
                raise ValueError("invalid roman numeral")
            if nxt > val:
                total += nxt - val
                i += 2
                continue
        total += val
        i += 1
    if total < 1 or total > 3999:
        raise ValueError("n must be between 1 and 3999")
    return total
