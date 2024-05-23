import { COUNTRY_CODES } from "./constants";

export const getCountryNameFromCode = (countryCode: string): string | null => {
  return COUNTRY_CODES[countryCode] || null;
};
