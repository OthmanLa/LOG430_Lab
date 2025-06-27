from fastapi import FastAPI
from app.routes import paniers
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Paniers Service")
app.include_router(paniers.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)

