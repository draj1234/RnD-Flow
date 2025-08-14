# **ClearSight – Production Traceability System**  
**Report No.:** PB-TRK-001  
**Version:** v0.3  
**Date:** 2025-08-10  
**Prepared by:** GPT-5 Thinking (Assistant)  

**Tagline:** *Full Visibility. Total Accountability.*  

---

## **1. Purpose & Outcome**
1. Build an end-to-end system that **tracks each PCB/board** from receipt (from EMS) through internal stages to final production.
2. Achieve **full accountability**: at any time, know **which board** is at **which stage**, **who** handled it, and **when**.
3. Provide a **real-time dashboard** for floor managers to query status, bottlenecks, WIP, rework loops, and cycle times.
4. Ensure the system is **optimized for a small manufacturing team** (~20–25 people) where multi-role assignments, shift work, and resource constraints are common.

---

## **2. Scope**
1. **Included:** Inventory → QC → Soldering (touch-ups) → Electrical Testing → Final Production, with **rework loop** from Electrical Testing back to Soldering (and optionally QC) and then back to Electrical Testing.
2. **Excluded (for now):** Changes to EMS processes, DUT/test program modifications, external ERP overhaul (only light integrations if available).
3. **Deployment:** Internal network only (on Ubuntu server), accessible via browsers within the office LAN.

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
   - `role_context` (role used during this action; supports multi-role users)  
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
   - `multi_roles` (array of roles this person can perform)  
   - `skill_tags` (certifications, stage eligibility)  
   - `name`, `email/phone` (optional), `shift`  
5. **Station**  
   - `station_id`, `stage`, `location`, `capability`, `status` (Free/In Use/Down)  
6. **TestResult** (from Electrical Testing)  
   - `serial_no`, `test_suite_id`, `result` (Pass/Fail), `metrics` (JSON), `run_at`, `tester_id`, `artifact_link`

---

## **7. Roles & Permissions**
1. **Operator/QC/Tester** – Create/complete stage events; attach evidence; cannot edit history (append-only).
2. **ProdLead** – Override holds, reassign boards between stations, manage stage capacity.
3. **Floor Manager** – Read-only global view; bottlenecks; WIP; SLA breach alerts.
4. **Admin** – Manage users, stations, product SKUs, stage definitions, integration settings.
5. **Auditor** – Full read-only history exports; immutable logs.

---

## **8. Additional Features for Small-Team Needs**
1. **Multi-Role Support** – Users can switch roles in-session without logging out; role context recorded per event.
2. **Secondary Verification** – Critical actions (e.g., QC pass) can require second user approval.
3. **Stage Capacity Thresholds** – Configurable WIP limits per stage; dashboard warnings before overload.
4. **No Stage Skip Enforcement** – System blocks starting a stage unless previous stage is marked complete.
5. **Mandatory Rework Logging** – Any board returned to soldering requires a defect entry (quick templates supported).
6. **Station Availability Tracking** – Status (Free/In Use/Down) visible to all users; impacts assignment logic.
7. **Skill-Based Assignment** – Only certified operators can be assigned certain reworks/tests.
8. **Shift Handover Tracking** – Boards in progress must be reassigned at shift end; handover checklist recorded.
9. **Stage Notice Board** – Broadcast messages linked to specific stages; shown to operators before next scan.
10. **Quick Help & Training Mode** – Context-sensitive help; dummy boards for role training without affecting live data.
11. **Audit-Ready Exports** – Preformatted PDF/CSV exports for last 3 months’ history; customer-view mode.

---

## **9. Dashboards (Floor Manager & Leads)**
1. **Live WIP by Stage:** Count of boards at each stage + trend (last 24h/7d).
2. **Where is my board?** Search by `serial_no` → full history + current stage/operator/time.
3. **Rework Heatmap:** Top defect categories, stations causing rework, mean rework cycles/board.
4. **Throughput & SLA:** Avg time per stage, total cycle time, bottlenecks (95th percentile), SLA breaches.
5. **Operator Productivity:** Boards processed per shift, pass rates, rework ratios.
6. **Quality KPIs:** First-pass yield (FPY), Defect per Unit (DPU), Mean Time To Repair (MTTR).
7. **Alarms/Alerts:** Stale boards, repeated failures, station downtime.
8. **Resource Utilization:** Station use %, downtime logs.
9. **Shift View:** Boards in progress by shift; handover status.
10. **Notices:** Active broadcast messages with expiry times.

---

## **10. Non-Functional Requirements**
1. **Auditability:** Append-only `StageEvent` log; edits require new events.
2. **Latency:** <1s write, <2s read for dashboard queries on LAN.
3. **Uptime Goal:** ≥99.5% for on-prem instance.
4. **Security:** Role-based permissions; hashed passwords; TLS in transit.
5. **Scalability:** Start with ≤5 stations; scale to 20+ without redesign.
6. **Device UX:** Tablet-friendly station UI; fast scanner workflows.
7. **Internationalization:** Timezone Asia/Kolkata; 24h timestamps.

---

## **11. KPIs (Success Metrics)**
1. **FPY Improvement:** +X% vs baseline within 60 days.
2. **Mean Rework Cycle Reduction:** -Y%.
3. **WIP Visibility:** 100% boards traceable with ≤2 clicks.
4. **SLA Compliance:** ≥95% stages within target time.
5. **Data Completeness:** ≥99% events with operator, role, and timestamps.

---

**Confidence:** High (9/10) – This version addresses both your stated needs and common operational gaps in small-scale, multi-role manufacturing teams.
