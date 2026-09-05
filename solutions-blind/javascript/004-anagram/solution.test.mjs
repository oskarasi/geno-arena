import test from "node:test";
import assert from "node:assert/strict";
import { is_anagram } from "./solution.mjs";

test("is_anagram", () => {
  assert.equal(is_anagram("listen", "silent"), true);
  assert.equal(is_anagram("Listen", "Silent"), true);
  assert.equal(is_anagram("A gentleman", "Elegant man"), true);
  assert.equal(is_anagram("rail safety", "fairy tales"), true);
  assert.equal(is_anagram("hello", "world"), false);
  assert.equal(is_anagram("abc", "ab"), false);
});
