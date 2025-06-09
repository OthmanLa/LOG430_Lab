from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    magasin_id = Column(Integer, ForeignKey("magasins.id"))
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer, nullable=False)

    magasin = relationship("Magasin")
    produit = relationship("Produit")

    def __repr__(self):
        return f"<Stock(magasin_id={self.magasin_id}, produit_id={self.produit_id}, quantite={self.quantite})>"
