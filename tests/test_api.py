import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_status():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {
    'Version': '0.1', 
    'System': 'd4k CT Load Microservice'
  }
