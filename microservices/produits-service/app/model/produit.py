from sqlalchemy import Column, Integer, String, Float
from app.model.base import Base

class Produit(Base):
    __tablename__ = 'produits'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prix = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Produit(nom='{self.nom}', prix={self.prix})>"
