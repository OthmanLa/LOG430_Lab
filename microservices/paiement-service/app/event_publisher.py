import pika
import json
import uuid
from datetime import datetime

def publish_paiement_effectue(client_id: int, commande_id: int, montant: float):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Déclare un exchange fanout durable
    channel.exchange_declare(exchange='commande_broadcast', exchange_type='fanout', durable=True)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "PaiementEffectue",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "client_id": client_id,
            "commande_id": commande_id,
            "montant": montant
        }
    }

    channel.basic_publish(
        exchange='commande_broadcast',  # Publish to fanout exchange
        routing_key='',  # Ignored by fanout
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )

    print(f"[PUBLISH] Event sent: {event}")
    connection.close()
