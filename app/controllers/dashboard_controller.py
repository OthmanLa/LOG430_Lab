from sqlalchemy import func, extract
from app.db.session import SessionLocal
from app.models.magasin import Magasin
from app.models.vente import Vente
from app.models.stock import Stock
from app.models.produit import Produit
import datetime

def afficher_tableau_de_bord():
    session = SessionLocal()
    try:
        print("\n --- Tableau de bord des performances ---\n")

        print(" Chiffre d'affaires par magasin :")
        chiffres = session.query(
            Magasin.nom,
            func.sum(Vente.total).label("total")
        ).join(Vente).group_by(Magasin.id).all()

        for nom, total in chiffres:
            print(f" - {nom} : {total:.2f}$")

        print("\n Produits en rupture (stock < 10) :")
        ruptures = session.query(Stock, Produit, Magasin).join(Produit).join(Magasin).filter(Stock.quantite < 10).all()
        if ruptures:
            for s, p, m in ruptures:
                print(f" - {p.nom} à {m.nom} : {s.quantite} unités")
        else:
            print("Aucune rupture de stock détectée.")

        print("\n Produits en surstock (stock > 300) :")
        surstocks = session.query(Stock, Produit, Magasin).join(Produit).join(Magasin).filter(Stock.quantite > 300).all()
        if surstocks:
            for s, p, m in surstocks:
                print(f" - {p.nom} à {m.nom} : {s.quantite} unités")
        else:
            print("Aucun surstock détecté.")

        print("\n Tendances hebdomadaires :")
        ventes_par_semaine = session.query(
            extract('week', Vente.date).label("semaine"),
            func.sum(Vente.total)
        ).group_by("semaine").order_by("semaine").all()

        for semaine, total in ventes_par_semaine:
            print(f" - Semaine {int(semaine)} : {total:.2f}$")

    finally:
        session.close()

def get_dashboard_metrics() -> dict:
    """
    Retourne les indicateurs clés :
    - total_ventes : somme de toutes les ventes
    - sous_total_ventes : nombre total de ventes
    - stock_faible : liste des stocks < 10 unités
    """
    session = SessionLocal()
    try:
        total_ventes = session.query(func.sum(Vente.total)).scalar() or 0
        sous_total_ventes = session.query(func.count(Vente.id)).scalar() or 0
        low_stock = (
            session.query(
                Stock.magasin_id,
                Stock.produit_id,
                Stock.quantite
            )
            .filter(Stock.quantite < 10)
            .all()
        )
        stock_alerts = [
            {"magasin_id": m_id, "produit_id": p_id, "quantite": qty}
            for m_id, p_id, qty in low_stock
        ]
        return {
            "total_ventes": float(total_ventes),
            "sous_total_ventes": sous_total_ventes,
            "stock_faible": stock_alerts
        }
    finally:
        session.close()