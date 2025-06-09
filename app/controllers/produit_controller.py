from app.db.session import SessionLocal
from app.models.produit import Produit
from app.models.stock import Stock
from app.models.magasin import Magasin

def ajouter_produit(nom, prix):
    session = SessionLocal()
    try:
        existant = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
        if existant:
            print(f"Le produit '{nom}' existe déjà !")
            return
        if prix < 0:
            print("Le prix est négatif.")
            return

        produit = Produit(nom=nom, prix=prix)
        session.add(produit)
        session.commit()
        print(f"Produit ajouté avec succès : {produit}")
    except Exception as e:
        session.rollback()
        print("Erreur :", e)
    finally:
        session.close()

def rechercher_produit(nom):
    session = SessionLocal()
    try:
        resultats = session.query(Produit).filter(Produit.nom.ilike(f"%{nom}%")).all()
        if resultats:
            print("Produits trouvés :")
            for p in resultats:
                print(f" - {p.nom} | Prix: {p.prix}$")
                stocks = session.query(Stock).filter_by(produit_id=p.id).all()
                for s in stocks:
                    mag = session.query(Magasin).get(s.magasin_id)
                    print(f"    ↳ {s.quantite} unités au {mag.nom}")
        else:
            print("Aucun produit trouvé.")
    finally:
        session.close()

def modifier_produit():
    session = SessionLocal()
    try:
        nom = input("Nom du produit à modifier : ")
        produit = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
        if not produit:
            print(f"Produit '{nom}' non trouvé.")
            return

        print(f"\nProduit actuel : nom = {produit.nom}, prix = {produit.prix}")
        
        nouveau_nom = input(f"Nouveau nom [{produit.nom}] : ") or produit.nom
        nouveau_prix = input(f"Nouveau prix [{produit.prix}] : ") or produit.prix

        produit.nom = nouveau_nom
        produit.prix = float(nouveau_prix)

        session.commit()
        print(" Produit mis à jour avec succès.")
    except Exception as e:
        session.rollback()
        print(" Erreur lors de la modification :", e)
    finally:
        session.close()

def ajouter_produit_centre():
    session = SessionLocal()
    try:
        nom = input("Nom du produit : ")
        prix = float(input("Prix : "))

        existant = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
        if existant:
            print(" Ce produit existe déjà.")
            return

        produit = Produit(nom=nom, prix=prix)
        session.add(produit)
        session.commit() 

        quantite = int(input("Quantité initiale à stocker au Centre Logistique : "))
        centre_id = 6  

        stock = Stock(magasin_id=centre_id, produit_id=produit.id, quantite=quantite)
        session.add(stock)
        session.commit()

        print(f"Produit '{nom}' ajouté avec succès au Centre Logistique.")
    except Exception as e:
        session.rollback()
        print(" Erreur :", e)
    finally:
        session.close()
