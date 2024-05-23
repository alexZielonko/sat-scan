const axios = require("axios");
import { RouteConfig, SpaceObject } from "@/types/spaceObject";

export const fetchSpaceObjects = async (
  routeConfig: RouteConfig,
): Promise<SpaceObject[]> => {
  const url = `http://${routeConfig.API_URL}/space-objects`;

  const response = await axios.get(url);

  return response.data;
};
