import os, configparser


def get_config(file_path: str):
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, file_path)

    config = configparser.ConfigParser()
    config.read(file)

    return config
