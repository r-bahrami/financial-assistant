# PBI-8: Savings Goals Foundation

**Status**: Done  
**Priority**: Medium  
**Complexity**: Medium  
**Owner**: Saeed  
**Created**: 2025-10-19  
**Last Reviewed**: 2025-11-09  

[View in Backlog](../backlog.md#user-content-8)

---

## Overview

Lay the groundwork for savings goal tracking by adding persistent storage and model abstractions. The initial scope intentionally excludes UI to keep Phase 3 focused on backend readiness, enabling future front-end experiences without major data migrations.

## Problem Statement

Users need a way to plan for medium/long-term objectives (e.g., emergency funds, vacations, down payments). Without a structured representation of goals and progress, the system cannot provide meaningful guidance or reporting.

Current gaps:
- No schema to store goal metadata (target amount, target date, progress).
- No service/model layer to manipulate goal data.
- No linkage between goals and categories to inform budgeting.

## User Stories

- **As a user**, I want to define savings goals with targets so I can track progress.
- **As a developer**, I want a stable database schema for goals so UI iterations can ship independently.
- **As a product owner**, I want goals associated with categories to align with budgeting/reporting.

## Technical Approach

- Introduce a `savings_goals` table with target/current amounts, dates, category linkage, and status.
- Provide a lightweight model class (`models/goal.py`) encapsulating CRUD operations.
- Ensure forward-compatible schema (timestamps, status enum) for future automation.
- Defer API/UI/automation until subsequent PBIs.

## UX/UI Considerations

- UI intentionally deferred; future work should expose progress bars, projections, and linking to budgets.
- Ensure schema supports storing sufficient metadata for eventual visualization (e.g., target date, progress).

## Acceptance Criteria

### Must Have
- [x] Database migration creates `savings_goals` table with required columns and constraints.
- [x] Model abstraction exposes CRUD operations for savings goals.
- [x] API endpoints for creating/updating goals.
- [x] UI for viewing and editing goals.
- [ ] Goal progress auto-updates based on transactions (future enhancement).

### Should Have
- [x] Category association for goals (enables future reporting).
- [ ] Validation to prevent duplicate active goals with same name/category (future).
- [ ] Seeds/sample data (future).

### Could Have
- [ ] Automated reminders or projections.
- [ ] Integration with budgets dashboard.
- [ ] Goal sharing/export capabilities.

## Dependencies

- Existing categories infrastructure (for category_id foreign key).
- Transaction import and categorization for future progress calculations.

## Open Questions

1. Should goals support multiple contributing categories or only one?
2. How should recurring contributions be tracked against goal progress?
3. What permissions/audit requirements are needed for future multi-user scenarios?

## Related Tasks

- [Tasks for PBI 8](./tasks.md)
- [Recurring transaction PBI (foundation for alerts)](../9/prd.md)

---

