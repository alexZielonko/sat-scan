import configparser, os
from typing import Dict

from app.config_parsers.credentials import Credentials


class DatabaseCredentials:
    def __init__(self):
        self.credentials = Credentials()
        self.connection_url = self._get_db_connection_url()

    def _get_db_connection_url(self):
        route_config = self._get_route_config()
        driver = "postgresql"
        db_user = f"{self.credentials.db_user}:{self.credentials.db_pass}"
        db_route = f'{route_config["endpoint"]}/{route_config["name"]}'

        if route_config["env"] == "PROD":
            db_route = f'{route_config["endpoint"]}/{route_config["name"]}'

        return f"{driver}://{db_user}@{db_route}"

    def _get_route_config(self):
        try:
            directory = os.path.dirname(__file__)
            file = os.path.join(directory, "../../route-config.ini")

            config = configparser.ConfigParser()
            config.read(file)

            return {
                "env": config.get("database", "env"),
                "endpoint": config.get("database", "database_endpoint"),
                "name": config.get("database", "database_name"),
            }
        except Exception as err:
            return {"env": None, "endpoint": None, "name": None}
