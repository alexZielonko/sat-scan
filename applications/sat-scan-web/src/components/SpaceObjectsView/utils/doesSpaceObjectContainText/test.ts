import { generateRawMockSpaceObject } from "@/test/mocks/generateRawMockSpaceObject";
import { doesSpaceObjectContainText } from ".";

describe("doesSpaceObjectContainText", () => {
  it.each([{ field: "sat_id", value: "__search_text__" }])(
    "returns true if the field contains the search text",
    ({ field, value }) => {
      const spaceObject = {
        ...generateRawMockSpaceObject(),
        [field]: value,
      };
      const actual = doesSpaceObjectContainText(spaceObject, value);

      expect(actual).toBe(true);
    },
  );
});
