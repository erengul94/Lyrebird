import pika
import json

import bson

class AudioStorageProcessPublisher:
    def __init__(self, routing_key, exchange):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost',
                                      credentials=pika.PlainCredentials("cool", "test3142"),
                                      virtual_host="lyrebird",
                                      heartbeat=600, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.routing_key = routing_key
        self.exchange = exchange
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct',  # Change to 'fanout', 'topic', etc., as needed
            durable=True  # Ensures the exchange survives a broker restart
        )

        self.queue_name = f"{routing_key}_queue"
        self.routing_key = routing_key
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue_name,
            routing_key=self.routing_key
        )
        print(f"Setup complete: Virtual host lyrebird, Exchange {exchange}, Queue {self.queue_name}")



    def publish(self, body):
        try:

            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(delivery_mode=2)  # Makes message persistent
            )
        except pika.exceptions.AMQPError as e:
            print(str(e))
        except Exception as e:
            print(str(e))