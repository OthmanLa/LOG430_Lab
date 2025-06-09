from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Magasin(Base):
    __tablename__ = 'magasins'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Magasin(nom='{self.nom}')>"
