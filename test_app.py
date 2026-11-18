from app import app

def test_health_endpoint_returns_ok():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_root_endpoint_identifies_service():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["service"] == "sample-service"
