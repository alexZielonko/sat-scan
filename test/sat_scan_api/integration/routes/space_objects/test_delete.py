import json, requests
from faker import Faker

from route_helper import RouteHelper


class TestDelete(RouteHelper):
    def test_delete_space_object(self):
        """
        it deletes a space object
        """
        space_object = self.generate_space_object()

        post_res = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object),
        )

        assert post_res.status_code == 200

        initial_get_res = requests.get(
            f"{RouteHelper.BASE_ENDPOINT}/{space_object['sat_id']}",
            headers=self.get_headers(),
        )

        initial_get_res.status_code == 200

        delete_res = requests.delete(
            f"{RouteHelper.BASE_ENDPOINT}/{space_object['sat_id']}",
            headers=self.get_headers(),
        )

        assert delete_res.status_code == 200

        final_get_res = requests.get(
            f"{RouteHelper.BASE_ENDPOINT}/{space_object['sat_id']}",
            headers=self.get_headers(),
        )

        assert final_get_res.status_code == 404

    def test_it_requires_auth(self):
        """
        it returns a 401 if an invalid api key is provided
        """
        fake = Faker()
        delete_res = requests.delete(
            f"{RouteHelper.BASE_ENDPOINT}/{fake.uuid4()}",
            headers={
                **self.get_headers(),
                "Authorization": "Bearer __INVALID_BEARER_TOKEN__",
            },
        )

        assert delete_res.status_code == 401

    def test_get_space_object_by_id_404(self):
        """
        it returns a 404 if the space object is not found
        """
        fake = Faker()
        delete_res = requests.delete(
            f"{RouteHelper.BASE_ENDPOINT}/{fake.uuid4()}",
            headers=self.get_headers(),
        )

        assert delete_res.status_code == 404
