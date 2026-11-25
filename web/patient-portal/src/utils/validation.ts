const UK_POSTCODE = /^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$/i;
const EIRCODE = /^([AC-FHKNPRTV-Y][0-9]{2}|D6W) ?[0-9AC-FHKNPRTV-Y]{4}$/i;
const NHS = /^\d{3} ?\d{3} ?\d{4}$/;

export const isUkPostcode = (v: string) => UK_POSTCODE.test(v.trim());
export const isEircode = (v: string) => EIRCODE.test(v.trim());

export function isNhsNumber(v: string): boolean {
  const digits = v.replace(/\s/g, "");
  if (!NHS.test(v) || digits.length !== 10) return false;
  const sum = digits.slice(0, 9).split("").reduce((acc, d, i) => acc + Number(d) * (10 - i), 0);
  const check = 11 - (sum % 11);
  return (check === 11 ? 0 : check) === Number(digits[9]);
}
