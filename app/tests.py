from apistar.test import TestClient
from app import app
from project.routes import homepage
from re import match
from unittest import TestCase, skip


class MyTest(TestCase):
    """
    Class for structured tests.
    """
    def setUp(self:TestCase) -> None:
        pass
    
    def tearDown(self:TestCase) -> None:
        pass

    def test_this_class(self:TestCase) -> bool:
        self.assertEqual(1, 1)

    def test_templated_page(self:TestCase) -> bool:
        """
        Verify that the basic page templates are processing ok.
        """
        response = get_response('http://localhost:8080/hi')
        self.assertEqual(b'<html>\n<h1>Hi Everybody!</h1>\n</html>',
                        response.content)

def default_page_return() -> dict:
    """
    Single copy of the string returned by the default home page.
    """
    return {'message': "Welcome to the future, mystery person!"}

def test_homepage() -> bool:
    """
    Testing a view directly.
    """
    data:dict = homepage()
    assert data == default_page_return()

def get_response(url:str):
    """
    Return a URL resource using the TestClient
    """
    client:TestClient = TestClient(app)
    return client.get(url)

def get_json_url(url:str, returnResponse:bool=False) -> dict:
    """
    Return the json content returned from a URL, parsed to a dict.
    """
    response = get_response(url)
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


