from fastapi import FastAPI
from app.routes import clients
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Clients Service")
app.include_router(clients.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)