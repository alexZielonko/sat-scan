import { SpaceObject } from "@/types/spaceObject";

export const hasFilterResults = (
  filteredSpaceObjects: SpaceObject[],
): boolean => {
  return filteredSpaceObjects.length > 0;
};
