import fetch from "node-fetch";
import { RouteConfig, SpaceObject } from "@/types/spaceObject";

export const fetchSpaceObjects = async (
  routeConfig: RouteConfig,
): Promise<SpaceObject[]> => {
  const url = `http://${routeConfig.API_URL}/space-objects`;

  const response = await fetch(url);
  const spaceObjects = await response.json();

  return spaceObjects as SpaceObject[];
};
