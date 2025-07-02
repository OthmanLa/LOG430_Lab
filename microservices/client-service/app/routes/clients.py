from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.controllers.client_controller import create_client, get_clients, get_commandes_by_client
from app.db.session import SessionLocal
from app.model.client import Client


router = APIRouter(prefix="/clients", tags=["Clients"])

class ClientRequest(BaseModel):
    nom: str
    email: str

class SoldeUpdateRequest(BaseModel):
    solde: float

@router.post("/")
def ajouter_client(client: ClientRequest):
    return create_client(client.nom, client.email)

@router.put("/clients/{client_id}/solde")
def update_solde(client_id: int, solde_data: SoldeUpdateRequest):
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client introuvable")
        client.solde = solde_data.solde
        db.commit()
        db.refresh(client)
        return client
    finally:
        db.close()

@router.get("/")
def lister_clients():
    return get_clients()

@router.get("/{client_id}/commandes")
def afficher_commandes_client(client_id: int):
    return get_commandes_by_client(client_id)

@router.get("/clients/{client_id}")
def get_client_by_id(client_id: int):
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client introuvable")
        return client
    finally:
        db.close()
