from fastapi import APIRouter

router = APIRouter()

@router.post("/commandes")
def valider_commande():
    return {"message": "Commande validée avec succès"}
