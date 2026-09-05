const VALUES = [
  [1000, "M"], [900, "CM"], [500, "D"], [400, "CD"],
  [100, "C"], [90, "XC"], [50, "L"], [40, "XL"],
  [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"],
];
const ROMAN_VAL = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };

export function to_roman(n) {
  if (!Number.isInteger(n) || n < 1 || n > 3999) {
    throw new Error("n must be between 1 and 3999");
  }
  let remaining = n;
  let result = "";
  for (const [value, symbol] of VALUES) {
    while (remaining >= value) {
      result += symbol;
      remaining -= value;
    }
  }
  return result;
}

export function from_roman(s) {
  if (!s) throw new Error("empty roman numeral");
  const upper = s.toUpperCase();
  let total = 0;
  let i = 0;
  while (i < upper.length) {
    const ch = upper[i];
    if (!(ch in ROMAN_VAL)) throw new Error("invalid roman numeral");
    const val = ROMAN_VAL[ch];
    if (i + 1 < upper.length) {
      const next = upper[i + 1];
      if (!(next in ROMAN_VAL)) throw new Error("invalid roman numeral");
      const nextVal = ROMAN_VAL[next];
      if (nextVal > val) {
        total += nextVal - val;
        i += 2;
        continue;
      }
    }
    total += val;
    i += 1;
  }
  if (total < 1 || total > 3999) throw new Error("invalid roman numeral");
  return total;
}
