from datetime import date
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

def generate_sales_report(start: date, end: date) -> dict:
    """
    Génère un rapport JSON-friendly des ventes consolidées entre deux dates.
    """
    session = SessionLocal()
    try:
        ventes_q = (
            session.query(
                Magasin.nom.label("magasin"),
                func.sum(Vente.total).label("total_ventes")
            )
            .join(Vente, Vente.magasin_id == Magasin.id)
            .filter(Vente.date.between(start, end))
            .group_by(Magasin.id)
            .all()
        )
        ventes_par_magasin = [
            {"magasin": nom, "total_ventes": float(total or 0)}
            for nom, total in ventes_q
        ]

        top_q = (
            session.query(
                Produit.nom.label("produit"),
                func.sum(LigneVente.quantite).label("total_vendu")
            )
            .join(LigneVente, LigneVente.produit_id == Produit.id)
            .join(Vente, LigneVente.vente_id == Vente.id)
            .filter(Vente.date.between(start, end))
            .group_by(Produit.id)
            .order_by(desc("total_vendu"))
            .limit(5)
            .all()
        )
        top_produits = [
            {"produit": nom, "total_vendu": int(qty)}
            for nom, qty in top_q
        ]

        stock_q = (
            session.query(
                Magasin.nom.label("magasin"),
                Produit.nom.label("produit"),
                Stock.quantite
            )
            .join(Stock, Stock.magasin_id == Magasin.id)
            .join(Produit, Stock.produit_id == Produit.id)
            .order_by(Magasin.nom)
            .all()
        )
        stock_par_magasin = [
            {"magasin": m_nom, "produit": p_nom, "quantite": q}
            for m_nom, p_nom, q in stock_q
        ]

        return {
            "periode": {"start": start.isoformat(), "end": end.isoformat()},
            "ventes_par_magasin": ventes_par_magasin,
            "top_produits": top_produits,
            "stock_par_magasin": stock_par_magasin
        }
    finally:
        session.close()