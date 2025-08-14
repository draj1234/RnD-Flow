# CS-API-Specification-v1_0
**Project:** ClearSight – Production Traceability System  
**Persona:** Solutions Architect  
**Version:** v1.0  
**Date:** 2025-08-10

---

## Authentication
- **POST /auth/login** – Returns JWT token
- **POST /auth/logout** – Invalidates token

---

## Boards
- **POST /boards**  
  - Create new board with serial number and SKU.
  - Request: `{ "serial_number": "20250810-SKU001-001", "sku_code": "SKU001" }`  
  - Response: `{ "board_id": 123, "status": "created" }`

- **GET /boards/{serial_number}**  
  - Retrieve board details and history.

---

## Stages
- **GET /stages** – List all stages in sequence.

---

## Stage Events
- **POST /stage-events**  
  - Log a stage action (pass/fail/rework).
  - Request: `{ "board_serial": "20250810-SKU001-001", "stage_name": "QC", "action": "pass" }`  
  - Response: `{ "event_id": 456, "status": "logged" }`

---

## SKU Master
- **GET /sku** – List all SKUs.
- **POST /sku** – Add a new SKU.

---

## ERP Sync
- **POST /erp-sync** – Trigger ERP sync.
- **GET /erp-sync/logs** – Get last 10 sync results.

---

## Dashboard
- **GET /dashboard/wip** – WIP counts by stage.
- **GET /dashboard/rework-stats** – Rework statistics by stage.
