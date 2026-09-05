function shiftChar(ch, shift) {
  const code = ch.charCodeAt(0);
  if (code >= 97 && code <= 122) {
    return String.fromCharCode(97 + (((code - 97 + shift) % 26) + 26) % 26);
  }
  if (code >= 65 && code <= 90) {
    return String.fromCharCode(65 + (((code - 65 + shift) % 26) + 26) % 26);
  }
  return ch;
}

export function encrypt(text, shift) {
  let out = "";
  for (const ch of text) out += shiftChar(ch, shift);
  return out;
}

export function decrypt(text, shift) {
  return encrypt(text, -shift);
}
