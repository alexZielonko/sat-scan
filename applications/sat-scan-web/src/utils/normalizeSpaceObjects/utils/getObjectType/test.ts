import { getObjectType } from ".";
import {
  DESCRIPTIVE_UNKNOWN_OBJECT_TYPE,
  GENERIC_UNKNOWN_OBJECT_TYPE,
} from "./constants";

describe("getObjectType", () => {
  it("returns the object type if not unknown", () => {
    const mockObjectType = "Satellite";
    const actual = getObjectType(mockObjectType);

    expect(actual).toBe(mockObjectType);
  });

  it("returns a string describing unknown object types", () => {
    const actual = getObjectType(GENERIC_UNKNOWN_OBJECT_TYPE);
    const expected = DESCRIPTIVE_UNKNOWN_OBJECT_TYPE;

    expect(actual).toBe(expected);
  });
});
