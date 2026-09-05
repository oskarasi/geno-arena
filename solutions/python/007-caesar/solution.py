"""Caesar cipher encrypt / decrypt."""

def _norm(n: int) -> int:
    m = n % 26
    return m + 26 if m < 0 else m


def _shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        return chr(ord("a") + _norm(ord(ch) - ord("a") + shift))
    if "A" <= ch <= "Z":
        return chr(ord("A") + _norm(ord(ch) - ord("A") + shift))
    return ch


def encrypt(text: str, shift: int) -> str:
    return "".join(_shift_char(ch, shift) for ch in text)


def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)
