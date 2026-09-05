const VALUES = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1];
const SYMBOLS = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"];
const MAP = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };

export function toRoman(n) {
  if (n < 1 || n > 3999) throw new Error("n must be between 1 and 3999");
  let remaining = n;
  let result = "";
  for (let i = 0; i < VALUES.length; i++) {
    while (remaining >= VALUES[i]) {
      result += SYMBOLS[i];
      remaining -= VALUES[i];
    }
  }
  return result;
}

export function fromRoman(s) {
  if (!s) throw new Error("empty roman numeral");
  const upper = s.toUpperCase();
  let total = 0;
  let i = 0;
  while (i < upper.length) {
    const val = MAP[upper[i]];
    if (val === undefined) throw new Error("invalid roman numeral");
    if (i + 1 < upper.length) {
      const nxt = MAP[upper[i + 1]];
      if (nxt === undefined) throw new Error("invalid roman numeral");
      if (nxt > val) {
        total += nxt - val;
        i += 2;
        continue;
      }
    }
    total += val;
    i += 1;
  }
  if (total < 1 || total > 3999) throw new Error("n must be between 1 and 3999");
  return total;
}
