# ToDo-List-Using-Fast-Api
# ToDo-List-Using-Fast-Api

A FastAPI-based ToDo application with authentication, role-based access, and MySQL persistence.

## Branches

This repository is organized into branches, each representing a different deployment setup.

### 1. `main`

The base branch. It contains only the **FastAPI backend** with **Docker** support.

- REST API for auth (register, login, logout, token refresh) and todo CRUD
- MySQL database with connection pooling
- `docker-compose.yml` runs the backend and MySQL as containers

Use this branch if you only need the API and want a simple containerized backend.

### 2. `kubernetes-integration`

Extends the backend from `main` with **Kubernetes** deployment configuration.

- Same FastAPI backend and MySQL setup as `main`
- Kubernetes manifests for deploying the app in a cluster (e.g. Minikube or a cloud provider)
- Suited for learning or running the backend in a Kubernetes environment

Use this branch when you want to deploy and manage the backend with Kubernetes instead of plain Docker Compose.

### 3. `nginx-reverse-proxy-with-frontnd`

The **full-stack** branch extend from main branch. It adds a **React frontend** and **Nginx** as a reverse proxy, with every service containerized.

| Service | Role |
|---------|------|
| **React frontend** | Web UI for login, registration, and todo management |
| **FastAPI backend** | API server (not exposed directly to the internet) |
| **MySQL** | Database |
| **Nginx** | Single entry point on port 80 — serves the frontend and proxies `/api` to the backend |

**Why Nginx?**

- One public URL for the whole app (frontend + API)
- Frontend and backend appear on the same origin, so auth cookies and API calls work without CORS issues
- Easy to deploy on a **single VPS**: run `docker compose up` and expose port 80

**Why containerize each service?**

- Services are isolated — if one crashes, others keep running
- Consistent environments across development and production
- Simple to scale or replace individual components later

Use this branch for a complete, production-style setup on one server.
