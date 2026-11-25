import { describe, expect, it } from "vitest";
import { isNhsNumber } from "../../utils/validation";

describe("DetailsStep validation", () => {
  it("accepts a test-range NHS number with a valid check digit", () => {
    expect(isNhsNumber("999 000 0018")).toBe(true);
  });
  it("rejects a bad check digit", () => {
    expect(isNhsNumber("999 000 0019")).toBe(false);
  });
});
