# tests/conftest.py
import pytest
from app.db.init_db import init_db

# Automatically initialize the database schema before tests
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # This will create all tables as per your models
    init_db()
    yield
    # Optionally, teardown logic here (e.g., drop tables)
