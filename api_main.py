from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid, logging

# 1. Import du setup logging et metrics
from app.logging_config import setup_logging
from app.metrics import setup_metrics

# 2. Configuration du logger JSON
setup_logging()
logger = logging.getLogger("api")

# 3. Création de l’application FastAPI
app = FastAPI(
    title="API Multi-Magasins",
    description="""
Une API RESTful pour :
- Consulter le stock d’un magasin
- Générer un rapport consolidé des ventes
- Visualiser un tableau de bord FinOps
- Gérer les produits (CRUD)
""",
    version="1.0.0"
)

# 4. Middleware pour CORS (inchangé)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Middleware pour tracer chaque requête
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # Génération d’un ID unique pour tracer la requête
    request_id = str(uuid.uuid4())
    # Stockage dans l’objet request (utile si tu veux le réutiliser dans tes routes)
    request.state.request_id = request_id

    # Logging d’entrée
    logger.info(
        f"Incoming {request.method} {request.url.path}",
        extra={"message_id": request_id}
    )

    # Appel de la route
    response = await call_next(request)

    # Logging de sortie
    logger.info(
        f"Completed {request.method} {request.url.path} → {response.status_code}",
        extra={"message_id": request_id}
    )

    return response

# 6. Initialisation des métriques Prometheus
setup_metrics(app)

# 7. Inclusion de tes routers (inchangé)
from app.api_lab3.routes import stores, products, reports, dashboard

app.include_router(stores.router,    prefix="/api/v1/stores",    tags=["Magasins"])
app.include_router(products.router,  prefix="/api/v1/products",  tags=["Produits"])
app.include_router(reports.router,   prefix="/api/v1/reports",   tags=["Rapports"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
