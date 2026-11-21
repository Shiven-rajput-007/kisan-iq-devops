# KisanIQ — Intelligent Digital Farming Assistant (Full-Stack & DevOps Enabled)

> **“KisanIQ does not just show farming data. KisanIQ converts farming data into clear decisions and actions.”**  
> Core flow: **DATA → INTELLIGENCE → DECISION → ACTION**  
> Primary farmer question: **“Aaj mujhe kya karna hai?” / “आज मला काय करायचे आहे?”**

[![KisanIQ CI/CD Pipeline](https://github.com/Shiven-rajput-007/kisan-iq-devops/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Shiven-rajput-007/kisan-iq-devops/actions/workflows/ci-cd.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--Container-blue?logo=docker)](compose.yaml)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016-336791?logo=postgresql)](compose.yaml)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-61DAFB?logo=react)](frontend/)
[![Node.js](https://img.shields.io/badge/Backend-Node.js%20%2B%20Express-339933?logo=node.js)](server/)

---

## 📚 B.Tech DevOps Practical Submission Documentation

This repository implements practical engineering assignments for **DevOps Laboratory**:
- **Assignment 14**: Docker Compose for a Multi-Container Application (Web + Database + Reverse Proxy).
- **Assignment 15**: Simple CI/CD Pipeline integrating GitHub, build tools, Docker, and remote deployment.

For complete academic lab submission notes, viva-voce answers, and architectural explanations, refer to:
👉 **[DEVOPS-ASSIGNMENT.md](DEVOPS-ASSIGNMENT.md)**

---

## 🏗️ Production System Architecture

```
                                 [ Browser / Mobile Client ]
                                              │
                                       HTTP Port 5173 / 80
                                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │    Frontend Container (kisaniq-frontend)         │
                    │    • Nginx Alpine Web Server                     │
                    │    • React 19 + Vite + Tailwind CSS SPA          │
                    │    • Reverse Proxy (/api/* -> backend:8000)      │
                    └─────────────────────────┬────────────────────────┘
                                              │ Internal Docker Network
                                              │ (kisaniq-network)
                                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │    Backend Container (kisaniq-backend)           │
                    │    • Node.js 20 + Express + TypeScript           │
                    │    • RESTful APIs & Auth Middleware (JWT)        │
                    │    • Explainable Agronomic Decision Engine       │
                    └───────────┬───────────────────────────┬──────────┘
                                │                           │
                 TCP Port 5432  ▼                           ▼ External APIs
┌──────────────────────────────────────────────┐   ┌───────────────────────────────┐
│ Database Container (kisaniq-db)              │   │ • Open-Meteo Weather API      │
│ • PostgreSQL 16 Alpine Engine                │   │ • CEDA Agmarknet Mandi API    │
│ • 25 Relational Schema Tables                │   │ • Soil Health Card Directory  │
│ • Persistent Volume (kisaniq_pgdata)         │   └───────────────────────────────┘
└──────────────────────────────────────────────┘
```

---

## 🐳 Assignment 14: Docker Compose Implementation

KisanIQ is fully containerized as a three-tier micro-architecture orchestrated via [`compose.yaml`](compose.yaml) (and legacy-compatible [`docker-compose.yml`](docker-compose.yml)).

### 1. Services Specification

| Service | Container Name | Image / Build Base | Host Port | Role |
|---|---|---|---|---|
| `frontend` | `kisaniq-frontend` | `node:20-alpine` $\to$ `nginx:alpine` | `5173:80`, `80:80` | Serves compiled React assets, handles SPA client routing, and reverse-proxies `/api/` traffic to the backend. |
| `backend` | `kisaniq-backend` | `node:20-alpine` (Multi-stage) | `8000:8000` | Executes Express TypeScript API, manages database migrations, runs decision logic. |
| `db` | `kisaniq-db` | `postgres:16-alpine` | `5432:5432` | Stores all persistent relational records (users, crops, soil tests, mandis, orders). |

### 2. Multi-Container Orchestration Features

- **Isolated Docker Bridge Network (`kisaniq-network`)**: Services communicate internally over secure DNS names (`db`, `backend`, `frontend`).
- **Data Persistence (`kisaniq_pgdata`)**: PostgreSQL data is mapped to a dedicated Docker volume so database records persist across reboots.
- **Automated Health Checks**:
  - `db`: Monitored with `pg_isready -U kisaniq_user -d kisaniq_db`.
  - `backend`: Monitored with `wget http://127.0.0.1:8000/api/health` (actively performs `SELECT 1` on PostgreSQL).
  - `frontend`: Monitored with `wget http://127.0.0.1:80/`.
- **Dependency Chaining (`depends_on: condition: service_healthy`)**:
  - `backend` waits until PostgreSQL is verified healthy.
  - `frontend` waits until backend API server is verified healthy.
- **Zero-Hardcoded Secrets**: Uses environment variable interpolation with safe defaults (`.env.example`).

---

## 🚀 Quick Start: Running with Docker Compose

Ensure Docker and Docker Compose are installed:

```bash
# 1. Clone repository
git clone https://github.com/Shiven-rajput-007/kisan-iq-devops.git
cd kisan-iq-devops

# 2. Configure Environment (optional, defaults provided)
cp .env.example .env

# 3. Validate Docker Compose Configuration
docker compose config

# 4. Build and Start the Entire Multi-Container Application
docker compose up -d --build

# 5. Check Container Status and Health
docker compose ps
```

Access the running application:
- **Frontend Web UI**: [http://localhost:5173/](http://localhost:5173/) or [http://localhost:80/](http://localhost:80/)
- **Backend Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)
- **Database**: PostgreSQL on `localhost:5432` (`user: kisaniq_user`, `database: kisaniq_db`)

### Container Management Commands

```bash
# View live application logs
docker compose logs -f

# View logs for a specific service
docker compose logs -f backend
docker compose logs -f db

# Restart a service
docker compose restart backend

# Stop all containers (preserving persistent database volume)
docker compose down

# Stop all containers and remove database volume (full reset)
docker compose down -v
```

---

## 🔄 Assignment 15: CI/CD Pipeline (GitHub Actions)

The automated Continuous Integration & Continuous Deployment pipeline is configured in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml).

### Pipeline Stages

```mermaid
flowchart LR
    S1["Stage 1: Source<br/>(Git Checkout)"] --> S2["Stage 2: Build & Test<br/>(tsc, Vite, npm test)"]
    S2 --> S3["Stage 3: Docker & GHCR<br/>(Buildx, Tag, Publish)"]
    S3 --> S4["Stage 4: Deployment<br/>(SSH to Remote Host)"]
```

1. **Stage 1: Source**
   - Triggers on `push` to `main`, `pull_request` to `main`, and manual dispatch (`workflow_dispatch`).
   - Checks out complete source repository using `actions/checkout@v4`.

2. **Stage 2: Build & Test**
   - Sets up Node.js 20 with dependency caching.
   - Installs backend packages (`npm ci`) and compiles TypeScript (`npm run build`).
   - Runs backend test suite (`npm run test:mandi`, 30 unit & regression tests).
   - Installs frontend packages (`npm ci`) and runs translation parity test (`npm run test:i18n`).
   - Compiles production React Vite bundle (`npm run build`).

3. **Stage 3: Docker & GHCR Publishing**
   - Validates `compose.yaml` using `docker compose config`.
   - Sets up Docker Buildx for optimized multi-stage caching.
   - Authenticates against GitHub Container Registry (`ghcr.io`) using `GITHUB_TOKEN`.
   - Builds and tags Docker images with `latest` and commit SHA (`sha-<short_hash>`).
   - Publishes images to:
     - `ghcr.io/<owner>/kisaniq-backend`
     - `ghcr.io/<owner>/kisaniq-frontend`

4. **Stage 4: Automated Remote Deployment (SSH)**
   - Connects to remote Linux host via SSH (`appleboy/ssh-action@v1.2.0`).
   - Conditionally executes only when deployment secrets are configured.
   - Pulls updated container images from GHCR.
   - Runs `docker compose up -d --remove-orphans`.
   - Validates running container health.

### Deployment Secrets Configuration

To enable Stage 4 deployment, configure the following secrets in **GitHub Repository $\to$ Settings $\to$ Secrets and variables $\to$ Actions**:

| Secret | Description | Example |
|---|---|---|
| `DEPLOY_HOST` | Remote server IP address or domain | `192.0.2.1` |
| `DEPLOY_USER` | Remote SSH user account | `ubuntu` |
| `DEPLOY_SSH_KEY` | SSH Private Key authorized on server | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_PATH` | Target directory on remote server | `/home/ubuntu/kisaniq-deployment` |
| `GHCR_USERNAME` | GitHub username | `shiven-rajput-007` |
| `GHCR_TOKEN` | GitHub Personal Access Token (PAT) with `read:packages` | `ghp_...` |

---

## 💻 Local Development (Without Docker)

If developing locally without Docker:

```bash
# 1. Install dependencies
cd server && npm install
cd ../frontend && npm install
cd ..

# 2. Run backend and frontend concurrently
npm run dev:full

# 3. Run automated tests
npm test
```

---

## 🗄️ Database Architecture (25 Tables)

The database schema is defined in [`server/db/schema.sql`](server/db/schema.sql) and [`prisma/schema.prisma`](prisma/schema.prisma):
- **Core Entities**: `users`, `farmers`, `farms`, `fields`.
- **Agronomics**: `crops`, `crop_stages`, `crop_actions`, `recommendations`, `alerts`.
- **Mandi Intelligence**: `markets`, `market_prices`, `selling_decisions`, `mandi_sync_logs`.
- **Direct Marketplace**: `buyer_profiles`, `crop_listings`, `marketplace_orders`, `orders`, `shipments`, `vehicles`.
- **Soil & Lab Testing**: `laboratories`, `soil_test_requests`, `soil_reports`, `soil_sensor_readings`.

---

## 🌐 Marathi-First Experience (`mr` / `mr-IN`)

- **Default Language**: Marathi (`mr`) is the primary language across all pages and advisories.
- **Tri-State Switcher**: Instant live switching between **मराठी**, **हिन्दी**, and **English**.
- **Voice Assistant**: Slide-over drawer with 5 lifecycle states (`IDLE`, `LISTENING`, `PROCESSING`, `SPEAKING`, `ERROR`) and authentic Marathi speech recognition.

---

## 📄 License & Academic Submission

This project is submitted for the B.Tech DevOps Engineering Curriculum.  
Author: **Shiven Rajput**  
Repository: [kisan-iq-devops](https://github.com/Shiven-rajput-007/kisan-iq-devops)
