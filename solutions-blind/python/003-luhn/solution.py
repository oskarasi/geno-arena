def luhn_valid(digits: str) -> bool:
    s = "".join(ch for ch in digits if ch not in " -")
    if not s or not s.isdigit():
        return False
    total = 0
    alt = False
    for ch in reversed(s):
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0
