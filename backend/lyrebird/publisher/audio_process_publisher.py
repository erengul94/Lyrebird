import pika
import json
import logging


class Publisher:
    """
    Publisher class to send messages to a RabbitMQ exchange with a specified routing key.

    This class connects to a RabbitMQ server, declares an exchange, and creates a queue that
    is bound to that exchange using the provided routing key. It also includes a method for
    publishing messages to the exchange.

    Attributes:
        connection (pika.BlockingConnection): A connection to the RabbitMQ server.
        channel (pika.channel.Channel): The communication channel to the RabbitMQ server.
        routing_key (str): The routing key to use for binding the queue and publishing messages.
        exchange (str): The name of the exchange to publish messages to.
        queue_name (str): The name of the queue created and bound to the exchange.
    """

    def __init__(self, routing_key, exchange):
        """
        Initializes the Publisher class by establishing a connection to RabbitMQ,
        declaring an exchange and a queue, and binding the queue to the exchange.

        Args:
            routing_key (str): The routing key to bind the queue to the exchange.
            exchange (str): The name of the exchange.
        """
        # Setup logger
        self.logger = logging.getLogger(__name__)

        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    'localhost',
                    credentials=pika.PlainCredentials("cool", "test3142"),
                    virtual_host="lyrebird",
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
            self.routing_key = routing_key
            self.exchange = exchange

            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='direct',  # You can change the type to 'fanout', 'topic', etc.
                durable=True  # Ensures exchange survives broker restart
            )

            # Declare queue
            self.queue_name = f"{routing_key}_queue"
            self.channel.queue_declare(queue=self.queue_name, durable=True)

            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=self.routing_key
            )

            self.logger.info(
                f"Setup complete: Virtual host 'lyrebird', Exchange '{exchange}', Queue '{self.queue_name}'")

        except Exception as e:
            self.logger.error(f"Error during initialization: {str(e)}")
            raise

    def publish(self, body):
        """
        Publishes a message to the RabbitMQ exchange with the specified routing key.

        Args:
            body (dict): The message body to be sent as a JSON-encoded string.

        Raises:
            Exception: If any error occurs while publishing the message.
        """
        try:
            # Convert the message body to JSON
            message_body = json.dumps(body)

            # Publish message to exchange with persistent delivery mode
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=message_body,
                properties=pika.BasicProperties(delivery_mode=2)  # Makes message persistent
            )

            self.logger.info(f"Message published to {self.exchange} with routing key {self.routing_key}")

        except pika.exceptions.AMQPError as e:
            self.logger.error(f"AMQP Error while publishing message: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error while publishing message: {str(e)}")
