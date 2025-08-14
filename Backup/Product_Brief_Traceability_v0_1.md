# **Product Brief: Board Traceability & Accountability System**  
**Report No.:** PB-TRK-001  
**Version:** v0.1  
**Date:** 2025-08-10  
**Prepared by:** GPT-5 Thinking (Assistant)  

---

## **1. Purpose & Outcome**
1. Build an end-to-end system that **tracks each PCB/board** from receipt (from EMS) through internal stages to final production.
2. Achieve **full accountability**: at any time, know **which board** is at **which stage**, **who** handled it, and **when**.
3. Provide a **real-time dashboard** for floor managers to query status, bottlenecks, WIP, rework loops, and cycle times.

---

## **2. Scope**
1. **Included:** Inventory → QC → Soldering (touch-ups) → Electrical Testing → Final Production, with **rework loop** from Electrical Testing back to Soldering (and optionally QC) and then back to Electrical Testing.
2. **Excluded (for now):** Changes to EMS processes, DUT/test program modifications, external ERP overhaul (only light integrations if available).

---

## **3. Context**
1. Boards are **received from EMS** with most assembly completed.
2. **Soldering** in-house is **limited to final touch-ups / minor additions** not covered by EMS.
3. The system must assign a **unique serial number** at intake and maintain a **single source of truth** across all stages.

---

## **4. Stages**
1. **Inventory** – Receive boards, verify PO/lot, register/assign serial numbers, store, and release to next stage.
2. **QC (Quality Control)** – Visual/mechanical checks; early defect identification.
3. **Soldering (Touch-ups)** – Minor rework/add-ons only (EMS completed most soldering).
4. **Electrical Testing** – Functional tests; defect diagnosis; approval for release.
5. **Final Production Team** – Final assembly steps, final inspection, packout/dispatch readiness.

---

## **5. Process Flow (with Rework Loop)**
1. **Inventory → QC → Soldering → Electrical Testing → Final Production**.
2. If **Electrical Testing fails**: **Electrical Testing → Soldering (fix)** → (optional) **QC** → **Electrical Testing (final verify)** → **Final Production**.

```mermaid
flowchart LR
  A[Inventory] --> B[QC]
  B --> C[Soldering (Touch-ups)]
  C --> D[Electrical Testing]
  D -->|Pass| E[Final Production]
  D -->|Fail| C
  C --> B
  B --> D
```

---

## **6. Data Model (Minimum Viable Fields)**
1. **Board**  
   - `serial_no` (string, unique, human-readable + QR/Code128)  
   - `ems_lot_id`, `po_no`, `sku`/`pn`, `rev`  
   - `board_type` (e.g., product variant)  
2. **StageEvent** (immutable audit log)  
   - `serial_no`  
   - `stage` (Inventory, QC, Soldering, ElectricalTesting, FinalProduction)  
   - `status` (Started, Completed, Failed, OnHold)  
   - `operator_id` (user who performed action)  
   - `timestamp_start`, `timestamp_end`  
   - `station_id` (workbench/line)  
   - `notes` (free text)  
   - `attachments` (images/test reports/CSV)  
3. **Defect/Rework**  
   - `defect_id`, `serial_no`, `source_stage` (where found)  
   - `category` (solder, component, mechanical, test)  
   - `severity` (minor/major/blocker)  
   - `action_taken` (what soldering did)  
   - `closed_by`, `closed_at`  
4. **User**  
   - `operator_id`, `role` (Operator, QC, Tester, ProdLead, FloorMgr, Admin)  
   - `name`, `email/phone` (optional), `shift`  
5. **Station**  
   - `station_id`, `stage`, `location`, `capability`  
6. **TestResult** (from Electrical Testing)  
   - `serial_no`, `test_suite_id`, `result` (Pass/Fail), `metrics` (JSON), `run_at`, `tester_id`, `artifact_link`

---

## **7. Roles & Permissions**
1. **Operator/QC/Tester** – Create/complete stage events; attach evidence; cannot edit history (append-only).
2. **ProdLead** – Override holds, reassign boards between stations.
3. **Floor Manager** – Read-only global view; bottlenecks; WIP; SLA breach alerts.
4. **Admin** – Manage users, stations, product SKUs, stage definitions, integration settings.
5. **Auditor** – Full read-only history exports; immutable logs.

---

## **8. Authentication & Access**
1. **Login providers:** Local (email+password), optional SSO (Google/Microsoft) if available.
2. **Session policy:** 8–12 hour sessions; idle timeout 30–60 min.
3. **MFA (optional but recommended)** for Admin/ProdLead.
4. **Access control:** Role-based access control (RBAC) mapped to actions per stage.

---

## **9. User Journeys**
1. **Intake (Inventory):** Scan/assign `serial_no` → record `StageEvent(Inventory, Completed)` → hand off to QC.
2. **QC:** Pull next board → inspect → record `status` + notes/attachments → pass to Soldering.
3. **Soldering (Touch-ups):** Perform fix/add-on → record `StageEvent` with `action_taken` if rework → send to Electrical Testing.
4. **Electrical Testing:** Run suite → upload `TestResult` → pass/fail. If fail → create `Defect` & return to Soldering.
5. **Final Production:** Final inspection/packout → mark `Completed` → ready for dispatch.

---

## **10. Dashboards (Floor Manager & Leads)**
1. **Live WIP by Stage:** Count of boards at each stage + trend (last 24h/7d).
2. **Where is my board?** Search by `serial_no` → full history + current stage/operator/time.
3. **Rework Heatmap:** Top defect categories, stations causing rework, mean rework cycles/board.
4. **Throughput & SLA:** Avg time per stage, total cycle time, bottlenecks (95th percentile), SLA breaches.
5. **Operator Productivity:** Boards processed per shift, pass rates, rework ratios (privacy-aware).
6. **Quality KPIs:** First-pass yield (FPY), Defect per Unit (DPU), Mean Time To Repair (MTTR).
7. **Alarms/Alerts:** Stale boards (no progress > threshold), repeated failures, station offline.
8. **Exports:** CSV/Excel/PDF with filters & date ranges.

---

## **11. Required Data Inputs & Integrations**
1. **Barcode/QR Scanners** at every station.
2. **Time source:** NTP sync for accurate timestamps.
3. **Electrical Test Rigs:** Ability to export `TestResult` (CSV/JSON) or API hook; minimal adapter if needed.
4. **Optional Integrations:** ERP (PO/lot/SKU), LDAP/SSO, cloud/object storage for attachments.
5. **Local-first:** System should work on LAN; cloud sync optional.

---

## **12. Non-Functional Requirements**
1. **Auditability:** Append-only `StageEvent` log; edits require new events (no destructive updates).
2. **Latency:** <1s write, <2s read for dashboard queries on LAN.
3. **Uptime Goal:** ≥99.5% for on-prem instance.
4. **Security:** Role-based permissions; hashed passwords; encrypted at rest (if feasible) and TLS in transit.
5. **Scalability:** Start with ≤5 stations; scale to 20+ without redesign.
6. **Device UX:** Tablet-friendly station UI; keyboard-only fast paths for scanners.
7. **Internationalization:** Timezone Asia/Kolkata; 24h timestamps.

---

## **13. KPIs (Success Metrics)**
1. **FPY Improvement:** +X% vs baseline within 60 days.
2. **Mean Rework Cycle Reduction:** -Y%.
3. **WIP Visibility:** 100% boards traceable with ≤2 clicks.
4. **SLA Compliance:** ≥95% stages within target time.
5. **Data Completeness:** ≥99% events with operator & timestamps.

---

## **14. Edge Cases & Policies**
1. **Lost/Damaged Label:** Reprint policy with supervisor approval; maintain mapping via lot + metrics to avoid duplicates.
2. **Station Downtime:** Auto-flag boards queued > threshold; reroute permission to ProdLead.
3. **Partial Test Uploads:** Mark as `OnHold` with reason; alert after N minutes.
4. **Manual Overrides:** Logged with reason and approver; visible in audit exports.
5. **Returned from Field (RMA):** Treat as new intake with link to prior serial_no.

---

## **15. Deliverables (for Agent/Team)**
1. **Data Schemas:** Board, StageEvent, Defect, User, Station, TestResult (as above).
2. **APIs (CRUD + Queries):**  
   - `POST /intake` (assign serial)  
   - `POST /stage-event`  
   - `POST /test-result`  
   - `GET /board/{serial_no}` (status + history)  
   - `GET /dashboards/wip`, `.../rework`, `.../throughput`  
3. **Station UIs:** Inventory, QC, Soldering, Electrical Testing, Final Production.
4. **Floor Dashboard:** Live and historical analytics with filters.
5. **RBAC Matrix:** Actions per role.
6. **Deployment:** On-prem (Docker Compose), LAN-first; optional cloud backup.

---

## **16. Open Questions (to Confirm Later)**
1. Serial format preference (e.g., `SKU-REV-YYWW-XXXX`)?
2. Mandatory QC after rework or conditional based on defect class?
3. Which test rigs export formats exist today? (CSV/JSON/XML) 
4. ERP/SSO availability and priority for Phase-1?

---

## **17. Next Steps (Proposed)**
1. Freeze `serial_no` format and label spec (sticker/QR size, placement).
2. Confirm **mandatory re-QC** policy after soldering fixes.
3. Collect sample **test result files** to define parsers.
4. Approve **RBAC** and **dashboard KPIs** for MVP.
5. Spin up a **Docker Compose** scaffold (API + DB + Web UI) and seed with demo data.

---

## **18. Glossary**
1. **EMS:** Electronics Manufacturing Services (external provider assembling most components).  
2. **FPY:** First-Pass Yield.  
3. **WIP:** Work In Progress.  
4. **RMA:** Return Merchandise Authorization.

---

**Confidence:** High (8.5/10) — Based strictly on your provided context and standard manufacturing IT patterns.
