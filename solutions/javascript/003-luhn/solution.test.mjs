import test from "node:test";
import assert from "node:assert/strict";
import { luhnValid } from "./solution.mjs";

test("luhn", () => {
  assert.equal(luhnValid("79927398713"), true);
  assert.equal(luhnValid("79927398714"), false);
  assert.equal(luhnValid("4532015112830366"), true);
  assert.equal(luhnValid("7992-7398-713"), true);
  assert.equal(luhnValid(""), false);
  assert.equal(luhnValid("12a"), false);
  assert.equal(luhnValid("0"), true);
});
