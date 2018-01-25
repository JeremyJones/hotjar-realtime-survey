from apistar.test import TestClient
from app import app
from project.routes import hello


def default_page_return() -> dict:
    """
    Single copy of the string returned by the default home page.
    """
    return {'message': "Welcome to the future, mystery person!"}


def test_hello() -> bool:
    """
    Testing a view directly.
    """
    data = hello()
    assert data == default_page_return()

def get_json_url(url, returnResponse=False) -> dict:
    """
    Return the json content returned from a URL, parsed to a dict.
    """
    client = TestClient(app)
    response = client.get(url)
    return response if returnResponse else response.json()

def test_http_request() -> bool:
    """
    Testing a view, using the test client.
    """
    response = get_json_url('http://localhost:8080/',
                            returnResponse=True)
    assert response.status_code == 200
    assert response.json() == default_page_return()

def test_proxy_http_request() -> bool:
    """
    Same test view, using the client but through port 80.
    """
    response = get_json_url('http://localhost/',
                            returnResponse=True)
    assert response.status_code == 200
    assert response.json() == default_page_return()
