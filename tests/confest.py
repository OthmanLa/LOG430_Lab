# tests/conftest.py
import pytest
from app.db.init_db import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()
    yield
