export function normalizeDigits(s) {
  return [...s].filter((ch) => ch !== " " && ch !== "-").join("");
}

export function luhnValid(raw) {
  const digits = normalizeDigits(raw);
  if (!digits || !/^\d+$/.test(digits)) return false;
  let sum = 0;
  let alt = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = digits.charCodeAt(i) - 48;
    if (alt) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
    alt = !alt;
  }
  return sum % 10 === 0;
}
