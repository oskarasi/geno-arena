from solution import fizz_buzz, fizz_buzz_range

assert fizz_buzz(1) == "1"
assert fizz_buzz(3) == "Fizz"
assert fizz_buzz(5) == "Buzz"
assert fizz_buzz(15) == "FizzBuzz"
assert fizz_buzz(7) == "7"
assert fizz_buzz(30) == "FizzBuzz"
r = fizz_buzz_range(15)
assert r.startswith("1 2 Fizz 4 Buzz")
assert r.endswith("FizzBuzz")
print("ok")
