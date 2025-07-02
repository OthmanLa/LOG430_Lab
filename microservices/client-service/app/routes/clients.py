from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.controllers.client_controller import create_client, get_clients, get_commandes_by_client

router = APIRouter(prefix="/clients", tags=["Clients"])

class ClientRequest(BaseModel):
    nom: str
    email: str

@router.post("/")
def ajouter_client(client: ClientRequest):
    return create_client(client.nom, client.email)

@router.get("/")
def lister_clients():
    return get_clients()

@router.get("/{client_id}/commandes")
def afficher_commandes_client(client_id: int):
    return get_commandes_by_client(client_id)