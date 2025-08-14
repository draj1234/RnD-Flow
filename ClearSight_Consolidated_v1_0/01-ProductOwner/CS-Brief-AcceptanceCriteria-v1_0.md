# CS-Brief-AcceptanceCriteria-v1_0
**Project:** ClearSight – Production Traceability System  
**Doc Type:** Acceptance Criteria (MVP)  
**Version:** v1.0  
**Date:** 2025-08-10  
**Owner Persona:** Product Owner / Client Representative

---

## 1. Serial Numbering & Labels
1. When a board is intaked, the system generates a **unique** serial using the configured template (default: SKU-REV-YYWW-NNNN).  
2. Duplicate serial attempts are rejected with a clear error.  
3. Label print includes QR + human-readable text; **reprints require a reason** and are logged.

## 2. Stage Events & Enforcement
1. Stage events are **append-only**; no destructive edits.  
2. A board **cannot start** a stage unless the previous stage is marked **Completed** (no stage-skip).  
3. Role context is captured for each event (user may have multi-roles).

## 3. Rework Loop & Defects
1. If Electrical Testing **fails**, system requires a **Defect** entry with category and notes before moving to Soldering.  
2. After Soldering, optional QC (per policy) and then **mandatory** return to Electrical Testing for final verify.  
3. Final Production is accessible only if Electrical Testing is **Pass**.

## 4. Electrical Test Results
1. Test bench exports **CSV/JSON**; ClearSight ingests and attaches to the board record.  
2. Each test import records timestamp, tester ID, pass/fail, and metrics JSON.  
3. Test artifacts (files/links) are accessible from the board view.

## 5. Product Master (SKU) & ERP Continuity
1. Admin can import Product Master via **CSV** (SKU, description, revision, ERP ID).  
2. Intake requires SKU selection; board views show SKU + description.  
3. (Optional) On completion, ClearSight can export completion list as CSV for ERP.

## 6. Dashboards
1. **WIP by Stage** displays correct counts and color-codes vs WIP limits.  
2. **Board Tracker** finds any serial and shows full history.  
3. **Alerts** panel lists stale boards and SLA breaches with timestamps.

## 7. RBAC & Audit
1. Roles: Operator, QC, Tester, ProdLead, FloorMgr, Admin.  
2. Each role can only perform allowed actions; overrides require elevated approval + reason.  
3. **Audit Export** (CSV/PDF) is available with filters by date/stage/SKU/operator.

## 8. Deployment & Resilience
1. Deployed via **Docker Compose** on Ubuntu; LAN reachable as `clearsight.local` with TLS.  
2. Nightly backup job exists; restore drill document is included; success verified once.  
3. Health check endpoint returns OK; dashboard shows system status.

## 9. Offline/Kiosk Behavior
1. Station UI permits **scan-first** entries during transient network loss, queues locally, and auto-retries.  
2. UI displays an **offline warning** and clears it automatically on reconnect.
