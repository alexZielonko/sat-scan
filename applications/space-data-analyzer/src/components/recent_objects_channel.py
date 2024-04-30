import pika, sys, os, json

class RecentObjectsChannel:
  def __init__(self):
    print(' [*] Starting recent objects channel')
    connection = pika.BlockingConnection(pika.ConnectionParameters('event-collaboration-messaging'))
    channel = connection.channel()
    channel.queue_declare(queue='recent_objects')
    channel.basic_consume(queue='recent_objects', on_message_callback=self._process_message, auto_ack=True)
    channel.start_consuming()
    print(' [*] Waiting for messages. To exit press CTRL+C')

  def _process_message(self, ch, method, properties, message_body):
    message_body = json.loads(message_body)
    print(" [x] Received %r" % message_body)

