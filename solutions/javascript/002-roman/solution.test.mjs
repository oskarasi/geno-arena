import test from "node:test";
import assert from "node:assert/strict";
import { toRoman, fromRoman } from "./solution.mjs";

test("toRoman / fromRoman", () => {
  assert.equal(toRoman(1), "I");
  assert.equal(toRoman(4), "IV");
  assert.equal(toRoman(9), "IX");
  assert.equal(toRoman(40), "XL");
  assert.equal(toRoman(44), "XLIV");
  assert.equal(toRoman(1994), "MCMXCIV");
  assert.equal(toRoman(3999), "MMMCMXCIX");
  assert.equal(fromRoman("MCMXCIV"), 1994);
  assert.equal(fromRoman("lviii"), 58);
  assert.throws(() => toRoman(0));
  assert.throws(() => fromRoman("ABC"));
  for (const n of [1, 4, 9, 40, 44, 1994, 3999]) {
    assert.equal(fromRoman(toRoman(n)), n);
  }
});
