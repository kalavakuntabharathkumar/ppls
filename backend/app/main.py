from typing import Any
import uuid
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.ensemble import IsolationForest

app = FastAPI(title="PayPulse API", version="1.0.0")

rules: list[dict[str, Any]] = [
    {"id": "rule-001", "name": "Prefer Bank A", "condition": "merchant_tier == 'gold'", "action": "bank-a", "enabled": True},
    {"id": "rule-002", "name": "Failover Bank B", "condition": "gateway_success_rate < 0.92", "action": "bank-b", "enabled": True},
]

class RuleIn(BaseModel):
    name: str = Field(min_length=2)
    condition: str = Field(min_length=2)
    action: str = Field(min_length=2)
    enabled: bool = True

class Event(BaseModel):
    latency_ms: float
    amount: float
    decline_rate: float
    retries: float

class AnomalyRequest(BaseModel):
    events: list[Event]

@app.get("/health")
def health():
    return {"status": "ok", "service": "paypulse"}

@app.get("/rules")
def list_rules():
    return rules

@app.post("/rules")
def create_rule(rule: RuleIn):
    item = {"id": str(uuid.uuid4()), **rule.model_dump()}
    rules.append(item)
    return item

@app.post("/anomalies/detect")
def detect(req: AnomalyRequest):
    if len(req.events) < 5:
        return {"error": "at least 5 events are required"}
    X = np.array([[e.latency_ms, e.amount, e.decline_rate, e.retries] for e in req.events], dtype=float)
    model = IsolationForest(n_estimators=150, contamination="auto", random_state=42)
    predictions = model.fit_predict(X)
    scores = model.decision_function(X)
    results = [
        {
            "index": i,
            "anomaly": bool(predictions[i] == -1),
            "score": round(float(scores[i]), 5),
        }
        for i in range(len(predictions))
    ]
    return {
        "event_count": len(results),
        "anomaly_count": sum(r["anomaly"] for r in results),
        "results": results,
    }
