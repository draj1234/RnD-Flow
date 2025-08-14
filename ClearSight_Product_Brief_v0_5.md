# **ClearSight – Production Traceability System**  
**Report No.:** PB-TRK-001  
**Version:** v0.5  
**Date:** 2025-08-10  
**Prepared by:** GPT-5 Thinking (Assistant)  

**Tagline:** *Full Visibility. Total Accountability.*  

---

## **0. What Changed in v0.5 (Delta from v0.4)**
1. **Governance:** Added **NCMR/CAPA workflow** for non-conformances and corrective actions.  
2. **ECO Handling:** Defined **Engineering Change Order** and **revision roll-over** rules for WIP.  
3. **Panelization:** Support for **panel + child board tracking** with sub-serials.  
4. **Calibration/Maintenance:** Station/test-rig **calibration schedules** with lockout-on-expiry.  
5. **Labeling:** Barcode/QR **printer support**, **reprint policy** with reason logs, anti-dup checks.  
6. **Security & Privacy:** RBAC hardening, minimal PII, **session/role elevation** with time limits.  
7. **Backups/DR & Monitoring:** Daily backups, retention, health checks, metrics/alerts.  
8. **Offline/Kiosk UX:** Graceful **scan-first flows**, local caching, auto-resume.  
9. **KPIs:** Added NCMR metrics, calibration compliance, ECO effectiveness.  

---

## **1. Purpose & Outcome**
(unchanged from v0.4)  
1. End-to-end board tracking from EMS intake to final production.  
2. Full accountability (who/when/where).  
3. Real-time dashboards for visibility and control.  
4. Optimized for ~20–25 person teams.  
5. Multi-SKU with ERP continuity.  
6. **New:** Governance, panelization, maintenance, and resilience.

---

## **2. Scope**
1. Included: Inventory → QC → Soldering (touch-ups) → Electrical Testing → Final Production, with rework loop.  
2. Excluded: EMS process changes, DUT/test program modifications, ERP overhaul.  
3. Deployment: **Ubuntu on-prem**, LAN-only browser access.  
4. **New:** Panelized boards and RMA handling retained; ECO cut-in logic covered.

---

## **3. Context**
1. Boards received from EMS; in-house soldering is final touch-ups/minor additions.  
2. Unique serials at intake; single source of truth.  
3. Products vary by **SKU** and **revision**; ERP continuity required.  
4. **Shifted operations, multi-role users, shared equipment constraints** common in small teams.

---

## **4. Stages**
(unchanged) Inventory → QC → Soldering → Electrical Testing → Final Production (+ rework loop).

---

## **5. Process Flow**
(unchanged diagram; panelization and governance add side-flows)

```mermaid
flowchart LR
  A[Inventory] --> B[QC]
  B --> C[Soldering (Touch-ups)]
  C --> D[Electrical Testing]
  D -->|Pass| E[Final Production]
  D -->|Fail| C
  C --> B
  B --> D
  D -->|NCMR->Hold| H[Quarantine]
  H -->|CAPA Approved| C
```

---

## **6. Data Model (Expanded)**
1. **Board**  
   - `serial_no` (unique, QR/Code128)  
   - `sku`, `sku_description`, `rev`, `ems_lot_id`, `po_no`, `board_type`  
   - `panel_id` (nullable), `panel_index` (nullable)  
2. **Panel**  
   - `panel_id` (unique)  
   - `sku`, `rev`, `child_count`  
3. **PanelMember**  
   - `panel_id`, `serial_no`, `panel_index` (0..n-1)  
4. **StageEvent** (append-only)  
   - `serial_no`, `stage`, `status`, `operator_id`, `role_context`, `timestamp_start/end`, `station_id`, `notes`, `attachments`  
5. **Defect/Rework**  
   - `defect_id`, `serial_no`, `source_stage`, `category`, `severity`, `action_taken`, `closed_by`, `closed_at`  
6. **NCMR** (Non-Conforming Material Report)  
   - `ncmr_no`, `serial_no`/`panel_id`, `reason_code`, `disposition` (Rework/Scrap/Use-as-is/Return-to-EMS/Hold), `raised_by`, `approved_by`, `created_at`, `closed_at`, `attachments`  
7. **CAPA** (Corrective & Preventive Action)  
   - `capa_no`, `linked_ncmr_no`, `root_cause_code`, `actions`, `owner`, `due_date`, `status`, `verified_by`, `verified_at`  
8. **ECO** (Engineering Change Order)  
   - `eco_no`, `sku`, `from_rev`, `to_rev`, `cut_in_date`, `requires_requal` (Y/N), `notes`, `approver`  
9. **CalibrationMaintenance**  
   - `asset_id` (station/test-rig), `type` (Calibration/Maintenance), `due_date`, `performed_at`, `performed_by`, `result`, `certificate_link`, `lockout` (Y/N)  
10. **User**  
   - `operator_id`, `name`, `multi_roles`, `skill_tags`, `shift`  
11. **Station**  
   - `station_id`, `stage`, `location`, `capability`, `status` (Free/In Use/Down)  
12. **TestResult**  
   - `serial_no`, `test_suite_id`, `result` (Pass/Fail), `metrics` (JSON), `run_at`, `tester_id`, `artifact_link`  
13. **ProductMaster**  
   - `sku` (PK), `description`, `revision`, `erp_id`, `category`, `default_test_suite`, `label_template`, `image_link`  
14. **LabelPrintLog**  
   - `serial_no`/`panel_id`, `printer_id`, `template`, `printed_by`, `printed_at`, `reprint_reason`  
15. **Notice**  
   - `notice_id`, `stage`, `message`, `active_from`, `active_until`, `author`

---

## **7. Serial Numbering, Panels & ERP**
1. **Serial Format (default):** `{SKU}-{REV}-{YYWW}-{NNNN}` (configurable).  
2. **Global Uniqueness:** Enforced across all SKUs; collision-proof with index on `serial_no`.  
3. **Panelization:**  
   - `panel_id` generated at intake (e.g., `{SKU}-P{YYWW}-{NN}`).  
   - Child boards get sub-serials: `{SERIAL_NO}-C{INDEX}`.  
   - Movements can be **panel-level** or **child-level** post-depanel.  
4. **Labeling:** QR/Code128 with human-readable text; **reprint requires reason**; logs in `LabelPrintLog`.  
5. **ERP Continuity:** CSV/API import of ProductMaster; optional push of completion/disposition; manual/scheduled sync.

---

## **8. Floor Manager Dashboard (Views & Tools)**
(From v0.4, plus new governance/maintenance views)  
**Views:** WIP by Stage, Board Tracker, Stage Performance, Rework Heatmap, Operator Productivity, Shift View, Resource Utilization, Notice Board, Alerts, **SKU Summary**, **NCMR/CAPA Queue**, **Calibration Due Calendar**.  
**Tools:** Reassign Board, Override Capacity, Station Control, Broadcast Notice, Approve/Reject Exceptions, Audit Export, SLA Ack, Handover Mgmt, Quick Defect Report, SKU Master Mgmt, **Open NCMR**, **Start CAPA**, **Quarantine/Release**, **Schedule Calibration**.

---

## **9. Governance Workflows**
1. **NCMR:** Any stage can raise; board moves to **Quarantine**; disposition decided by ProdLead/FloorMgr.  
2. **CAPA:** For repeated/critical issues; root cause (5-Why/pareto), action owners, due dates, verification step.  
3. **Holds & Releases:** Boards on hold cannot proceed; releases require role approval with reason.

---

## **10. ECO & Revision Roll-Over**
1. **Cut-in Logic:** ECO defines **effective date**; boards started before can finish as-is or require re-qual based on ECO.  
2. **In-WIP Boards:** System flags WIP with old rev; FloorMgr chooses **grandfather** or **re-route to re-qual**.  
3. **Traceability:** Test suites may change per rev; dashboards show mixed-rev WIP to avoid confusion.

---

## **11. Equipment Calibration & Maintenance**
1. **Schedules:** Per station/test-rig; calendar view; reminders 7/3/1 days prior.  
2. **Lockout:** Starting tests on **overdue** rigs blocked (override requires Admin + reason).  
3. **Certificates:** Upload calibration PDFs; link from dashboard.  
4. **Metrics:** Calibration compliance rate; mean overdue days.

---

## **12. Labeling & Printers**
1. **Supported:** USB network printers (e.g., Zebra) via ZPL/TSPL; print templates per SKU.  
2. **Reprints:** Require operator reason; limited count; manager notified beyond threshold.  
3. **Anti-dup:** Scan-on-issue validates serial not already in system; mismatch alerts.  
4. **Layout:** Serial as QR + text; optional lot/PO and SKU description footer.

---

## **13. Security, Privacy & Compliance**
1. **RBAC Hardening:** Fine-grained actions; time-limited **role elevation** for overrides.  
2. **PII Minimization:** Store minimal operator info; expose initials on shared screens if needed.  
3. **Session & Audit:** 8–12h sessions; idle timeout; immutable event logs.  
4. **Data Retention:** Configurable retention for attachments/logs; archive older data.  
5. **Clock Integrity:** NTP sync; drift >2 min triggers admin alert.

---

## **14. Deployment, Backups & Monitoring**
1. **Stack:** Docker Compose (API/Web/PostgreSQL); Nginx reverse proxy; clearsight.local on LAN; TLS (self-signed/internal CA).  
2. **Backups:** Nightly `pg_dump` + weekly full snapshot; **30/90** day retention; restore drill quarterly.  
3. **Monitoring:** Health endpoints; metrics (Prometheus); alerts via email/Teams/Slack.  
4. **Logs:** Rotated; searchable (optional lightweight ELK/Vector+Loki).

---

## **15. Performance & Offline**
1. **Concurrency:** Sized for 20–30 users; API p95 < 300ms on LAN.  
2. **Offline/Kiosk:** Scan-first forms; local cache queue with retry; warning banner when offline.  
3. **Attachments:** Max size per file (configurable), store to LAN NAS/object store.

---

## **16. Localization & Accessibility**
1. **Timezone:** Asia/Kolkata; 24h timestamps.  
2. **Language:** English first; consider stage-notice i18n later (Kannada/Tamil capable).  
3. **Accessibility:** High-contrast mode; keyboard-only workflows for scanners.

---

## **17. KPIs (Expanded)**
1. FPY (overall/by SKU/station/operator).  
2. DPU, MTTR, throughput, cycle & queue time (p50/p95).  
3. **NCMR Rate**, **CAPA closure on-time %**, repeat-defect reduction.  
4. **Calibration Compliance %**, overdue count.  
5. SLA compliance and stale WIP reduction.

---

## **18. Open Questions**
1. Panelization: always panel intake, or mixed (single boards sometimes)?  
2. ECO policy: who approves re-qual vs grandfathering?  
3. Printers in use (Zebra model)? Label size & material spec?  
4. ERP in scope (Tally/Odoo/SAP?) – API or CSV? Sync cadence?  
5. Attachments storage (NAS path/S3-compatible object store)?

---

**Confidence:** Very High (9.3/10) – v0.5 closes the major practical gaps for a small, multi-role manufacturing team with strong governance and resilience.
