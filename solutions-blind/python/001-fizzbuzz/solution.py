def fizz_buzz(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def fizz_buzz_range(end: int = 15) -> str:
    return " ".join(fizz_buzz(i) for i in range(1, end + 1))
