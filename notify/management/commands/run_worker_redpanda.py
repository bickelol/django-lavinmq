# my_django_app/management/commands/run_consumer.py
import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Starts a long-running Redpanda consumer worker process."

    def handle(self, *args, **options):
        # Configure consumer-specific properties alongside global config
        consumer_config = settings.REDPANDA_CONFIG.copy()
        consumer_config.update({
            'group.id': 'django-auth-consumer-group',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False, # Manual commit for reliability
        })

        consumer = Consumer(consumer_config)
        topic = settings.REDPANDA_TOPICS['redpanda_notifications']
        consumer.subscribe([topic])

        self.stdout.write(self.style.SUCCESS(f"Listening to Redpanda topic: {topic}..."))

        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Process the message
                key = msg.key().decode('utf-8') if msg.key() else None
                value = json.loads(msg.value().decode('utf-8'))

                self.stdout.write(f"Processing Event | Key: {key} | Data: {value}")

                # --- EXECUTE YOUR DJANGO DB OR BUSINESS LOGIC HERE ---
                # e.g., Send a welcome email, update analytics database, etc.

                # Explicitly commit offset after successful processing
                consumer.commit(asynchronous=False)

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Aborting consumer..."))
        finally:
            consumer.close()