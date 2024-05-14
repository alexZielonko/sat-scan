from typing import Dict
import requests

from components.configuration_parser import DataRequestConfig


class DataRequest:
    SPACE_TRACK_API_SESSION_URL = "https://www.space-track.org/ajaxauth/login"

    def __init__(self, data_request_config: DataRequestConfig, auth: Dict[str, str]):
        self.data_request = data_request_config
        self._start_session(auth)

    def _start_session(self, auth) -> bool:
        self.session = requests.Session()
        res = self.session.post(DataRequest.SPACE_TRACK_API_SESSION_URL, auth)

        if res.status_code == 200:
            print(
                f"✅ Started session for: {self.data_request.name} {self.data_request.routing_key}"
            )
        else:
            print(
                f"🚨 Failed to start session for: {self.data_request.name} {self.data_request.routing_key}"
            )

    def get(self):
        res = self.session.get(self.data_request.request_url)
        return res.json()
