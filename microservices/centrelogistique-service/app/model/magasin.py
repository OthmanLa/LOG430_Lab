from sqlalchemy import Column, Integer, String
from app.model.base import Base

class Magasin(Base):
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
