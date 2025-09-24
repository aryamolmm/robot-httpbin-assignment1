import pika
import time
import threading


class RabbitMQLibrary:
    """A custom library for Robot Framework to interact with RabbitMQ."""

    def __init__(self, host='localhost', port=5672):
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None

    def connect_to_rabbitmq(self):
        """Establishes a connection to the RabbitMQ server."""
        print(f"Connecting to RabbitMQ at {self.host}:{self.port}")
        max_retries = 10
        retry_delay = 5
        for attempt in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                self.channel = self.connection.channel()
                print("Successfully connected to RabbitMQ.")
                return True
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Attempt {attempt + 1}/{max_retries}: Failed to connect to RabbitMQ: {e}")
                time.sleep(retry_delay)
        raise ConnectionError("Could not connect to RabbitMQ after multiple retries.")

    def publish_message(self, exchange, routing_key, message_body):
        """Publishes a message to a RabbitMQ exchange."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ. Call 'Connect To RabbitMQ' first.")

        self.channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        print(f"Published message: '{message_body}' to exchange '{exchange}' with routing key '{routing_key}'")

    def consume_message_and_validate(self, queue_name, expected_message_body, timeout=10):
        """
        Consumes a message from a queue and validates its content.
        This is a blocking function that waits for a message.
        """
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ. Call 'Connect To RabbitMQ' first.")

        # Declare the queue and bind it to the default exchange (or a temporary one)
        self.channel.queue_declare(queue=queue_name, durable=False, exclusive=True)
        print(f"Waiting for message on queue '{queue_name}'...")

        received_message_body = None
        message_received_event = threading.Event()

        def on_message_callback(ch, method, properties, body):
            nonlocal received_message_body
            received_message_body = body.decode('utf-8')
            print(f"Received message: '{received_message_body}'")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            message_received_event.set()  # Signal that the message has been received

        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

        # Use a separate thread to run the consumer in the background
        consumer_thread = threading.Thread(target=self.channel.start_consuming, daemon=True)
        consumer_thread.start()

        # Wait for the message to be received, with a timeout
        message_received = message_received_event.wait(timeout)
        self.channel.stop_consuming()

        if not message_received:
            raise AssertionError(f"Timeout: No message received on queue '{queue_name}' within {timeout} seconds.")

        # Validate the message content
        if received_message_body != expected_message_body:
            raise AssertionError(
                f"Message mismatch! Expected '{expected_message_body}', but received '{received_message_body}'"
            )
        print("Message content validated successfully.")

        # Cleanup the temporary queue after validation
        self.channel.queue_delete(queue=queue_name)

    def close_connection(self):
        """Closes the connection to RabbitMQ."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("RabbitMQ connection closed.")
