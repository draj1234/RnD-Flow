# CS-SAD-SystemArchitecture-v1_0
**Project:** ClearSight – Production Traceability System  
**Persona:** Solutions Architect  
**Version:** v1.0  
**Date:** 2025-08-10

---

## 1. Introduction
This document defines the overall architecture for ClearSight, covering logical layers, deployment setup, data flows, and technology stack.

---

## 2. Logical Architecture
### Layers:
1. **Presentation Layer** – React.js SPA served via Nginx; accessible via modern browsers.
2. **Application Layer** – Node.js backend (Express framework) handling API requests, business logic, and ERP integration.
3. **Data Layer** – PostgreSQL database for persistent storage.

---

## 3. Deployment Architecture
- **Server OS**: Ubuntu 20.04+ (on-premise)
- **Containerization**: Docker Compose orchestrating services:
  - `frontend` (React build served by Nginx)
  - `backend` (Node.js + Express)
  - `db` (PostgreSQL 14)
- **Network**: LAN-only access; no public internet exposure.
- **Security**: TLS termination via Nginx; RBAC in backend.

---

## 4. Data Flow
### Serial Tracking Flow:
1. User at Soldering station scans or assigns serial number.
2. Backend logs event in `stage_events` table, linked to `boards` table.
3. Dashboard queries API for WIP counts.

### SKU Onboarding:
1. Admin uploads CSV of SKUs or triggers ERP sync.
2. Backend updates `sku_master` table.
3. SKUs become selectable in station interfaces.

### ERP Sync:
1. Backend calls ERP API or ingests daily CSV.
2. Sync results logged in `erp_sync_logs`.

---

## 5. Technology Stack
- **Frontend**: React.js, TailwindCSS
- **Backend**: Node.js (Express)
- **Database**: PostgreSQL 14
- **Web Server**: Nginx
- **Container**: Docker Compose

---

## 6. Scaling & Extensibility
- Modular services allow adding new stages or product lines without code overhaul.
- APIs are versioned to support backward compatibility.
