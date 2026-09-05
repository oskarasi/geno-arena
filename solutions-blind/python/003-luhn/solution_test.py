from solution import luhn_valid

assert luhn_valid("79927398713") is True
assert luhn_valid("79927398714") is False
assert luhn_valid("4532015112830366") is True
assert luhn_valid("7992-7398-713") is True
assert luhn_valid("") is False
assert luhn_valid("12a") is False
assert luhn_valid("0") is True
print("ok")
