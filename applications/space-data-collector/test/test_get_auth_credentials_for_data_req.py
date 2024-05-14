import unittest
from unittest.mock import MagicMock

from components.get_auth_credentials_for_data_req import (
    get_auth_credentials_for_data_req,
)


class TestGetAuthCredentialsForDataReq(unittest.TestCase):
    def test_get_auth_credentials_for_data_req(self):
        MOCK_USERNAME = "MOCK_USERNAME"
        MOCK_PASSWORD = "MOCK_PASSWORD"
        CONFIG_SECTION_KEY = "space-track.org"

        config = MagicMock()
        config.get.side_effect = [MOCK_USERNAME, MOCK_PASSWORD]

        actual = get_auth_credentials_for_data_req(config, CONFIG_SECTION_KEY)
        expected = {"identity": MOCK_USERNAME, "password": MOCK_PASSWORD}

        config.get.assert_called_with(CONFIG_SECTION_KEY, "password")
        self.assertEqual(actual, expected)
