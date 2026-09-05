from solution import encode, decode

assert encode("") == ""
assert encode("a") == "a1"
assert encode("aaabbc") == "a3b2c1"
assert encode("WWWWWWWWWWWWBWWWWWWWWWWWWBBB") == "W12B1W12B3"
assert decode("a3b2c1") == "aaabbc"
assert decode("W12B1W12B3") == "WWWWWWWWWWWWBWWWWWWWWWWWWBBB"
try:
    decode("a")
    raise AssertionError
except ValueError:
    pass
try:
    decode("a0")
    raise AssertionError
except ValueError:
    pass
for s in ["aaabbc", "Hello", ""]:
    assert decode(encode(s)) == s
print("ok")
