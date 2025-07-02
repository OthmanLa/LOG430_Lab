from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from app.model.base import Base

class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    commande_id = Column(Integer, nullable=False)
    montant = Column(Float, nullable=False)
    date_paiement = Column(DateTime, default=datetime.utcnow)
