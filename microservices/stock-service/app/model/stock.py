from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.model.base import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    magasin_id = Column(Integer, ForeignKey("magasins.id"), nullable=False)
    quantite = Column(Integer, nullable=False)

    magasin = relationship("Magasin", back_populates="stocks")  # Optionnel

    def __repr__(self):
        return f"<Stock(magasin_id={self.magasin_id}, product_id={self.product_id}, quantite={self.quantite})>"
