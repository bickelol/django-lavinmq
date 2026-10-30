# notify/management/commands/run_worker.py
import pika
import json
import sys
import time
from django.core.management.base import BaseCommand
from django.conf import settings
# Importez vos modèles ou services Django ici si besoin
# from notify.models import Notification

class Command(BaseCommand):
    help = "Lance le worker Pika pour consommer les tâches LavinMQ"

    def handle(self, *args, **options):
        lavinmq_url = getattr(settings, 'LAVINMQ_URL', 'amqp://guest:guest@localhost:5672//')
        self.stdout.write(self.style.SUCCESS(f"Connexion à LavinMQ sur {lavinmq_url}..."))

        try:
            params = pika.URLParameters(lavinmq_url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            # S'assurer que la queue existe
            channel.queue_declare(queue='notifications_queue', durable=True)

            # Équitable : ne donne pas de nouveau message au worker tant qu'il n'a pas fini le sien
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                self.stdout.write(self.style.HTTP_INFO(f" [x] Message reçu de LavinMQ"))
                try:
                    # Analyse du payload
                    data = json.loads(body.decode('utf-8'))
                    user_id = data.get('user_id')
                    message = data.get('message')

                    # --- VOTRE LOGIQUE MÉTIER ICI ---
                    self.stdout.write(f"Traitement de la notification pour l'utilisateur {user_id} : {message}")
                    time.sleep(2)  # Simulation d'un traitement (envoi de mail, push, etc.)
                    # ---------------------------------

                    # Accuser réception du message réussi
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    self.stdout.write(self.style.SUCCESS(" [v] Tâche traitée avec succès et acquittée."))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur lors du traitement de la tâche : {e}"))
                    # En cas d'erreur de traitement, on remet le message dans la queue (requeue=True)
                    # Ou False si vous préférez le rejeter / l'envoyer dans une Dead Letter Queue
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(queue='notifications_queue', on_message_callback=callback)
            self.stdout.write(self.style.SUCCESS("Worker démarré avec succès. En attente de messages. Pour quitter : CTRL+C"))

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            self.stdout.write(self.style.ERROR("Impossible de se connecter à LavinMQ. Vérifiez que le serveur tourne."))
            sys.exit(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nArrêt du worker demandé par l'utilisateur."))
            try:
                connection.close()
            except Exception:
                pass