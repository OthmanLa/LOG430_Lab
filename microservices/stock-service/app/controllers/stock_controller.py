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
        raise HTTPException(status_code=500, detail="Erreur service produit")

def get_stocks_by_magasin(magasin_id: int):
    db = SessionLocal()
    try:
        stocks = db.query(Stock).filter(Stock.magasin_id == magasin_id).all()
        results = []
        for stock in stocks:
            produit = requests.get(f"{PRODUITS_SERVICE_URL}/api/v1/products/{stock.product_id}", headers=HEADERS)
            produit_data = produit.json() if produit.status_code == 200 else {}
            results.append({
                "product_id": stock.product_id,
                "magasin_id": stock.magasin_id,
                "quantite": stock.quantite,
                "produit": produit_data
            })
        return results
    finally:
        db.close()

def get_stock(product_id: int, magasin_id: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.magasin_id == magasin_id
        ).first()
        if not stock:
            raise HTTPException(status_code=404, detail="Stock introuvable")

        produit = requests.get(f"{PRODUITS_SERVICE_URL}/api/v1/products/{product_id}", headers=HEADERS)
        produit_data = produit.json() if produit.status_code == 200 else {}

        return {
            "product_id": stock.product_id,
            "magasin_id": stock.magasin_id,
            "quantite": stock.quantite,
            "produit": produit_data
        }
    finally:
        db.close()

def update_stock_quantity(product_id: int, magasin_id: int, quantite: int):
    db = SessionLocal()
    try:
        if not produit_existe(product_id):
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.magasin_id == magasin_id
        ).first()

        if not stock:
            raise HTTPException(status_code=404, detail="Stock introuvable")

        stock.quantite = quantite
        db.commit()
        db.refresh(stock)

        return {
            "message": "Stock mis à jour",
            "product_id": stock.product_id,
            "magasin_id": stock.magasin_id,
            "quantite": stock.quantite
        }
    finally:
        db.close()

def reserver_stock_api(product_id: int, magasin_id: int, quantite: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.magasin_id == magasin_id
        ).first()

        if not stock:
            raise HTTPException(status_code=404, detail="Stock introuvable")

        if stock.quantite < quantite:
            raise HTTPException(status_code=400, detail="Stock insuffisant")

        stock.quantite -= quantite
        db.commit()
        db.refresh(stock)

        return {
            "message": "Stock réservé",
            "product_id": stock.product_id,
            "magasin_id": stock.magasin_id,
            "quantite_restante": stock.quantite
        }
    finally:
        db.close()

def rollback_stock_api(product_id: int, magasin_id: int, quantite: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.magasin_id == magasin_id
        ).first()

        if not stock:
            raise HTTPException(status_code=404, detail="Stock introuvable")

        stock.quantite += quantite
        db.commit()
        db.refresh(stock)

        return {
            "message": "Rollback effectué",
            "product_id": stock.product_id,
            "magasin_id": stock.magasin_id,
            "quantite_actuelle": stock.quantite
        }
    finally:
        db.close()

def create_new_stock(product_id: int, magasin_id: int, quantite: int):
    db = SessionLocal()
    try:
        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.magasin_id == magasin_id
        ).first()
        if stock:
            raise HTTPException(status_code=400, detail="Stock déjà existant")

        nouveau_stock = Stock(product_id=product_id, magasin_id=magasin_id, quantite=quantite)
        db.add(nouveau_stock)
        db.commit()
        db.refresh(nouveau_stock)

        return {
            "message": "Stock créé",
            "product_id": nouveau_stock.product_id,
            "magasin_id": nouveau_stock.magasin_id,
            "quantite": nouveau_stock.quantite
        }
    finally:
        db.close()
