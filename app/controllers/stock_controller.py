from app.db.session import SessionLocal
from app.models.stock import Stock
from app.models.produit import Produit
from app.models.magasin import Magasin

def afficher_stock_magasin(magasin_id: int):
    session = SessionLocal()
    try:
        stocks = session.query(Stock).filter_by(magasin_id=magasin_id).all()
        if not stocks:
            print(f"Aucun stock trouvé pour le magasin {magasin_id}.")
            return

        print(f"\n--- Stock pour le magasin {magasin_id} ---")
        for stock in stocks:
            produit = session.query(Produit).get(stock.produit_id)
            print(f"{produit.nom} : {stock.quantite} unités restantes")

    finally:
        session.close()


def ajouter_stock(magasin_id, produit_id, quantite):
    session = SessionLocal()
    try:
        if quantite < 0:
            print("Quantité invalide.")
            return

        stock = Stock(magasin_id=magasin_id, produit_id=produit_id, quantite=quantite)
        session.add(stock)
        session.commit()
        print(f"Stock ajouté : {quantite} unités pour produit {produit_id} dans magasin {magasin_id}")
    except Exception as e:
        session.rollback()
        print("Erreur stock :", e)
    finally:
        session.close()

def consulter_stock_central():
    session = SessionLocal()
    try:
        centre = session.query(Magasin).filter(Magasin.nom.ilike("Centre Logistique")).first()
        if not centre:
            print(" Centre logistique introuvable.")
            return

        stocks = session.query(Stock).filter_by(magasin_id=centre.id).all()
        print(" Stock du Centre Logistique :")
        for stock in stocks:
            produit = session.query(Produit).get(stock.produit_id)
            print(f" - {produit.nom} : {stock.quantite} unités")
    finally:
        session.close()


def demander_reapprovisionnement(magasin_id, produit_id, quantite):
    session = SessionLocal()
    try:
        centre = session.query(Magasin).filter(Magasin.nom.ilike("Centre Logistique")).first()
        if not centre:
            print(" Centre logistique introuvable.")
            return

        stock_central = session.query(Stock).filter_by(
            magasin_id=centre.id, produit_id=produit_id).first()

        if not stock_central or stock_central.quantite < quantite:
            print(" Stock insuffisant dans le centre logistique.")
            return

        stock_central.quantite -= quantite

        stock_magasin = session.query(Stock).filter_by(
            magasin_id=magasin_id, produit_id=produit_id).first()

        if stock_magasin:
            stock_magasin.quantite += quantite
        else:
            stock_magasin = Stock(magasin_id=magasin_id, produit_id=produit_id, quantite=quantite)
            session.add(stock_magasin)

        session.commit()
        print(f" Réapprovisionnement réussi : {quantite} unités transférées au magasin {magasin_id}")

    except Exception as e:
        session.rollback()
        print(" Erreur de réapprovisionnement :", e)
    finally:
        session.close()

def get_stock_by_store(store_id: int):
    """
    Récupère la liste des produits et quantités pour un magasin donné.
    Retourne None si le magasin n'existe pas, sinon une liste de dicts.
    """
    session = SessionLocal()
    try:
        stocks = session.query(Stock).filter(Stock.magasin_id == store_id).all()
        if not stocks:
            return []  
        result = []
        for s in stocks:
            prod = session.query(Produit).get(s.produit_id)
            result.append({
                "produit_id":   s.produit_id,
                "produit_nom":  prod.nom if prod else None,
                "quantite":     s.quantite
            })
        return result
    finally:
        session.close()


