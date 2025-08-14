# ClearSight Frontend Integration Test Plan
**Version:** v1.0

## Objective
Validate that the ClearSight frontend communicates correctly with backend APIs and renders expected UI states.

---

## Test Cases

### 1. Board Search
- **Action:** Search for board by serial number
- **Expected Result:** Board details appear with current stage & assigned user
- **Negative Test:** Non-existent serial → "Board not found" message

### 2. Stage Update
- **Action:** Update board stage from 'QC' to 'Electrical Testing'
- **Expected Result:** Backend confirms update; UI refreshes with new stage

### 3. ERP Data Sync
- **Action:** Trigger ERP sync for a SKU
- **Expected Result:** Updated SKU data displayed in ERP Sync View

### 4. SKU Onboarding
- **Action:** Add a new SKU with required details
- **Expected Result:** SKU appears in SKU list; backend stores entry

---
**Tools:** Cypress or Playwright for automation  
**Environments:** Staging & Production
