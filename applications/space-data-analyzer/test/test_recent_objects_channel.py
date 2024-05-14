import io
import responses
import unittest

from typing import Dict
from contextlib import redirect_stderr
from unittest.mock import patch, mock_open, MagicMock

import components.config_parsers.route_config
from components.interfaces.response_status import ResponseStatus
from components.channels.recent_objects_channel import RecentObjectsChannel


class TestRecentObjectsChannel(unittest.TestCase):
    MOCK_API_KEY = "__MOCK_API_KEY__"

    @patch("components.config_parsers.route_config")
    def test_it_sets_request_headers(self, route_config_mock):
        route_config = route_config_mock()
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY,
            route_config=route_config,
        )

        actual = channel.request_headers
        expected = {
            "Authorization": "Bearer " + TestRecentObjectsChannel.MOCK_API_KEY,
            "Content-Type": "application/json",
        }

        self.assertEqual(actual, expected)

    @patch("components.config_parsers.route_config")
    def test_it_uses_the_expected_api_path(self, route_config_mock):
        MOCK_API_URL = "__API_URL__"
        route_config = route_config_mock()
        route_config.api_url = MOCK_API_URL
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY,
            route_config=route_config,
        )

        actual = channel._get_space_objects_api_path()
        expected = MOCK_API_URL + "/space-objects"

        self.assertEqual(actual, expected)

    def _before_has_space_object(self, sat_id: str, json_response: Dict[str, str]):
        """
        Utility to stub channel for _has_space_object method test
        """
        API_URL = "https://__API_URL__"
        GET_URL = f"{API_URL}/{sat_id}"

        get_response = responses.Response(
            responses.GET,
            GET_URL,
            json=json_response,
            status=200,
        )

        responses.add(get_response)
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )
        channel._get_space_objects_api_path = MagicMock(return_value=API_URL)
        return channel

    @responses.activate
    def test_has_space_object_returns_true(self):
        """
        It returns True when an entry for the space object exists in the Sat Scan DB
        """
        SAT_ID = "12345"
        channel = self._before_has_space_object(
            SAT_ID, json_response={"sat_id": SAT_ID}
        )
        self.assertTrue(channel._has_space_object(SAT_ID))

    @responses.activate
    def test_has_space_object_returns_false(self):
        """
        It returns False when an entry does not exist for the given satellite id
        """
        SAT_ID = "12345"
        channel = self._before_has_space_object(
            SAT_ID,
            json_response={},
        )
        self.assertFalse(channel._has_space_object(SAT_ID))

    def test_has_space_object_returns_false_on_error(self):
        """
        It returns False when an exception is thrown
        """
        with io.StringIO() as buffer, redirect_stderr(buffer):
            SAT_ID = "12345"
            channel = self._before_has_space_object(
                SAT_ID, json_response={"sat_id": SAT_ID}
            )
            channel._get_space_objects_api_path = MagicMock(
                side_effect=Exception("Mocked Error")
            )
            self.assertFalse(channel._has_space_object(SAT_ID))

    def _before_update_space_object(self, status: int):
        """
        Utility to stub channel for _update_space_object method test
        """
        API_URL = "https://__API_URL__"

        put_response = responses.Response(
            responses.PUT,
            API_URL,
            status=status,
        )

        responses.add(put_response)
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )
        channel._get_space_objects_api_path = MagicMock(return_value=API_URL)
        return channel

    @responses.activate
    def test_update_space_object_returns_true(self):
        """
        It creates a success response object on a successful PUT request
        """
        channel = self._before_update_space_object(status=200)
        self.assertTrue(channel._update_space_object(space_object={}).success)

    @responses.activate
    def test_update_space_object_returns_false(self):
        """
        It creates a failed response object on an unauthorized PUT request
        """
        channel = self._before_update_space_object(status=401)
        self.assertFalse(channel._update_space_object(space_object={}).success)

    @responses.activate
    def test_update_space_object_returns_false_on_error(self):
        """
        It returns False when an exception is thrown
        """
        with io.StringIO() as buffer, redirect_stderr(buffer):
            channel = self._before_update_space_object(status=200)
            channel._get_space_objects_api_path = MagicMock(
                side_effect=Exception("Mocked Error")
            )
            self.assertFalse(channel._update_space_object(space_object={}).success)

    def _before_create_space_object(self, status: int):
        """
        Utility to stub channel for _create_space_object method test
        """
        API_URL = "https://__API_URL__"

        put_response = responses.Response(
            responses.POST,
            API_URL,
            status=status,
        )

        responses.add(put_response)
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )
        channel._get_space_objects_api_path = MagicMock(return_value=API_URL)
        return channel

    @responses.activate
    def test_update_space_object_returns_true(self):
        """
        It creates a success response object on a successful PUT request
        """
        channel = self._before_create_space_object(status=200)
        self.assertTrue(channel._create_space_object(space_object={}).success)

    @responses.activate
    def test_create_space_object_returns_false(self):
        """
        It creates a failed response object on an unauthorized PUT request
        """
        channel = self._before_create_space_object(status=401)
        self.assertFalse(channel._create_space_object(space_object={}).success)

    @responses.activate
    def test_create_space_object_returns_false_on_error(self):
        """
        It returns False when an exception is thrown
        """
        with io.StringIO() as buffer, redirect_stderr(buffer):
            channel = self._before_create_space_object(status=200)
            channel._get_space_objects_api_path = MagicMock(
                side_effect=Exception("Mocked Error")
            )
            self.assertFalse(channel._create_space_object(space_object={}).success)

    def test_create_or_update_updates_existing_space_object(self):
        """
        _create_or_update updates a space object if it already exists
        """
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )
        channel._has_space_object = MagicMock(return_value=True)
        channel._update_space_object = MagicMock()
        channel._create_space_object = MagicMock()

        channel._create_or_update(space_object={"sat_id": "1234"})

        self.assertTrue(channel._update_space_object.called)
        self.assertFalse(channel._create_space_object.called)

    def test_create_or_update_creates_new_space_object(self):
        """
        _create_or_update create a space object if it does not exist
        """
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )
        channel._has_space_object = MagicMock(return_value=False)
        channel._update_space_object = MagicMock()
        channel._create_space_object = MagicMock()

        channel._create_or_update(space_object={"sat_id": "1234"})

        self.assertFalse(channel._update_space_object.called)
        self.assertTrue(channel._create_space_object.called)

    def test_create_or_update_exception(self):
        """
        It returns False when an exception is thrown
        """
        with io.StringIO() as buffer, redirect_stderr(buffer):
            channel = RecentObjectsChannel(
                sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
            )
            channel._has_space_object = MagicMock(side_effect=Exception("Mock Error"))
            channel._create_or_update(space_object={})
            self.assertFalse(channel._create_or_update(space_object={}).success)

    def _before_process_message(self, create_or_update_response_status):
        channel = RecentObjectsChannel(
            sat_scan_api_key=TestRecentObjectsChannel.MOCK_API_KEY, route_config={}
        )

        channel._normalize_message_body = MagicMock(return_value={})
        channel._create_or_update = MagicMock(
            return_value=ResponseStatus(success=create_or_update_response_status)
        )

        rabbit_mq_channel = MagicMock()
        channel._process_message(
            ch=rabbit_mq_channel,
            method=MagicMock(),
            properties=MagicMock(),
            message_body="{}",
        )
        return rabbit_mq_channel

    def test_process_message_acknowledges_message(self):
        rabbit_mq_channel = self._before_process_message(
            create_or_update_response_status=True
        )
        self.assertTrue(rabbit_mq_channel.basic_ack.called)

    def test_process_message_does_not_acknowledge_message(self):
        rabbit_mq_channel = self._before_process_message(
            create_or_update_response_status=False
        )
        self.assertFalse(rabbit_mq_channel.basic_ack.called)


if __name__ == "__main__":
    unittest.main()
