from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///magasin.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
