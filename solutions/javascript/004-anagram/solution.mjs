function signature(text) {
  const normalized = text.toLowerCase().replaceAll(" ", "");
  return [...normalized].sort().join("");
}

export function isAnagram(a, b) {
  return signature(a) === signature(b);
}
