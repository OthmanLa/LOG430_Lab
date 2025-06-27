from fastapi import FastAPI
from app.routes import stocks
from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Stock Service")

init_db()
app.include_router(stocks.router)

Instrumentator().instrument(app).expose(app)
