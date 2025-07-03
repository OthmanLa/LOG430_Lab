from app.domain.etats import EtatCommande
import logging
import requests
from prometheus_client import Counter, Histogram
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
etat = EtatCommande.EN_ATTENTE

CLIENT_URL = "http://client-service:8000/clients/clients"
COMMANDE_URL = "http://commande-service:8000/api/v1/commandes"
STOCK_URL = "http://stock-service:8000/api/v1/stocks"
PAIEMENT_URL = "http://paiement-service:8000/api/v1/paiements"

# Prometheus metrics
saga_success_counter = Counter("saga_success_total", "Nombre total de sagas réussies")
saga_failure_counter = Counter("saga_failure_total", "Nombre total de sagas échouées")
saga_duration_histogram = Histogram("saga_duration_seconds", "Durée des sagas en secondes")
saga_etapes_counter = Counter("saga_etapes_total", "Étapes atteintes dans les sagas", ["etape"])

def lancer_saga(client_id: int, magasin_id: int, lignes: list):
    global etat
    start_time = time.time()
    try:
        logger.info(f"Début de la saga - État : {etat}")

        # 1. Vérifier que le client existe
        r_client = requests.get(f"{CLIENT_URL}/{client_id}")
        if r_client.status_code != 200:
            etat = EtatCommande.ECHEC
            saga_failure_counter.inc()
            saga_etapes_counter.labels(etape="verif_client_echec").inc()
            saga_duration_histogram.observe(time.time() - start_time)
            return {"status": "ECHEC", "étape": "Vérification client", "etat": etat, "detail": "Client introuvable"}

        etat = EtatCommande.CLIENT_VERIFIE
        logger.info(f"Client vérifié - État : {etat}")
        saga_etapes_counter.labels(etape="verif_client").inc()

        # 2. Créer la commande
        payload_commande = {
            "client_id": client_id,
            "magasin_id": magasin_id,
            "lignes": lignes
        }
        r_commande = requests.post(f"{COMMANDE_URL}/", json=payload_commande)
        if r_commande.status_code != 200:
            etat = EtatCommande.ECHEC
            saga_failure_counter.inc()
            saga_etapes_counter.labels(etape="commande_creation_echec").inc()
            saga_duration_histogram.observe(time.time() - start_time)
            return {"status": "ECHEC", "étape": "Création commande", "etat": etat, "detail": r_commande.json()}

        commande_data = r_commande.json()
        commande_id = commande_data["commande_id"]
        montant = commande_data["montant"]

        etat = EtatCommande.COMMANDE_CREEE
        logger.info(f"Commande créée - État : {etat}")
        saga_etapes_counter.labels(etape="commande_creee").inc()

        # 3. Réserver les stocks
        for ligne in lignes:
            r_reserve = requests.post(
                f"{STOCK_URL}/reserve",
                json={
                    "product_id": ligne["product_id"],
                    "quantite": ligne["quantite"],
                    "magasin_id": magasin_id
                }
            )
            if r_reserve.status_code != 200:
                rollback_stocks(lignes, magasin_id)
                etat = EtatCommande.STOCK_LIBERE
                saga_failure_counter.inc()
                saga_etapes_counter.labels(etape="stock_reservation_echec").inc()
                saga_duration_histogram.observe(time.time() - start_time)
                return {
                    "status": "ECHEC",
                    "étape": "Réservation stock",
                    "etat": etat,
                    "detail": f"Réservation échouée pour produit {ligne['product_id']}"
                }

        etat = EtatCommande.STOCK_RESERVE
        logger.info(f"Stock réservé - État : {etat}")
        saga_etapes_counter.labels(etape="stock_reserve").inc()

        # 4. Paiement
        r_paiement = requests.post(f"{PAIEMENT_URL}?client_id={client_id}&commande_id={commande_id}")
        if r_paiement.status_code != 200:
            rollback_stocks(lignes, magasin_id)
            etat = EtatCommande.STOCK_LIBERE
            saga_failure_counter.inc()
            saga_etapes_counter.labels(etape="paiement_echec").inc()
            saga_duration_histogram.observe(time.time() - start_time)
            return {"status": "ECHEC", "étape": "Paiement", "etat": etat, "detail": "Paiement échoué"}

        etat = EtatCommande.PAIEMENT_EFFECTUE
        logger.info(f"Paiement effectué - État : {etat}")
        saga_etapes_counter.labels(etape="paiement").inc()

        # ✅ Fin de saga
        etat = EtatCommande.COMMANDE_CONFIRMEE
        logger.info(f"Saga réussie - État final : {etat}")
        saga_etapes_counter.labels(etape="commande_confirmee").inc()
        saga_success_counter.inc()
        saga_duration_histogram.observe(time.time() - start_time)
        return {
            "status": "SUCCES",
            "commande_id": commande_id,
            "montant": montant,
            "etat": etat,
            "message": "CommandeConfirmée"
        }

    except Exception as e:
        rollback_stocks(lignes, magasin_id)
        etat = EtatCommande.ECHEC
        logger.exception("Erreur dans la saga")
        saga_failure_counter.inc()
        saga_etapes_counter.labels(etape="exception").inc()
        saga_duration_histogram.observe(time.time() - start_time)
        return {"status": "ECHEC", "étape": "Exception", "etat": etat, "detail": str(e)}

def rollback_stocks(lignes, magasin_id):
    for ligne in lignes:
        try:
            requests.post(
                f"{STOCK_URL}/rollback",
                json={
                    "product_id": ligne["product_id"],
                    "quantite": ligne["quantite"],
                    "magasin_id": magasin_id
                }
            )
        except Exception as e:
            logger.warning(f"Échec du rollback pour produit {ligne['product_id']} : {e}")
