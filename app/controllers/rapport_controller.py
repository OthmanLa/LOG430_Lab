from sqlalchemy import func, desc
from app.db.session import SessionLocal
from app.models.magasin import Magasin
from app.models.vente import Vente, LigneVente
from app.models.produit import Produit
from app.models.stock import Stock

def generer_rapport_consolide():
    session = SessionLocal()
    try:
        print(" --- Rapport consolidé des ventes ---\n")

        print(" Ventes par magasin :")
        ventes = session.query(
            Magasin.nom,
            func.sum(Vente.total).label("total_ventes")
        ).join(Vente).group_by(Magasin.id).all()

        for nom, total in ventes:
            print(f" - {nom} : {total:.2f}$")

        print(" Produits les plus vendus :")
        top_produits = session.query(
            Produit.nom,
            func.sum(LigneVente.quantite).label("total_vendu")
        ).join(LigneVente.produit).group_by(Produit.id).order_by(desc("total_vendu")).limit(5).all()

        for nom, quantite in top_produits:
            print(f" - {nom} : {quantite} unités vendues")

        print(" Stock restant par magasin :")
        stocks = session.query(
            Magasin.nom,
            Produit.nom,
            Stock.quantite
        ).join(Stock.magasin).join(Stock.produit).order_by(Magasin.nom).all()

        for magasin_nom, produit_nom, quantite in stocks:
            print(f" - {magasin_nom} | {produit_nom} : {quantite} unités")

    finally:
        session.close()
