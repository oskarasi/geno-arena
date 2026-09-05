import test from "node:test";
import assert from "node:assert/strict";
import { luhn_valid } from "./solution.mjs";

test("luhn_valid", () => {
  assert.equal(luhn_valid("79927398713"), true);
  assert.equal(luhn_valid("79927398714"), false);
  assert.equal(luhn_valid("4532015112830366"), true);
  assert.equal(luhn_valid("7992-7398-713"), true);
  assert.equal(luhn_valid(""), false);
  assert.equal(luhn_valid("12a"), false);
  assert.equal(luhn_valid("0"), true);
});
