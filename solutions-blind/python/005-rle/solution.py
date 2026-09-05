def encode(s: str) -> str:
    if not s:
        return ""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        j = i + 1
        while j < len(s) and s[j] == ch:
            j += 1
        out.append(ch + str(j - i))
        i = j
    return "".join(out)


def decode(s: str) -> str:
    if s == "":
        return ""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        i += 1
        if i >= len(s) or not s[i].isdigit():
            raise ValueError("missing count after character")
        start = i
        while i < len(s) and s[i].isdigit():
            i += 1
        n = int(s[start:i])
        if n < 1:
            raise ValueError("count must be at least 1")
        out.append(ch * n)
    return "".join(out)
