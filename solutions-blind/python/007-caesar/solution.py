def _shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + (ord(ch) - base + shift) % 26)
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + (ord(ch) - base + shift) % 26)
    return ch


def encrypt(text: str, shift: int) -> str:
    return "".join(_shift_char(ch, shift) for ch in text)


def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)
