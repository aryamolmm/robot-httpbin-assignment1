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

    def publish_message(self, queue, message, durable=False):
        self.channel.queue_declare(queue=queue, durable=durable)
        body = json.dumps(message) if not isinstance(message, str) else message
        self.channel.basic_publish(exchange='', routing_key=queue, body=body)

    def consume_message(self, queue, timeout=5):
        start = time.time()
        while time.time() - start < timeout:
            method, header, body = self.channel.basic_get(queue=queue, auto_ack=True)
            if method:
                return body.decode()
            time.sleep(0.2)
        return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
