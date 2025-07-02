from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.model.commande import Commande
from app.controllers.commande_controller import creer_commande, get_commandes
from app.db.session import SessionLocal

router = APIRouter(prefix="/commandes", tags=["Commandes"])

# ✅ Définition directe des modèles de requête ici (pas dans un fichier séparé)
class LigneCommandeRequest(BaseModel):
    product_id: int
    quantite: int

class CommandeRequest(BaseModel):
    client_id: int
    magasin_id: int
    lignes: List[LigneCommandeRequest]

@router.post("/")
def creer(commande: CommandeRequest):
    return creer_commande(commande)

@router.get("/")
def lister_commandes():
    return get_commandes()

@router.get("/commandes/{commande_id}")
def get_commande_by_id(commande_id: int):
    db = SessionLocal()
    try:
        commande = db.query(Commande).filter(Commande.id == commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        return commande
    finally:
        db.close()