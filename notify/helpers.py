import pika, json
from confluent_kafka import Producer
from django.conf import settings

#### LAVIN MQ
def lavinmq_queue_notification(user_id: int, message: str):
    """Envoie un payload JSON à la file d'attente LavinMQ."""
    # Récupération de l'URL LavinMQ depuis vos réglages (ou fallback local)
    lavinmq_url = getattr(settings, 'LAVINMQ_URL', 'amqp://guest:guest@localhost:5672//')

    # Connexion et ouverture du canal
    params = pika.URLParameters(lavinmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Déclaration de la queue (robuste : créée si elle n'existe pas)
    channel.queue_declare(queue='notifications_queue', durable=True)

    payload = {
        'user_id': user_id,
        'message': message
    }

    # Publication persistante du message
    channel.basic_publish(
        exchange='',
        routing_key='notifications_queue',
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Rendre le message persistant sur le disque
            content_type='application/json'
        )
    )
    connection.close()


#### RED PANDA
def _delivery_report(err, msg):
    """ Called once for each message to determine delivery success/failure. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def get_redpanda_producer():
    return Producer(settings.REDPANDA_CONFIG)

def redpanda_emit_event(topic_name, key, payload):
    producer = get_redpanda_producer()

    # Serialize data to JSON string
    json_data = json.dumps(payload).encode('utf-8')

    # Produce asynchronously
    producer.produce(
        topic=topic_name,
        key=str(key),
        value=json_data,
        callback=_delivery_report
    )

    # Flush makes sure the message is delivered before moving on
    # Use flush() judiciously in high-throughput environments
    producer.flush()