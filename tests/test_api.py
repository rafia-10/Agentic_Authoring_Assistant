from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_generate_metadata_endpoint():
    response = client.post("/generate", data={"text": "Sample input for testing"})
    assert response.status_code == 200
    assert "Results" in response.text
