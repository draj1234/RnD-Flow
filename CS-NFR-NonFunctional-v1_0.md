# CS-NFR-NonFunctional-v1_0
**Project:** ClearSight – Production Traceability System  
**Persona:** Business Analyst  
**Version:** v1.0  
**Date:** 2025-08-10

---

## NFR-001: Performance
- p95 latency for dashboard updates SHALL be ≤ 5 seconds.
- Stage event logging SHALL complete in ≤ 2 seconds.

## NFR-002: Uptime & Availability
- Target uptime: 99.5% within working hours (06:00–22:00 IST).
- Scheduled maintenance windows SHALL be announced at least 24 hours in advance.

## NFR-003: Security
- All data in transit SHALL be encrypted with TLS 1.2+.
- Role-based access control (RBAC) SHALL be enforced for all users.
- Passwords SHALL be stored using salted hashing (bcrypt or Argon2).

## NFR-004: Data Retention & Audit
- All board history SHALL be retained for at least 5 years.
- Audit logs SHALL be immutable.

## NFR-005: Integration
- ERP sync SHALL be via secure API or file drop.
- Sync frequency: at least once per day.

## NFR-006: Hosting Constraints
- System SHALL run on existing Ubuntu 20.04+ server.
- Deployment SHALL use Docker Compose for container orchestration.

## NFR-007: Offline Handling
- Stage events SHALL be queued locally if server connection is lost, then auto-synced when connection restores.
