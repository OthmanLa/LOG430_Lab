from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.db import SessionLocal
from app.models import Event, CommandeProjection
import json

EVENT_TO_ETAT = {
    "CommandeCreee": "Commande passée",
    "PaiementEffectue": "Commande payée",
}
app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/etat/{commande_id}")
def get_current_state(commande_id: int):
    session = SessionLocal()
    events = session.query(Event).all()
    etats = []

    for event in sorted(events, key=lambda e: e.timestamp):
        try:
            data = json.loads(event.data)
            if "commande_id" in data and int(data["commande_id"]) == commande_id:
                # On convertit le type d'événement en état métier lisible
                etat_humain = EVENT_TO_ETAT.get(event.event_type)
                if etat_humain and etat_humain not in etats:
                    etats.append(etat_humain)
        except Exception as e:
            print(f"[Erreur JSON] {e}")

    session.close()
    return {
        "commande_id": commande_id,
        "etats": etats
    }

@app.get("/projections/{commande_id}")
def get_commande_projection(commande_id: int):
    session = SessionLocal()
    projection = session.query(CommandeProjection).filter_by(commande_id=commande_id).first()
    session.close()

    if projection:
        return {
            "commande_id": projection.commande_id,
            "etat": projection.etat
        }
    return {"message": "Commande inconnue"}

@app.post("/replay")
def replay_events():
    session = SessionLocal()

    # 1. Réinitialiser la projection
    session.query(CommandeProjection).delete()
    session.commit()

    # 2. Rejouer tous les événements dans l'ordre
    events = session.query(Event).order_by(Event.timestamp).all()
    for event in events:
        data = json.loads(event.data)
        commande_id = data.get("commande_id")

        if commande_id is None:
            continue

        projection = session.query(CommandeProjection).filter_by(commande_id=commande_id).first()
        if not projection:
            projection = CommandeProjection(commande_id=commande_id, etat="")

        if event.event_type == "CommandeCreee":
            projection.etat = "Commande passée"
        elif event.event_type == "PaiementEffectue":
            projection.etat = "Commande payée"

        session.merge(projection)

    session.commit()
    session.close()
    return {"message": "Replay exécuté avec succès"}


