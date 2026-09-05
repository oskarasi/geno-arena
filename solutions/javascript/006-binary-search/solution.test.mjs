import test from "node:test";
import assert from "node:assert/strict";
import { binarySearch } from "./solution.mjs";

test("binary search", () => {
  const xs = [1, 3, 5, 7, 9];
  assert.equal(binarySearch(xs, 5), 2);
  assert.equal(binarySearch(xs, 1), 0);
  assert.equal(binarySearch(xs, 9), 4);
  assert.equal(binarySearch(xs, 4), -1);
  assert.equal(binarySearch([], 1), -1);
  assert.equal(binarySearch([2], 2), 0);
});
