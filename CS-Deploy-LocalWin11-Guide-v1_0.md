# CS-Deploy-LocalWin11-Guide-v1_0
**Persona:** Deployment Engineer (Local-first)  
**Version:** v1.0  
**Date:** 2025-08-10

---

## 1) Goal (Local-first)
Bring up ClearSight **on a single Windows 11 laptop** first. Once stable, promote to internal LAN.

---

## 2) Prerequisites (Win11)
1. **Docker Desktop** (WSL2 backend enabled).  
2. **Git** and **PowerShell**.  
3. Optional: **Node 20+** and **pnpm/npm** if you want to run without Docker.

---

## 3) File Layout (local workspace)
```
C:\Projects\ClearSight\
  backend\  -> unzip CS-Backend-Service-v1_0.zip here
  frontend\ -> unzip CS-Frontend-AppScaffold-v1_0.zip here (optional for local dev)
  deploy\
    CS-Compose-LOCAL-v1_0.yml
    CS-Env-LOCAL-v1_0.example
    Start-LocalClearSight.ps1
```
> Tip: If you keep the names exactly as above, the scripts work unmodified.

---

## 4) Configure Environment
1. Copy `deploy\CS-Env-LOCAL-v1_0.example` to `backend\.env` and adjust if needed.  
2. Default local ports:
   - API: **http://localhost:8080**
   - DB: **localhost:5432** (password `postgres` by default)
   - Web (if you host SPA with Nginx later): **http://localhost**

---

## 5) Bring Up with Docker
From `C:\Projects\ClearSight\deploy\`:
```powershell
# First run (build images)
docker compose -f .\CS-Compose-LOCAL-v1_0.yml up --build -d

# Follow logs
docker compose -f .\CS-Compose-LOCAL-v1_0.yml logs -f api
```

**Initialize DB schema:**
```powershell
# copy your CS-DBDDL-PostgresSchema-v1_0.sql into backend\
docker exec -i clearsight_db psql -U postgres -d clearsight < ..\backend\CS-DBDDL-PostgresSchema-v1_0.sql
```

---

## 6) Smoke Tests (basic)
1. **API health:** `GET http://localhost:8080/health` → `{ "ok": true }`  
2. **Create SKU:** `POST http://localhost:8080/sku` → returns SKU row.  
3. **Create board:** `POST http://localhost:8080/boards` → returns board_id.  
4. **WIP query:** `GET http://localhost:8080/dashboard/wip` → JSON array.

(See `CS-Deploy-SmokeChecklist-v1_0.md` for a full checklist.)

---

## 7) Troubleshooting
1. **Port in use:** change `8080/5432` in compose file and `.env`.  
2. **DB auth errors:** ensure `DATABASE_URL` in backend `.env` points to `postgres://postgres:postgres@db:5432/clearsight`.  
3. **Cannot exec psql:** container name must be `clearsight_db` (from compose).

---

## 8) Next: Promote to LAN (later)
Only after local is green: add Nginx reverse proxy + TLS (see earlier DevOps files) and switch `.env` to LAN URL.
