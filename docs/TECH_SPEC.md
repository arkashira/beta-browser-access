# TECH_SPEC.md – beta-browser-access

---

## 1. Overview

**beta-browser-access** is a lightweight, self‑hosted web service that manages the deployment of beta or secondary browsers (e.g., Chrome Canary, Firefox Nightly, Edge Dev) on client machines. It provides:

- A **web UI** for administrators to configure which beta browsers are available, their launch URLs, and visibility rules.
- A **client‑side agent** that runs on user machines, automatically installs/updates the selected browsers, and exposes a local API for launching them.
- A **feedback collector** that captures crash reports, usage metrics, and user feedback, sending them back to the central server.

The system is designed to be **platform‑agnostic** (Windows, macOS, Linux) and **extensible** to support new browsers or deployment strategies.

---

## 2. Architecture

```
+-------------------+          +-------------------+          +-------------------+
|  Admin Web UI     |<-------->|  API Gateway      |<-------->|  Client Agent     |
|  (React + TS)     |  REST/WS  |  (FastAPI + Uvicorn) |  HTTP/WS  |  (Python 3.11)    |
+-------------------+          +-------------------+          +-------------------+
          |                               |                           |
          |  CRUD (browsers, policies)    |  Launch / Status          |
          |                               |  / Feedback               |
          |                               |                           |
          |                               |                           |
          v                               v                           v
+-------------------+          +-------------------+          +-------------------+
|  PostgreSQL       |          |  Redis (Cache)    |          |  Local File Store |
|  (PostgreSQL 15)  |          |  (Redis 7)        |          |  (JSON / SQLite)  |
+-------------------+          +-------------------+          +-------------------+
```

### 2.1 Core Components

| Component | Responsibility | Tech |
|-----------|----------------|------|
| **Admin UI** | Configuration, reporting | React, TypeScript, Tailwind CSS, Vite |
| **API Gateway** | Auth, rate‑limit, routing | FastAPI, Uvicorn, JWT, OAuth2 |
| **Client Agent** | Browser installation, launch, telemetry | Python 3.11, `subprocess`, `requests`, `watchdog` |
| **PostgreSQL** | Persistent store for browser definitions, policies, user sessions | SQLAlchemy ORM |
| **Redis** | Session cache, rate‑limit counters | aioredis |
| **Telemetry** | Crash/usage data ingestion | HTTP POST, optional Kafka producer |
| **Deployment** | Docker, Kubernetes, Helm | Dockerfile, Helm chart, ArgoCD |

---

## 3. Data Model

### 3.1 Browser Definition

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `name` | string | Human‑readable name (e.g., “Chrome Canary”) |
| `version` | string | Semantic version or channel |
| `platforms` | array<string> | Supported OSes (`win`, `mac`, `linux`) |
| `download_url` | string | URL to the installer or tarball |
| `checksum` | string | SHA‑256 checksum |
| `install_path` | string | Default install directory |
| `launch_args` | array<string> | Default command‑line arguments |
| `metadata` | JSON | Arbitrary key/value (e.g., icon URL) |

### 3.2 Deployment Policy

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `name` | string | Policy name |
| `browsers` | array<UUID> | Browser IDs included |
| `visibility` | enum | `always`, `beta_only`, `user_choice` |
| `auto_update` | boolean | Whether to auto‑update browsers |
| `schedule` | JSON | Cron‑style schedule for updates |
| `metadata` | JSON | Optional notes |

### 3.3 User Session

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `agent_id` | string | Unique identifier of the client agent |
| `last_seen` | timestamp | Last heartbeat |
| `status` | enum | `online`, `offline`, `error` |
| `metadata` | JSON | OS, architecture, installed browsers |

---

## 4. Key APIs & Interfaces

### 4.1 Admin API (FastAPI)

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/v1/browsers` | GET | List all browsers | JWT |
| `/api/v1/browsers` | POST | Create browser | JWT |
| `/api/v1/browsers/{id}` | GET | Get browser | JWT |
| `/api/v1/browsers/{id}` | PUT | Update browser | JWT |
| `/api/v1/browsers/{id}` | DELETE | Delete browser | JWT |
| `/api/v1/policies` | CRUD | Manage deployment policies | JWT |
| `/api/v1/agents/{id}/status` | GET | Get agent status | JWT |
| `/api/v1/agents/{id}/heartbeat` | POST | Agent heartbeat | None (public) |
| `/api/v1/feedback` | POST | Receive telemetry | None (public) |

### 4.2 Client Agent API (Local)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /agent/status` | Returns agent health and installed browsers |
| `POST /agent/launch` | Body: `{browser_id, args}` | Launch specified browser |
| `POST /agent/update` | Triggers update of all browsers |
| `GET /agent/telemetry` | Returns local telemetry logs |

### 4.3 WebSocket Streams

- **Admin UI**: `/ws/agents` – real‑time agent status updates.
- **Agent**: `/ws/updates` – push update notifications.

---

## 5. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS | Modern, fast, type safety |
| **Backend** | FastAPI, Uvicorn, SQLAlchemy, Alembic | Async, high‑performance, ORM |
| **Database** | PostgreSQL 15 | ACID, JSONB support |
| **Cache** | Redis 7 | Session, rate‑limit |
| **Agent** | Python 3.11, `subprocess`, `watchdog` | Cross‑platform, easy packaging |
| **Container** | Docker, Docker Compose | Reproducible builds |
| **Orchestration** | Kubernetes, Helm | Scalable, self‑healing |
| **CI/CD** | GitHub Actions | Automated tests, lint, build |
| **Monitoring** | Prometheus + Grafana | Metrics, alerts |
| **Logging** | Loki | Centralized logs |
| **Telemetry** | OpenTelemetry SDK | Structured tracing |

---

## 6. Dependencies

| Category | Package | Version |
|----------|---------|---------|
| **Backend** | fastapi | ^0.110.0 |
| | uvicorn | ^0.29.0 |
| | sqlalchemy | ^2.0.30 |
| | alembic | ^1.13.1 |
| | pydantic | ^2.7.1 |
| | python-jose | ^3.3.0 |
| | passlib | ^1.7.4 |
| | redis | ^5.0.1 |
| **Frontend** | react | ^18.2.0 |
| | typescript | ^5.3.3 |
| | tailwindcss | ^3.4.1 |
| | axios | ^1.6.7 |
| **Agent** | requests | ^2.32.3 |
| | watchdog | ^4.0.0 |
| | tqdm | ^4.66.2 |
| **Dev** | pytest | ^8.2.0 |
| | black | ^24.4.2 |
| | isort | ^5.13.2 |
| | pre-commit | ^3.7.1 |

All dependencies are pinned in `requirements.txt` and `package.json`. The Dockerfile uses `python:3.11-slim` and `node:20-alpine`.

---

## 7. Deployment

### 7.1 Docker

```dockerfile
# Backend
FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build
```

### 7.2 Helm Chart

- `values.yaml` exposes:
  - `replicaCount`
  - `image.repository`, `image.tag`
  - `postgresql.enabled`, `postgresql.postgresqlPassword`
  - `redis.enabled`, `redis.password`
  - `ingress.enabled`, `ingress.hosts`
  - `resources.limits`, `resources.requests`

### 7.3 CI/CD Pipeline

1. **Lint**: `pre-commit run --all-files`
2. **Test**: `pytest` (backend) + `npm test` (frontend)
3. **Build**: Docker images pushed to `ghcr.io/arkashira/beta-browser-access`
4. **Release**: Helm chart packaged and deployed via ArgoCD
5. **Monitoring**: Prometheus scrape config added automatically

### 7.4 Scaling

- **Stateless API**: Horizontal pod autoscaler based on CPU/Memory.
- **Redis**: Single‑node for small installs; cluster for high‑throughput.
- **PostgreSQL**: Patroni for HA; read replicas for reporting.

---

## 8. Security

- **Auth**: OAuth2 with JWT for admin endpoints. Public endpoints are rate‑limited via Redis.
- **Transport**: TLS termination at Ingress (cert-manager).
- **Secrets**: Managed via Kubernetes Secrets + sealed‑secrets.
- **Agent**: Runs as non‑root; uses `sudo` only for installation when necessary.

---

## 9. Extensibility

- **New Browsers**: Add a new entry in `browsers` table; agent auto‑detects platform.
- **Custom Launchers**: `launch_args` can be overridden per policy.
- **Plugins**: Agent exposes a Python entry‑point for custom telemetry collectors.

---

## 10. Roadmap (Q3 2026)

| Feature | Target | Notes |
|---------|--------|-------|
| **Auto‑update scheduler** | 2026‑07 | Cron‑style, per‑policy |
| **Crash analytics** | 2026‑08 | Integrate Sentry |
| **Multi‑tenant support** | 2026‑09 | Separate namespaces |
| **CLI client** | 2026‑10 | For headless environments |

---
