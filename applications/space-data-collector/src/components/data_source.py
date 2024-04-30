from typing import Dict
import requests

from components.configuration_parser import DataSourceConfig

class DataSource:
  def __init__(self, dataSourceConfig: DataSourceConfig, auth: Dict[str, str]):
    self.data_source = dataSourceConfig
    self.session = requests.Session()
    res = self.session.post('https://www.space-track.org/ajaxauth/login', auth)

    print(res.status_code)


  def get_data(self):
    res = self.session.get(self.data_source.request_url)
    print('post it')
    print(res.json())

  