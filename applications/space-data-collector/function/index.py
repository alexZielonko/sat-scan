#!/usr/bin/env python3

import json
from typing import Dict

from components.data_request import DataRequest
from components.configuration_parser import ConfigurationParser, DataRequestConfig
from components.rabbit_mq_connection_interface import RabbitMqConnectionInterface
from components.mq_broker_config import MqBrokerConfig
from components.get_auth_credentials_for_data_req import (
    get_auth_credentials_for_data_req,
)
from components.get_config import get_config

ROUTE_CONFIG_FILE_PATH = "../route-config.ini"
CREDENTIALS_CONFIG_FILE_PATH = "../credentials.ini"


def publish_messages(request_config: DataRequestConfig, data: Dict[str, str]) -> None:
    routing_key = request_config.routing_key

    print(f"👉 Publishing message to routing_key: {routing_key}")

    rabbit_mq_connection_interface = RabbitMqConnectionInterface(
        broker_config=MqBrokerConfig(config=get_config(ROUTE_CONFIG_FILE_PATH))
    )

    connection = rabbit_mq_connection_interface.establish_connection()
    channel = connection.channel()
    channel.queue_declare(queue=routing_key)

    for record in data:
        print(f"👉 PUBLISHING MESSAGE: {json.dumps(record)}")
        channel.basic_publish(
            exchange="", routing_key=routing_key, body=json.dumps(record)
        )

    connection.close()


def lambda_handler(event, context):
    print("👉 Running space-data-collector")

    parser = ConfigurationParser()
    data_requests_config = parser.run()
    credentials_config = get_config(CREDENTIALS_CONFIG_FILE_PATH)

    for request_config in data_requests_config:
        auth = get_auth_credentials_for_data_req(
            credentials_config=credentials_config, data_request_name=request_config.name
        )
        data_request = DataRequest(request_config, auth)
        data = data_request.get()
        publish_messages(request_config, data)
