import configparser, os
from typing import Dict

from app.config_parsers.credentials import Credentials

class RouteConfig:
    def __init__(self):
        self.credentials = Credentials()
        route_config = self._get_route_config()
        self.api_url = route_config["base_url"]

    def _get_route_config(self):
      try:
          directory = os.path.dirname(__file__)
          file = os.path.join(directory, '../../route-config.ini')
          
          config = configparser.ConfigParser()
          config.read(file)

          return {
              "base_url": config.get('sat-scan-api', 'base_url'),
          }
      except Exception as err:
          print('Failed to parse route-config.ini')
          return {}