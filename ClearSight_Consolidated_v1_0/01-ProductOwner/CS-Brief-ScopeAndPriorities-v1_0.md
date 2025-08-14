# CS-Brief-ScopeAndPriorities-v1_0
**Project:** ClearSight – Production Traceability System  
**Doc Type:** Scope & Priorities  
**Version:** v1.0  
**Date:** 2025-08-10  
**Owner Persona:** Product Owner / Client Representative

---

## 1. Problem Statement (from brief v0.5)
1. Lack of end-to-end board traceability across Inventory → QC → Soldering → Electrical Testing → Final Production.
2. Weak accountability: unclear “who did what, when, where” at each stage.
3. No single dashboard for floor visibility (WIP, bottlenecks, rework, SLA breaches).
4. Multi-SKU operations need serial-number continuity with ERP.
5. Small-team realities (multi-role, shifts, shared rigs) not supported by current tools.

---

## 2. Goals & Outcomes
1. Real-time, per-board traceability and accountability with unique serial numbers.
2. Floor Manager dashboard for live WIP, alerts, bottlenecks, and “where is my board?”
3. Enforce rework loop (Electrical Testing ↔ Soldering, optional QC) with defect logging.
4. Multi-SKU/Product Master onboarding with ERP continuity (CSV/API).
5. Internal LAN deployment on Ubuntu; audit-ready, low-friction UI for scanners/printers.

---

## 3. In Scope (Functional)
1. Serial number generation, labels (QR/Code128), reprint policy with reason.
2. Stage events (append-only) with role context; no stage-skip enforcement.
3. Rework loop with mandatory defect reason; Electrical Test result ingestion.
4. Product Master (SKU, rev, description, ERP ID); CSV import; manual CRUD.
5. Dashboards: WIP by stage, Board Tracker, Alerts, Rework Heatmap, basic throughput.
6. Roles: Operator, QC, Tester, ProdLead, FloorMgr, Admin; RBAC.
7. Station tracking: status (Free/In Use/Down); assignment and visibility.
8. Audit exports (CSV/PDF) and immutable history logs.
9. Deployment: Docker Compose on Ubuntu; LAN TLS; daily backups; monitoring.
10. Offline-friendly station UI (scan-first, local retry queue).

---

## 4. Out of Scope (Phase Later)
1. Cloud/SaaS external access; mobile app.
2. Full ERP overhaul (limited to SKU import & optional completion push).
3. Advanced analytics/ML; customer external portal.
4. Full i18n of UI (notices/text only in English for MVP).

---

## 5. Prioritization (MVP → Phase 2 → Phase 3)
**MVP (Target 6–8 weeks):**
1. Serial numbers + labels, Product Master CSV import.
2. Stage events, no-skip enforcement, rework loop with defect logging.
3. Electrical Test result import (CSV/JSON).
4. Dashboard core: WIP by stage, Board Tracker, Alerts (stale/SLA).
5. RBAC; audit exports; basic station status.
6. On-prem deployment (Docker Compose), daily backup, monitoring, TLS.

**Phase 2:**
1. NCMR/CAPA governance; quarantine & release.
2. ECO cut-in & rev roll-over handling.
3. Panelization (panel + child board tracking).
4. Calibration & maintenance schedules; lockout on overdue.
5. Shift handover; skill-based assignment; notice board.
6. SKU-wise KPIs; predictive SLA warnings; station utilization.

**Phase 3:**
1. Advanced analytics; customer-view mode.
2. Deeper ERP two-way sync; label template per SKU.
3. i18n (Kannada/Tamil notices), mobile/tablet enhancements.

---

## 6. Non-Functional Targets (MVP)
1. Latency: API p95 < 300 ms on LAN; dashboard refresh < 2 s.
2. Uptime: ≥ 99.5% on-prem; safe restart procedures documented.
3. Security: RBAC; hashed passwords; TLS in transit; minimal PII.
4. Auditability: append-only logs; export within 2 clicks.
5. Backup/Restore: Nightly `pg_dump`; restore drill documented.
6. Timezone: Asia/Kolkata; 24h timestamps; NTP enforced.

---

## 7. Acceptance at MVP (business level)
1. 100% of boards have unique serials; duplicates blocked.
2. Floor Manager can locate any board and view full history within 2 clicks.
3. Rework loop enforced; defects logged with category & action taken.
4. Electrical Test results ingested and linked to board.
5. CSV import of Product Master successful; SKU shown in all board views.
6. Audit export (CSV/PDF) available with filters; immutable logs verified.
7. Deployed on Ubuntu LAN with TLS; backups visible; health checks pass.
