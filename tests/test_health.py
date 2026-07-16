from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["application"] == "Home Logistics Platform"
    assert body["version"] == "0.1.0"