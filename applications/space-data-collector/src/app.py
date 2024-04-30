#!/usr/bin/env python3

import os
import configparser
from typing import Dict

from components.data_source import DataSource
from components.configuration_parser import ConfigurationParser

def get_auth_credentials(data_source_name: str) -> Dict[str, str]:
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, '../credentials.ini')    
    
    config = configparser.ConfigParser()
    res = config.read(file)

    username = config.get(data_source_name, "username")
    password = config.get(data_source_name, "password")

    return {'identity': username, 'password': password}

if __name__ == "__main__":
    parser = ConfigurationParser()
    data_source_configs = parser.run()
    
    for source in data_source_configs:
        auth = get_auth_credentials(data_source_name=source.name)
        data_source = DataSource(source, auth)
        data_source.get_data()
    
    