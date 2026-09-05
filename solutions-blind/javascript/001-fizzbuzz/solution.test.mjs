import test from "node:test";
import assert from "node:assert/strict";
import { fizz_buzz, fizz_buzz_range } from "./solution.mjs";

test("fizz_buzz cases", () => {
  assert.equal(fizz_buzz(1), "1");
  assert.equal(fizz_buzz(3), "Fizz");
  assert.equal(fizz_buzz(5), "Buzz");
  assert.equal(fizz_buzz(15), "FizzBuzz");
  assert.equal(fizz_buzz(7), "7");
  assert.equal(fizz_buzz(30), "FizzBuzz");
});

test("range 1..15", () => {
  const r = fizz_buzz_range(15);
  assert.ok(r.startsWith("1 2 Fizz 4 Buzz"));
  assert.ok(r.includes("FizzBuzz"));
});
