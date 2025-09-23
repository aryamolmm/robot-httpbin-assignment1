import pika, json, time

class PikaLibrary:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"   # 👈 important so Robot sees it

    def __init__(self):
        self.connection = None
        self.channel = None

    def connect_to_rabbitmq(self, host='localhost', port=5672, username='guest', password='guest', vhost='/'):
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def create_queue(self, queue):
        self.channel.queue_declare(queue=queue)

    def publish_message(self, queue, message):
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)

    def consume_message(self, queue, timeout=5):
        method_frame, header_frame, body = self.channel.basic_get(queue=queue, auto_ack=True)
        start_time = time.time()
        while method_frame is None:
            if time.time() - start_time > timeout:
                raise Exception("Timeout waiting for message")
            method_frame, header_frame, body = self.channel.basic_get(queue=queue, auto_ack=True)
        return body.decode()

    def close_connection(self):
        if self.connection:
            self.connection.close()
