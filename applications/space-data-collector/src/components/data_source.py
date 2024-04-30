from typing import Dict
import requests

from components.configuration_parser import DataSourceConfig

class DataSource:
  def __init__(self, dataSourceConfig: DataSourceConfig, auth: Dict[str, str]):
    self.data_source = dataSourceConfig
    self._start_session(auth)
  
  def _start_session(self, auth) -> None:
    self.session = requests.Session()
    res = self.session.post('https://www.space-track.org/ajaxauth/login', auth)

    if res.status_code == 200:
      print(f'✅ Started session for: {self.data_source.name} {self.data_source.subject}')
    else:
      print(f'🚨 Failed to start session for: {self.data_source.name} {self.data_source.subject}')

  def get_data(self):
    res = self.session.get(self.data_source.request_url)
    print(res.json())

  