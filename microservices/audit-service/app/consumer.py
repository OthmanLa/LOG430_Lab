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
LOG_FILE = "logs/audit.jsonl"
METRICS_PORT = 9002  # Prometheus viendra ici

# 📊 Métriques Prometheus
AUDIT_EVENTS_CONSUMED = Counter("audit_evenements_consomme_total", "Nombre total d'événements consommés (audit)")
AUDIT_LOGS_ECRITS = Counter("audit_logs_ecrits_total", "Nombre total de lignes d’audit écrites")

def wait_for_rabbitmq(max_retries=10, delay=5):
    for i in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            print("[AUDIT] Connexion RabbitMQ établie.")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"[AUDIT] RabbitMQ non dispo, tentative {i + 1}/{max_retries}...")
            time.sleep(delay)
    raise Exception("[AUDIT] Échec de connexion à RabbitMQ après plusieurs tentatives.")

def callback(ch, method, properties, body):
    try:
        AUDIT_EVENTS_CONSUMED.inc()  # ✅ événement reçu

        message = json.loads(body)
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": message.get("event_type", "unknown"),
            "commande_id": message.get("data", {}).get("commande_id"),
            "client_id": message.get("data", {}).get("client_id"),
            "montant": message.get("data", {}).get("montant"),
            "raw": message
        }

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

        AUDIT_LOGS_ECRITS.inc()  # ✅ ligne d’audit ajoutée
        print(f"[AUDIT] Événement enregistré pour commande {message.get('data', {}).get('commande_id')}")
    except Exception as e:
        print(f"[AUDIT][ERREUR] {e}")

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

    print(f"[AUDIT] Queue temporaire '{queue_name}' liée à l'exchange 'commande_broadcast'. En attente des messages...")

    # Consomme la queue temporaire
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    # ✅ Lance le serveur Prometheus en parallèle
    threading.Thread(target=start_http_server, args=(METRICS_PORT,)).start()

    consume()
