import { SpaceObject } from "@/types/spaceObject";

export const hasFilterResults = (isLoading: boolean, filteredSpaceObjects: SpaceObject[], currentFilterTerm: string | null): boolean => {
  return !isLoading && filteredSpaceObjects.length > 0 && !!currentFilterTerm;
}