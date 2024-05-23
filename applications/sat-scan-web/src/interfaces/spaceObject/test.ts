import { generateRawMockSpaceObject } from "@/test/mocks/generateRawMockSpaceObject";
import { fetchSpaceObjects } from ".";
import axios from "axios";
import { SpaceObject } from "@/types/spaceObject";

describe("fetchSpaceObjects", () => {
  const mockRouteConfig = {
    API_URL: "__MOCK_API_URL__",
  };

  it("returns the request's json response", async () => {
    const mockSpaceObjects = [
      generateRawMockSpaceObject(),
      generateRawMockSpaceObject(),
      generateRawMockSpaceObject(),
    ];

    const spy = jest
      .spyOn(axios, "get")
      .mockReturnValue({ data: mockSpaceObjects } as any);

    const actual = await fetchSpaceObjects(mockRouteConfig);

    expect(actual).toBe(mockSpaceObjects);
    expect(spy).toHaveBeenCalledWith("http://__MOCK_API_URL__/space-objects");
  });
});
