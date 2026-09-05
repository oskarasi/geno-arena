import test from "node:test";
import assert from "node:assert/strict";
import { binary_search } from "./solution.mjs";

test("binary_search", () => {
  const xs = [1, 3, 5, 7, 9];
  assert.equal(binary_search(xs, 5), 2);
  assert.equal(binary_search(xs, 1), 0);
  assert.equal(binary_search(xs, 9), 4);
  assert.equal(binary_search(xs, 4), -1);
  assert.equal(binary_search([], 1), -1);
  assert.equal(binary_search([2], 2), 0);
});
