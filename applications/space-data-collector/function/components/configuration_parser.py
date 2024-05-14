import os
import yaml
from typing import Dict, List


class DataRequestConfig:
    def __init__(self, name, routing_key, request_url):
        self.name = name
        self.routing_key = routing_key
        self.request_url = request_url


class ConfigurationParser:
    DATA_REQUESTS_KEY = "space-track-requests"
    DATA_REQUESTS_FILE_NAME = "space_track_requests.yml"

    def _parse_config(self) -> List[Dict[str, str]]:
        directory = os.path.dirname(__file__)
        file = os.path.join(directory, ConfigurationParser.DATA_REQUESTS_FILE_NAME)

        with open(file) as stream:
            try:
                return yaml.safe_load(stream)[ConfigurationParser.DATA_REQUESTS_KEY]
            except yaml.YAMLError as exception:
                print(exception)

    def generate_data_requests(
        self, json_config: List[Dict[str, str]]
    ) -> List[DataRequestConfig]:
        build_config_object = lambda data_request: (
            DataRequestConfig(
                name=data_request["name"],
                routing_key=data_request["routing_key"],
                request_url=data_request["request_url"],
            )
        )

        return list(map(build_config_object, json_config))

    def run(self) -> List[DataRequestConfig]:
        json_config = self._parse_config()
        return self.generate_data_requests(json_config)
