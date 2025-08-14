# CS-Backup-RetentionPolicy-v1_0.md
**Date:** 2025-08-10

## 1) Scope
Back up PostgreSQL database and critical config (Nginx, Compose, .env).

## 2) Schedule
- **Nightly pg_dump** at 02:00 IST (compressed)
- **Weekly full volume snapshot** (Sunday 03:00 IST)

## 3) Retention
- Nightly: **30 days**
- Weekly: **12 weeks**
- Monthly (first Sunday): **12 months**

## 4) Storage
- Local NAS share mounted at `/backups/clearsight/`
- Optional offsite rsync (weekly)

## 5) Commands (cron examples)
```bash
# /etc/cron.d/clearsight-backup
0 2 * * * postgres pg_dump -Fc -U postgres -d clearsight > /backups/clearsight/pgdump-$(date +\%F).dump
0 3 * * 0 root tar -czf /backups/clearsight/snapshot-$(date +\%F).tar.gz /var/lib/docker/volumes/dbdata/
```

## 6) Restore Drill
- Quarterly: pick a random nightly dump, restore to test DB, run smoke query.
- Record outcome in `/backups/clearsight/restore-log.md`.

## 7) Verification
- After each backup, compute and store SHA256.
- Alert on missing or size < 10MB.
