from fastapi import FastAPI
from app.routes import commandes
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Commandes Service")
app.include_router(commandes.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)

