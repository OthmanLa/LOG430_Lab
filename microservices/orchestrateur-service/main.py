from fastapi import FastAPI
from app.routes import orchestrateur
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Orchestrateur Service")

app.include_router(orchestrateur.router)

instrumentator = Instrumentator().instrument(app).expose(app)