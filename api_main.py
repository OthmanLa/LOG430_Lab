
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api_lab3.routes import stores, products, reports, dashboard

app = FastAPI(
    title="API Multi-Magasins",
    description="""
Une API RESTful pour :
- Consulter le stock d’un magasin
- Générer un rapport consolidé des ventes
- Visualiser un tableau de bord FinOps
- Gérer les produits (CRUD)
""",
    version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stores.router,    prefix="/api/v1/stores",    tags=["Magasins"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Produits"])
app.include_router(reports.router,   prefix="/api/v1/reports",   tags=["Rapports"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
