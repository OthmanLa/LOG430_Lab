from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from fastapi.security import APIKeyHeader
from fastapi import Security
from typing import List
from app.controllers.produit_controller import update_product_api


API_KEY_HEADER_NAME = "Authorization"
API_KEY = "token1"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Token invalide", headers={"WWW-Authenticate": "Bearer"})
    return api_key

router = APIRouter(
    tags=["Produits"],
    dependencies=[Depends(verify_api_key)]
    )

class ProductIn(BaseModel):
    nom: str
    prix: float

class ProductOut(BaseModel):
    id: int
    nom: str
    prix: float


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Mettre à jour un produit existant"
)
def update_product(product_id: int, payload: ProductIn):
    """
    UC4 – PUT /api/v1/products/{product_id}
    Met à jour le nom et le prix d'un produit.
    """
    try:
        updated = update_product_api(product_id, payload.nom, payload.prix)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))