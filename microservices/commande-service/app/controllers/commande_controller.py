import requests
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
from app.db.session import SessionLocal
from app.model.commande import Commande, LigneCommande

STOCK_SERVICE_URL = "http://stock-service:8000"
HEADERS = {"Authorization": "token1"}

PRODUIT_SERVICE_URL = "http://produits-service:8000/api/v1/products"
HEADERS = {"Authorization": "token1"}

# ==== Modèles ====
class LigneCommandeRequest(BaseModel):
    product_id: int
    quantite: int

class CommandeRequest(BaseModel):
    client_id: int
    magasin_id: int  # 🔥 Utilisé partout
    lignes: List[LigneCommandeRequest]

# ==== Vérification ====
def verifier_stock(product_id: int, quantite: int, magasin_id: int) -> bool:
    try:
        response = requests.get(
            f"{STOCK_SERVICE_URL}/api/v1/stocks/{product_id}/magasin/{magasin_id}",
            headers=HEADERS
        )
        if response.status_code != 200:
            return False
        stock_data = response.json()
        return stock_data["quantite"] >= quantite
    except Exception:
        return False

def reserver_stock(product_id: int, quantite: int, magasin_id: int) -> bool:
    try:
        payload = {
            "product_id": product_id,
            "quantite": quantite,
            "magasin_id": magasin_id
        }
        response = requests.post(f"{STOCK_SERVICE_URL}/api/v1/stocks/reserve", headers=HEADERS, json=payload)
        return response.status_code == 200
    except Exception:
        return False

def rollback_stock(product_id: int, quantite: int, magasin_id: int):
    try:
        payload = {
            "product_id": product_id,
            "quantite": quantite,
            "magasin_id": magasin_id
        }
        requests.post(f"{STOCK_SERVICE_URL}/api/v1/stocks/rollback", headers=HEADERS, json=payload)
    except:
        pass

def effectuer_paiement(client_id: int, montant: float) -> bool:
    return True  # Simulé

# ==== Création de commande ====
def creer_commande(commande: CommandeRequest):
    db = SessionLocal()
    try:
        for ligne in commande.lignes:
            if not verifier_stock(ligne.product_id, ligne.quantite, commande.magasin_id):
                raise HTTPException(status_code=400, detail=f"Stock insuffisant pour produit {ligne.product_id}")

        for ligne in commande.lignes:
            if not reserver_stock(ligne.product_id, ligne.quantite, commande.magasin_id):
                raise HTTPException(status_code=500, detail=f"Réservation échouée pour produit {ligne.product_id}")

        if not effectuer_paiement(commande.client_id, montant=0):
            for ligne in commande.lignes:
                rollback_stock(ligne.product_id, ligne.quantite, commande.magasin_id)
            raise HTTPException(status_code=402, detail="Paiement refusé. Stock annulé.")

        # ✅ Enregistrement avec magasin_id
        nouvelle_commande = Commande(client_id=commande.client_id, magasin_id=commande.magasin_id)
        db.add(nouvelle_commande)
        db.commit()
        db.refresh(nouvelle_commande)

        for ligne in commande.lignes:
            ligne_commande = LigneCommande(
                commande_id=nouvelle_commande.id,
                product_id=ligne.product_id,
                quantite=ligne.quantite
            )
            db.add(ligne_commande)

        db.commit()

        return {
            "message": "Commande créée avec succès",
            "commande_id": nouvelle_commande.id
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
    finally:
        db.close()

# ==== Récupération des commandes ====
def get_commandes():
    db = SessionLocal()
    try:
        commandes = db.query(Commande).all()
        result = []
        for c in commandes:
            total = 0
            lignes_data = []

            for l in c.lignes:
                # 🔄 Récupérer le prix du produit depuis le service produit
                try:
                    response = requests.get(f"{PRODUIT_SERVICE_URL}/{l.product_id}", headers=HEADERS)
                    if response.status_code != 200:
                        raise Exception(f"Erreur produit {l.product_id}")
                    produit_data = response.json()
                    prix = produit_data["prix"]
                except:
                    prix = 0  # fallback

                montant = prix * l.quantite
                total += montant

                lignes_data.append({
                    "product_id": l.product_id,
                    "quantite": l.quantite,
                    "prix_unitaire": prix,
                    "montant": montant
                })

            result.append({
                "id": c.id,
                "client_id": c.client_id,
                "magasin_id": c.magasin_id,
                "lignes": lignes_data,
                "total_commande": total
            })

        return result
    finally:
        db.close()
