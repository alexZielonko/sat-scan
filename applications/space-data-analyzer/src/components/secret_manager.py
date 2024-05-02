import os, configparser

class SecretManager:
    def __init__(self):
        directory = os.path.dirname(__file__)
        file = os.path.join(directory, '../credentials.ini')
        
        config = configparser.ConfigParser()
        config.read(file)

        self.sat_scan_api_key = config.get('sat-scan-key', 'key')