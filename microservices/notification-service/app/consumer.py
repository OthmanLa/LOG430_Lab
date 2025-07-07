import time
import pika
import json
import os
import threading
from datetime import datetime
from prometheus_client import Counter, start_http_server

# 🔧 Config
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "commande.events"
NOTIFICATION_LOG = "logs/notifications.jsonl"
METRICS_PORT = 9001  # Prometheus va venir lire ici

# 📊 Métriques Prometheus
NOTIFICATIONS_TOTAL = Counter("notifications_envoyees_total", "Nombre total de notifications envoyées")
EVENTS_CONSUMED_TOTAL = Counter("evenements_consomme_total", "Nombre total d'événements consommés")

def wait_for_rabbitmq(max_retries=10, delay=5):
    for i in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            print("[NOTIF] Connexion RabbitMQ établie.")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"[NOTIF] RabbitMQ non dispo, tentative {i + 1}/{max_retries}...")
            time.sleep(delay)
    raise Exception("[NOTIF] Échec de connexion à RabbitMQ après plusieurs tentatives.")

def callback(ch, method, properties, body):
    try:
        EVENTS_CONSUMED_TOTAL.inc()

        message = json.loads(body)
        data = message.get("data", {})

        if message.get("event_type") == "CommandeCreee":
            texte = f"Une nouvelle commande {data.get('commande_id')} a été créée pour le client {data.get('client_id')}."
        elif message.get("event_type") == "PaiementEffectue":
            texte = f"Le paiement pour la commande {data.get('commande_id')} du client {data.get('client_id')} a été effectué."
        else:
            texte = f"Événement {message.get('event_type')} reçu pour la commande {data.get('commande_id')}."

        notification = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": message.get("event_type", "unknown"),
            "client_id": data.get("client_id"),
            "commande_id": data.get("commande_id"),
            "message": texte
        }

        os.makedirs(os.path.dirname(NOTIFICATION_LOG), exist_ok=True)
        with open(NOTIFICATION_LOG, "a") as f:
            f.write(json.dumps(notification) + "\n")

        NOTIFICATIONS_TOTAL.inc()
        print(f"[NOTIF] Notification envoyée pour commande {data.get('commande_id')}")
    except Exception as e:
        print(f"[NOTIF][ERREUR] {e}")

def consume():
    connection = wait_for_rabbitmq()
    channel = connection.channel()

    # Déclare l'exchange fanout
    channel.exchange_declare(exchange="commande_broadcast", exchange_type="fanout", durable=True)

    # Crée une queue temporaire exclusive (auto-delete à la fin)
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # Lie la queue à l'exchange fanout
    channel.queue_bind(exchange="commande_broadcast", queue=queue_name)

    print(f"[NOTIF] Queue temporaire '{queue_name}' liée à l'exchange 'commande_broadcast'. En attente des messages...")

    # Consomme la queue temporaire
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    # ✅ Lancer Prometheus exporter sur /metrics
    threading.Thread(target=start_http_server, args=(METRICS_PORT,)).start()

    consume()
