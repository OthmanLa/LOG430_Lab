import random
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.controllers.paiement_controller import effectuer_paiement

router = APIRouter()

class PaiementRequest(BaseModel):
    client_id: int
    montant: float

@router.post("/paiements")
def creer_paiement(client_id: int = Query(...), commande_id: int = Query(...)):
    return effectuer_paiement(client_id, commande_id)
