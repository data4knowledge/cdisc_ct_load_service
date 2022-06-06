import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_status():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {
    'version': '0.1', 
    'system': 'd4k CT Load Microservice'
  }

def test_configuration_ok():
  response = client.post("/configuration")
  assert response.status_code == 200
  assert response.json() == {
    'status': 'ok'
  }
