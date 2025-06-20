from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from fastapi.security import APIKeyHeader
from fastapi import Security

# Import du cache
from app.cache import stock_cache
# Import du controller
from app.controllers.stock_controller import get_stock_by_store

# Sécurité API Key
API_KEY_HEADER_NAME = "Authorization"
API_KEY = "token1"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Token invalide", headers={"WWW-Authenticate": "Bearer"})
    return api_key

router = router = APIRouter(
    tags=["Magasins"],
    dependencies=[Depends(verify_api_key)]
)


# Schéma de réponse
class StockItem(BaseModel):
    produit_id: int
    produit_nom: str
    quantite: int

class StockResponse(BaseModel):
    store_id: int
    stock: List[StockItem]

# Fonction cachée pour lecture stock
@stock_cache
def _fetch_stock(store_id: int):
    return get_stock_by_store(store_id)

@router.get(
    "/{store_id}/stock",
    response_model=StockResponse,
    summary="Consulter le stock d’un magasin"
)
def lire_stock_magasin(store_id: int):
    """
    UC2 – GET /api/v1/stores/{store_id}/stock
    Renvoie pour chaque produit du magasin : son ID, son nom et la quantité en stock.
    """
    stock = _fetch_stock(store_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Magasin introuvable")
    return StockResponse(store_id=store_id, stock=stock)
