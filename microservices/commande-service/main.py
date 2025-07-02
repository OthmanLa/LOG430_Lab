from fastapi import FastAPI
from app.routes import commandes
from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Commandes Service")

init_db()  # ← Création automatique des tables

app.include_router(commandes.router, prefix="/api/v1")
Instrumentator().instrument(app).expose(app)
