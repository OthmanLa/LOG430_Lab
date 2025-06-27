from fastapi import APIRouter

router = APIRouter()

@router.get("/paniers")
def get_paniers():
    return [
        {"id": 1, "client_id": 1, "produits": [1, 2]},
        {"id": 2, "client_id": 2, "produits": [3]},
    ]
