function isAlnum(c) {
  return /[A-Za-z0-9]/.test(c);
}

export function encode(s) {
  if (!s) return "";
  let result = "";
  let i = 0;
  while (i < s.length) {
    const ch = s[i];
    let j = i + 1;
    while (j < s.length && s[j] === ch) j++;
    result += ch + String(j - i);
    i = j;
  }
  return result;
}

export function decode(s) {
  if (!s) return "";
  let result = "";
  let i = 0;
  while (i < s.length) {
    const ch = s[i];
    if (!isAlnum(ch)) throw new Error("expected alphanumeric character");
    i++;
    if (i >= s.length || !/\d/.test(s[i])) throw new Error("missing count after character");
    let countStr = "";
    while (i < s.length && /\d/.test(s[i])) {
      countStr += s[i];
      i++;
    }
    const n = Number(countStr);
    if (n < 1) throw new Error("count must be at least 1");
    result += ch.repeat(n);
  }
  return result;
}
