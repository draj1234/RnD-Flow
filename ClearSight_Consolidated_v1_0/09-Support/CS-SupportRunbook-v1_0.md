# ClearSight Support Runbook
**Version:** v1.0  
**Date:** 2025-08-10  
**Audience:** Internal Support Team / AI Support Agent  
**Scope:** Support for ClearSight Production Traceability System running in internal office network (Ubuntu server hosted).

---

## 1. Purpose & Scope
This runbook guides support staff or AI agents to maintain and troubleshoot the ClearSight system.  
It covers only internal deployment issues — excludes external hosting, internet-related outages, or unrelated enterprise systems.

---

## 2. User Support Channels
- **Internal Ticketing System**: Primary channel for issue reporting.
- **Email Support**: support@company.local (auto-logs into ticketing).
- **Walk-up Requests**: Allowed for urgent floor issues, but must be logged after.

---

## 3. Common Issues & Fixes

### 3.1 Login Failures
- **Symptom:** User cannot log in to ClearSight.
- **Checks:**
  1. Confirm network connectivity.
  2. Verify account status in User Management module.
  3. Reset password if necessary.

### 3.2 Dashboard Not Loading
- **Symptom:** Browser stuck on loading spinner.
- **Checks:**
  1. Clear browser cache.
  2. Check server CPU/memory load (`htop`).
  3. Restart frontend service: `sudo systemctl restart clearsight-frontend`.

### 3.3 Missing Board Serial Data
- **Symptom:** Board appears without history or current stage.
- **Checks:**
  1. Search by alternate identifiers (ERP SKU, internal lot number).
  2. Check ingestion service logs for errors.
  3. Re-run sync job for that day.

### 3.4 ERP Sync Errors
- **Symptom:** SKU descriptions missing or outdated.
- **Checks:**
  1. Verify ERP connection settings.
  2. Run manual sync job.
  3. Contact ERP admin if persistent.

---

## 4. Incident Response Workflow
1. **Detect/Receive Issue** – via ticket/email/monitoring alert.
2. **Acknowledge** – respond within 15 minutes.
3. **Diagnose** – check logs, reproduce issue.
4. **Resolve** – apply documented fix or escalate.
5. **Document** – update ticket with resolution and KB entry if needed.

---

## 5. Knowledge Base Starter
- **KB001:** How to reset user password.
- **KB002:** Restarting ClearSight frontend service.
- **KB003:** Manually triggering ERP sync.
- **KB004:** Querying board history by serial.

---

## 6. Log & Monitoring Access
- **Application Logs:** `/var/log/clearsight/`
- **ERP Sync Logs:** `/var/log/clearsight/erp_sync.log`
- **Search by Serial/SKU:** `grep <serial> /var/log/clearsight/*.log`
- **Monitoring:** Grafana dashboard at `http://monitor.local:3000`.

---

## 7. Version Management
- **Check Current Version:** `clearsight --version`
- **Update:** `sudo apt update && sudo apt install clearsight`
- **Rollback:** Keep last two package versions in local cache; `sudo apt install clearsight=<version>`

---

## 8. Escalation Contacts
- **Level 1:** Floor Support (local IT)
- **Level 2:** DevOps Team
- **Level 3:** ClearSight Development Lead
