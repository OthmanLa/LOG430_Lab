from sqlalchemy import Column, Integer, String
from app.model.base import Base
from sqlalchemy.orm import relationship

class Magasin(Base):
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True, nullable=False)

    stocks = relationship("Stock", back_populates="magasin")  # Optionnel
