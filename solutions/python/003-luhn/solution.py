"""Luhn checksum validation."""

def normalize_digits(s: str) -> str:
    return "".join(ch for ch in s if ch not in " -")


def luhn_valid(raw: str) -> bool:
    digits = normalize_digits(raw)
    if not digits or not digits.isdigit():
        return False
    total = 0
    alt = False
    for ch in reversed(digits):
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0
