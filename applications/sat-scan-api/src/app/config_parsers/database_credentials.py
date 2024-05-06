import configparser, os
from typing import Dict

from app.config_parsers.credentials import Credentials

    
class DatabaseCredentials:
    def __init__(self):
        self.credentials = Credentials().get_database_credentials()
        self.route_config = self._get_route_config()

    def get_db_connection_url(self):
        route_config = self._get_route_config()
        driver = 'postgresql'
        db_user = f'{self.credentials["user"]}:{self.credentials["password"]}'
        db_route = f'{route_config["endpoint"]}/{route_config["name"]}'

        print('env')
        print(route_config['env'])

        if route_config["env"] == "PROD":
          db_route = f'{route_config["endpoint"]}:{route_config["port"]}/{route_config["name"]}'
  
        return f'{driver}://{db_user}@{db_route}'        

    def _get_route_config(self):
      try:
          directory = os.path.dirname(__file__)
          file = os.path.join(directory, '../../route-config.ini')
          
          config = configparser.ConfigParser()
          config.read(file)

          return {
              "env": config.get('database', 'env'),
              "endpoint": config.get('database', "database_endpoint"),
              "port": config.get('database', "database_port"),
              "name": config.get('database', "database_name"),
          }
      except Exception as err:
          return {}