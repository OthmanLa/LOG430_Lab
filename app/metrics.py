from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()

def setup_metrics(app):
    # Instrumente automatiquement tous les endpoints
    instrumentator.instrument(app).expose(
        app,
        endpoint="/metrics",       # URL pour Prometheus
        include_in_schema=False     # pas exposé dans /docs
    )
