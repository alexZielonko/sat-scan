import os
from typing import Dict, List
import yaml

class DataSourceConfig:
    def __init__(self, name, subject, request_url):
        self.name = name
        self.subject = subject
        self.request_url = request_url


class ConfigurationParser:
    DATA_SOURCE_KEY = 'data-sources'
    DATA_SOURCE_FILE_NAME = 'data_sources.yaml'

    def _parse_config(self) -> List[Dict[str, str]]:
      directory = os.path.dirname(__file__)
      file = os.path.join(directory, '../../' + ConfigurationParser.DATA_SOURCE_FILE_NAME)

      with open(file) as stream:
          try:
              return yaml.safe_load(stream)[ConfigurationParser.DATA_SOURCE_KEY]
          except yaml.YAMLError as exception:
              print(exception)

    def generate_data_sources(self, json_config: List[Dict[str, str]]) -> List[DataSourceConfig]:
        build_config_object = lambda data_source: (
            DataSourceConfig(
                name=data_source['name'], 
                subject=data_source['subject'],
                request_url=data_source['request_url']
            )
        )

        return list(map(build_config_object, json_config))
            
    def run(self) -> List[DataSourceConfig]:
      json_config = self._parse_config()
      return self.generate_data_sources(json_config)
