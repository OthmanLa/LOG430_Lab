from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import clients
from app.init_db import init_db

app = FastAPI(title="Client Service")

init_db()
app.include_router(clients.router)

Instrumentator().instrument(app).expose(app)
