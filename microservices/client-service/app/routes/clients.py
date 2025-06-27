from fastapi import APIRouter

router = APIRouter()

@router.get("/clients")
def get_clients():
    return [
        {"id": 1, "nom": "Alice Dupont", "email": "alice@example.com"},
        {"id": 2, "nom": "Bob Martin", "email": "bob@example.com"},
    ]
