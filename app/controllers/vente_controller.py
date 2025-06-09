from datetime import datetime
from app.db.session import SessionLocal
from app.models.produit import Produit
from app.models.vente import Vente, LigneVente
from app.models.stock import Stock 
from sqlalchemy.exc import SQLAlchemyError

def enregistrer_vente(caisse_id=1, magasin_id=1):
    session = SessionLocal()
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

            stock = session.query(Stock).filter_by(produit_id=produit.id, magasin_id=magasin_id).first()
            if not stock:
                print(f"Pas de stock pour ce produit dans le magasin {magasin_id}.")
                continue

            quantite = int(input(f"Quantité à acheter (disponible : {stock.quantite}) : "))
            if quantite <= 0:
                print("Quantité invalide.")
                continue
            if quantite > stock.quantite:
                print("Stock insuffisant.")
                continue

            sous_total = produit.prix * quantite
            total += sous_total

            ligne = LigneVente(produit_id=produit.id, quantite=quantite, sous_total=sous_total)
            lignes.append(ligne)

            stock.quantite -= quantite 

        if not lignes:
            print("Aucune vente saisie.")
            return

        vente = Vente(date=datetime.now(), total=total, caisse_id=caisse_id, magasin_id=magasin_id, lignes=lignes)
        session.add(vente)
        session.commit()
        print(f"Vente enregistrée (caisse {caisse_id}, magasin {magasin_id}). Total : {total:.2f}$")

    except SQLAlchemyError as e:
        session.rollback()
        print("Erreur vente:", e)
    finally:
        session.close()



def afficher_ventes_par_caisse(caisse_id=None, magasin_id=None):
    session = SessionLocal()
    try:
        query = session.query(Vente)
        if caisse_id:
            query = query.filter(Vente.caisse_id == caisse_id)
        if magasin_id:
            query = query.filter(Vente.magasin_id == magasin_id)

        ventes = query.all()
        if not ventes:
            print("Aucune vente trouvée.")
            return

        print(f"\n--- Historique des ventes ---")
        for vente in ventes:
            print(f"ID: {vente.id} | Magasin: {vente.magasin_id} | Caisse: {vente.caisse_id} | Date: {vente.date} | Total: {vente.total:.2f}$")
    finally:
        session.close()

