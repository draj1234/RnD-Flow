# **ClearSight – Production Traceability System**  
**Report No.:** PB-TRK-001  
**Version:** v0.4  
**Date:** 2025-08-10  
**Prepared by:** GPT-5 Thinking (Assistant)  

**Tagline:** *Full Visibility. Total Accountability.*  

---

## **1. Purpose & Outcome**
1. Build an end-to-end system that **tracks each PCB/board** from receipt (from EMS) through internal stages to final production.
2. Achieve **full accountability**: at any time, know **which board** is at **which stage**, **who** handled it, and **when**.
3. Provide a **real-time dashboard** for floor managers to query status, bottlenecks, WIP, rework loops, and cycle times.
4. Ensure the system is **optimized for a small manufacturing team** (~20–25 people) where multi-role assignments, shift work, and resource constraints are common.
5. Support **multiple products/SKUs** with ERP continuity and robust onboarding for product master data.

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
4. Products vary by SKU and revision; the system must handle **multiple product types** and maintain ERP continuity.

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
   - `sku` (linked to Product Master)  
   - `ems_lot_id`, `po_no`, `sku_description`, `rev`  
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
7. **ProductMaster**  
   - `sku` (primary key)  
   - `description`  
   - `revision`  
   - `erp_id`  
   - `category`  
   - `default_test_suite`  
   - `label_template`  
   - `image_link`

---

## **7. Serial Number & SKU/ERP Handling**
1. **Serial Number Format:** `{SKU}-{REV}-{YYWW}-{NNNN}`  
   - Configurable; default uses SKU from Product Master, revision, year/week, and sequential number.  
2. **Uniqueness:** System validates against all existing records before assignment.  
3. **Labeling:** Generated serial embedded in QR/Code128 barcode for scanning.  
4. **Multi-SKU Support:** Product Master table links each board to its SKU, description, revision, and ERP ID.  
5. **ERP Continuity:**  
   - Import SKU master from ERP via CSV or API.  
   - Optional push of completion data back to ERP.  
   - Manual or scheduled sync supported.  

---

## **8. Additional Features for Small-Team Needs**
(From v0.3, retained with additions)
1. **Multi-Role Support**  
2. **Secondary Verification**  
3. **Stage Capacity Thresholds**  
4. **No Stage Skip Enforcement**  
5. **Mandatory Rework Logging**  
6. **Station Availability Tracking**  
7. **Skill-Based Assignment**  
8. **Shift Handover Tracking**  
9. **Stage Notice Board**  
10. **Quick Help & Training Mode**  
11. **Audit-Ready Exports**  
12. **SKU/Product Master Management** – Add/edit SKUs, assign revisions, link to ERP, group by production line/pole.

---

## **9. Floor Manager Dashboard**

### **Views**
1. Live WIP by Stage  
2. Where is my board?  
3. Stage Performance Summary  
4. Rework Heatmap  
5. Operator Productivity  
6. Shift View & Handover  
7. Resource Utilization  
8. Notice Board  
9. Alarms & Alerts Panel  
10. SKU-Wise Summary (WIP, defects, throughput per SKU)

### **Tools**
1. Reassign Board  
2. Override Stage Capacity  
3. Station Control  
4. Broadcast Notice  
5. Approve/Reject Exceptions  
6. Audit Export  
7. SLA Alert Acknowledgement  
8. Handover Management  
9. Quick Defect Report  
10. SKU/Product Master Management  

---

## **10. Non-Functional Requirements**
(Same as v0.3)

---

## **11. KPIs (Success Metrics)**
(Same as v0.3, but also include SKU-specific FPY and throughput metrics.)

---

**Confidence:** Very High (9.2/10) – Incorporates operational workflow, SKU/product data handling, ERP integration, and detailed floor manager tools.
