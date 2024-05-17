import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { hasFilterResults } from ".";

describe("hasFilterResults", () => {
  it.each([
    {
      testCase:
        "returns true when there are filtered space object results for the filter term",
      expected: true,
      isLoading: false,
      filteredSpaceObjects: [generateMockSpaceObject()],
      currentFilterTerm: "__MOCK_SEARCH_TERM__",
    },
  ])(
    "$testCase",
    ({ expected, isLoading, filteredSpaceObjects, currentFilterTerm }) => {
      const actual = hasFilterResults(
        isLoading,
        filteredSpaceObjects,
        currentFilterTerm,
      );
      expect(actual).toBe(expected);
    },
  );
});
