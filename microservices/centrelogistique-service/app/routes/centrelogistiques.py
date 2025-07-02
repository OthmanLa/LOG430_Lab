from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from app.controllers.centrelogistique_controller import ajouter_ou_mettre_a_jour_stock

router = APIRouter(prefix="/logistique", tags=["Centre Logistique"])

PRODUIT_SERVICE_URL = "http://produits-service:8000/api/v1/products"
HEADERS = {"Authorization": "token1"}

class MagasinRequest(BaseModel):
    nom: str

class StockAjoutRequest(BaseModel):
    product_id: int
    magasin_id: int
    quantite: int

class ProduitCreateRequest(BaseModel):
    nom: str
    prix: float

@router.post("/ajouter-stock")
def ajouter_stock(req: StockAjoutRequest):
    return ajouter_ou_mettre_a_jour_stock(req.product_id, req.magasin_id, req.quantite)

@router.post("/creer-produit")
def creer_produit(req: ProduitCreateRequest):
    try:
        response = requests.post(
            PRODUIT_SERVICE_URL,
            headers=HEADERS,
            json={"nom": req.nom, "prix": req.prix}
        )
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création produit: {str(e)}")