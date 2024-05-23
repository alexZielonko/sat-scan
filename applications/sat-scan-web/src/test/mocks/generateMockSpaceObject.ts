import { SpaceObject } from "@/types/spaceObject";
import { normalizeSpaceObjects } from "@/utils/normalizeSpaceObjects";
import { generateRawMockSpaceObject } from "./generateRawMockSpaceObject";

export const generateMockSpaceObject = (): SpaceObject => {
  const [spaceObject] = normalizeSpaceObjects([generateRawMockSpaceObject()]);
  return spaceObject;
};
