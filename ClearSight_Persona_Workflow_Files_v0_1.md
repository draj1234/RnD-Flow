# **ClearSight – Persona Workflow & File Map**
**Version:** v0.1  
**Date:** 2025-08-10  
**Project Code Prefix:** `CS-` (use to prefix all files)  

---

## **0. Conventions**
1. **Folders:**  
   - `/01-Brief/`, `/02-Analysis/`, `/03-Architecture/`, `/04-Design/`, `/05-Backend/`, `/06-Frontend/`, `/07-QA/`, `/08-DevOps/`, `/09-Training/`, `/10-Support/`
2. **File Naming:** `CS-<Area>-<Title>-v<major>_<minor>.<ext>` (e.g., `CS-Brief-ProductBrief-v0_5.md`)
3. **Formats:** `.md` for docs, `.drawio/.png` for diagrams, `.json/.yml` for configs, `.sql` for DB, `.csv` for imports.
4. **Versioning:** Increment minor for edits; major when scope changes.

---

## **1. Product Owner / Client Representative**
- **Inputs (files):**
  1. `/01-Brief/CS-Brief-ProductBrief-v0_5.md` (from earlier)  
- **Work:** Prioritize scope, define acceptance criteria.
- **Outputs (files):**
  1. `/01-Brief/CS-Brief-ScopeAndPriorities-v1_0.md`  
  2. `/01-Brief/CS-Brief-AcceptanceCriteria-v1_0.md`  

---

## **2. Business Analyst (BA)**
- **Inputs:**
  1. `/01-Brief/CS-Brief-ProductBrief-v0_5.md`  
  2. Stakeholder notes: `/02-Analysis/CS-BA-InterviewNotes-v1_0.md`
- **Work:** Functional breakdown, use-cases, NFRs.
- **Outputs:**
  1. `/02-Analysis/CS-FRD-FunctionalRequirements-v1_0.md`  
  2. `/02-Analysis/CS-UseCases-FlowDiagram-v1_0.drawio` (+ `.png`)  
  3. `/02-Analysis/CS-NFR-NonFunctional-v1_0.md`  

---

## **3. Solutions Architect**
- **Inputs:**
  1. `/02-Analysis/CS-FRD-FunctionalRequirements-v1_0.md`  
  2. `/02-Analysis/CS-NFR-NonFunctional-v1_0.md`
- **Work:** System design, data model, integrations.
- **Outputs:**
  1. `/03-Architecture/CS-SAD-SystemArchitecture-v1_0.md`  
  2. `/03-Architecture/CS-Arch-ContextContainerComponents-v1_0.drawio` (+ `.png`)  
  3. `/03-Architecture/CS-DB-LogicalSchema-v1_0.drawio` (+ `.png`)  
  4. `/03-Architecture/CS-DB-PhysicalDDL-v1_0.sql`  
  5. `/03-Architecture/CS-API-Spec-v1_0.md` (OpenAPI YAML optional: `/03-Architecture/CS-API-OpenAPI-v1_0.yml`)  
  6. `/03-Architecture/CS-ERP-IntegrationPlan-v1_0.md`  

---

## **4. UX/UI Designer**
- **Inputs:**
  1. `/02-Analysis/CS-UseCases-FlowDiagram-v1_0.png`  
  2. `/03-Architecture/CS-SAD-SystemArchitecture-v1_0.md`
- **Work:** Wireframes, UI kit, prototypes.
- **Outputs:**
  1. `/04-Design/CS-UX-Wireframes-FloorManager-v1_0.png`  
  2. `/04-Design/CS-UX-Wireframes-OperatorStations-v1_0.png`  
  3. `/04-Design/CS-UI-StyleGuide-v1_0.md`  
  4. `/04-Design/CS-UX-ClickablePrototype-v1_0.mp4` (or link note `.md`)

---

## **5. Backend Developer**
- **Inputs:**
  1. `/03-Architecture/CS-DB-PhysicalDDL-v1_0.sql`  
  2. `/03-Architecture/CS-API-Spec-v1_0.md`
- **Work:** Implement services, models, integrations.
- **Outputs:**
  1. `/05-Backend/CS-API-Server-v1_0/` (source tree)  
  2. `/05-Backend/CS-DB-Migrations-v1_0.sql`  
  3. `/05-Backend/CS-Seeds-DemoData-v1_0.sql`  
  4. `/05-Backend/CS-Backend-UnitTests-v1_0.md`  

---

## **6. Frontend Developer**
- **Inputs:**
  1. `/04-Design/CS-UI-StyleGuide-v1_0.md`  
  2. `/03-Architecture/CS-API-OpenAPI-v1_0.yml` (or API spec md)
- **Work:** Build role-based web UI.
- **Outputs:**
  1. `/06-Frontend/CS-WebApp-v1_0/` (source tree)  
  2. `/06-Frontend/CS-Frontend-IntegrationTests-v1_0.md`  
  3. `/06-Frontend/CS-ScannerPrinter-Config-v1_0.md`  

---

## **7. QA Engineer / Tester**
- **Inputs:**
  1. `/01-Brief/CS-Brief-AcceptanceCriteria-v1_0.md`  
  2. `/05-Backend/CS-API-Server-v1_0/`, `/06-Frontend/CS-WebApp-v1_0/`
- **Work:** Test planning, execution, regression.
- **Outputs:**
  1. `/07-QA/CS-QA-TestPlan-v1_0.md`  
  2. `/07-QA/CS-QA-TestCases-v1_0.xlsx`  
  3. `/07-QA/CS-QA-ExecutionReport-v1_0.md`  
  4. `/07-QA/CS-QA-RegressionSuite-v1_0.md`  

---

## **8. DevOps / Deployment Engineer**
- **Inputs:**
  1. `/03-Architecture/CS-SAD-SystemArchitecture-v1_0.md`  
  2. `/05-Backend/CS-API-Server-v1_0/`, `/06-Frontend/CS-WebApp-v1_0/`
- **Work:** Packaging, deployment, monitoring.
- **Outputs:**
  1. `/08-DevOps/CS-Compose-DockerStack-v1_0.yml`  
  2. `/08-DevOps/CS-Nginx-Config-v1_0.conf`  
  3. `/08-DevOps/CS-Backup-RetentionPolicy-v1_0.md`  
  4. `/08-DevOps/CS-Monitoring-Setup-v1_0.md`  

---

## **9. Trainer / Documentation Writer**
- **Inputs:**
  1. Built system + workflows  
- **Work:** Create user-facing docs & training aids.
- **Outputs:**
  1. `/09-Training/CS-UserGuide-Operator-v1_0.pdf`  
  2. `/09-Training/CS-UserGuide-FloorManager-v1_0.pdf`  
  3. `/09-Training/CS-AdminGuide-v1_0.pdf`  
  4. `/09-Training/CS-QuickCards-Station-Set-v1_0.zip`  

---

## **10. Support Engineer**
- **Inputs:**
  1. `/08-DevOps/CS-Monitoring-Setup-v1_0.md`  
  2. Logs & metrics
- **Work:** Triage, resolve, escalate.
- **Outputs:**
  1. `/10-Support/CS-Support-Runbook-v1_0.md`  
  2. `/10-Support/CS-IncidentReports-YYYY-MM.md`  
  3. `/10-Support/CS-KB-Articles-v1_0.md`  

---

## **11. Optional Governance Roles (Small-Team Shared)**
- **Quality Lead (NCMR/CAPA)**  
  - **Inputs:** `/02-Analysis/CS-FRD-FunctionalRequirements-v1_0.md`, system defect logs  
  - **Outputs:** `/02-Analysis/CS-NCMR-CAPA-Plan-v1_0.md`
- **Change Control Board (ECO)**  
  - **Inputs:** ECO requests  
  - **Outputs:** `/02-Analysis/CS-ECO-Policy-v1_0.md`, `/02-Analysis/CS-ECO-Register-v1_0.xlsx`

---

## **12. End-to-End Handoff Chain (Files)**
1. **Brief →** `/01-Brief/CS-Brief-ProductBrief-v0_5.md`  
2. **FRD/NFR →** `/02-Analysis/CS-FRD-FunctionalRequirements-v1_0.md`, `/02-Analysis/CS-NFR-NonFunctional-v1_0.md`  
3. **Architecture →** `/03-Architecture/CS-SAD-SystemArchitecture-v1_0.md`, `/03-Architecture/CS-DB-PhysicalDDL-v1_0.sql`, `/03-Architecture/CS-API-OpenAPI-v1_0.yml`  
4. **Design →** `/04-Design/CS-UX-Wireframes-*.png`, `/04-Design/CS-UI-StyleGuide-v1_0.md`  
5. **Build →** `/05-Backend/CS-API-Server-v1_0/`, `/06-Frontend/CS-WebApp-v1_0/`  
6. **Test →** `/07-QA/CS-QA-ExecutionReport-v1_0.md`  
7. **Deploy →** `/08-DevOps/CS-Compose-DockerStack-v1_0.yml`  
8. **Train →** `/09-Training/CS-UserGuide-*.pdf`  
9. **Support →** `/10-Support/CS-IncidentReports-YYYY-MM.md`

---

**Confidence:** High (9/10) – This map fits small-team delivery with clear inputs/outputs for agent orchestration.
