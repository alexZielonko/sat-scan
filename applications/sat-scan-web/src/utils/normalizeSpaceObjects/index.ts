import { RawSpaceObject, SpaceObject } from "@/types/spaceObject";
import { getCountryNameFromCode } from "../getCountryNameFromCode";
import { getLaunchSiteFromCode } from "../getLaunchSiteFromCode";
import { getObjectType } from "./utils/getObjectType";
import { UNKNOWN_ORIGIN_TEXT } from "./constants";

export const normalizeSpaceObjects = (
  rawSpaceObjects: RawSpaceObject[],
): SpaceObject[] => {
  return rawSpaceObjects.map((rawObject) => {
    return {
      objectType: getObjectType(rawObject.object_type),
      launch: {
        location: {
          country:
            getCountryNameFromCode(rawObject.launch_country) ||
            UNKNOWN_ORIGIN_TEXT,
          site:
            getLaunchSiteFromCode(rawObject.launch_site) || UNKNOWN_ORIGIN_TEXT,
        },
        date: rawObject.launch_date,
        number: rawObject.launch_number,
        piece: rawObject.launch_piece,
        year: rawObject.launch_year,
      },
      satellite: {
        catalogNumber: rawObject.sat_catalog_number,
        id: rawObject.sat_id,
        name: rawObject.sat_name,
      },
    };
  });
};
