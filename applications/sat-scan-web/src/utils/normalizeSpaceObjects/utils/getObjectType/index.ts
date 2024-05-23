import {
  DESCRIPTIVE_UNKNOWN_OBJECT_TYPE,
  GENERIC_UNKNOWN_OBJECT_TYPE,
} from "./constants";

export const getObjectType = (objectType: string): string => {
  return objectType.toLowerCase() === GENERIC_UNKNOWN_OBJECT_TYPE.toLowerCase()
    ? DESCRIPTIVE_UNKNOWN_OBJECT_TYPE
    : objectType;
};
