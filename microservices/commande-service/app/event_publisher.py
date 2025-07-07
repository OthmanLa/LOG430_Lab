import pika
import json
import uuid
from datetime import datetime

def publier_commande_creee(commande, lignes):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Déclare un exchange fanout durable
    channel.exchange_declare(exchange='commande_broadcast', exchange_type='fanout', durable=True)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "CommandeCreee",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "commande_id": commande.id,
            "client_id": commande.client_id,
            "magasin_id": commande.magasin_id,
            "montant": commande.montant,
            "lignes": [
                {"product_id": l.product_id, "quantite": l.quantite}
                for l in lignes
            ]
        }
    }
    print(f"📤 Envoi de l'événement: {event['event_type']} - {event['event_id']}")

    channel.basic_publish(
        exchange='commande_broadcast',  # Publie sur l'exchange fanout
        routing_key='',                 # Fanout ignore routing_key
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2)  # message persistant
    )
    print("✅ Événement publié dans RabbitMQ via exchange fanout.")

    connection.close()
