import { describe, it, expect } from "vitest";
import { formatDate, getMonday, toISODate, getWeekDays } from "@/utils/date";

describe("date utilities", () => {
  it("formats a date string correctly", () => {
    const result = formatDate("2026-03-27");
    expect(result).toContain("27");
    expect(result).toContain("Mar");
    expect(result).toContain("2026");
  });

  it("returns Monday for a given date", () => {
    // March 27 2026 is a Friday
    const monday = getMonday(new Date("2026-03-27"));
    expect(toISODate(monday)).toBe("2026-03-23");
  });

  it("generates 7 weekdays starting from Monday", () => {
    const days = getWeekDays(new Date("2026-03-27"));
    expect(days).toHaveLength(7);
    expect(days[0]).toBe("2026-03-23"); // Monday
    expect(days[6]).toBe("2026-03-29"); // Sunday
  });
});
