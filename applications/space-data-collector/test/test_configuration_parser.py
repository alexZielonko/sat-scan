import unittest
from unittest.mock import patch, mock_open

from components.configuration_parser import ConfigurationParser


class TestConfigurationParser(unittest.TestCase):

    def test_it_generates_the_expected_list_of_data_request_config_objects(self):
        parser = ConfigurationParser()
        data_request_config = parser.run()[0]

        self.assertEqual(data_request_config.name, "space-track.org")
        self.assertEqual(data_request_config.routing_key, "recent_objects")
        self.assertEqual(
            data_request_config.request_url,
            "https://www.space-track.org/basicspacedata/query/class/satcat/LAUNCH/%3Enow-7/CURRENT/Y/orderby/LAUNCH%20DESC/format/json",
        )


if __name__ == "__main__":
    unittest.main()
