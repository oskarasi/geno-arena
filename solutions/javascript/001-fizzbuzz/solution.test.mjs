import test from "node:test";
import assert from "node:assert/strict";
import { fizzBuzz, fizzBuzzRange } from "./solution.mjs";

test("fizzBuzz cases", () => {
  assert.equal(fizzBuzz(1), "1");
  assert.equal(fizzBuzz(3), "Fizz");
  assert.equal(fizzBuzz(5), "Buzz");
  assert.equal(fizzBuzz(15), "FizzBuzz");
  assert.equal(fizzBuzz(7), "7");
  assert.equal(fizzBuzz(30), "FizzBuzz");
});

test("range 1..15", () => {
  const r = fizzBuzzRange(15);
  assert.ok(r.startsWith("1 2 Fizz 4 Buzz"));
  assert.ok(r.endsWith("FizzBuzz"));
});
