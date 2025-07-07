from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    event_type = Column(String)
    timestamp = Column(DateTime)
    data = Column(Text)

class CommandeProjection(Base):
    __tablename__ = "commande_projection"

    commande_id = Column(String, primary_key=True, index=True)
    etat = Column(String)  # Exemple : "Commande passée", "Commande payée"