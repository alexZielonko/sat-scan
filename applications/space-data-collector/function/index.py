#!/usr/bin/env python3

import ssl, json, os, configparser, pika
from typing import Dict

from components.data_request import DataRequest
from components.configuration_parser import ConfigurationParser, DataRequestConfig


ROUTE_CONFIG_FILE_PATH = './route-config.ini'
CREDENTIALS_CONFIG_FILE_PATH = './credentials.ini'

def get_config(file_path: str):
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, file_path)
    
    config = configparser.ConfigParser()
    config.read(file)

    return config

class MqBrokerConfig:
    config_key = 'mq_broker'

    def __init__(self):
        config = get_config(ROUTE_CONFIG_FILE_PATH)
        self.env = config.get(MqBrokerConfig.config_key, 'env')
        self.user = config.get(MqBrokerConfig.config_key, 'rabbitmq_user')
        self.password = config.get(MqBrokerConfig.config_key, 'rabbitmq_password')
        self.broker_id = config.get(MqBrokerConfig.config_key, 'rabbitmq_broker_id')
        self.region = config.get(MqBrokerConfig.config_key, 'rabbitmq_region')

def get_auth_credentials(data_request_name: str) -> Dict[str, str]:
    config = get_config(CREDENTIALS_CONFIG_FILE_PATH)
    username = config.get(data_request_name, "username")
    password = config.get(data_request_name, "password")

    return {'identity': username, 'password': password}

def get_pika_connection_parameters():
    config = MqBrokerConfig()

    if config.env == 'PROD':
        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        url = f"amqps://{config.user}:{config.password}@{config.broker_id}.mq.{config.region}.amazonaws.com:5671"

        print('CONNECTION URL:')
        print(url)

        parameters = pika.URLParameters(url)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)
        
        return parameters
    
    docker_compose_instance_name = 'event-collaboration-messaging'
    return pika.ConnectionParameters(docker_compose_instance_name)

def publish_messages(request_config: DataRequestConfig, data: Dict[str, str]) -> None:
    routing_key = request_config.routing_key

    print(f'👉 Publishing message to routing_key: {routing_key}')

    connection_parameters = get_pika_connection_parameters()

    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()    
    channel.queue_declare(queue=routing_key)

    for record in data:
        print(f'👉 PUBLISHING MESSAGE: {json.dumps(record)}')
        channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(record))

    connection.close()

def lambda_handler(event, context):
    print('👉 Running space-data-collector')

    parser = ConfigurationParser()
    data_requests_config = parser.run()

    for request_config in data_requests_config:
        auth = get_auth_credentials(data_request_name=request_config.name)
        data_request = DataRequest(request_config, auth)
        data = data_request.get()
        publish_messages(request_config, data)
