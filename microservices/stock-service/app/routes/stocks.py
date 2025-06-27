from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.controllers.stock_controller import get_all_stocks, get_stock_by_product, update_stock_quantity

router = APIRouter(prefix="/api/v1", tags=["Stock"])

# 🔸 Modèle du produit retourné par l'API produit
class Product(BaseModel):
    id: int
    nom: str
    prix: float

# 🔸 Réponse enrichie pour le stock avec info produit
class StockWithProduct(BaseModel):
    id: int
    product_id: int
    magasin_id: int
    quantite: int
    produit: Optional[Product]


class StockUpdate(BaseModel):
    quantite: int

@router.get("/stocks", response_model=List[StockWithProduct])
def list_stocks():
    return get_all_stocks()

@router.get("/stocks/{product_id}", response_model=StockWithProduct)
def get_stock(product_id: int):
    try:
        return get_stock_by_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/stocks/{product_id}", response_model=StockWithProduct)
def update_stock(product_id: int, update: StockUpdate):
    try:
        return update_stock_quantity(product_id, update.quantite)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
