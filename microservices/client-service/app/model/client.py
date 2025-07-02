from sqlalchemy import Column, Integer, String, Float
from app.model.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    email = Column(String, unique=True)
    solde = Column(Float, default=100.0)
