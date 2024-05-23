export type RouteConfig = {
  API_URL: String;
};

export type SpaceObject = {
  objectType: string;
  launch: {
    location: {
      country: string;
      site: string;
    };
    date: string;
    number: string;
    piece: string;
    year: string;
  };
  satellite: {
    catalogNumber: string;
    id: string;
    name: string;
  };
};

export type RawSpaceObject = {
  file_id: string;
  launch_country: string;
  launch_date: string;
  launch_number: string;
  launch_piece: string;
  launch_site: string;
  launch_year: string;
  object_id: string;
  object_name: string;
  object_number: string;
  object_type: string;
  sat_catalog_number: string;
  sat_id: string;
  sat_name: string;
};
