import pika
import json
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from session.models import Session
from publisher.audio_process_publisher import Publisher
from utils.storage import upload_to_gcs

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to consume audio processing messages from a RabbitMQ queue,
    upload the audio file to Google Cloud Storage, and publish the message to the next queue.

    This command listens for messages in a RabbitMQ queue, processes the audio files,
    uploads them to Google Cloud Storage (GCS), and then publishes the result to another queue.

    Attributes:
        help (str): Description of the command functionality.
    """

    help = "Audio Storages"

    def handle(self, *args, **options):
        """
        Handles the RabbitMQ connection and message consumption.

        Establishes a connection to RabbitMQ, consumes messages from a specified queue,
        and invokes the callback function for each received message.

        Args:
            *args: Positional arguments passed to the command.
            **options: Keyword arguments passed to the command.
        """
        try:
            # Establish connection to RabbitMQ
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    settings.RABBITMQ_URI,
                    credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD),
                    virtual_host=settings.VHOST,
                    heartbeat=300,
                    blocked_connection_timeout=600
                )
            )
            self.channel = self.connection.channel()

            # Set up the consumer
            self.channel.basic_consume(
                queue=settings.CONSUME_FROM_QUEUE,
                on_message_callback=self.callback,
                auto_ack=False
            )

            # Start consuming messages
            self.run()

        except Exception as e:
            logger.error(f"Error during command execution: {str(e)}")

    def callback(self, ch, method, properties, body):
        """
        Callback function to process received messages from RabbitMQ.

        This function decodes the message, processes the associated audio file,
        uploads it to Google Cloud Storage, removes the local file, and publishes the
        result to the next RabbitMQ queue.

        Args:
            ch (pika.channel.Channel): The channel object used to communicate with RabbitMQ.
            method (pika.spec.Basic.Deliver): Message delivery information.
            properties (pika.spec.BasicProperties): Message properties.
            body (bytes): The message body as bytes, which is then decoded to a JSON object.
        """
        try:
            message = json.loads(body.decode('utf-8'))
            logger.info(f"Received message: {message}")

            session_id = message["session_id"]
            destination_path = message["directory_name"]
            session = Session.objects.get(session_id=session_id)
            record_file = session.record_file

            bucket_name = 'erentestproject'
            destination_path = f"{destination_path}/{record_file.name}"

            # Upload the file to GCS
            cloud_destination = upload_to_gcs(
                bucket_name=bucket_name,
                source_file=record_file,
                destination_blob_name=destination_path
            )

            message['destination_path'] = cloud_destination

            # Remove the local file after upload
            self.remove_file_from_local(session=session)

            # Publish the result to the next queue
            self.publish_to_next_queue(message=message)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def remove_file_from_local(self, session):
        """
        Removes the local audio file associated with a session and clears the record file field.

        This method ensures that the local file is deleted from the server after being successfully
        uploaded to Google Cloud Storage.

        Args:
            session (Session): The session object containing the record file.
        """
        try:
            file_path = Path(session.record_file.path)  # Get the full file path

            if file_path.exists():  # Check if the file exists in the filesystem
                file_path.unlink()  # Remove the file

            # Optionally, clear the field in the database
            session.record_file = None
            session.save()

            logger.info(f"Local file for session {session.session_id} removed.")

        except Exception as e:
            logger.error(f"Error removing local file for session {session.session_id}: {str(e)}")

    def publish_to_next_queue(self, message):
        """
        Publishes the processed message to the next RabbitMQ queue.

        This method sends the message containing the cloud destination path to the
        next queue for further processing.

        Args:
            message (dict): The message containing the processed data, such as the cloud storage path.
        """
        try:
            publisher = Publisher(routing_key="speech_text_converter", exchange="text_converter")
            publisher.publish(message)
            logger.info(f"Published message to the next queue: {message}")

        except Exception as e:
            logger.error(f"Error publishing message to next queue: {str(e)}")

    def run(self):
        """
        Starts the message consumption process.

        Listens for messages from the specified queue, invoking the `callback` method for each message.
        This method runs in an infinite loop until interrupted.
        """
        logger.info("Starting to consume messages.")
        try:
            self.channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("Interrupted by user. Stopping...")
            self.channel.stop_consuming()

        finally:
            logger.info("Closing connection.")
            self.connection.close()
