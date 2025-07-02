from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.model.base import Base

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    magasin_id = Column(Integer, nullable=False)  # 🆕 Magasin associé à la commande

    lignes = relationship("LigneCommande", back_populates="commande")

class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey("commandes.id"))
    product_id = Column(Integer)
    quantite = Column(Integer)

    commande = relationship("Commande", back_populates="lignes")