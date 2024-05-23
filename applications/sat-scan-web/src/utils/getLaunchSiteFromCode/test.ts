import { getLaunchSiteFromCode } from ".";

describe("getLaunchSiteFromCode", () => {
  it("returns the expected launch site name", () => {
    const actual = getLaunchSiteFromCode("TSC");
    const expected = "Taiyuan Satellite Launch Center";

    expect(actual).toBe(expected);
  });

  it("returns null if passed an invalid country code", () => {
    const actual = getLaunchSiteFromCode("Invalid Launch Site Code");

    expect(actual).toBeNull();
  });
});
