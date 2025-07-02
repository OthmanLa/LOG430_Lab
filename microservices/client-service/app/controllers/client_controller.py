from app.db.session import SessionLocal
from app.model.client import Client
from fastapi import HTTPException
import requests

COMMANDE_SERVICE_URL = "http://commande-service:8000/api/v1"


def create_client(nom: str, email: str, solde_initial: float = 100.0):
    db = SessionLocal()
    try:
        existing = db.query(Client).filter(Client.email == email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Client déjà existant")
        client = Client(nom=nom, email=email, solde=solde_initial)
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    finally:
        db.close()


def get_clients():
    db = SessionLocal()
    try:
        return db.query(Client).all()
    finally:
        db.close()

def get_commandes_by_client(client_id: int):
    try:
        response = requests.get(f"{COMMANDE_SERVICE_URL}/commandes/", timeout=5)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erreur en récupérant les commandes")

        commandes = response.json()
        commandes_client = [c for c in commandes if c["client_id"] == client_id]
        return commandes_client
    except Exception as e:
        print("[ERREUR] get_commandes_by_client:", e)
        raise HTTPException(status_code=500, detail="Service commande inaccessible")
