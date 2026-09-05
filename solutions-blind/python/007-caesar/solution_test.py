from solution import encrypt, decrypt

assert encrypt("Hello, World!", 3) == "Khoor, Zruog!"
assert encrypt("abc", 1) == "bcd"
assert encrypt("XYZ", 3) == "ABC"
assert encrypt("abc", -1) == "zab"
assert encrypt("abc", 26) == "abc"
assert decrypt("Khoor, Zruog!", 3) == "Hello, World!"
for s, k in (("Hello", 3), ("Zzz!", 25), ("", 0), ("Geno", 7)):
    assert decrypt(encrypt(s, k), k) == s
print("ok")
