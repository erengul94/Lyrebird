import pika
import json
import requests
import logging
import random

from storage import upload_to_gcs

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioStorageConsumer(object):
    def __init__(self, web_app_url,
                 channel, consumer_queue_name, routing_key, exchange):
        self.channel = channel
        self.consumer_queue_name = consumer_queue_name
        self.routing_key = routing_key
        self.exchange = exchange
        self.web_app_url = web_app_url


        logger.info(f"Setting up consumer on queue: {consumer_queue_name}")
        self.channel.basic_consume(
            queue=self.consumer_queue_name,
            on_message_callback=self.callback,
            auto_ack=False
            )


    def publish(self):
        """
        Publish message to channel
        :return:
        """
        try:
            event = {
                "session_id": 1,
                "event_name": "speech_text_converter"
            }
            logger.info(f"Publishing event: {event}")
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=json.dumps(event))
        except pika.exceptions.AMQPError as e:
            logger.error(f"AMQP Error while publishing: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while publishing: {e}")


    def callback(self, ch, method, properties, body):
        import base64
        message = json.loads(body.decode('utf-8'))
        logger.info(f"Received message: {message}")
        audio_data = base64.b64decode(message['audio_data'])
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb') as temp_file:
            temp_file.write(audio_data)
            temp_file_name = temp_file.name
        bucket_name = 'erentestproject'
        destination_path = f'test_audio/{temp_file_name}'
        public_url = upload_to_gcs(bucket_name, temp_file, destination_path)
        self.publish()
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def run(self):
        logger.info("Starting to consume messages.")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Interrupted by user. Stopping...")
            self.channel.stop_consuming()
        finally:
            logger.info("Closing connection.")
            connection.close()

if __name__ == '__main__':
    from parser import EnvArgumentParser

    parser = EnvArgumentParser(description='Audio Storage Consumer')

    # CONNECTIONS
    parser.add_argument('--web-app-url', metavar='WEB_APP_URL',
                        default='http:://localhost:8000',
                        help='WEB APP URL',
                        required=True)

    # CONSUME FROM
    parser.add_argument('--rabbitmq-uri', metavar='RABBITMQ_URI',
                        required=True,
                        help='URI of the source AMQP server')
    parser.add_argument('--rabbitmq-username', metavar='RABBITMQ_USERNAME',
                        required=True,
                        help='URI of the source AMQP server username')
    parser.add_argument('--rabbitmq-password', metavar='RABBITMQ_PASSWORD',
                        required=True,
                        help='URI of the source AMQP server password')
    parser.add_argument('--vhost', metavar='VHOST',
                        required=True,
                        help='Name of the source vhost')

    parser.add_argument('--consume-from-queue', metavar='CONSUME_FROM_QUEUE', required=True,
                        help='Name of the source queue')

    parser.add_argument('--publish-to-exchange', metavar='PUBLISH_TO_EXCHANGE', required=True,
                        help='Name of the target exchange')

    parser.add_argument('--publish-to-routing-key', metavar='PUBLISH_TO_ROUTING_KEY', required=True,
                        help='Name of the target routing key')

    parser.add_argument('--consume-from-exchange', metavar='CONSUME_FROM_EXCHANGE', required=True,
                        help='Name of the target exchange')

    parser.add_argument('--rabbitmq-heartbeat', metavar='RABBITMQ_HEARTBEAT',
                        help='Heartbeat interval for RabbitMQ', default=600)

    parser.add_argument('--rabbitmq-timeout', metavar='RABBITMQ_TIMEOUT',
                        help='Timeout for RabbitMQ connection', default=300)

    args = parser.parse_args()

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(args.rabbitmq_uri,
                                      credentials=pika.PlainCredentials(args.rabbitmq_username, args.rabbitmq_password),
                                      virtual_host=args.vhost,
                                      heartbeat=args.rabbitmq_heartbeat,
                                      blocked_connection_timeout=args.rabbitmq_timeout)
        )
        channel = connection.channel()
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        raise

    service = AudioStorageConsumer(web_app_url=args.web_app_url,
                                      channel=channel, consumer_queue_name=args.consume_from_queue,
                                      routing_key=args.publish_to_routing_key, exchange=args.publish_to_exchange)

    service.run()