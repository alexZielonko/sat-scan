import json, requests

from route_helper import RouteHelper

class TestCreate(RouteHelper):
  def test_create_space_object_success(self):
    """
    it creates a new space object
    """
    space_object = self.generate_space_object()

    post_res = requests.post(
        RouteHelper.BASE_ENDPOINT,
        headers=self.get_headers(),
        data=json.dumps(space_object)
    )

    assert post_res.status_code == 200

    cleanup_res = self.cleanup_test_object(space_object['sat_id'])

    assert cleanup_res.status_code == 200

  def test_it_requires_auth(self):
    """
    it returns a 401 if an invalid api key is provided
    """
    space_object = self.generate_space_object()

    post_res = requests.post(
        RouteHelper.BASE_ENDPOINT,
        headers={
          **self.get_headers(),
          'Authorization': 'Bearer __INVALID_BEARER_TOKEN__'
        },
        data=json.dumps(space_object)
    )

    assert post_res.status_code == 401

  def test_create_space_object_invalid_schema(self):
    """
    it returns a 422 when POSTing an invalid space object
    """
    space_object = {
      **self.generate_space_object(),
      "invalid_key": "INVALID VALUE"
    }

    post_res = requests.post(
        RouteHelper.BASE_ENDPOINT,
        headers=self.get_headers(),
        data=json.dumps(space_object)
    )

    assert post_res.status_code == 422

    get_res = requests.get(
        f'{RouteHelper.BASE_ENDPOINT}/{space_object["sat_id"]}',
        headers=self.get_headers(),
    )

    assert get_res.status_code == 404

  def test_create_space_object_duplicate_object(self):
    """
    it returns a 409 when POSTing a space object that already exists
    """
    space_object = self.generate_space_object()

    initial_res = requests.post(
        RouteHelper.BASE_ENDPOINT,
        headers=self.get_headers(),
        data=json.dumps(space_object)
    )

    assert initial_res.status_code == 200

    second_res = requests.post(
        RouteHelper.BASE_ENDPOINT,
        headers=self.get_headers(),
        data=json.dumps(space_object)
    )

    assert second_res.status_code == 409

    cleanup_res = self.cleanup_test_object(space_object['sat_id'])

    assert cleanup_res.status_code == 200

