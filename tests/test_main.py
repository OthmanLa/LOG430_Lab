from app.main import hello

def test_hello_returns_string():
    """La fonction doit renvoyer une chaîne."""
    assert isinstance(hello(), str)

def test_hello_value():
    """Le contenu exact doit être 'Hello, World!'."""
    assert hello() == "Hello, World!"
