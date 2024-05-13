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

            self.api_keys = config.get("api-keys", "keys").split(" ")
            self.db_user = config.get("database", "database_user")
            self.db_pass = config.get("database", "database_password")
        except Exception as err:
            print("Failed to parse credentials.ini")
            print(err)
