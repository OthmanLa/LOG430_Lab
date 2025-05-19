from app.main import hello

def test_hello_returns_string():
    assert isinstance(hello(), str)

def test_hello_value():
    assert hello() == "Hello, World!"
