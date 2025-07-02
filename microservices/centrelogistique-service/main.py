from fastapi import FastAPI
from app.routes import centrelogistiques
from app.init_db import init_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Centre Logistique Service")

# Initialisation de la base de données (SQLite)
init_db()

# Inclusion des routes (ajout stock, etc.)
app.include_router(centrelogistiques.router)

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app)
