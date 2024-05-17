import { SpaceObject } from "@/types/spaceObject";

/** Checks if the passed `spaceObject` fields contain the provided `searchText` */
export const doesSpaceObjectContainText = (
  spaceObject: SpaceObject,
  searchText: string,
) => {
  const filterableFields: (keyof SpaceObject)[] = [
    "sat_id",
    "launch_country",
    "sat_name",
    "launch_date",
    "object_type",
  ];

  return filterableFields.some((field) => {
    return spaceObject[field].toLowerCase().includes(searchText.toLowerCase());
  });
};
