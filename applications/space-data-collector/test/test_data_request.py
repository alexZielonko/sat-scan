import responses
import unittest

from components.data_request import DataRequest
from components.configuration_parser import DataRequestConfig


class TestDataRequest(unittest.TestCase):

    @responses.activate
    def test_gets_data_for_the_data_request_url(self):
        post_response = responses.Response(
            responses.POST,
            DataRequest.SPACE_TRACK_API_SESSION_URL,
            status=200,
        )

        responses.add(post_response)

        MOCK_NAME = "MOCK_NAME"
        MOCK_ROUTING_KEY = "MOCK_ROUTING_KEY"
        MOCK_REQUEST_URL = "https://MOCK_REQUEST_URL"

        data_request_config = DataRequestConfig(
            name=MOCK_NAME, routing_key=MOCK_ROUTING_KEY, request_url=MOCK_REQUEST_URL
        )

        data_request = DataRequest(data_request_config=data_request_config, auth={})

        expected_json_response = {"mock_response_object": True}

        get_response = responses.Response(
            responses.GET,
            MOCK_REQUEST_URL,
            json=expected_json_response,
            status=200,
        )

        responses.add(get_response)

        res = data_request.get()

        self.assertEqual(res, expected_json_response)


if __name__ == "__main__":
    unittest.main()
