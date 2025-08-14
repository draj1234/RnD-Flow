# CS-Backend-DeploymentGuide-v1_0
**Target:** Ubuntu 20.04+ (on-prem) | **Stack:** Docker Compose

## 1) Prereqs
- Install Docker & Docker Compose Plugin
  ```bash
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl gnupg
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
  newgrp docker
  ```

## 2) Unpack and run
```bash
unzip CS-Backend-Service-v1_0.zip -d clearsight-backend
cd clearsight-backend/CS-Backend-Service-v1_0
cp .env.example .env
docker compose up --build -d
docker compose logs -f
```

## 3) Initialize DB (optional quick seed)
- Use the DDL: `CS-DBDDL-PostgresSchema-v1_0.sql` against the `db` container, or mount via volume/tooling.
```bash
docker exec -it clearsight_db psql -U postgres -d clearsight -c "\dt"
```

## 4) Smoke test
- `curl http://localhost:8080/health` → `{"ok":true}`

## 5) Next
- Import Postman: `CS-Backend-PostmanCollection-v1_0.json`
- Add Nginx reverse proxy & TLS in front (as per overall SAD).
