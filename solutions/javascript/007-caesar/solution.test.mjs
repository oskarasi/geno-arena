import test from "node:test";
import assert from "node:assert/strict";
import { encrypt, decrypt } from "./solution.mjs";

test("caesar", () => {
  assert.equal(encrypt("Hello, World!", 3), "Khoor, Zruog!");
  assert.equal(encrypt("abc", 1), "bcd");
  assert.equal(encrypt("XYZ", 3), "ABC");
  assert.equal(encrypt("abc", -1), "zab");
  assert.equal(encrypt("abc", 26), "abc");
  assert.equal(decrypt("Khoor, Zruog!", 3), "Hello, World!");
  for (const [s, k] of [["Hello", 3], ["", 0], ["Zzz!", 25], ["Geno", 7]]) {
    assert.equal(decrypt(encrypt(s, k), k), s);
  }
});
