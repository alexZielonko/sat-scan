#!/usr/bin/env python3

import os
import configparser
from typing import Dict

from components.data_request import DataRequest
from components.configuration_parser import ConfigurationParser

def get_auth_credentials(data_request_name: str) -> Dict[str, str]:
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, '../credentials.ini')    
    
    config = configparser.ConfigParser()
    res = config.read(file)

    username = config.get(data_request_name, "username")
    password = config.get(data_request_name, "password")

    return {'identity': username, 'password': password}

if __name__ == "__main__":
    print('👉 Running space-data-collector')

    parser = ConfigurationParser()
    data_requests_config = parser.run()
    
    for request in data_requests_config:
        auth = get_auth_credentials(data_request_name=request.name)
        data_request = DataRequest(request, auth)
        data_request.get_data()
    
    