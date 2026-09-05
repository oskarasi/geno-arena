import test from "node:test";
import assert from "node:assert/strict";
import { levenshtein } from "./solution.mjs";

test("levenshtein", () => {
  assert.equal(levenshtein("", ""), 0);
  assert.equal(levenshtein("a", ""), 1);
  assert.equal(levenshtein("", "abc"), 3);
  assert.equal(levenshtein("kitten", "sitting"), 3);
  assert.equal(levenshtein("cat", "cat"), 0);
  assert.equal(levenshtein("cat", "cats"), 1);
  assert.equal(levenshtein("book", "back"), 2);
  assert.equal(levenshtein("abc", "ac"), 1);
});
