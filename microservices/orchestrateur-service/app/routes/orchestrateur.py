from fastapi import APIRouter
from app.services.orchestrateur_logic import lancer_saga
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/orchestrateur", tags=["Orchestrateur"])

class LigneCommande(BaseModel):
    product_id: int
    quantite: int

class CommandeSagaRequest(BaseModel):
    client_id: int
    magasin_id: int
    lignes: List[LigneCommande]

@router.post("/lancer")
def demarrer_saga(payload: CommandeSagaRequest):
    return lancer_saga(
        client_id=payload.client_id,
        magasin_id=payload.magasin_id,
        lignes=[ligne.dict() for ligne in payload.lignes]
    )
