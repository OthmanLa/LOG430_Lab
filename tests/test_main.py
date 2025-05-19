"""Tests for app.main. Ensures hello() returns the expected greeting."""

from app.main import hello

def test_hello_returns_string() -> None:
    """hello() should return a string."""
    assert isinstance(hello(), str)

def test_hello_value() -> None:
    """hello() should return exactly 'Hello, World!'."""
    assert hello() == "Hello, World!"
