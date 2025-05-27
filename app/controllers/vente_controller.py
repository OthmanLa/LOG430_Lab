from datetime import datetime
from app.db.session import Session
from app.models.produit import Produit
from app.models.vente import Vente, LigneVente

def enregistrer_vente(caisse_id=1):
    session = Session()
    lignes = []
    total = 0.0

    try:
        while True:
            nom = input("Nom du produit (ou 'fin' pour terminer) : ")
            if nom.lower() == 'fin':
                break

            produit = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
            if not produit:
                print(f"Produit '{nom}' non trouvé.")
                continue

            quantite = int(input(f"Quantité à acheter (disponible : {produit.quantite}) : "))
            if quantite <= 0:
                print("Quantité invalide.")
                continue

            if quantite > produit.quantite:
                print("Stock insuffisant.")
                continue

            sous_total = produit.prix * quantite
            total += sous_total

            ligne = LigneVente(produit_id=produit.id, quantite=quantite, sous_total=sous_total)
            lignes.append(ligne)

            produit.quantite -= quantite 

        if not lignes:
            print("Aucune vente saisie.")
            return

        vente = Vente(date=datetime.now(), total=total, caisse_id=caisse_id, lignes=lignes)
        session.add(vente)
        session.commit()
        print(f"Vente enregistrée dans la caisse {caisse_id}. Total : {total:.2f}$")

    except Exception as e:
        session.rollback()
        print("Erreur vente:", e)
    finally:
        session.close()


def afficher_ventes_par_caisse(caisse_id):
    session = Session()
    try:
        ventes = session.query(Vente).filter(Vente.caisse_id == caisse_id).all()
        if not ventes:
            print(f"Aucune vente trouvée pour la caisse {caisse_id}.")
            return
        print(f"\n--- Historique des ventes pour la caisse {caisse_id} ---")
        for vente in ventes:
            print(f"ID: {vente.id} | Date: {vente.date} | Total: {vente.total:.2f}$")
    finally:
        session.close()
