import pika, ssl

from components.mq_broker_config import MqBrokerConfig


class RabbitMqConnectionInterface:
    PRODUCTION_ENVIRONMENT_KEY = "PROD"
    DOCKER_COMPOSE_INSTANCE_NAME = "event-collaboration-messaging"

    def __init__(self, broker_config: MqBrokerConfig):
        self.broker_config = broker_config

    def establish_connection(self):
        connection_parameters = self._get_pika_connection_parameters()
        self.connection = pika.BlockingConnection(connection_parameters)

        return self.connection

    def _get_pika_connection_parameters(self):
        config = self.broker_config

        if config.env == RabbitMqConnectionInterface.PRODUCTION_ENVIRONMENT_KEY:
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")

            url = f"amqps://{config.user}:{config.password}@{config.broker_id}.mq.{config.region}.amazonaws.com:5671"

            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            return parameters

        # Return default connection name in non-prod environments
        return pika.ConnectionParameters(
            RabbitMqConnectionInterface.DOCKER_COMPOSE_INSTANCE_NAME
        )
