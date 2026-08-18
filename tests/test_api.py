import os
os.environ["DATABASE_URL"] = "sqlite:///./test_sentinelx.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_event():
    response = client.post("/api/events", json={
        "source": "linux",
        "event_type": "process_execution",
        "message": "sudo -u root whoami",
        "source_ip": "203.0.113.10"
    })
    assert response.status_code == 200
    assert response.json()["source"] == "linux"
