from app.db.session import Session
from app.models.produit import Produit

def ajouter_produit(nom, prix, quantite):
    session = Session()
    try:
        existant = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
        if existant:
            print(f"Le produit '{nom}' existe déjà !")
            return
        if prix < 0:
            print("Le prix est négatif.")
            return
        if quantite < 0:
            print("La quantité est négative.")
            return
        produit = Produit(nom=nom, prix=prix, quantite=quantite)
        session.add(produit)
        session.commit()
        print(f"Produit ajouté avec succès : {produit}")
    except Exception as e:
        session.rollback()
        print("Erreur :", e)
    finally:
        session.close()

def rechercher_produit(nom):
    session = Session()
    try:
        resultats = session.query(Produit).filter(Produit.nom.ilike(f"%{nom}%")).all()
        if resultats:
            print("Voici le produits :")
            for p in resultats:
                print(f" - {p.nom} | Prix: {p.prix}$ | Dsiponibilité: {p.quantite}")
        else:
            print("Aucun produit trouvé.")
    finally:
        session.close()
