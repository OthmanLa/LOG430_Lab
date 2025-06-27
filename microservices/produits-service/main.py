from fastapi import FastAPI
from app.routes import products
from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Produits Service")
init_db()

app.include_router(products.router)

Instrumentator().instrument(app).expose(app)
