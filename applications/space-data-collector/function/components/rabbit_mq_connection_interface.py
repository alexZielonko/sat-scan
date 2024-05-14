import pika, ssl


class RabbitMqConnectionInterface:
    def __init__(self, broker_config):
        self.broker_config = broker_config

    def establish_connection(self):
        connection_parameters = self._get_pika_connection_parameters()
        self.connection = pika.BlockingConnection(connection_parameters)

        return self.connection

    def _get_pika_connection_parameters(self):
        config = self.broker_config

        if config.env == "PROD":
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")

            url = f"amqps://{config.user}:{config.password}@{config.broker_id}.mq.{config.region}.amazonaws.com:5671"

            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            return parameters

        # Return default connection name in non-prod environments
        docker_compose_instance_name = "event-collaboration-messaging"
        return pika.ConnectionParameters(docker_compose_instance_name)
