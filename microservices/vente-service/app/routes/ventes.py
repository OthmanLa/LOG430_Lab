from fastapi import APIRouter

router = APIRouter()

@router.get("/ventes")
def get_ventes():
    return [{"id": 1, "produit": "Ordinateur"}]
