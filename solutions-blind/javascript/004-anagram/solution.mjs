function normalize(s) {
  return s.toLowerCase().replace(/ /g, "").split("").sort().join("");
}

export function is_anagram(a, b) {
  return normalize(a) === normalize(b);
}
