from app.model.base import Base
from app.db.session import engine, SessionLocal
from app.model.stock import Stock

def init_db():
    print("📦 Initialisation de la base stock...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
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

if __name__ == "__main__":
    init_db()
