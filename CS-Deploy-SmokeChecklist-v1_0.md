# CS-Deploy-SmokeChecklist-v1_0
**Target:** Windows 11 local laptop  
**Date:** 2025-08-10

---

## A. Containers Healthy
1. `docker ps` shows `clearsight_db` and `clearsight_api` up.
2. DB healthcheck is **healthy**.

## B. API Health
1. `curl http://localhost:8080/health` → `{"ok":true}`

## C. Minimal CRUD
1. **Add SKU:**  
   `POST /sku` → 200 OK with `sku_code` visible.
2. **Add Board:**  
   `POST /boards` with `serial_number` + `sku_code` → returns `board_id`.
3. **Log Stage Event:**  
   `POST /stage-events` with `board_serial`, `stage_name`, `action` → 200 OK.

## D. Dashboard
1. `GET /dashboard/wip` returns JSON counts.
2. No 5xx errors in API logs.

## E. Persistency
1. Stop & start containers → data still present (volumes working).

## F. Ready to Promote
1. All above checks green → proceed to LAN deployment.
