# Cloud Detection Lab
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20CloudWatch%20%7C%20CloudTrail-orange?logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)
![Detection Engineering](https://img.shields.io/badge/Security-Detection%20Engineering-red)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green)

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
       │
       ▼
Docker Container
       │
       ▼
AWS EC2 (Terraform-managed)
       │
       ▼
CloudWatch Logs / Detection Pipelines (planned)
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
- Explicit logging of:
  - Authentication success and failure  
  - Authorization failures (403)  
  - Admin endpoint access  
  - Legacy-mode access paths  
- Environment-driven configuration  
- Optional bootstrap admin creation via environment variables  
- Containerized execution via Docker 

### Security Telemetry Design

The backend is intentionally instrumented to emit security-relevant events such as:

- `auth_login_failed`
- `auth_login_success`
- `admin_stats_accessed`
- `legacy_tenant_bypass_used`
- `cross_tenant_access_detected`
- `file_uploaded`
- `http_request`

These logs are designed to support:

- Brute-force detection  
- Password spraying detection  
- Privilege misuse detection  
- Cross-tenant access analysis  
- Rare endpoint monitoring  
- Suspicious upload behavior analysis  

The application acts as a controlled signal generator for detection engineering workflows.

See `app/README.md` for full backend setup.

### Infrastructure & Deployment

The backend is containerized using Docker and designed for deployment to AWS using Terraform.

#### Infrastructure Design Goals

- Infrastructure-as-Code (IaC) via Terraform  
- Controlled network exposure using security groups  
- Environment-based secret injection  
- Non-root container execution  
- Log streaming via stdout for centralized logging  

#### Planned AWS Components

- VPC  
- Public Subnet  
- Internet Gateway  
- EC2 instance (Docker runtime)  
- CloudWatch Logs  
- CloudTrail  
- VPC Flow Logs  
- Detection alarms via CloudWatch metric filters  

This enables:

- Full end-to-end observability  
- Cloud-native detection engineering workflows  
- Realistic cloud security simulations  

## Running with Docker (Backend Only)

Build the backend container:


```python
cd app
docker build -t cdl-backend -f app/Dockerfile app
```

Run the container

```python
docker run --rm -p 8000:8000 -e JWT_SECRET="dev-change-me" cdl-backend
```

If you want to bootstrap the admin while running, use the following command, no default admin exists
```python
docker run --rm -p 8000:8000 -e JWT_SECRET=dev-change-me -e BOOTSTRAP_ADMIN_EMAIL=admin@bootstrap.com -e BOOTSTRAP_ADMIN_PASSWORD=admin1234 cdl-backend
```


The API will be available at:
http://localhost:8000

Logs are emitted as structured JSON to stdout.

## Frontend Overview (React)

The frontend is a thin UI layer built to:

- exercise backend APIs realistically
- visualize session and auth state
- drive different backend execution paths
- Simulate user behavior patterns

### Key frontend features

- Login and registration
- Notes creation and viewing
- Note details view with legacy-mode toggle
- Session Inspector panel showing :
    - JWT presence
    - token expiry (`exp`, `iat`)
    - user metadata
    - example request headers

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
- Environment-driven secrets
- No secrets committed to source control
- No AWS credentials or cloud keys in repo

This project is safe to publish publicly.

## Detection Engineering Focus

This lab is designed to support detection development and validation.

### Planned Detection Examples

- Authentication abuse detection (failed login spikes)
- Password spraying detection
- Rare admin endpoint access
- Cross-tenant data access attempts
- Suspicious upload patterns
- IAM privilege misuse (CloudTrail-based)
- Network anomaly detection (VPC Flow Logs-based)

Detection logic will be implemented using:

- CloudWatch metric filters
- CloudWatch alarms
- Structured log analysis
- Attack simulation scripts

The goal is to demonstrate:

- Signal generation
- False positive tuning
- Alert validation
- Detection lifecycle thinking



## What this project is good for

- Detection engineering practice
- Cloud security demonstrations
- Terraform + AWS deployment walkthroughs
- Interview walkthroughs
- Explaining auth, authz, and telemetry
- Demonstrating realistic security tradeoffs

## What this project is NOT

- A production-ready SaaS
- A hardened authentication reference
- A polished UI showcase

Those tradeoffs are intentional.

## Future Extensions

- Full Terraform-based AWS deployment
- CloudWatch logging pipelines
- CloudTrail and VPC Flow Log integration
- Attack simulation scripts
- Detection rule repository
- Alert validation workflows
- Frontend hosting via S3 + CloudFront

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
