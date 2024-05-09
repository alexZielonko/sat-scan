import traceback
from typing import Dict
import pika, ssl, os, json, requests

from app.config_parsers.credentials import Credentials
from app.config_parsers.route_config import RouteConfig

route_config = RouteConfig()

class ResponseStatus:
  def __init__(self, success: bool):
    self.success = bool

class RecentObjectsChannel:
  BASE_API_URL = route_config.api_url

  def __init__(self, sat_scan_api_key):
    try:
      print('📡 Subscribing to recent_objects channel')

      self.credentials = Credentials()
      self.request_headers = self._get_headers(sat_scan_api_key=sat_scan_api_key)

      connection_parameters = self.get_pika_connection_parameters()

      print('CONNECTION PARAMS')
      print(connection_parameters)

      connection = pika.BlockingConnection(connection_parameters)

      channel = connection.channel()
      channel.queue_declare(queue='recent_objects')
      channel.basic_consume(
        queue='recent_objects', 
        on_message_callback=self._process_message, 
        auto_ack=False
      )
      channel.start_consuming()
      
      print('Waiting for recent_objects messages')
    except Exception:
      print('Failed to create recent objects channel')
      traceback.print_exc()

  def get_pika_connection_parameters(self):
    print('GETTING PIKA CONNECTION PARAMS')
    config = route_config.mq_broker

    if config.env == 'PROD':
        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        url = f"amqps://{config.user}:{config.password}@{config.broker_id}.mq.{config.region}.amazonaws.com:5671"

        print('PIKE CONNECTION URL')
        print(url)

        parameters = pika.URLParameters(url)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)
        
        return parameters
    
    docker_compose_instance_name = 'event-collaboration-messaging'
    return pika.ConnectionParameters(docker_compose_instance_name)

  def _get_headers(self, sat_scan_api_key) -> Dict[str, str]:
    return {
      'Authorization': 'Bearer ' + sat_scan_api_key,
      'Content-Type': 'application/json'
    }

  def _normalize_message_body(self, message_body) -> Dict[str, str]:
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
  
  def _get_space_objects_api_path(self) -> str:
    return f'{RecentObjectsChannel.BASE_API_URL}/space-objects'
  
  def _has_space_object(self, satellite_id) -> bool:
      try:          
        url = f'{self._get_space_objects_api_path()}/{satellite_id}'
        res = requests.get(url)
        return bool(res.json()['sat_id'])
      except:
         return False
  
  def _update_space_object(self, space_object) -> ResponseStatus:
    try:
      print(f'Updating space object: {json.dumps(space_object)}')

      res = requests.put(
        self._get_space_objects_api_path(), 
        headers=self.request_headers, 
        data=json.dumps(space_object)
      )
      
      if (res.status_code == 200):
        return ResponseStatus(True)
      else:
        return ResponseStatus(False)
    except Exception as err:
      print(err)
      return ResponseStatus(False)
    
  def _create_space_object(self, space_object) -> ResponseStatus:
    try:
      print(f'Creating space object: {json.dumps(space_object)}')

      res = requests.post(
        self._get_space_objects_api_path(), 
        headers=self.request_headers,
        data=json.dumps(space_object)
      )

      if (res.status_code == 200):
        return ResponseStatus(True)
      else:
        return ResponseStatus(False)
    except Exception as err:
      print(err)
      return ResponseStatus(False)
  
  def _create_or_update(self, space_object) -> ResponseStatus:
    if self._has_space_object(space_object["sat_id"]):
      return self._update_space_object(space_object)
    else:
      return self._create_space_object(space_object)

  def _process_message(self, ch, method, properties, message_body):
    try:
      print("Processing message: %r" % message_body)

      message_body = json.loads(message_body)
      formatted_body = self._normalize_message_body(message_body=message_body)
      response_status = self._create_or_update(space_object=formatted_body)

      if response_status.success:
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except Exception:
      print('Failed to process message')
      traceback.print_exc()

