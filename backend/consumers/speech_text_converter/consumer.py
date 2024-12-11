import pika
import json
import requests
import logging
import random
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpechTextConverterConsumer(object):
    def __init__(self, slot_machine_api_url,
                 channel, consumer_queue_name, routing_key, exchange):
        self.channel = channel
        self.consumer_queue_name = consumer_queue_name
        self.routing_key = routing_key
        self.exchange = exchange
        self.slot_machine_api_url = slot_machine_api_url


        logger.info(f"Setting up consumer on queue: {consumer_queue_name}")
        self.channel.basic_consume(
            queue=self.consumer_queue_name,
            on_message_callback=self.callback,
            auto_ack=False
            )

    @staticmethod
    def generate_random_for_number():
        """
        Generate a list of 4 random numbers, each between 0 and 11 (inclusive).

        :return: List of 4 random numbers
        """
        return [random.randint(0, 11) for _ in range(4)]

    def create_game_session(self, message):
        """
        Checks any free slot machine available
        :return: True if a slot machine is available, False otherwise
        """
        initial_session_number = self.generate_random_for_number()
        try:
            response = requests.post(url=f"{self.slot_machine_api_url}/create/gamesession",
                                    data=json.dumps({"user_id": message["user_id"],
                                                     "initial_session_number": '/'.join(str(x) for x in initial_session_number),
                                                     "slot_machine_id": message["slot_machine_id"]
                                                     }),
                                    headers={'Content-Type': 'application/json'}
                                     )
            response.raise_for_status()
            logger.info("Slot machine check successful. Slot machine is available.")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking slot machine availability: {e}")
            return response

    def check_available_slot_machine(self, message):
        """
        Checks any free slot machine available
        :return: True if a slot machine is available, False otherwise
        """
        try:
            response = requests.post(url=f"{self.slot_machine_api_url}/slotmachine/check",
                                    data=json.dumps({"user_id": message["user_id"], "username": message["username"]}),
                                    headers={'Content-Type': 'application/json'}
                                     )
            response.raise_for_status()
            logger.info("Slot machine check successful. Slot machine is available.")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking slot machine availability: {e}")
            return response

    def get_user(self, message):
        """
        Notify user via the WebSocket server.
        :param user_id: ID of the user to notify
        :param message: The notification message
        """
        user_id = message["user_id"]
        try:
            response = requests.get(
                url=f"http://127.0.0.1:8000/users/{int(user_id)}",  # WebSocket server endpoint
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user {user_id}: {str(e)}")
            return response

    def notify_user(self, message):
        """
        Notify user via the WebSocket server.
        :param user_id: ID of the user to notify
        :param message: The notification message
        """
        user_id = message["user_id"]
        try:
            response = requests.post(
                url=f"http://127.0.0.1:5001/notify_user",  # WebSocket server endpoint
                json={"user_id": str(user_id), "message": message}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to notify user {user_id}: {str(e)}")

    def publish(self):
        """
        Publish message to channel
        :return:
        """
        try:
            event = {
                "event_id": 7,
                "event_name": "update_user_total_token"
            }
            logger.info(f"Publishing event: {event}")
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=json.dumps(event))
        except pika.exceptions.AMQPError as e:
            logger.error(f"AMQP Error while publishing: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while publishing: {e}")

    def give_bonus(self):
        """
        If the user has logged in the last 24 hours, they are awarded a 1 credit bonus token
        :return: True if bonus is given
        """
        self.publish()
        logger.info("User awarded with 1 credit bonus token.")
        return True

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        logger.info(f"Received message: {message}")

        #TODO: code optimization !!!
        available_slot_machine = self.check_available_slot_machine(message=message)
        if available_slot_machine.status_code == 200:
            message["slot_machine_id"] = available_slot_machine.json()["slot_machine_id"]
            response = self.get_user(message=message)
            if response.status_code == 200:
                user = response.json()
                message["token_count"] = user["token_count"]
                response = self.create_game_session(message=message)
                if response.status_code == 201:
                    game_session = response.json()
                    initial_session_number = game_session["initial_session_number"]
                    game_session_id = game_session["game_session_id"]
                    message["game_session_id"] = game_session_id
                    message["initial_session_number"] = [int(x) for x in initial_session_number.split("/")]
                    self.notify_user(message)
                    # self.give_bonus()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

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

    parser = EnvArgumentParser(description='Slot Availability Service')

    # CONNECTIONS
    parser.add_argument('--slot-machine-api-url', metavar='SLOT_MACHINE_API_URL',
                        default='http:://localhost:8000',
                        help='Slot Machine API URL',
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

    service = SpechTextConverterConsumer(slot_machine_api_url=args.slot_machine_api_url,
                                      channel=channel, consumer_queue_name=args.consume_from_queue,
                                      routing_key=args.publish_to_routing_key, exchange=args.publish_to_exchange)

    service.run()