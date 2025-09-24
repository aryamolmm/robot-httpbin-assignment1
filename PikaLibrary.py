import pika
import time
import threading


class PikaLibrary:
    """A custom library for Robot Framework to interact with RabbitMQ.

    This library provides keywords for connecting, publishing, consuming,
    and closing a connection to a RabbitMQ server.
    """
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        """Initializes the library with no active connection."""
        self.connection = None
        self.channel = None

    def connect_to_rabbitmq(self, host='localhost', port=5672, username='guest', password='guest', vhost='/'):
        """Establishes a connection to the RabbitMQ server.

        This keyword handles retries to ensure a connection is established,
        which is important in CI/CD environments where services might
        start at slightly different times.
        """
        print(f"Connecting to RabbitMQ at {host}:{port}")
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials)
        max_retries = 10
        retry_delay = 5  # seconds
        for attempt in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(params)
                self.channel = self.connection.channel()
                print("Successfully connected to RabbitMQ.")
                return True
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Attempt {attempt + 1}/{max_retries}: Failed to connect to RabbitMQ: {e}")
                time.sleep(retry_delay)
        raise ConnectionError("Could not connect to RabbitMQ after multiple retries.")

    def create_queue(self, queue):
        """Creates a durable queue on the RabbitMQ server."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ. Call 'Connect To Rabbitmq' first.")
        self.channel.queue_declare(queue=queue, durable=True)
        print(f"Created queue: '{queue}'")

    def publish_message(self, queue, message):
        """Publishes a message to a RabbitMQ queue.

        This keyword publishes a persistent message to a specific queue.
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ. Call 'Connect To Rabbitmq' first.")
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message.encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,  # makes message persistent
            )
        )
        print(f"Published message: '{message}' to queue '{queue}'")

    def consume_message(self, queue, timeout=10):
        """Consumes a single message from a queue and returns it.

        This method uses a reliable, blocking approach with a timeout to
        ensure the message is received, which is better for testing than
        simple polling.
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ. Call 'Connect To Rabbitmq' first.")

        received_message = None
        message_received_event = threading.Event()

        def on_message_callback(ch, method, properties, body):
            nonlocal received_message
            received_message = body.decode('utf-8')
            print(f"Received message: '{received_message}'")
            # Acknowledge the message so it's removed from the queue
            ch.basic_ack(delivery_tag=method.delivery_tag)
            message_received_event.set()

        # Start consuming in a background thread
        self.channel.basic_consume(queue=queue, on_message_callback=on_message_callback, auto_ack=False)

        # We start consuming on a separate thread to allow a timeout
        consumer_thread = threading.Thread(target=self.channel.start_consuming, daemon=True)
        consumer_thread.start()

        # Wait for the message to be received
        message_received = message_received_event.wait(timeout)

        # Stop consuming and clean up the thread
        if consumer_thread.is_alive():
            self.channel.stop_consuming()
            consumer_thread.join()

        if not message_received:
            raise Exception(f"Timeout waiting for message on queue '{queue}' after {timeout} seconds.")

        return received_message

    def close_connection(self):
        """Closes the connection to the RabbitMQ server."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("RabbitMQ connection closed.")
