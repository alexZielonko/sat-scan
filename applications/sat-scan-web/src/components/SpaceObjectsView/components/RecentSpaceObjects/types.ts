import { SpaceObject } from "@/types/spaceObject";

export type RecentSpaceObjectsProps = {
  spaceObjects: SpaceObject[];
  selectedSpaceObject: SpaceObject | null;
  onSpaceObjectClick: (spaceObject: SpaceObject) => void;
};
