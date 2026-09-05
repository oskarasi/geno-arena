function norm(n) {
  const m = n % 26;
  return m < 0 ? m + 26 : m;
}

function shiftChar(ch, shift) {
  const code = ch.charCodeAt(0);
  if (code >= 97 && code <= 122) return String.fromCharCode(97 + norm(code - 97 + shift));
  if (code >= 65 && code <= 90) return String.fromCharCode(65 + norm(code - 65 + shift));
  return ch;
}

export function encrypt(text, shift) {
  return [...text].map((ch) => shiftChar(ch, shift)).join("");
}

export function decrypt(text, shift) {
  return encrypt(text, -shift);
}
