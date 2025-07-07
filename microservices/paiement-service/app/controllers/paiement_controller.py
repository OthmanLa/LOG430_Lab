import requests
from fastapi import HTTPException
from app.db.session import SessionLocal
from app.model.paiement import Paiement
from datetime import datetime
from app.event_publisher import publish_paiement_effectue

CLIENT_SERVICE_URL = "http://client-service:8000/clients/clients"
COMMANDE_SERVICE_URL = "http://commande-service:8000/api/v1/commandes/commandes"

def effectuer_paiement(client_id: int, commande_id: int):
    db = SessionLocal()
    try:
        # 1. Récupérer les infos du client
        r_client = requests.get(f"{CLIENT_SERVICE_URL}/{client_id}")
        if r_client.status_code == 404:
            raise HTTPException(status_code=404, detail="Client introuvable")
        client_data = r_client.json()

        # Vérifie que le solde existe
        if "solde" not in client_data or client_data["solde"] is None:
            raise HTTPException(status_code=500, detail="Solde du client manquant ou invalide")

        # 2. Récupérer la commande
        r_commande = requests.get(f"{COMMANDE_SERVICE_URL}/{commande_id}")
        if r_commande.status_code == 404:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        commande_data = r_commande.json()

        # Vérifie que le montant existe
        if "montant" not in commande_data or commande_data["montant"] is None:
            raise HTTPException(status_code=500, detail="Montant de la commande manquant ou invalide")

        montant = commande_data["montant"]

        # 3. Vérifier le solde du client
        if client_data["solde"] < montant:
            raise HTTPException(status_code=400, detail="Solde insuffisant")

        # 4. Mettre à jour le solde du client
        nouveau_solde = client_data["solde"] - montant
        r_update = requests.put(
            f"{CLIENT_SERVICE_URL}/{client_id}/solde",
            json={"solde": nouveau_solde}
        )
        if r_update.status_code != 200:
            raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour du solde")

        # 5. Enregistrer le paiement localement
        paiement = Paiement(
            client_id=client_id,
            commande_id=commande_id,
            montant=montant,
            date_paiement=datetime.utcnow()
        )
        db.add(paiement)
        db.commit()
        db.refresh(paiement)
        publish_paiement_effectue(client_id, commande_id, montant)
        
        return {
            "message": "✅ Paiement effectué avec succès",
            "paiement": {
                "id": paiement.id,
                "client_id": paiement.client_id,
                "commande_id": paiement.commande_id,
                "montant": paiement.montant,
                "date_paiement": paiement.date_paiement
            },
            "nouveau_solde": nouveau_solde
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("[ERREUR] effectuer_paiement:", e)
        raise HTTPException(status_code=500, detail="Erreur interne lors du paiement")

    finally:
        db.close()
