import { SpaceObject } from "@/types/spaceObject";

export const fetchSpaceObjects = async (): Promise<SpaceObject[]> => {
  const res = await fetch("http://127.0.0.1:5000/space-objects");
  const spaceObjects: SpaceObject[] = await res.json();

  return spaceObjects;
};
