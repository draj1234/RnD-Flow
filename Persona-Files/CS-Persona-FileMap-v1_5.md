# ClearSight Persona File Map
**Version:** v1.5  
**Date:** 2025-08-10  

---

## Persona 1: Project Owner / Initiator
- **Input:** None (originates brief)
- **Output:** `CS-ProductBrief-vX_X.md`

## Persona 2: Business Analyst
- **Input:** `CS-ProductBrief-vX_X.md`
- **Output:** `CS-BusinessRequirements-vX_X.md`, `CS-UseCases-vX_X.md`

## Persona 3: Solutions Architect
- **Input:** `CS-BusinessRequirements-vX_X.md`, `CS-UseCases-vX_X.md`
- **Output:** `CS-SystemArchitecture-vX_X.md`, `CS-DataFlow-vX_X.md`

## Persona 4: Backend Developer
- **Input:** `CS-SystemArchitecture-vX_X.md`, `CS-API-Specification-vX_X.md`
- **Output:** `CS-Backend-Service-vX_X.zip`, `CS-Backend-PostmanCollection-vX_X.json`, `CS-Backend-DeploymentGuide-vX_X.md`

## Persona 5: Frontend Developer
- **Input:** `CS-UI-StyleGuide-vX_X.md`, `CS-API-Specification-vX_X.md`
- **Output:**
  - `CS-Frontend-AppScaffold-v1_0.zip`
  - `CS-Frontend-IntegrationTests-v1_0.md`
  - `CS-Frontend-ScannerPrinterConfig-v1_0.md`

## Persona 6: QA / Tester
- **Input:** `CS-Frontend-AppScaffold-vX_X.zip`, `CS-Backend-Service-vX_X.zip`, `CS-Frontend-IntegrationTests-vX_X.md`, `CS-UseCases-vX_X.md`
- **Output:**
  - `CS-QA-TestCases-v1_0.md`
  - `CS-QA-TestExecutionReportTemplate-v1_0.md`
  - `CS-QA-BugReportTemplate-v1_0.md`

---
## Notes
- All files use semantic versioning (vMAJOR_MINOR).
- `vX_X` in file names denotes latest available version for that artifact.
- This map ensures AI agents can trace responsibility and hand-offs between personas.
