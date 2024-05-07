#!/usr/bin/env python3

import json, os, configparser, pika
from flask import Flask
from typing import Dict

from components.data_request import DataRequest
from components.configuration_parser import ConfigurationParser, DataRequestConfig

app = Flask(__name__)

def get_auth_credentials(data_request_name: str) -> Dict[str, str]:
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, '../credentials.ini')    
    
    config = configparser.ConfigParser()
    config.read(file)

    username = config.get(data_request_name, "username")
    password = config.get(data_request_name, "password")

    return {'identity': username, 'password': password}

def publish_messages(request_config: DataRequestConfig, data: Dict[str, str]) -> None:
    routing_key = request_config.routing_key

    print(f'Publishing message to routing_key: {routing_key}')

    connection = pika.BlockingConnection(pika.ConnectionParameters('event-collaboration-messaging'))
    channel = connection.channel()    
    channel.queue_declare(queue=routing_key)

    for record in data:
        channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(record))

    connection.close()

@app.route('/health-check')
def health_check():
  return 'Success', 200

if __name__ == "__main__":
    print('👉 Running space-data-collector')
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("👉 Data Collector is up (🆙)")

    # parser = ConfigurationParser()
    # data_requests_config = parser.run()
    
    # for request_config in data_requests_config:
    #     auth = get_auth_credentials(data_request_name=request_config.name)
    #     data_request = DataRequest(request_config, auth)
    #     data = data_request.get()
    #     # publish_messages(request_config, data)

    
    