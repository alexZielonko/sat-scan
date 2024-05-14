import configparser, os

from components.config_parsers.credentials import Credentials


class MqBrokerConfig:
    config_key = "mq_broker"

    def __init__(self, config):
        self.env = config.get(MqBrokerConfig.config_key, "env")
        self.user = config.get(MqBrokerConfig.config_key, "rabbitmq_user")
        self.password = config.get(MqBrokerConfig.config_key, "rabbitmq_password")
        self.broker_id = config.get(MqBrokerConfig.config_key, "rabbitmq_broker_id")
        self.region = config.get(MqBrokerConfig.config_key, "rabbitmq_region")


class RouteConfig:
    def __init__(self):
        self.credentials = Credentials()
        config = self._get_route_config()
        self.api_url = config.get("sat-scan-api", "base_url")
        self.mq_broker = MqBrokerConfig(config)

    def _get_route_config(self):
        try:
            directory = os.path.dirname(__file__)
            file = os.path.join(directory, "../../route-config.ini")

            config = configparser.ConfigParser()
            config.read(file)

            return config
        except Exception as err:
            print("Failed to parse route-config.ini")
            return {}
