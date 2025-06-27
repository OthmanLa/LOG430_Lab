from fastapi import FastAPI
from app.routes import ventes
#from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Ventes Service")
#init_db()

app.include_router(ventes.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)
