from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.controllers.stock_controller import (
    get_stocks_by_magasin,
    get_stock,
    update_stock_quantity,
    reserver_stock_api,
    rollback_stock_api,
    create_new_stock
)

router = APIRouter(prefix="/api/v1", tags=["Stock"])

# 🔸 Modèle du produit retourné par l'API produit
class Product(BaseModel):
    id: int
    nom: str
    prix: float

# 🔸 Réponse enrichie pour le stock avec info produit
class StockWithProduct(BaseModel):
    product_id: int
    magasin_id: int
    quantite: int
    produit: Optional[Product]

class StockUpdate(BaseModel):
    quantite: int

class StockActionRequest(BaseModel):
    product_id: int
    magasin_id: int
    quantite: int

class StockCreate(BaseModel):
    product_id: int
    magasin_id: int
    quantite: int

# 🔹 Liste des stocks dans un magasin
@router.get("/stocks/magasin/{magasin_id}", response_model=List[StockWithProduct])
def list_stocks_by_magasin(magasin_id: int):
    return get_stocks_by_magasin(magasin_id)

# 🔹 Obtenir un stock précis (produit + magasin)
@router.get("/stocks/{product_id}/magasin/{magasin_id}", response_model=StockWithProduct)
def get_stock_by_product_and_magasin(product_id: int, magasin_id: int):
    try:
        return get_stock(product_id, magasin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 🔹 Mettre à jour un stock pour un produit et magasin
@router.put("/stocks/{product_id}/magasin/{magasin_id}", response_model=StockWithProduct)
def update_stock(product_id: int, magasin_id: int, update: StockUpdate):
    try:
        return update_stock_quantity(product_id, magasin_id, update.quantite)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 🔹 Réserver un stock pour un magasin donné
@router.post("/stocks/reserve")
def reserver_stock(payload: StockActionRequest):
    return reserver_stock_api(payload.product_id, payload.magasin_id, payload.quantite)

# 🔹 Rollback d’un stock dans un magasin donné
@router.post("/stocks/rollback")
def rollback_stock(payload: StockActionRequest):
    return rollback_stock_api(payload.product_id, payload.magasin_id, payload.quantite)

@router.post("/stocks/", status_code=201)
def creer_stock(stock: StockCreate):
    return create_new_stock(stock.product_id, stock.magasin_id, stock.quantite)