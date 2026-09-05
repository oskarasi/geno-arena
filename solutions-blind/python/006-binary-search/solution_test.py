from solution import binary_search

xs = [1, 3, 5, 7, 9]
assert binary_search(xs, 5) == 2
assert binary_search(xs, 1) == 0
assert binary_search(xs, 9) == 4
assert binary_search(xs, 4) == -1
assert binary_search([], 1) == -1
assert binary_search([2], 2) == 0
print("ok")
