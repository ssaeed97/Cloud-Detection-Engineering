# Cloud Detection Lab

A **full-stack security lab** designed to demonstrate **authentication, authorization, and detection engineering concepts** using a deliberately minimal application.

This project is built to:
- simulate realistic application behavior
- generate meaningful security telemetry
- support detection engineering and security research
- serve as an interview-ready, explainable system

It is **not** intended to be a production-ready SaaS.



## High-level Architecture

```text
┌────────────┐      HTTP / JSON     ┌──────────────┐
│ React UI   │ ───────────────────▶ │ FastAPI API  │
│ (Vite)     │                      │ (Python)     │
└────────────┘                      └──────────────┘
       │                                     │
       │ JWT (Authorization header)          │
       │                                     ▼
       │                            Structured JSON logs
       │                            (auth, authz, errors)
```

- Frontend: React + TypeScript (Vite)
- Backend: FastAPI (Python)
- Auth: JWT-based authentication
- Focus: observability, security signals, and detection-friendly behavior

## Project Structure

```text
.
├── app/        # FastAPI backend
├── web/        # React frontend
├── terraform/  # (planned) infrastructure as code
└── README.md   # This file
```

Each subdirectory contains its own README with deeper implementation details.

## Backend Overview (FastAPI)

The backend is a multi-tenant API that exposes:

- user registration and login
- JWT-based authentication
- tenant-scoped notes
- file upload endpoints
- admin-only endpoints

### Key backend characteristics

- Structured JSON logging for every request
- Explicit logging of auth success/failure, authorization errors (403s), and legacy access paths
- Environment-driven configuration
- Optional bootstrap admin creation via env vars

### Why it exists

The backend is intentionally simple, but:

- mirrors real-world auth flows
- contains legacy compatibility paths
- produces logs suitable for brute-force detection, privilege misuse detection, and cross-tenant access analysis

See `app/README.md` for full backend setup.

## Running with Docker (Backend Only)
s
Build the backend container:


```python
cd app
docker build -t cdl-backend -f app/Dockerfile app
```

Run the container

```python
docker run --rm -p 8000:8000 -e JWT_SECRET="dev-change-me" cdl-backend
```

If you want to bootstrap the admin while running, use the following command
```python
docker run --rm -p 8000:8000 -e JWT_SECRET=dev-change-me -e BOOTSTRAP_ADMIN_EMAIL=admin@example.com -e BOOTSTRAP_ADMIN_PASSWORD=AdminPass123! cdl-backend
```


The API will be available at:
http://localhost:8000

Logs are emitted as structured JSON to stdout.

## Frontend Overview (React)

The frontend is a thin UI layer built to:

- exercise backend APIs realistically
- visualize session and auth state
- drive different backend execution paths

### Key frontend features

- Login and registration
- Notes creation and viewing
- Note details view with legacy-mode toggle
- Session Inspector panel showing JWT presence, token expiry (`exp`, `iat`), user metadata, and example request headers

### Intentional design choices

- JWTs stored in `localStorage` (demo only)
- Legacy mode toggle exposed in UI
- Minimal styling, maximum clarity

See `web/README.md` for full frontend setup.

## Legacy Mode (Important Concept)

The application includes an explicit legacy access mode.

This simulates:

- deprecated or backward-compatible code paths
- feature-flag-controlled behavior
- historically weaker authorization logic

Legacy mode is intentionally exposed to:

- generate distinct log signals
- demonstrate detection of risky access paths
- support "before vs after" security stories

## Security Model (at a glance)

- JWT authentication
- Role-based access control (`user` / `admin`)
- Tenant isolation at the API layer
- No secrets committed to source control
- No AWS credentials or cloud keys in repo

This project is safe to publish publicly.

## What this project is good for

- Detection engineering practice
- Security research demos
- Interview walkthroughs
- Explaining auth, authz, and telemetry
- Demonstrating realistic security tradeoffs

## What this project is NOT

- A production-ready SaaS
- A hardened authentication reference
- A polished UI showcase

Those tradeoffs are intentional.

## License

MIT

## Final note

This repository is structured to be:

- readable
- explainable
- extendable

Future extensions may include:

- containerization
- Terraform-based deployment
- cloud logging pipelines
- detection rule examples
