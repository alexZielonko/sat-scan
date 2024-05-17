import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { fetchSpaceObjects } from ".";

describe("fetchSpaceObjects", () => {
  beforeAll(() => {
    global.fetch = jest.fn();
  });

  it("returns the request's json response", async () => {
    const mockSpaceObjects = [
      generateMockSpaceObject(),
      generateMockSpaceObject(),
      generateMockSpaceObject(),
    ];

    const fetchMock = jest.fn(async () => ({
      json: async () => {
        return mockSpaceObjects;
      },
    })) as jest.Mock;

    jest.spyOn(global, "fetch").mockImplementation(fetchMock);

    const actual = await fetchSpaceObjects();

    expect(actual).toBe(mockSpaceObjects);
  });
});
