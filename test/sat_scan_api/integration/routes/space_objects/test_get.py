import json, requests
from faker import Faker

from route_helper import RouteHelper


class TestGet(RouteHelper):
    def test_get_all_space_objects(self):
        """
        it returns a list of space objects
        """
        space_object_a = self.generate_space_object()
        space_object_b = self.generate_space_object()

        create_res_a = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object_a),
        )

        create_res_b = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object_b),
        )

        assert create_res_a.status_code == 200
        assert create_res_b.status_code == 200

        get_res = requests.get(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
        )

        assert get_res.status_code == 200

        space_object_ids = list(map(lambda object: object["sat_id"], get_res.json()))

        assert space_object_a["sat_id"] in space_object_ids
        assert space_object_b["sat_id"] in space_object_ids

        cleanup_space_object_a_res = self.cleanup_test_object(space_object_a["sat_id"])
        cleanup_space_object_b_res = self.cleanup_test_object(space_object_b["sat_id"])

        assert cleanup_space_object_a_res.status_code == 200
        assert cleanup_space_object_b_res.status_code == 200

    def test_get_space_object_by_id(self):
        """
        it returns a single space object
        """
        space_object = self.generate_space_object()

        post_res = requests.post(
            RouteHelper.BASE_ENDPOINT,
            headers=self.get_headers(),
            data=json.dumps(space_object),
        )

        assert post_res.status_code == 200

        get_res = requests.get(
            f"{RouteHelper.BASE_ENDPOINT}/{space_object['sat_id']}",
            headers=self.get_headers(),
        )

        assert get_res.status_code == 200
        assert get_res.json() == space_object

        cleanup_res = self.cleanup_test_object(space_object["sat_id"])

        assert cleanup_res.status_code == 200

    def test_get_space_object_by_id_404(self):
        """
        it returns a 404 if the space object is not found
        """
        fake = Faker()
        get_res = requests.get(
            f"{RouteHelper.BASE_ENDPOINT}/{fake.uuid4()}",
            headers=self.get_headers(),
        )

        assert get_res.status_code == 404
