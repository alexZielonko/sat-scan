import unittest
from unittest.mock import patch, mock_open

from src.config_parsers.credentials import Credentials


class TestCredentials(unittest.TestCase):

    MOCK_KEY = "__MOCK_SAT_SCAN_API_KEY__"
    MOCK_CREDENTIALS_FILE_CONTENTS = f"[sat-scan-api]\nkey={MOCK_KEY}"

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=MOCK_CREDENTIALS_FILE_CONTENTS,
    )
    def test_it_exposes_a_sat_scan_api_key(self, mock):
        credentials = Credentials()
        self.assertEqual(credentials.sat_scan_api_key, TestCredentials.MOCK_KEY)
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
