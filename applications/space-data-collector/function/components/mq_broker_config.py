class MqBrokerConfig:
    config_key = "mq_broker"

    def __init__(self, config):
        self.env = config.get(MqBrokerConfig.config_key, "env")
        self.user = config.get(MqBrokerConfig.config_key, "rabbitmq_user")
        self.password = config.get(MqBrokerConfig.config_key, "rabbitmq_password")
        self.broker_id = config.get(MqBrokerConfig.config_key, "rabbitmq_broker_id")
        self.region = config.get(MqBrokerConfig.config_key, "rabbitmq_region")
