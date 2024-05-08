# #!/usr/bin/env python3

# import json, os, configparser, pika
# from typing import Dict

# from components.data_request import DataRequest
# from components.configuration_parser import ConfigurationParser, DataRequestConfig


# def get_auth_credentials(data_request_name: str) -> Dict[str, str]:
#     directory = os.path.dirname(__file__)
#     file = os.path.join(directory, '../credentials.ini')    
    
#     config = configparser.ConfigParser()
#     config.read(file)

#     username = config.get(data_request_name, "username")
#     password = config.get(data_request_name, "password")

#     return {'identity': username, 'password': password}

# def publish_messages(request_config: DataRequestConfig, data: Dict[str, str]) -> None:
#     routing_key = request_config.routing_key

#     print(f'Publishing message to routing_key: {routing_key}')

#     connection = pika.BlockingConnection(pika.ConnectionParameters('event-collaboration-messaging'))
#     channel = connection.channel()    
#     channel.queue_declare(queue=routing_key)

#     for record in data:
#         channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(record))

#     connection.close()

# if __name__ == "__main__":
#     print('👉 Running space-data-collector')

#     parser = ConfigurationParser()
#     data_requests_config = parser.run()
    
#     for request_config in data_requests_config:
#         auth = get_auth_credentials(data_request_name=request_config.name)
#         data_request = DataRequest(request_config, auth)
#         data = data_request.get()
#         print('DATA!')
#         print(data)
#         # publish_messages(request_config, data)

    
import sys
def lambda_handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'