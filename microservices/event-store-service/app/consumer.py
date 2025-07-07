from datetime import datetime
import pika
import json
import os
import time
import threading

from app.db import SessionLocal, init_db
from app.models import Event, CommandeProjection

from prometheus_client import Counter, Histogram, start_http_server

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "event-store-queue"
PROMETHEUS_PORT = 9003  # Port exposé pour /metrics

# Prometheus Metrics
EVENTS_CONSUMED = Counter("eventstore_events_consumed_total", "Nombre total d’événements consommés")
EVENT_LATENCY = Histogram("eventstore_event_latency_seconds", "Latence entre émission et consommation")

def wait_for_rabbitmq(max_retries=10, delay=5):
    for i in range(max_retries):
        try:
            return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        except pika.exceptions.AMQPConnectionError:
            print(f"[STORE] RabbitMQ indisponible... tentative {i + 1}")
            time.sleep(delay)
    raise Exception("Impossible de se connecter à RabbitMQ")

def callback(ch, method, properties, body):
    print(f"📥 Message reçu du broker: {body}")

    session = SessionLocal()
    try:
        message = json.loads(body)
        print(f"➡️ Contenu des données de l’événement: {message['data']}")

        # ✅ Incrémenter les métriques
        EVENTS_CONSUMED.inc()

        # ✅ Mesurer latence entre émission et consommation
        try:
            event_timestamp = datetime.fromisoformat(message["timestamp"])
            latence = (datetime.utcnow() - event_timestamp).total_seconds()
            EVENT_LATENCY.observe(latence)
        except Exception as e:
            print(f"[STORE][WARNING] Impossible de calculer la latence: {e}")

        # Éviter les doublons
        if session.query(Event).filter_by(event_id=message["event_id"]).first():
            print(f"[STORE] Événement déjà traité: {message['event_id']}")
            return

        # 1. Stockage brut de l'événement
        evt = Event(
            event_id=message["event_id"],
            event_type=message["event_type"],
            timestamp=event_timestamp,
            data=json.dumps(message["data"])
        )
        session.add(evt)

        # 2. Mise à jour de la projection
        commande_id = message["data"].get("commande_id")
        if commande_id is not None:
            projection = session.query(CommandeProjection).filter_by(commande_id=commande_id).first()
            if not projection:
                projection = CommandeProjection(commande_id=commande_id, etat="")

            if message["event_type"] == "CommandeCreee":
                projection.etat = "Commande passée"
            elif message["event_type"] == "PaiementEffectue":
                projection.etat = "Commande payée"

            session.merge(projection)

        session.commit()
        print(f"[STORE] Événement stocké + projection mise à jour: {message['event_type']} - {message['event_id']}")

    except Exception as e:
        print(f"[STORE][ERREUR] {e}")
    finally:
        session.close()

def consume():
    init_db()
    connection = wait_for_rabbitmq()
    channel = connection.channel()

    # Déclare l'exchange fanout durable (doit correspondre au publisher)
    channel.exchange_declare(exchange="commande_broadcast", exchange_type="fanout", durable=True)

    # Crée une queue temporaire exclusive (auto-delete à la fermeture)
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # Lie la queue temporaire à l'exchange fanout
    channel.queue_bind(exchange="commande_broadcast", queue=queue_name)

    print(f"[STORE] Queue temporaire '{queue_name}' liée à l'exchange 'commande_broadcast'. En attente des messages...")

    # Consomme la queue temporaire
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    # 🟢 Lancer Prometheus exporter sur /metrics
    threading.Thread(target=start_http_server, args=(PROMETHEUS_PORT,), daemon=True).start()
    consume()
