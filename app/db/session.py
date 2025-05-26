from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Création de l'engine SQLite
engine = create_engine("sqlite:///magasin.db", echo=True)

# Création de la session
Session = sessionmaker(bind=engine)
