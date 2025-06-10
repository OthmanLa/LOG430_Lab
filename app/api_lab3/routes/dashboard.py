from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from fastapi.security import APIKeyHeader
from fastapi import Security
from app.controllers.dashboard_controller import get_dashboard_metrics

API_KEY_HEADER_NAME = "Authorization"
API_KEY = "token1"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Token invalide", headers={"WWW-Authenticate": "Bearer"})
    return api_key

router = APIRouter(
    tags=["Dashboard"],
    dependencies=[Depends(verify_api_key)]
    )

@router.get(
    "/",
    summary="Voir les indicateurs globaux des magasins",
    response_model=dict
)
def dashboard():
    """
    UC3 – GET /api/v1/dashboard
    Retourne des indicateurs globaux de performance.
    """
    try:
        return get_dashboard_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
