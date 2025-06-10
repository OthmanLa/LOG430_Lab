# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from api_main import app
from datetime import datetime, timedelta

client = TestClient(app)

def auth_hdr():
    return {"Authorization": "token1"}

def test_reports_sales_unauthorized():
    r = client.get("/api/v1/reports/sales?start=2025-06-01&end=2025-06-07")
    assert r.status_code == 401

def test_reports_sales_success():
    r = client.get(
        "/api/v1/reports/sales?start=2025-06-01&end=2025-06-07",
        headers=auth_hdr()
    )
    assert r.status_code == 200
    json = r.json()
    assert "periode" in json and "ventes_par_magasin" in json

def test_stores_stock():
    r = client.get("/api/v1/stores/1/stock", headers=auth_hdr())
    assert r.status_code == 200
    json = r.json()
    assert "store_id" in json and "stock" in json


@pytest.fixture(scope="module")
def product_id():
    resp = client.post("/api/v1/products/", json={"nom":"Test","prix":1.23}, headers=auth_hdr())
    assert resp.status_code == 200 or resp.status_code == 201
    data = resp.json()
    return data.get("id") or client.get("/api/v1/products/search/Test", headers=auth_hdr()).json()[0]["id"]

