from app.db.session import engine, SessionLocal
from app.model.base import Base
from app.model.magasin import Magasin
from app.model.stock import Stock

def init_db():
    print("🔧 Initialisation de la base centrelogistique...")

    # Création des tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Ajouter les magasins s'ils ne sont pas encore là
        noms_magasins = [
            "Magasin Centre-Ville",
            "Magasin Quartier-Nord",
            "Magasin Quartier-Sud",
            "Magasin Quartier-Est",
            "Magasin Quartier-Ouest",
            "Centre Logistique"
        ]

        for nom in noms_magasins:
            if not db.query(Magasin).filter_by(nom=nom).first():
                db.add(Magasin(nom=nom))

        db.commit()
        print("✅ Magasins initialisés.")

    finally:
        db.close()

# Optionnel si tu veux pouvoir exécuter ce fichier seul
if __name__ == "__main__":
    init_db()
