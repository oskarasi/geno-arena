from solution import to_roman, from_roman

assert to_roman(1) == "I"
assert to_roman(4) == "IV"
assert to_roman(9) == "IX"
assert to_roman(40) == "XL"
assert to_roman(44) == "XLIV"
assert to_roman(1994) == "MCMXCIV"
assert to_roman(3999) == "MMMCMXCIX"
assert from_roman("MCMXCIV") == 1994
assert from_roman("lviii") == 58
try:
    to_roman(0)
    raise AssertionError("expected fail")
except ValueError:
    pass
try:
    from_roman("ABC")
    raise AssertionError("expected fail")
except ValueError:
    pass
for n in [1, 4, 9, 40, 44, 1994, 3999]:
    assert from_roman(to_roman(n)) == n
print("ok")
