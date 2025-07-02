from sqlalchemy import Column, Integer
from app.model.base import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)    # pas besoin de ForeignKey ici
    magasin_id = Column(Integer, nullable=False)    # pas besoin de ForeignKey ici
    quantite = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Stock(magasin_id={self.magasin_id}, product_id={self.product_id}, quantite={self.quantite})>"
