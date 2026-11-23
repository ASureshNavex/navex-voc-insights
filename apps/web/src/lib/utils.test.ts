import { cn, formatArr, formatDate } from "./utils";

describe("utils", () => {
  it("merges conflicting Tailwind classes, last one wins", () => {
    const hidden = false;
    expect(cn("px-2", hidden && "hidden", "px-4")).toBe("px-4");
  });

  it("formats ARR compactly in US dollars", () => {
    expect(formatArr("290000")).toBe("$290K");
    expect(formatArr(1_250_000)).toBe("$1.3M");
  });

  it("formats a missing date as Not set", () => {
    expect(formatDate(null)).toBe("Not set");
    expect(formatDate("2027-01-31")).toBe("31 Jan 2027");
  });
});
