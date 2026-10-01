from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_rules():
    assert client.get("/rules").status_code == 200

def test_anomaly_detection():
    events = [{"latency_ms": 100+i, "amount": 1000, "decline_rate": .02, "retries": 1} for i in range(8)]
    events[-1] = {"latency_ms": 1200, "amount": 9000, "decline_rate": .8, "retries": 9}
    response = client.post("/anomalies/detect", json={"events": events})
    assert response.status_code == 200
    body = response.json()
    assert body["event_count"] == 8
