from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.controllers.commande_controller import creer_commande, get_commandes

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
