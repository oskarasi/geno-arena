_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]
_ROMAN_VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def to_roman(n: int) -> str:
    if not isinstance(n, int) or n < 1 or n > 3999:
        raise ValueError("n must be between 1 and 3999")
    remaining = n
    parts = []
    for value, symbol in _VALUES:
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
        ch = upper[i]
        if ch not in _ROMAN_VAL:
            raise ValueError("invalid roman numeral")
        val = _ROMAN_VAL[ch]
        if i + 1 < len(upper):
            nxt = upper[i + 1]
            if nxt not in _ROMAN_VAL:
                raise ValueError("invalid roman numeral")
            next_val = _ROMAN_VAL[nxt]
            if next_val > val:
                total += next_val - val
                i += 2
                continue
        total += val
        i += 1
    if total < 1 or total > 3999:
        raise ValueError("invalid roman numeral")
    return total
