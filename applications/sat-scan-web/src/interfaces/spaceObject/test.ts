import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { fetchSpaceObjects } from ".";

describe("fetchSpaceObjects", () => {
  beforeAll(() => {
    global.fetch = jest.fn();
  });

  const mockRouteConfig = {
    API_URL: "__MOCK_API_URL__",
  };

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

    const spy = jest.spyOn(global, "fetch").mockImplementation(fetchMock);

    const actual = await fetchSpaceObjects(mockRouteConfig);

    expect(actual).toBe(mockSpaceObjects);
    expect(spy).toHaveBeenCalledWith("http://__MOCK_API_URL__/space-objects");
  });
});
