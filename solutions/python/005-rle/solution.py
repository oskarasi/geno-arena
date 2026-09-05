"""Run-length encoding / decoding."""

def encode(s: str) -> str:
    if not s:
        return ""
    result: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        j = i + 1
        while j < len(s) and s[j] == ch:
            j += 1
        result.append(ch + str(j - i))
        i = j
    return "".join(result)


def decode(s: str) -> str:
    if not s:
        return ""
    result: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if not ch.isalnum():
            raise ValueError("expected alphanumeric character")
        i += 1
        if i >= len(s) or not s[i].isdigit():
            raise ValueError("missing count after character")
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        n = int(count_str)
        if n < 1:
            raise ValueError("count must be at least 1")
        result.append(ch * n)
    return "".join(result)
