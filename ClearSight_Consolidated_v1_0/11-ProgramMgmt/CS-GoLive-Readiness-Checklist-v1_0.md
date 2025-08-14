# ClearSight – Next Steps & Go‑Live Readiness Checklist
**Version:** v1.0  
**Date:** 2025-08-10

---

## 1) Finish Local Proof (Windows 11)
1. Import Postman collection and hit: `/health`, `/sku`, `/boards`, `/stage-events`, `/dashboard/wip`.
2. Load DB schema: `CS-DBDDL-PostgresSchema-v1_0.sql` (already noted in local guide).
3. Seed minimum data:
   - SKU: `SKU-DEMO-001` (desc: Demo board)
   - Stages: Soldering (1), QC (2), Electrical (3), Final (4)
4. Create 5 boards and walk them across stages (incl. 1 rework flow).

## 2) Wire Frontend to Backend (local)
1. In `frontend`, set API base URL to `http://localhost:8080` (e.g., `.env.local` → `VITE_API_BASE=http://localhost:8080`).
2. Run `npm install && npm run dev` (or serve via Nginx later).
3. Validate:
   - Dashboard shows WIP counts.
   - Board Tracker returns history after a few transitions.
   - SKU onboarding form can add + list SKUs.

## 3) Label Printing & Scanners (desk test)
1. Connect barcode scanner (USB HID) → ensure it types into serial input.
2. Test label print from browser (pick a 50mm x 30mm page size).
3. Reprint flow requires “reason” and writes to audit log.

## 4) QA Pass (target)
1. Execute `CS-QATestPlan-v1_0.md` (at least smoke + core flows).
2. No Critical/High defects outstanding.
3. Export audit CSV/PDF and verify content.

## 5) Promote to LAN (on Ubuntu)
1. Prepare hostnames & TLS (internal CA or self-signed).
2. Use: `CS-Compose-DockerStack-v1_0.yml` + `CS-Nginx-Config-v1_0.conf`.
3. Set backend `.env` → `DATABASE_URL=postgres://...@db:5432/clearsight`
4. Health checks:
   - `https://clearsight.local/healthz` → 200
   - `http://clearsight_api:8080/health` → {"ok":true}
5. Add nightly backup cron (see Backup & Retention doc).

## 6) ERP Connector (move from mock → real)
1. Configure ERP endpoint/CSV drop + credentials.
2. Dry-run sync on a test SKU; verify mapping & timestamp.
3. Schedule daily sync and set alert on failure.

## 7) Monitoring & Alerts
1. Enable health check cron or hook into Prometheus/Grafana.
2. Alerts for:
   - API down
   - Disk > 80%
   - Backup missing
   - ERP sync failure

## 8) User Onboarding
1. Create users/roles: Operator, QC, Tester, FloorMgr, Admin.
2. Distribute the **Quick Start Guide** + Training slides.
3. 30‑minute floor walk-through + sign-off.

## 9) Cutover Plan (MVP)
1. Freeze manual logs for 1 shift; run ClearSight in parallel.
2. Compare outputs at end of shift (WIP, defects, cycle time).
3. Go/no‑go with rollback:
   - Rollback = stop Compose + revert to manual log for that shift.

## 10) After Go‑Live
1. Open CAPA loop for first 2 weeks to catch process tweaks.
2. Start ECO numbering for changes affecting workflow.
3. Plan v1.1 (panelization, NCMR/CAPA UI, predictive SLA alerts).

---

### Quick Command Snippets

**Docker (local):**
```powershell
cd C:\Projects\ClearSight\deploy
.\Start-LocalClearSight.ps1 -Rebuild
```

**DB init (local):**
```powershell
docker exec -i clearsight_db psql -U postgres -d clearsight < ..\backend\CS-DBDDL-PostgresSchema-v1_0.sql
```

**LAN bring-up (Ubuntu):**
```bash
docker compose -f CS-Compose-DockerStack-v1_0.yml up -d
curl -k https://clearsight.local/healthz
```

---

**Sign‑offs:**
- QA Lead: __________  Date: __________
- Floor Manager: _____ Date: __________
- Product Owner: _____ Date: __________
