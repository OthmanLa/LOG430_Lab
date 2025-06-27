from app.db.session import SessionLocal
from app.model.produit import Produit

def update_product_api(product_id: int, name: str, price: float) -> dict:
    session = SessionLocal()
    try:
        prod = session.query(Produit).get(product_id)
        if not prod:
            raise ValueError("Produit non trouvé")
        prod.nom = name
        prod.prix = price
        session.commit()
        session.refresh(prod)
        return {"id": prod.id, "nom": prod.nom, "prix": prod.prix}
    finally:
        session.close()

def get_all_products_api() -> list[dict]:
    session = SessionLocal()
    try:
        produits = session.query(Produit).all()
        return [{"id": p.id, "nom": p.nom, "prix": p.prix} for p in produits]
    finally:
        session.close()

def get_product_by_id_api(product_id: int):
    db = SessionLocal()
    try:
        produit = db.query(Produit).filter(Produit.id == product_id).first()
        if not produit:
            raise ValueError("Produit non trouvé")
        return produit
    finally:
        db.close()