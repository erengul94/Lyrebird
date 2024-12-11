from django.core.management.base import BaseCommand

import pika

from session.models import Session
import logging
import json
from django.conf import settings
from utils.storage import upload_to_gcs
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Audio Storages"

    def handle(self, *args, **options):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(settings.RABBITMQ_URI,
                                      credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD),
                                      virtual_host=settings.VHOST,
                                      heartbeat=300,
                                      blocked_connection_timeout=600)
        )
        self.channel = self.connection.channel()
        self.channel.basic_consume(
            queue=settings.CONSUME_FROM_QUEUE,
            on_message_callback=self.callback,
            auto_ack=False
        )
        self.run()

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        logger.info(f"Received message: {message}")
        session = Session.objects.get(session_id="f5be9c1b-6678-4fa6-bff1-1d4a1780450b")
        record_file = session.record_file
        bucket_name = 'erentestproject'
        destination_path = f'test_audio/{record_file.name}'
        upload_to_gcs(bucket_name, record_file, destination_path)
        self.remove_file_from_local(session=session)


    def remove_file_from_local(self, session):
        file_path = Path(session.record_file.path)  # Get the full file path

        if file_path.exists():  # Check if the file exists in the filesystem
            file_path.unlink()  # Remove the file

        # Optionally, clear the field in the database
        session.record_file = None
        session.save()



    def run(self):
        logger.info("Starting to consume messages.")
        try:
            self.channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("Interrupted by user. Stopping...")
            self.channel.stop_consuming()
        finally:
            logger.info("Closing connection.")
            self.connection.close()



