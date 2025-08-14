# CS-FRD-FunctionalRequirements-v1_0
**Project:** ClearSight – Production Traceability System  
**Persona:** Business Analyst  
**Version:** v1.0  
**Date:** 2025-08-10

---

## Overview
This FRD translates the Product Owner's scope and acceptance criteria into detailed, actionable functional requirements for the ClearSight system. Requirements are uniquely numbered and traceable to acceptance criteria.

---

## FRD-001: Unique Serial Number Generation
- The system SHALL generate a unique serial number for each board at the start of the process.
- Serial number SHALL encode: date code (YYYYMMDD), SKU code, and incremental batch counter.
- Serial number SHALL be stored in the database and linked to all subsequent events.
- Traceability: AC-001, AC-002

## FRD-002: SKU & ERP Master Data Integration
- The system SHALL maintain a master SKU table containing SKU code, description, and ERP reference.
- The system SHALL allow onboarding of new SKUs via CSV upload or ERP sync.
- ERP sync SHALL occur at least once per day.
- Traceability: AC-003

## FRD-003: Stage Workflow Management
- The system SHALL define sequential stages: Soldering → QC → Electrical Testing → Final Production.
- The system SHALL allow configurable stage definitions for different product lines.
- The system SHALL support rework loops (QC fail → Soldering; Electrical fail → QC optional → Electrical retest).
- Traceability: AC-004, AC-005

## FRD-004: Stage Event Logging
- Every transition SHALL log: board serial, stage name, user ID, timestamp, and action taken (pass/fail/rework).
- Users SHALL be authenticated before logging events.
- Traceability: AC-006, AC-007

## FRD-005: Dashboard – Floor Manager View
- Floor manager dashboard SHALL display:
  - Boards in each stage
  - WIP counts
  - Bottleneck alerts
  - Rework statistics
- Dashboard SHALL update in real-time (≤ 5s delay).
- Traceability: AC-008, AC-009

## FRD-006: Accountability Tracking
- The system SHALL maintain a complete audit trail of who performed each action.
- Audit trail SHALL be queryable by board serial number.
- Traceability: AC-010

## FRD-007: On-Premise Browser-Based Access
- The system SHALL be accessible via modern browsers within the corporate LAN.
- No public internet exposure is required for MVP.
- Traceability: AC-011
