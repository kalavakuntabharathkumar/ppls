# PayPulse — Rules Studio & Anomaly Detection Platform

A portfolio-grade self-service rules dashboard and anomaly-detection API.

## Components
- React + TypeScript frontend
- PureScript rules module demonstrating typed rule evaluation
- FastAPI backend
- scikit-learn Isolation Forest detector
- ClickHouse schema/seed scripts
- Kubernetes manifests
- Terraform environment scaffold
- GitHub Actions CI/CD

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` if needed.

## Endpoints
- `GET /health`
- `GET /rules`
- `POST /rules`
- `POST /anomalies/detect`

The anomaly endpoint accepts event rows and returns Isolation Forest predictions,
scores, and a compact alert summary. A deterministic demo dataset is included.

## Deployment
`infra/main.tf` is a deliberately small Terraform scaffold, while `k8s/` contains
a Deployment and Service suitable for adapting to a real cluster.
