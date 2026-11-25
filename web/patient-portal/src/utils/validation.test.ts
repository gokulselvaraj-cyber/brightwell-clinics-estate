import { describe, expect, it } from "vitest";
import { isEircode, isUkPostcode } from "./validation";

describe("address validation", () => {
  it("accepts the test postcode", () => expect(isUkPostcode("ZZ99 9ZZ")).toBe(true));
  it("rejects junk", () => expect(isUkPostcode("NOT A POSTCODE")).toBe(false));
  it("accepts a test Eircode", () => expect(isEircode("X00 X001")).toBe(true));
});
