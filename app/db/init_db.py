from app.models.base import Base
from app.db.session import engine
from app.models import produit, vente, magasin, stock
from app.db.session import SessionLocal

def init_db():
    print("Initialisation de la base...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if not db.query(magasin.Magasin).first():
        noms_magasins = [
            "Magasin Centre-Ville",
            "Magasin Quartier-Nord",
            "Magasin Quartier-Sud",
            "Magasin Quartier-Est",
            "Magasin Quartier-Ouest",
            "Centre Logistique"
        ]
        magasins = [magasin.Magasin(nom=nom) for nom in noms_magasins]

        db.add_all(magasins)
        db.commit()

        produit1 = produit.Produit(nom="Chocolat", prix=3.99)
        produit2 = produit.Produit(nom="Pain", prix=2.49)

        db.add_all([produit1, produit2])
        db.commit()

        for m in magasins[:-1]:
            db.add_all([
                stock.Stock(magasin_id=m.id, produit_id=produit1.id, quantite=100),
                stock.Stock(magasin_id=m.id, produit_id=produit2.id, quantite=60)
            ])

        centre_logistique = magasins[-1]
        db.add_all([
            stock.Stock(magasin_id=centre_logistique.id, produit_id=produit1.id, quantite=500),
            stock.Stock(magasin_id=centre_logistique.id, produit_id=produit2.id, quantite=500)
        ])

        db.commit()

    db.close()
