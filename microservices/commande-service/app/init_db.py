# app/init_db.py
from app.db.session import engine
from app.model.base import Base
from app.model.commande import Commande, LigneCommande

def init_db():
    Base.metadata.create_all(bind=engine)
