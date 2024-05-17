import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { hasFilterResults } from ".";

describe("hasFilterResults", () => {
  const hasFilterSuccessConditions = {
    isLoading: false,
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
      testCase: "returns false when loading",
      expected: false,
      ...hasFilterSuccessConditions,
      isLoading: true,
    },
    {
      testCase: "returns false when there are not any filtered space objects",
      expected: false,
      ...hasFilterSuccessConditions,
      filteredSpaceObjects: [],
    },
  ])("$testCase", ({ expected, isLoading, filteredSpaceObjects }) => {
    const actual = hasFilterResults(isLoading, filteredSpaceObjects);
    expect(actual).toBe(expected);
  });
});
