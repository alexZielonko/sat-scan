import { SpaceObject } from "@/types/spaceObject";

export const hasFilterResults = (
  isLoading: boolean,
  filteredSpaceObjects: SpaceObject[],
): boolean => {
  return !isLoading && filteredSpaceObjects.length > 0;
};
