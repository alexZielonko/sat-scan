import { generateMockSpaceObject } from "@/test/mocks/generateMockSpaceObject";
import { doesSpaceObjectContainText } from ".";

describe("doesSpaceObjectContainText", () => {
  it("returns true if the object type contains the search text", () => {
    const mockObjectValue = "mock object value";
    const searchText = mockObjectValue.slice(4, 9);
    const spaceObject = {
      ...generateMockSpaceObject(),
      objectType: mockObjectValue,
    };
    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(true);
  });

  it("returns true if the launch location contains the search text", () => {
    const mockValue = "mock object value";
    const searchText = mockValue.slice(4, 9);
    const spaceObject = {
      ...generateMockSpaceObject(),
      launch: {
        ...generateMockSpaceObject().launch,
        location: {
          ...generateMockSpaceObject().launch.location,
          country: mockValue,
        },
      },
    };
    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(true);
  });

  it("returns true if the launch site contains the search text", () => {
    const mockValue = "mock object value";
    const searchText = mockValue.slice(2, 4);
    const spaceObject = {
      ...generateMockSpaceObject(),
      launch: {
        ...generateMockSpaceObject().launch,
        location: {
          ...generateMockSpaceObject().launch.location,
          site: mockValue,
        },
      },
    };
    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(true);
  });

  it("returns true if the launch site contains the search text", () => {
    const mockValue = "2024-05-16";
    const searchText = "2024";
    const spaceObject = {
      ...generateMockSpaceObject(),
      launch: {
        ...generateMockSpaceObject().launch,
        date: mockValue,
      },
    };
    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(true);
  });

  it("returns true if the satellite name contains the search text", () => {
    const mockValue = "Starlink 235974";
    const searchText = "starlink";
    const spaceObject = {
      ...generateMockSpaceObject(),
      satellite: {
        ...generateMockSpaceObject().satellite,
        name: mockValue,
      },
    };
    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(true);
  });

  it("returns false if no match is found", () => {
    const searchText = "NO MATCH!";
    const spaceObject = generateMockSpaceObject();

    const actual = doesSpaceObjectContainText(spaceObject, searchText);

    expect(actual).toBe(false);
  });
});
