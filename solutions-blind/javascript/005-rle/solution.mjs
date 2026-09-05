export function encode(s) {
  if (s === "") return "";
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
  if (s === "") return "";
  let result = "";
  let i = 0;
  while (i < s.length) {
    const ch = s[i++];
    if (i >= s.length || s[i] < "0" || s[i] > "9") {
      throw new Error("missing count after character");
    }
    let countStr = "";
    while (i < s.length && s[i] >= "0" && s[i] <= "9") {
      countStr += s[i++];
    }
    const n = Number(countStr);
    if (n < 1) throw new Error("count must be at least 1");
    result += ch.repeat(n);
  }
  return result;
}
