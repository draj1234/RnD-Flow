# ClearSight QA Test Cases
**Version:** v1.0  
**Date:** 2025-08-10  

---
## 1. Functional Tests
### TC-001: Board Search
- **Precondition:** Board with known serial exists
- **Steps:** Search by serial in Dashboard
- **Expected:** Board details displayed with correct stage & user

### TC-002: Stage Transition
- **Precondition:** Board is in 'QC'
- **Steps:** Change stage to 'Electrical Testing'
- **Expected:** Backend update confirmed; UI shows updated stage

### TC-003: SKU Onboarding
- **Precondition:** Logged in as Floor Manager
- **Steps:** Add new SKU with mandatory fields
- **Expected:** SKU appears in SKU list; persisted in backend

---
## 2. Integration Tests
### TC-101: ERP Sync
- **Steps:** Trigger ERP sync for a SKU
- **Expected:** Updated SKU data from ERP visible in ERP Sync View

---
## 3. Regression Tests
- Retest all functional cases after backend or frontend changes

---
## 4. UAT Scenarios
- End-to-end board lifecycle from serial creation to production
