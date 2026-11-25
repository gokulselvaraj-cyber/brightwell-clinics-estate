import { describe, expect, it } from "vitest";
import { shouldWarnNoShows } from "./noShowWarning";

describe("shouldWarnNoShows", () => {
  const today = new Date("2026-06-01");
  it("warns at two recent no-shows", () => {
    expect(shouldWarnNoShows(["2026-04-01", "2026-05-01"], today)).toBe(true);
  });
  it("ignores old no-shows", () => {
    expect(shouldWarnNoShows(["2025-01-01", "2026-05-01"], today)).toBe(false);
  });
});
