# PBI-11: Cash Flow & Alerts

**Status**: InProgress (Alerts pending full integration)  
**Priority**: Medium  
**Complexity**: Medium  
**Owner**: Saeed  
**Created**: 2025-10-19  
**Last Reviewed**: 2025-11-09  

[View in Backlog](../backlog.md#user-content-11)

---

## Overview

Provide users with forward-looking cash flow insights and proactive alerts when recurring payments behave unexpectedly. This PBI sits on top of PBI 9’s recurring detection and PBI 10’s dashboard, surfacing actionable signals (missing payments, amount changes, net income trends).

## Problem Statement

Users need to know if essential payments are missed or spike unexpectedly and understand recent cash flow trends. Without alerts and context, they risk overdrafts, late fees, or undetected subscription price hikes.

## User Stories

- **As a user**, I want to be alerted when a recurring payment is missed so I can take corrective action.
- **As a user**, I want to know when a recurring payment amount changes significantly so I can investigate.
- **As a user**, I want to see recent net income trends so I can gauge cash flow direction.
- **As a user**, I want alerts reflected in the dashboard so I can act quickly.

## Technical Approach

- Extend `RecurringManager` to compute alert sets (missing payments, amount changes).
- Expose `/recurring/api/alerts` endpoint consumed by UI.
- Update dashboard metrics (via `/dashboard/api/health`) to include net income and savings rate.
- Ensure import/recategorization flow updates recurring instances so alerts stay accurate (pending).

## UX/UI Considerations

- Alerts appear prominently on `/recurring` page with severity styling.
- Stats card counts total alerts.
- Dashboard should incorporate cash flow metrics (net income, savings rate) already delivered in PBI 10.
- Future: consider surfacing alert badge in global nav.

## Acceptance Criteria

### Must Have
- [x] Alert generation logic for missing payments (>3 days overdue).
- [x] Alert generation logic for amount changes (>10% variance).
- [x] `/recurring/api/alerts` returns categorized alerts.
- [x] Recurring UI displays alerts with severity cues.
- [ ] Import flow updates recurring instances so alerts reflect new payments.
- [ ] Automated tests covering alert scenarios.

### Should Have
- [x] Dashboard includes net income and savings rate metrics.
- [ ] Alert counts surfaced on dashboard (future enhancement).

### Could Have
- [ ] Predictive cash flow charts.
- [ ] Configurable alert thresholds per recurring item.
- [ ] Email/push notifications.

## Dependencies

- PBI 9 recurring detection (patterns, instances).
- PBI 10 dashboard API for net income metrics.

## Open Questions

1. Should alert thresholds be user-configurable?
2. How should dismissed alerts be stored/audited?
3. Do we need a daily job to recompute alerts, or is on-demand evaluation sufficient?

## Related Tasks

- [Tasks for PBI 11](./tasks.md)
- [PBI 9: Recurring Transaction Detection](../9/prd.md)

---

