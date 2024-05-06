import configparser, os
from typing import List, Dict
    
class Credentials:
    def __init__(self):
        self.config = self._get_config()

    def _get_config(self):
        directory = os.path.dirname(__file__)
        file = os.path.join(directory, '../../credentials.ini')

        config = configparser.ConfigParser()
        config.read_file(open(file))

        return config
    
    def get_api_keys(self) -> List[str]:
        try:
            return self.config.get('api-keys', "keys").split(" ")
        except Exception:
            print('Failed to parse api-keys from credentials.ini')
            return []
    
    def get_database_credentials(self) -> Dict[str, str]:
        try:
            return {
              "user": self.config.get('database', "database_user"),
              "password": self.config.get('database', "database_password")
          }
        except Exception:
            print('Failed to prase database credentials from credentials.ini')
            return {}
