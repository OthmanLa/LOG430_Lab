import requests
from fastapi import HTTPException
from app.db.session import SessionLocal
from app.model.stock import Stock

PRODUITS_SERVICE_URL = "http://produits-service:8000"
HEADERS = {"Authorization": "token1"}

def produit_existe(product_id: int) -> bool:
    try:
        response = requests.get(f"{PRODUITS_SERVICE_URL}/api/v1/products/{product_id}", headers=HEADERS)
        return response.status_code == 200
    except Exception as e:
        print(f"[ERREUR] Impossible de vérifier le produit: {e}")
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service produit")

def get_all_stocks():
    db = SessionLocal()
    try:
        stocks = db.query(Stock).all()
        results = []
        for stock in stocks:
            try:
                produit = requests.get(f"{PRODUITS_SERVICE_URL}/api/v1/products/{stock.product_id}", headers=HEADERS)
                if produit.status_code == 200:
                    produit_data = produit.json()
                else:
                    continue  # Ignore stock si produit non trouvé
            except Exception:
                continue  # Ignore aussi en cas d'erreur réseau

            results.append({
                "id": stock.id,
                "product_id": stock.product_id,
                "magasin_id": stock.magasin_id,
                "quantite": stock.quantite,
                "produit": produit_data
            })
        return results
    finally:
        db.close()

def get_stock_by_product(product_id: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(Stock.product_id == product_id).first()
        if not stock:
            raise ValueError("Stock non trouvé")

        produit = requests.get(f"{PRODUITS_SERVICE_URL}/api/v1/products/{product_id}", headers=HEADERS)
        if produit.status_code != 200:
            raise ValueError("Produit non trouvé")

        produit_data = produit.json()

        return {
            "id": stock.id,
            "product_id": stock.product_id,
            "magasin_id": stock.magasin_id,
            "quantite": stock.quantite,
            "produit": produit_data
        }
    finally:
        db.close()

def update_stock_quantity(product_id: int, quantite: int):
    db = SessionLocal()
    try:
        if not produit_existe(product_id):
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        stock = db.query(Stock).filter(Stock.product_id == product_id).first()
        if not stock:
            raise ValueError("Stock non trouvé")

        stock.quantite = quantite
        db.commit()
        db.refresh(stock)
        return {
            "produit_id": stock.product_id,
            "quantite": stock.quantite
        }
    finally:
        db.close()
