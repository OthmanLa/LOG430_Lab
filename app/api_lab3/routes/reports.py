# app/api_lab3/routes/reports.py
from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import date
from pydantic import BaseModel, Field
from typing import List
from fastapi.security import APIKeyHeader
from fastapi import Security
from app.cache import reports_cache
from app.controllers.rapport_controller import generate_sales_report

API_KEY_HEADER_NAME = "Authorization"
API_KEY = "token1"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Token invalide", headers={"WWW-Authenticate": "Bearer"})
    return api_key

router = APIRouter(
    tags=["Rapports"],
    dependencies=[Depends(verify_api_key)]
)

class ReportPeriod(BaseModel):
    start: date = Field(..., description="Date de début (AAAA-MM-JJ)", example="2025-06-01")
    end:   date = Field(..., description="Date de fin (AAAA-MM-JJ)", example="2025-06-10")

class SalesByStore(BaseModel):
    magasin: str          = Field(..., example="Magasin Nord")
    total_ventes: float   = Field(..., example=1234)

class SalesReport(BaseModel):
    periode: ReportPeriod
    ventes_par_magasin: List[SalesByStore]

@reports_cache
def _fetch_sales_report(start: date, end: date):
    return generate_sales_report(start, end)

@router.get(
    "/sales",
    response_model=SalesReport,
    summary="UC1 – Rapport consolidé des ventes",
    responses={
        200: {"description": "Rapport généré avec succès"},
        400: {"description": "Paramètres invalides ou hors période"},
        401: {"description": "Authentification requise"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def sales_report(
    start: date = Query(..., description="Date de début AAAA-MM-JJ", example="2025-06-01"),
    end:   date = Query(..., description="Date de fin AAAA-MM-JJ", example="2025-06-10")
):
    """
    UC1 – GET /api/v1/reports/sales?start=YYYY-MM-DD&end=YYYY-MM-DD
    Retourne un JSON structuré du rapport de ventes.
    """
    try:
        return _fetch_sales_report(start, end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
