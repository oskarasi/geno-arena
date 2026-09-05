import test from "node:test";
import assert from "node:assert/strict";
import { isAnagram } from "./solution.mjs";

test("anagrams", () => {
  assert.equal(isAnagram("listen", "silent"), true);
  assert.equal(isAnagram("Listen", "Silent"), true);
  assert.equal(isAnagram("A gentleman", "Elegant man"), true);
  assert.equal(isAnagram("rail safety", "fairy tales"), true);
  assert.equal(isAnagram("hello", "world"), false);
  assert.equal(isAnagram("abc", "ab"), false);
});
