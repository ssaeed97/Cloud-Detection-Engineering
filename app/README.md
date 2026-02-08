# Cloud Detection Lab App (v1)

FastAPI multi-tenant API with structured JSON logging for detection engineering labs.

## Safe for public repos
- No AWS keys
- No credentials in code
- Uses env vars for secrets (JWT secret, optional bootstrap admin)

## Run locally

```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
