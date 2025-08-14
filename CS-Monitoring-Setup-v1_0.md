# CS-Monitoring-Setup-v1_0.md
**Date:** 2025-08-10

## 1) Health Checks
- Nginx: `https://clearsight.local/healthz` → 200
- API: `http://clearsight_api:8080/health` → `{"ok":true}`
- DB: `pg_isready` in Compose healthcheck

## 2) Metrics (lightweight)
- Use node-exporter + cAdvisor, or simpler: periodic shell checks with alerts.
- Log rotation via `logrotate` for Nginx and app logs.

## 3) Alerts
- Email to ops@yourdomain on:
  - Health check failure (3 consecutive)
  - Disk usage > 80%
  - Backup job missing

## 4) Example curl checks (cron every 5 min)
```bash
*/5 * * * * root curl -sk https://clearsight.local/healthz || echo "$(date) WEB DOWN" | mail -s "ClearSight Web Down" ops@yourdomain
*/5 * * * * root curl -s http://localhost:8080/health | grep '"ok":true' || echo "$(date) API DOWN" | mail -s "ClearSight API Down" ops@yourdomain
```

## 5) Logs
- Nginx access/error logs under `/var/log/nginx/`
- App logs via `docker logs clearsight_api` (recommend redirect to file or Loki later)
