from typing import Dict


def get_auth_credentials_for_data_req(credentials_config, data_request_name: str) -> Dict[str, str]:
    username = credentials_config.get(data_request_name, "username")
    password = credentials_config.get(data_request_name, "password")

    return {"identity": username, "password": password}
