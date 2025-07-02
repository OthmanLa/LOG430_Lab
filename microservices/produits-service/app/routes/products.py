from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List

from fastapi import Request
from app.controllers.produit_controller import update_product_api
from app.controllers.produit_controller import get_all_products_api
from app.controllers.produit_controller import get_product_by_id_api
from app.controllers.produit_controller import create_product_api

API_KEY_HEADER_NAME = "Authorization"
API_KEY = "token1"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Token invalide")
    return api_key

router = APIRouter(prefix="/api/v1", tags=["Produits"], dependencies=[Depends(verify_api_key)])

class ProductIn(BaseModel):
    nom: str
    prix: float

class ProductOut(BaseModel):
    id: int
    nom: str
    prix: float

@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductIn):
    try:
        return update_product_api(product_id, payload.nom, payload.prix)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products", response_model=List[ProductOut])
def list_products():
    try:
        return get_all_products_api()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, request: Request):
    print("=== Headers reçus ===")
    print(request.headers)
    try:
        return get_product_by_id_api(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(payload: ProductIn):
    try:
        return create_product_api(payload.nom, payload.prix)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))