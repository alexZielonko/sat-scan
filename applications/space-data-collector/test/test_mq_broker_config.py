import unittest
from unittest.mock import MagicMock, ANY

from components.get_config import get_config
from components.mq_broker_config import MqBrokerConfig


class TestMqBrokerConfig(unittest.TestCase):

    def test_mq_broker_config(self):
        """
        it creates the expected Rabbit MQ Broker configuration object
        """
        MOCK_ENV = "TEST_ENV"
        MOCK_USERNAME = "MOCK_USERNAME"
        MOCK_PASSWORD = "MOCK_PASSWORD"
        MOCK_BROKER_ID = "MOCK_BROKER_ID"
        MOCK_REGION = "MOCK_REGION"

        config = MagicMock()
        config.get.side_effect = [
            MOCK_ENV,
            MOCK_USERNAME,
            MOCK_PASSWORD,
            MOCK_BROKER_ID,
            MOCK_REGION,
        ]

        broker_config = MqBrokerConfig(config)

        self.assertEqual(broker_config.env, MOCK_ENV)
        self.assertEqual(broker_config.user, MOCK_USERNAME)
        self.assertEqual(broker_config.password, MOCK_PASSWORD)
        self.assertEqual(broker_config.broker_id, MOCK_BROKER_ID)
        self.assertEqual(broker_config.region, MOCK_REGION)


if __name__ == "__main__":
    unittest.main()
