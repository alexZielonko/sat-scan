import { RouteConfig, SpaceObject } from "@/types/spaceObject";

export const fetchSpaceObjects = async (
  routeConfig: RouteConfig,
): Promise<SpaceObject[]> => {
  const url = `http://${routeConfig.API_URL}/space-objects`;
  const res = await fetch(url);
  const spaceObjects: SpaceObject[] = await res.json();

  return spaceObjects;
};
