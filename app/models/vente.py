from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Vente(Base):
    __tablename__ = 'ventes'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)
    lignes = relationship("LigneVente", back_populates="vente")

class LigneVente(Base):
    __tablename__ = 'lignes_vente'

    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey('ventes.id'))
    produit_id = Column(Integer, ForeignKey('produits.id'))
    quantite = Column(Integer)
    sous_total = Column(Float)

    vente = relationship("Vente", back_populates="lignes")
