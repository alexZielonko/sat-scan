from typing import Dict
from faker import Faker

from flask import Response
import requests


class RouteHelper:
  BASE_ENDPOINT = 'http://localhost:5000/space-objects'

  INTEGRATION_TEST_API_KEY = 'integration_test_key'

  def get_headers(self) -> Dict[str, str]:
    return {
      "Authorization": f"Bearer {RouteHelper.INTEGRATION_TEST_API_KEY}",
      "Content-Type": "application/json",
    }

  def cleanup_test_object(self, space_object_id: str) -> Response:
    url = f'{RouteHelper.BASE_ENDPOINT}/{space_object_id}'
    return requests.delete(
        url,
        headers=self.get_headers(),
    )

  def generate_space_object(self):
    fake = Faker()

    sat_name = f"satellite name: {fake.name()}"
    catalog_number = f'{fake.random_number(10)}'

    return {
      "sat_id": fake.uuid4(),
      "sat_catalog_number": catalog_number,
      "object_type": "UNKNOWN",
      "sat_name": sat_name,
      "launch_country": "TBD",
      "launch_date": f'{fake.past_date()}',
      "launch_site": fake.uuid4(),
      "file_id": f'{fake.random_number(4)}',
      "launch_year": fake.year(),
      "launch_number": f'{fake.random_number(3)}',
      "launch_piece": f'{fake.random_letter()}',
      "object_name": sat_name,
      "object_id": fake.uuid4(),
      "object_number": catalog_number
    }  