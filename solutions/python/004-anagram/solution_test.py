from solution import is_anagram

assert is_anagram("listen", "silent") is True
assert is_anagram("Listen", "Silent") is True
assert is_anagram("A gentleman", "Elegant man") is True
assert is_anagram("rail safety", "fairy tales") is True
assert is_anagram("hello", "world") is False
assert is_anagram("abc", "ab") is False
print("ok")
