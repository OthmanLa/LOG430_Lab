from sqlalchemy import Engine
from app.db.session import SessionLocal
from app.model.magasin import Magasin  # ajoute ceci
from app.model.stock import Stock
from app.model.base import Base
from app.db.session import engine
...

def init_db():
    print("📦 Initialisation de la base stock...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Ajout automatique des magasins
    if not db.query(Magasin).first():
        noms = [
            "Magasin Centre-Ville",
            "Magasin Quartier-Nord",
            "Magasin Quartier-Sud",
            "Magasin Quartier-Est",
            "Magasin Quartier-Ouest",
            "Centre Logistique"
        ]
        db.add_all([Magasin(nom=nom) for nom in noms])
        db.commit()
        print("✅ Magasins initialisés.")

    # Ajout de stock de base si vide
    if not db.query(Stock).first():
        print("✅ Ajout d’un stock initial...")
        db.add_all([
            Stock(product_id=1, magasin_id=1, quantite=100),
            Stock(product_id=2, magasin_id=1, quantite=60)
        ])
        db.commit()
        print("✅ Stock initial inséré.")
    else:
        print("ℹ️ Stock déjà présent.")
    db.close()
