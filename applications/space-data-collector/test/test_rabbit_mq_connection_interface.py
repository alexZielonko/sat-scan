import pika
import unittest
from unittest.mock import MagicMock, patch

from components.mq_broker_config import MqBrokerConfig
from components.rabbit_mq_connection_interface import RabbitMqConnectionInterface


class TestRabbitMqConnectionInterface(unittest.TestCase):

    @patch("pika.BlockingConnection", spec=pika.BlockingConnection)
    @patch("pika.ConnectionParameters", spec=pika.ConnectionParameters)
    def test_it_establishes_a_development_connection(
        self, mock_pika_connection_parameters, mock_pika_blocking_connection
    ):
        broker_config = MqBrokerConfig(config=MagicMock())
        interface = RabbitMqConnectionInterface(broker_config=broker_config)
        interface.establish_connection()

        mock_pika_connection_parameters.assert_called_with(
            RabbitMqConnectionInterface.DOCKER_COMPOSE_INSTANCE_NAME
        )

    @patch("pika.URLParameters", spec=pika.URLParameters)
    @patch("pika.BlockingConnection", spec=pika.BlockingConnection)
    @patch("pika.ConnectionParameters", spec=pika.ConnectionParameters)
    def test_it_establishes_a_production_connection(
        self,
        mock_pika_connection_parameters,
        mock_pika_blocking_connection,
        mock_pika_url_parameters,
    ):
        PROD_ENV = RabbitMqConnectionInterface.PRODUCTION_ENVIRONMENT_KEY
        MOCK_USERNAME = "MOCK_USERNAME"
        MOCK_PASSWORD = "MOCK_PASSWORD"
        MOCK_BROKER_ID = "MOCK_BROKER_ID"
        MOCK_REGION = "MOCK_REGION"

        config = MagicMock()
        config.get.side_effect = [
            PROD_ENV,
            MOCK_USERNAME,
            MOCK_PASSWORD,
            MOCK_BROKER_ID,
            MOCK_REGION,
        ]
        broker_config = MqBrokerConfig(config=config)

        interface = RabbitMqConnectionInterface(broker_config=broker_config)
        interface.establish_connection()

        expected_connection_url = "amqps://MOCK_USERNAME:MOCK_PASSWORD@MOCK_BROKER_ID.mq.MOCK_REGION.amazonaws.com:5671"

        mock_pika_url_parameters.assert_called_with(expected_connection_url)


if __name__ == "__main__":
    unittest.main()
