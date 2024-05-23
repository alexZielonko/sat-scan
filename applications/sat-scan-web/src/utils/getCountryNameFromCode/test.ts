import { getCountryNameFromCode } from ".";

describe("getCountryNameFromCode", () => {
  it("returns the expected country name", () => {
    const actual = getCountryNameFromCode("PRC");
    const expected = "China";

    expect(actual).toBe(expected);
  });

  it("returns null if passed an invalid country code", () => {
    const actual = getCountryNameFromCode("Invalid Country Code");

    expect(actual).toBeNull();
  });
});
