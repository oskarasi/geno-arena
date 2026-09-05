def is_anagram(a: str, b: str) -> bool:
    def norm(s: str) -> str:
        return "".join(ch.lower() for ch in s if ch != " ")
    return sorted(norm(a)) == sorted(norm(b))
