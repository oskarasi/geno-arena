from solution import levenshtein

assert levenshtein("", "") == 0
assert levenshtein("a", "") == 1
assert levenshtein("", "abc") == 3
assert levenshtein("kitten", "sitting") == 3
assert levenshtein("cat", "cat") == 0
assert levenshtein("cat", "cats") == 1
assert levenshtein("book", "back") == 2
assert levenshtein("abc", "ac") == 1
print("ok")
