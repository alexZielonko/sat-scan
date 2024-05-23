import { generateRawMockSpaceObject } from "@/test/mocks/generateRawMockSpaceObject";
import { normalizeSpaceObjects } from ".";
import { UNKNOWN_ORIGIN_TEXT } from "./constants";
import { COUNTRY_CODES } from "../getCountryNameFromCode/constants";
import { LAUNCH_SITES } from "../getLaunchSiteFromCode/constants";

describe("normalizeSpaceObjects", () => {
  it("returns the expected object", () => {
    const mockSpaceObject = {
      ...generateRawMockSpaceObject(),
      launch_country: "Unknown Country Code",
      launch_site: "Unknown Launch Site",
    };

    const actual = normalizeSpaceObjects([mockSpaceObject]);
    const expected = [
      {
        objectType: mockSpaceObject.object_type,
        launch: {
          location: {
            country: UNKNOWN_ORIGIN_TEXT,
            site: UNKNOWN_ORIGIN_TEXT,
          },
          date: mockSpaceObject.launch_date,
          number: mockSpaceObject.launch_number,
          piece: mockSpaceObject.launch_piece,
          year: mockSpaceObject.launch_year,
        },
        satellite: {
          catalogNumber: mockSpaceObject.sat_catalog_number,
          id: mockSpaceObject.sat_id,
          name: mockSpaceObject.sat_name,
        },
      },
    ];

    expect(actual).toEqual(expected);
  });

  describe("country name behavior", () => {
    it("returns the expected country name when known", () => {
      const expectedCountryName = COUNTRY_CODES.US;
      const mockSpaceObject = {
        ...generateRawMockSpaceObject(),
        launch_country: "US",
      };

      const [actual] = normalizeSpaceObjects([mockSpaceObject]);

      expect(actual.launch.location.country).toEqual(expectedCountryName);
    });

    it("returns the expected text when the country name is unknown", () => {
      const expectedCountryName = UNKNOWN_ORIGIN_TEXT;
      const mockSpaceObject = {
        ...generateRawMockSpaceObject(),
        launch_country: "A Country",
      };

      const [actual] = normalizeSpaceObjects([mockSpaceObject]);

      expect(actual.launch.location.country).toEqual(expectedCountryName);
    });
  });

  describe("launch site name behavior", () => {
    it("returns the expected launch site name when known", () => {
      const expectedLaunchSite = LAUNCH_SITES.XSC;
      const mockSpaceObject = {
        ...generateRawMockSpaceObject(),
        launch_site: "XSC",
      };

      const [actual] = normalizeSpaceObjects([mockSpaceObject]);

      expect(actual.launch.location.site).toEqual(expectedLaunchSite);
    });

    it("returns the expected text when the launch site name is unknown", () => {
      const expectedLaunchSite = UNKNOWN_ORIGIN_TEXT;
      const mockSpaceObject = {
        ...generateRawMockSpaceObject(),
        launch_site: "A Launch Site",
      };

      const [actual] = normalizeSpaceObjects([mockSpaceObject]);

      expect(actual.launch.location.site).toEqual(expectedLaunchSite);
    });
  });
});
