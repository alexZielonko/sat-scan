import traceback
from typing import Dict
import json, requests

from components.interfaces.response_status import ResponseStatus
from components.interfaces.rabbit_mq_connection_interface import RabbitMqConnectionInterface


class RecentObjectsChannel:

    def __init__(self, sat_scan_api_key, route_config):
        self.route_config = route_config
        self.request_headers = self._get_headers(sat_scan_api_key=sat_scan_api_key)

    def start(self):
        try:
            print("📡 Subscribing to recent_objects channel")

            rabbit_mq_connection_interface = RabbitMqConnectionInterface(
                self.route_config
            )
            connection = rabbit_mq_connection_interface.establish_connection()

            channel = connection.channel()
            channel.queue_declare(queue="recent_objects")
            channel.basic_consume(
                queue="recent_objects",
                on_message_callback=self._process_message,
                auto_ack=False,
            )
            channel.start_consuming()
        except Exception:
            print("Failed to create recent objects channel")
            traceback.print_exc()

    def _get_headers(self, sat_scan_api_key) -> Dict[str, str]:
        return {
            "Authorization": "Bearer " + sat_scan_api_key,
            "Content-Type": "application/json",
        }

    def _normalize_message_body(self, message_body) -> Dict[str, str]:
        try:
            return {
                "sat_id": message_body["INTLDES"],
                "sat_catalog_number": message_body["NORAD_CAT_ID"],
                "object_type": message_body["OBJECT_TYPE"],
                "sat_name": message_body["SATNAME"],
                "launch_country": message_body["COUNTRY"],
                "launch_date": message_body["LAUNCH"],
                "launch_site": message_body["SITE"],
                "file_id": message_body["FILE"],
                "launch_year": message_body["LAUNCH_YEAR"],
                "launch_number": message_body["LAUNCH_NUM"],
                "launch_piece": message_body["LAUNCH_PIECE"],
                "object_name": message_body["OBJECT_NAME"],
                "object_id": message_body["OBJECT_ID"],
                "object_number": message_body["OBJECT_NUMBER"],
            }
        except Exception:
            print("Failed to normalize message body")
            traceback.print_exc()
            return {}

    def _get_space_objects_api_path(self) -> str:
        return f"{self.route_config.api_url}/space-objects"

    def _has_space_object(self, satellite_id) -> bool:
        try:
            url = f"{self._get_space_objects_api_path()}/{satellite_id}"
            res = requests.get(url)
            return "sat_id" in res.json()
        except:
            print("Failed to get space object")
            traceback.print_exc()
            return False

    def _update_space_object(self, space_object) -> ResponseStatus:
        try:
            print(f"Updating space object: {json.dumps(space_object)}")

            res = requests.put(
                self._get_space_objects_api_path(),
                headers=self.request_headers,
                data=json.dumps(space_object),
            )

            if res.status_code == 200:
                return ResponseStatus(True)
            else:
                return ResponseStatus(False)
        except Exception as err:
            print("Failed to update space object")
            traceback.print_exc()
            return ResponseStatus(False)

    def _create_space_object(self, space_object) -> ResponseStatus:
        try:
            print(f"Creating space object: {json.dumps(space_object)}")

            res = requests.post(
                self._get_space_objects_api_path(),
                headers=self.request_headers,
                data=json.dumps(space_object),
            )

            if res.status_code == 200:
                return ResponseStatus(True)
            else:
                return ResponseStatus(False)
        except Exception as err:
            print("Failed to create space object")
            traceback.print_exc()
            return ResponseStatus(False)

    def _create_or_update(self, space_object) -> ResponseStatus:
        try:
            if self._has_space_object(space_object["sat_id"]):
                return self._update_space_object(space_object)
            else:
                return self._create_space_object(space_object)
        except Exception:
            print("Failed to create or update space object")
            traceback.print_exc()
            return ResponseStatus(success=False)

    def _process_message(self, ch, method, properties, message_body):
        try:
            print("Processing message: %r" % message_body)

            message_body = json.loads(message_body)
            formatted_body = self._normalize_message_body(message_body=message_body)
            response_status = self._create_or_update(space_object=formatted_body)

            if response_status.success:
                print("Acknowledging message processing success")
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            print("Failed to process message")
            traceback.print_exc()
