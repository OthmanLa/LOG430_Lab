import requests
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
from app.db.session import SessionLocal
from app.model.commande import Commande, LigneCommande
from app.event_publisher import publier_commande_creee

# ==== URLs externes ====
STOCK_SERVICE_URL = "http://stock-service:8000"
PRODUIT_SERVICE_URL = "http://produits-service:8000/api/v1/products"
CLIENT_SERVICE_URL = "http://client-service:8000/clients"

HEADERS = {"Authorization": "token1"}

# ==== Modèles ====
class LigneCommandeRequest(BaseModel):
    product_id: int
    quantite: int

class CommandeRequest(BaseModel):
    client_id: int
    magasin_id: int
    lignes: List[LigneCommandeRequest]

# ==== Vérifications ====
def verifier_client_existe(client_id: int) -> bool:
    try:
        response = requests.get(CLIENT_SERVICE_URL)
        if response.status_code != 200:
            return False
        clients = response.json()
        return any(client["id"] == client_id for client in clients)
    except Exception:
        return False

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
    return True  # Simulation

# ==== Création de commande ====
def creer_commande(commande: CommandeRequest):
    db = SessionLocal()
    try:
        if not verifier_client_existe(commande.client_id):
            raise HTTPException(status_code=404, detail="Client non trouvé")

        for ligne in commande.lignes:
            if not verifier_stock(ligne.product_id, ligne.quantite, commande.magasin_id):
                raise HTTPException(status_code=400, detail=f"Stock insuffisant pour produit {ligne.product_id}")

        for ligne in commande.lignes:
            if not reserver_stock(ligne.product_id, ligne.quantite, commande.magasin_id):
                raise HTTPException(status_code=500, detail=f"Réservation échouée pour produit {ligne.product_id}")

        # 💰 Calculer le montant total de la commande
        montant_total = 0
        for ligne in commande.lignes:
            try:
                response = requests.get(f"{PRODUIT_SERVICE_URL}/{ligne.product_id}", headers=HEADERS)
                if response.status_code != 200:
                    raise Exception("Erreur produit")
                produit_data = response.json()
                prix = produit_data["prix"]
            except:
                prix = 0
            montant_total += prix * ligne.quantite

        # ✅ Ici on passe le bon montant
        if not effectuer_paiement(commande.client_id, montant=montant_total):
            for ligne in commande.lignes:
                rollback_stock(ligne.product_id, ligne.quantite, commande.magasin_id)
            raise HTTPException(status_code=402, detail="Paiement refusé. Stock annulé.")

        nouvelle_commande = Commande(
            client_id=commande.client_id,
            magasin_id=commande.magasin_id,
            montant=montant_total
        )
        db.add(nouvelle_commande)
        db.commit()
        db.refresh(nouvelle_commande)

        # 🟩 Enregistre les lignes dans la base
        for ligne in commande.lignes:
            ligne_commande = LigneCommande(
                commande_id=nouvelle_commande.id,
                product_id=ligne.product_id,
                quantite=ligne.quantite
            )
            db.add(ligne_commande)

        db.commit()

        # 🟩 Recharge les vraies lignes depuis la DB
        lignes_commande = db.query(LigneCommande).filter_by(commande_id=nouvelle_commande.id).all()

        # ✅ Publier l’événement APRÈS avoir tout enregistré
        publier_commande_creee(nouvelle_commande, lignes_commande)

        return {
            "message": "Commande créée avec succès",
            "commande_id": nouvelle_commande.id,
            "montant": montant_total
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
            lignes_data = []

            for l in c.lignes:
                try:
                    response = requests.get(f"{PRODUIT_SERVICE_URL}/{l.product_id}", headers=HEADERS)
                    if response.status_code != 200:
                        raise Exception(f"Erreur produit {l.product_id}")
                    produit_data = response.json()
                    prix = produit_data["prix"]
                except:
                    prix = 0

                montant = prix * l.quantite

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
                "total_commande": c.montant  # ✅ Utilise directement le montant stocké
            })

        return result
    finally:
        db.close()
