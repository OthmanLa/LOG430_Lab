from fastapi import FastAPI
from app.routes import paiements
from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Paiements Service")
init_db()

app.include_router(paiements.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)
