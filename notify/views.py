from django.shortcuts import render
from django.http import JsonResponse
from .helpers import lavinmq_queue_notification, redpanda_emit_event

def send_notification(request):
    # Envoi immédiat à LavinMQ (asynchrone pour l'utilisateur)
    lavinmq_queue_notification(user_id=42, message="Votre transaction a été validée. Jesus is the lord...")

    # Envoi d'événement à Redpanda
    '''event_payload = {
        "user_id": 42,
        "email": 'user@jesus.com',
        "status": "created"
    }

    redpanda_emit_event(
        topic_name=settings.REDPANDA_TOPICS['redpanda_notifications'],
        key=user_id,
        payload=event_payload
    )'''
    return JsonResponse({"status": "Message en cours de traitement par LavinMQ"})
