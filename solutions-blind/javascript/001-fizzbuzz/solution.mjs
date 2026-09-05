export function fizz_buzz(n) {
  if (n % 15 === 0) return "FizzBuzz";
  if (n % 3 === 0) return "Fizz";
  if (n % 5 === 0) return "Buzz";
  return String(n);
}

export function fizz_buzz_range(end = 15) {
  const parts = [];
  for (let i = 1; i <= end; i++) parts.push(fizz_buzz(i));
  return parts.join(" ");
}
