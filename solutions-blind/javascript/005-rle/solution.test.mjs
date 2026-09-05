import test from "node:test";
import assert from "node:assert/strict";
import { encode, decode } from "./solution.mjs";

test("encode", () => {
  assert.equal(encode(""), "");
  assert.equal(encode("a"), "a1");
  assert.equal(encode("aaabbc"), "a3b2c1");
  assert.equal(encode("WWWWWWWWWWWWBWWWWWWWWWWWWBBB"), "W12B1W12B3");
});

test("decode", () => {
  assert.equal(decode("a3b2c1"), "aaabbc");
  assert.equal(decode("W12B1W12B3"), "WWWWWWWWWWWWBWWWWWWWWWWWWBBB");
  assert.throws(() => decode("a"));
  assert.throws(() => decode("a0"));
});

test("round-trip", () => {
  for (const s of ["aaabbc", "Hello", ""]) {
    assert.equal(decode(encode(s)), s);
  }
});
