from app.model.base import Base
from app.db.session import engine, SessionLocal

# ✅ Importer AVANT le create_all
from app.model.produit import Produit

def init_db():
    print("📦 Initialisation de la base produits...")

    # ✅ Créer les tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if not db.query(Produit).first():
        print("✅ Ajout des produits initiaux...")
        produit1 = Produit(nom="Chocolat", prix=3.99)
        produit2 = Produit(nom="Pain", prix=2.49)
        db.add_all([produit1, produit2])
        db.commit()
        print("✅ Produits insérés avec succès.")
    else:
        print("ℹ️ Produits déjà présents.")
    db.close()

if __name__ == "__main__":
    init_db()
