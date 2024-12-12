import pika
import time
import json
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from session.models import Session
from utils.storage import download_file_from_gcs

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to consume messages from RabbitMQ, simulate speech-to-text conversion,
    and update the session with the converted text.

    This command listens for messages in a RabbitMQ queue, downloads the associated audio file,
    converts the speech to text, and then updates the corresponding session record with the text.

    Attributes:
        help (str): Description of the command functionality.
    """

    help = "Speech to text converter"

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
                queue="speech_text_converter_queue",
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

        This function decodes the message, downloads the audio file from storage, simulates
        speech-to-text conversion, updates the session with the converted text, and acknowledges
        the message.

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

            bucket_name = 'erentestproject'
            file_name = message["file_path"].split("/")[-1]

            # Download the file from storage
            file = self.get_file_from_storage(
                file_name=file_name,
                bucket_name=bucket_name,
                destination_path=destination_path,
                message=message
            )

            if file:
                # Convert speech to text
                converted_text = self.convert_speech_to_text(file=file)

                # Update session with the converted text
                self.update_session_text(session=session, converted_text=converted_text)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def get_file_from_storage(self, file_name, message, bucket_name, destination_path):
        """
        Simulates downloading a file from Google Cloud Storage (GCS).

        In a real scenario, this function would download the file from the cloud storage.
        Here, it returns a simulated file object for testing purposes.

        Args:
            file_name (str): The name of the file to download.
            message (dict): The message containing additional metadata.
            bucket_name (str): The name of the GCS bucket.
            destination_path (str): The path where the file is stored in GCS.

        Returns:
            dict: A simulated file object (in a real case, this would be the file itself).
        """
        try:
            # Simulate file retrieval (replace with actual GCS file download code)
            # file = download_file_from_gcs(bucket_name=bucket_name, destination_blob_name=destination_path, destination_file_name=file_name)
            file = {"file_name": "storage_file"}  # Simulated response
            logger.info(f"Simulated file download: {file}")
            return file

        except Exception as e:
            logger.error(f"Error downloading file from storage: {str(e)}")
            return None

    def convert_speech_to_text(self, file):
        """
        Simulates the process of converting speech to text.

        Since this requires third-party services, the function is simulated by a sleep
        call to represent the processing time.

        Args:
            file (dict): The file object containing the audio file data.

        Returns:
            str: Simulated converted text.
        """
        try:
            # Simulate speech-to-text conversion with a delay
            time.sleep(60)
            converted_text = self.get_dummy_text()
            logger.info("Speech-to-text conversion completed.")
            return converted_text

        except Exception as e:
            logger.error(f"Error during speech-to-text conversion: {str(e)}")
            return ""

    def get_dummy_text(self):
        """
        Returns a dummy text for testing purposes.

        In a real implementation, this would be the result of speech-to-text conversion.

        Returns:
            str: The dummy text used as a placeholder for actual converted text.
        """
        header = "This dummy text generated for "
        return "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."

    def update_session_text(self, session, converted_text):
        """
        Updates the session record with the converted text.

        Args:
            session (Session): The session object that contains the audio file.
            converted_text (str): The text obtained after converting the speech.
        """
        try:
            session.converted_text = converted_text
            session.save()
            logger.info(f"Session {session.session_id} updated with converted text.")

        except Exception as e:
            logger.error(f"Error updating session {session.session_id} with converted text: {str(e)}")

    def run(self):
        """
        Starts the message consumption process.

        Listens for messages from the specified queue and invokes the callback method for each message.
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
