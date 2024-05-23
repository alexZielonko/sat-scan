import { SpaceObject } from "@/types/spaceObject";

/** Checks if the passed `spaceObject` fields contain the provided `searchText` */
export const doesSpaceObjectContainText = (
  spaceObject: SpaceObject,
  searchText: string,
) => {
  const searchableValues = [
    spaceObject.objectType,
    spaceObject.launch.location.country,
    spaceObject.launch.location.site,
    spaceObject.launch.date,
    spaceObject.satellite.name,
  ];

  return searchableValues.some((value) =>
    value.toLowerCase().includes(searchText.toLowerCase()),
  );
};
