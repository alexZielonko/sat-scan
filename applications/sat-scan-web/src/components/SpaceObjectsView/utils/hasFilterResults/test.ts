import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { hasFilterResults } from ".";

describe("hasFilterResults", () => {
  const hasFilterSuccessConditions = {
    filteredSpaceObjects: [generateMockSpaceObject()],
  };

  it.each([
    {
      testCase:
        "returns true when there are filtered space object results for the filter term",
      expected: true,
      ...hasFilterSuccessConditions,
    },
    {
      testCase: "returns false when there are not any filtered space objects",
      expected: false,
      ...hasFilterSuccessConditions,
      filteredSpaceObjects: [],
    },
  ])("$testCase", ({ expected, filteredSpaceObjects }) => {
    const actual = hasFilterResults(filteredSpaceObjects);
    expect(actual).toBe(expected);
  });
});
