from typing import Dict
import requests

from components.configuration_parser import DataRequestConfig

class DataRequest:
  def __init__(self, DataRequestConfig: DataRequestConfig, auth: Dict[str, str]):
    self.data_request = DataRequestConfig
    self._start_session(auth)
  
  def _start_session(self, auth) -> None:
    self.session = requests.Session()
    res = self.session.post('https://www.space-track.org/ajaxauth/login', auth)

    if res.status_code == 200:
      print(f'✅ Started session for: {self.data_request.name} {self.data_request.subject}')
    else:
      print(f'🚨 Failed to start session for: {self.data_request.name} {self.data_request.subject}')

  def get_data(self):
    res = self.session.get(self.data_request.request_url)
    print(res.json())

  