import configparser, os
from typing import List, Dict


class Credentials:
    def __init__(self):
        self._parse_config()

    def _parse_config(self):
        try:
            directory = os.path.dirname(__file__)
            file = os.path.join(directory, "../../credentials.ini")

            config = configparser.ConfigParser()
            config.read_file(open(file))

            self.sat_scan_api_key = config.get("sat-scan-api", "key")
        except Exception as err:
            print("Failed to parse credentials.ini")
            print(err)
