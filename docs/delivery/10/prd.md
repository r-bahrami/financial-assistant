# PBI-10: Financial Health Dashboard

**Status**: Done  
**Priority**: High  
**Complexity**: Medium  
**Owner**: Saeed  
**Created**: 2025-10-19  
**Last Reviewed**: 2025-11-09  

[View in Backlog](../backlog.md#user-content-10)

---

## Overview

Deliver a dedicated dashboard that summarizes a user's financial health at a glance. The page aggregates core metrics (income, expenses, savings rate, balance, budgets) and surfaces the most critical spending insights alongside quick navigation links.

## Problem Statement

Without a consolidated view, users must bounce between transactions, reports, and budgets to understand their current financial status. This fragmentation increases cognitive load and hides actionable signals (e.g., overspending) behind multiple clicks.

## User Stories

- **As a user**, I want a health score so I can quickly gauge how I'm doing financially.
- **As a user**, I want to see recent income vs. expenses and savings rate so I can adjust behavior.
- **As a user**, I want to know my total balance and top spending categories so I can prioritize decisions.
- **As a user**, I want quick links to core modules so I can dive deeper with minimal friction.

## Technical Approach

- Create `dashboard` blueprint with `/dashboard` route serving template and `/dashboard/api/health` returning JSON metrics.
- Calculate income/expenses/net income using last 30 days of transactions (excluding transfers).
- Compute savings rate, budget count, total balance, and top categories via SQL queries.
- Derive health score via rule-based scoring considering savings rate, balance, budgets, and net income.
- Build responsive template with cards, top-category list, and quick links.

## UX/UI Considerations

- Prominent health score card with gradient styling to emphasize status.
- Grid layout for metric cards, responsive to smaller screens.
- Clear color coding (green income, red expenses) to reinforce semantics.
- Quick links panel for one-click navigation.
- Integration with navigation bar (Dashboard entry second position).

## Acceptance Criteria

### Must Have
- [x] `/dashboard` route renders dashboard template.
- [x] `/dashboard/api/health` returns JSON with income, expenses, net income, savings rate, total balance, budget count, top categories, health score.
- [x] Health score algorithm uses rule-based scoring (savings rate, balance, budgets, net income).
- [x] Top 5 categories (past 30 days) displayed on page.
- [x] Quick links to Accounts, Transactions, Budgets, Recurring, Reports.

### Should Have
- [x] Responsive layout for cards.
- [ ] Automated tests covering API calculations (pending).

### Could Have
- [ ] Trend charts for health score over time.
- [ ] Personalized recommendations based on metrics.
- [ ] Budget compliance badges.

## Dependencies

- Accounts, transactions, budgets data integrity.
- Categories for spending aggregation.

## Open Questions

1. Should the health score weights be user-configurable?
2. How should multi-currency accounts influence balance calculations?
3. Should alerts from PBI 11 appear directly on the dashboard?

## Related Tasks

- [Tasks for PBI 10](./tasks.md)
- [PBI 11: Cash Flow & Alerts](../11/prd.md)

---

