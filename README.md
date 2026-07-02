# ToDo-List-Using-Fast-Api

A FastAPI-based ToDo application with authentication, role-based access, and MySQL persistence.

## Project Structure

```text
ToDo/
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── api/
│       ├── components/
│       ├── context/
│       └── ...
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── controllers/
│   ├── routes/
│   ├── middleware/
│   ├── utils/
│   └── database/
│       ├── database.py
│       └── schema.sql
│
├── nginx/
│   └── nginx.conf
│
├── docker-compose.yml
├── docker-compose.hub.yml
├── .env
└── .env.example
```

## Services

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| **MySQL** | `todo_mysql` | 3307 (host) | Database |
| **Backend** | `todo_backend` | 8000 (internal) | FastAPI REST API |
| **Frontend** | `todo_frontend` | 80 (internal) | React app served by Nginx |
| **Nginx** | `todo_nginx` | 80 (public) | Reverse proxy — routes `/` to frontend, `/api/` to backend |

## Quick Start

1. Copy environment file:

```bash
cp .env.example .env
```

2. Build and run all services:

```bash
docker compose up --build
```

3. Open the app at [http://localhost](http://localhost)

## How It Works

### Backend (`backend/`)

FastAPI server running on port `8000` inside the Docker network.

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

API routes (no `/api` prefix on the backend itself):

- `POST /register`, `POST /login`, `GET /logout`, `POST /refresh-token`
- `GET /todos`, `POST /todos`, `GET /todo`, `PUT /todos/{id}`, `DELETE /todos/{id}`

### Frontend (`frontend/`)

React + Vite app. Built into static files and served by its own Nginx container on port `80`.

```dockerfile
# frontend/Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

`npm run build` creates a `dist/` folder that gets copied into the frontend Nginx container.

### Nginx Reverse Proxy (`nginx/`)

A separate Nginx container acts as the single public entry point:

- `location /` → proxies to `frontend:80` (React UI)
- `location /api/` → proxies to `backend:8000` (strips `/api` prefix)

```nginx
location /api/ {
    proxy_pass http://backend/;
}
```

So a browser request to `/api/login` reaches the backend as `/login`.

### Docker Compose

All services run on a shared `app-network`. Only Nginx exposes port `80` to the host.

```bash
docker compose up --build -d    # start in background
docker compose down             # stop all services
docker compose logs -f nginx    # view nginx logs
```

## Local Development (without Docker)

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Vite dev server proxies `/api` requests to `http://localhost:8000`.

## Branches

This repository is organized into branches, each representing a different deployment setup.

### 1. `main`

The base branch. It contains only the **FastAPI backend** with **Docker** support.

- REST API for auth and todo CRUD
- MySQL database with connection pooling
- `docker-compose.yml` runs the backend and MySQL as containers

Use this branch if you only need the API.

### 2. `kubernetes-integration`

Extends the backend from `main` with **Kubernetes** deployment configuration.

- Same FastAPI backend and MySQL setup as `main`
- Kubernetes manifests for cluster deployment

Use this branch when you want to deploy with Kubernetes.

### 3. `nginx-reverse-proxy-with-frontnd`

The **full-stack** branch. Adds a **React frontend** and **Nginx** reverse proxy with every service containerized.

**Why Nginx?**

- One public URL for the whole app (frontend + API)
- Frontend and backend share the same origin — no CORS issues
- Easy to deploy on a **single VPS**: run `docker compose up` and expose port 80

**Why containerize each service?**

- Services are isolated — if one crashes, others keep running
- Consistent environments across development and production
- Simple to scale or replace individual components later

Use this branch for a complete, production-style setup on one server.

### 4. `laodBalance-and-rateLimiting`

Created from **`nginx-reverse-proxy-with-frontnd`**. Extends the full-stack setup with **Nginx load balancing** and **rate limiting**.

| Feature | Description |
|---------|-------------|
| **Load balancing** | 2 backend instances (`backend` + `backend2`) — Nginx distributes API traffic using `least_conn` |
| **Rate limiting** | Limits requests per IP — `10 req/sec` for API, `5 req/min` for login/register |
| **Brute-force protection** | `/api/login` and `/api/register` get stricter limits |
| **Separate logs** | `logs/backend/` and `logs/backend2/` for each backend instance |

**What changed from `nginx-reverse-proxy-with-frontnd`:**

- `docker-compose.yml` — added `backend2` service
- `nginx/nginx.conf` — `upstream backend` with 2 servers + `limit_req_zone`
- `loadBalancingAndRatelimiting.text` — detailed notes on all config changes

**Documentation:**

- [loadBalancingAndRatelimiting.text](loadBalancingAndRatelimiting.text) — load balancing and rate limiting explained
- [nginxNote.text](nginxNote.text) — Nginx reverse proxy notes
- [logsNote.text](logsNote.text) — backend logging for VPS debugging

Use this branch to learn or deploy with load balancing and API rate limiting on a VPS.

```bash
git checkout laodBalance-and-rateLimiting
docker compose up --build -d
# App: http://localhost:8080
```

### 5. `ci-cd-pipeline`

Created from **`laodBalance-and-rateLimiting`**. Adds **CI/CD with GitHub Actions** using **cloud runners** and deploy to **VPS via SSH**.

| Feature | Description |
|---------|-------------|
| **GitHub Actions** | `.github/workflows/deploy.yml` — auto build on push |
| **Docker Hub** | Pushes `vickygeek/todo_fast_api` and `vickygeek/todo_frontend` |
| **Cloud runner** | `ubuntu-latest` (GitHub-hosted) |
| **Deploy** | SSH to VPS → `docker compose -f docker-compose.dockerhub.yml up -d` |

**Files added:**

- `.github/workflows/deploy.yml` — `deploy-cloud` job
- `docker-compose.dockerhub.yml` — pull images on VPS
- `cicdNote.text` — cloud CI/CD setup guide

Use this branch for **production-style deploy to remote VPS** on git push.

### 6. `ci-cd-pipeline-local-machine`

Created from **`ci-cd-pipeline`**. Same CI/CD pipeline but uses a **GitHub self-hosted runner** on your **local machine** instead of cloud runners.

| Feature | Description |
|---------|-------------|
| **Self-hosted runner** | Workflow runs on your PC (`runs-on: self-hosted`) |
| **Same build/push** | Builds and pushes backend + frontend to Docker Hub |
| **Local deploy** | `docker compose up` on your machine — **no SSH to VPS** |
| **Job name** | `deploy-self-hosted` in `deploy.yml` |

**What changed from `ci-cd-pipeline`:**

| | `ci-cd-pipeline` | `ci-cd-pipeline-local-machine` |
|---|------------------|-------------------------------|
| Runner | GitHub cloud (`ubuntu-latest`) | Your local machine (`self-hosted`) |
| Deploy target | Remote VPS via SSH | Local machine |
| SSH secrets | Required | Not required |
| Docker on runner | Not needed | Required locally |

**Documentation:**

- [cicdSelfHostedNote.text](cicdSelfHostedNote.text) — self-hosted runner setup (full guide)
- [cicdNote.text](cicdNote.text) — cloud CI/CD notes (parent branch)

**Branch tree:**

```text
laodBalance-and-rateLimiting
    └── ci-cd-pipeline              (cloud runner → VPS)
            └── ci-cd-pipeline-local-machine   (self-hosted → local PC)
```

```bash
git checkout ci-cd-pipeline-local-machine
# Install self-hosted runner first — see cicdSelfHostedNote.text
git push origin ci-cd-pipeline-local-machine
# App: http://localhost:8080
```