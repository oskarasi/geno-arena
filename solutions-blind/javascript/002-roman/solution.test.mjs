import test from "node:test";
import assert from "node:assert/strict";
import { to_roman, from_roman } from "./solution.mjs";

test("to_roman", () => {
  assert.equal(to_roman(1), "I");
  assert.equal(to_roman(4), "IV");
  assert.equal(to_roman(9), "IX");
  assert.equal(to_roman(40), "XL");
  assert.equal(to_roman(44), "XLIV");
  assert.equal(to_roman(1994), "MCMXCIV");
  assert.equal(to_roman(3999), "MMMCMXCIX");
});

test("from_roman", () => {
  assert.equal(from_roman("MCMXCIV"), 1994);
  assert.equal(from_roman("lviii"), 58);
});

test("errors", () => {
  assert.throws(() => to_roman(0));
  assert.throws(() => to_roman(4000));
  assert.throws(() => from_roman(""));
  assert.throws(() => from_roman("ABC"));
});

test("round-trip", () => {
  for (const n of [1, 4, 9, 40, 44, 58, 1994, 3999]) {
    assert.equal(from_roman(to_roman(n)), n);
  }
});
