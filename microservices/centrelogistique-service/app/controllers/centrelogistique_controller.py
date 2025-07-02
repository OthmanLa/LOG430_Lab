import requests
from app.db.session import SessionLocal
from app.model.magasin import Magasin
from app.model.stock import Stock
from fastapi import HTTPException


STOCK_SERVICE_URL = "http://stock-service:8000"
HEADERS = {"Authorization": "token1"}

def ajouter_ou_mettre_a_jour_stock(product_id: int, magasin_id: int, quantite: int):
    try:
        response = requests.get(
            f"{STOCK_SERVICE_URL}/api/v1/stocks/{product_id}?magasin_id={magasin_id}",
            headers=HEADERS
        )

        if response.status_code == 200:
            current_stock = response.json()
            nouvelle_quantite = current_stock["quantite"] + quantite

            update_response = requests.put(
                f"{STOCK_SERVICE_URL}/api/v1/stocks/{product_id}?magasin_id={magasin_id}",
                headers=HEADERS,
                json={"quantite": nouvelle_quantite}
            )
            return update_response.json()

        elif response.status_code == 404:
            create_response = requests.post(
                f"{STOCK_SERVICE_URL}/api/v1/stocks/",
                headers=HEADERS,
                json={
                    "product_id": product_id,
                    "magasin_id": magasin_id,
                    "quantite": quantite
                }
            )
            if create_response.status_code != 201:
                raise HTTPException(status_code=create_response.status_code, detail=create_response.text)
            return create_response.json()

        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur communication avec stock-service: {str(e)}")