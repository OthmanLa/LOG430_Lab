from app.models.base import Base
from app.db.session import engine

from app.models import produit, vente

def init_db():
    print("oui")
    Base.metadata.create_all(bind=engine)

