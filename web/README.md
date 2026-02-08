# Frontend — Cloud Detection Lab (React + Vite)

This folder contains the **React frontend** for the Cloud Detection Lab project.

The frontend is intentionally lightweight and is designed to:
- exercise backend APIs realistically
- generate meaningful authentication and authorization telemetry
- support security and detection engineering use cases

It is **not** a full production UI by design.

---

## Tech Stack

- **React** (TypeScript)
- **Vite** (dev server + build tool)
- **Fetch API** (wrapped via a custom API client)
- **LocalStorage** (for demo-only token storage)

---

## Project Structure

```text
web/
├── index.html # Single HTML entry point
├── src/
│ ├── main.tsx # React entry point
│ ├── App.tsx # Top-level app controller
│ ├── api/
│ │ └── client.ts # Centralized API wrapper
│ ├── auth/
│ │ └── token.ts # JWT + session helpers
│ ├── components/
│ │ ├── Guard.tsx # Auth guard for protected pages
│ │ ├── NoteDetails.tsx # Note details + legacy toggle
│ │ └── SessionInspector.tsx # Session/JWT inspection panel
│ ├── pages/
│ │ ├── Login.tsx # Login / registration
│ │ └── Notes.tsx # Notes UI
│ └── styles.css # Global styles
├── vite-env.d.ts # Vite environment typing
└── .env.example # Example environment config
```

---


## Local Setup

### Prerequisites
- Node.js 18+
- Backend API running locally (FastAPI)

### Install dependencies

npm install

## Configure Environment

Create a local `.env` file:


`cp .env.example .env`


Edit `.env` if needed:

`VITE_API_BASE_URL=http://localhost:8000`


## Run the Frontend


npm run dev


The app will be available at:

`http://localhost:5173`

## Authentication Model (Important)

- JWT access tokens are stored in `localStorage`.
- Tokens are attached to requests as:


`Authorization: Bearer <token>`


- This approach is for demo and lab purposes only.
- In production, tokens should be stored in HttpOnly cookies or memory-only storage.

## Session Inspector

The frontend includes a Session Inspector panel that displays:

- Token presence
- JWT `exp` and `iat` timestamps
- Logged-in user metadata
- API base URL
- Example request headers

This component is intended to:

- aid debugging
- visualize session state
- support detection engineering exercises

## Legacy Mode Toggle

The Notes UI includes a **"Use legacy mode"** toggle.

This is an intentional design choice used to simulate:

- legacy compatibility paths
- deprecated or risky backend code paths
- feature-flag-driven request behavior

The toggle modifies requests to:


`/notes/{id}?legacy=true`


This enables:

- detection of legacy access patterns
- experimentation with authorization edge cases
- realistic security telemetry generation

## Security Notes

- No secrets are hardcoded in this frontend.
- Environment-specific values are loaded via Vite env variables.
- The frontend avoids rendering raw HTML from user input.
- React's default escaping behavior prevents basic XSS by design.

## Disclaimer

This frontend is built for learning, security research, and interview demonstration.

It intentionally favors:

- clarity over completeness
- observability over polish
- security signal generation over UX depth

## License

MIT

---
