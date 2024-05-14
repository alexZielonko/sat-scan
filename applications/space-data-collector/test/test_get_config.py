import unittest
from unittest.mock import patch, ANY

from components.get_config import get_config


class TestGetConfig(unittest.TestCase):

    @patch("os.path.join", return_value="__MOCK_FILE_PATH__")
    @patch("configparser.ConfigParser")
    def test_get_config_reads_config_from_path(
        self, mock_config_parser, mock_path_join
    ):
        """
        expect get_config to read configuration file based on the passed file path/name
        """
        FILE_PATH = "FILE_PATH"
        mock_config = get_config(FILE_PATH)
        mock_path_join.assert_called_with(ANY, FILE_PATH)
        mock_config.read.assert_called_with("__MOCK_FILE_PATH__")


if __name__ == "__main__":
    unittest.main()
