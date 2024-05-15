import json, requests
from faker import Faker

from route_helper import RouteHelper


class TestUpdate(RouteHelper):
    def test_update_space_object_success(self):
        """
        it updates an existing space object
        """
        space_object = self.generate_space_object()

        res = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object),
        )

        assert res.status_code == 200

        fake = Faker()
        MOCK_OBJECT_TYPE = fake.uuid4()
        new_space_object = {**space_object, "object_type": MOCK_OBJECT_TYPE}

        res = requests.put(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(new_space_object),
        )

        assert res.status_code == 200

        response_json = res.json()

        assert response_json["sat_id"] == space_object["sat_id"]
        assert response_json["object_type"] == MOCK_OBJECT_TYPE

        cleanup_res = self.cleanup_test_object(space_object["sat_id"])

        assert cleanup_res.status_code == 200

    def test_it_requires_auth(self):
        """
        it returns a 401 if an invalid api key is provided
        """
        space_object = self.generate_space_object()

        post_res = requests.put(
            RouteHelper.BASE_ENDPOINT,
            headers={
                **self.get_headers(),
                "Authorization": "Bearer __INVALID_BEARER_TOKEN__",
            },
            data=json.dumps(space_object),
        )

        assert post_res.status_code == 401

    def test_update_space_object_not_found(self):
        """
        it returns a 404 if updating a record that doesn't exist
        """
        space_object = self.generate_space_object()

        res = requests.put(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object),
        )

        assert res.status_code == 404

    def test_update_space_object_invalid_schema(self):
        space_object = self.generate_space_object()

        res = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object),
        )

        assert res.status_code == 200

        new_space_object = {**space_object, "invalid_key": "INVALID VALUE"}

        res = requests.put(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(new_space_object),
        )

        assert res.status_code == 422

        cleanup_res = self.cleanup_test_object(space_object["sat_id"])

        assert cleanup_res.status_code == 200
