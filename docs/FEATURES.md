# ShiftDeck — Feature Catalog

Full feature matrix for the clock-in / clock-out + scheduling scope. Tagged by milestone:

- **MVP** — course deliverable, must demo end-to-end.
- **v1** — polish pass after the demo.
- **v2** — stretch; infra adds (Redis, mobile, SSO).

Status column: `☐` not started, `◐` in progress, `☑` done.

---

## 1. Clock-In / Clock-Out

| # | Feature | Milestone | Status |
|---|---|---|---|
| 1.1 | Badge-tap clock-in from kiosk (station-scoped) | MVP | ☐ |
| 1.2 | Clock-out with duration summary | MVP | ☐ |
| 1.3 | Prevent double clock-in (partial unique index) | MVP | ☐ |
| 1.4 | Supervisor-forced clock-out | MVP | ☐ |
| 1.5 | Match a clock-in to the matching `scheduled_shifts` row (late / early / missed flag) | MVP | ☐ |
| 1.6 | Nightly reaper for forgotten shifts (> 16 h → `auto_closed`) | v1 | ☐ |
| 1.7 | Mid-shift station reassignment (close + open) | v1 | ☐ |
| 1.8 | Overtime flag on shifts > 8 h | v1 | ☐ |
| 1.9 | Audit stream in `shift_events` | v1 | ☐ |
| 1.10 | Break tracking (sub-interval inside a shift) | v2 | ☐ |

## 2. Worker-Facing Scheduling

Each worker sees **their own** schedule, picks up open shifts, requests swaps, and submits time-off requests — all from the web app with no manager intervention required for the common path.

| # | Feature | Milestone | Status |
|---|---|---|---|
| 2.1 | "My Schedule" page (upcoming 2 weeks) | MVP | ☐ |
| 2.2 | Open-shift marketplace (view, claim) | MVP | ☐ |
| 2.3 | Swap request → counterpart approval → supervisor approval | MVP | ☐ |
| 2.4 | Mobile-friendly layout | MVP | ☐ |
| 2.5 | Time-off request with reason | v1 | ☐ |
| 2.6 | Availability window per worker (preferred days/hours) | v1 | ☐ |
| 2.7 | ICS calendar export of own shifts | v1 | ☐ |
| 2.8 | Shift reminder push 24 h / 1 h before | v2 | ☐ |

## 3. Manager Schedule Generator

Auto-builds a weekly schedule from a demand template and worker availability, then exposes a drag-to-adjust editor. Driven by a `schedule_runs` row so every generation is reproducible and auditable.

| # | Feature | Milestone | Status |
|---|---|---|---|
| 3.1 | Demand template editor (station × hour → head-count) | MVP | ☐ |
| 3.2 | Worker availability + hours cap intake | MVP | ☐ |
| 3.3 | Greedy generator (fills demand, respects caps + availability) | MVP | ☐ |
| 3.4 | Publish → notify all affected workers | MVP | ☐ |
| 3.5 | Drag-to-swap editor on the preview | MVP | ☐ |
| 3.6 | Constraint solver pass (minimize unfilled, prefer seniority) | v1 | ☐ |
| 3.7 | Side-by-side diff vs. prior week | v1 | ☐ |
| 3.8 | Coverage heat-map (red = under-staffed hours) | v1 | ☐ |
| 3.9 | Lock & publish with signature (immutable after lock) | v1 | ☐ |
| 3.10 | Re-run from the same inputs → identical output (deterministic) | v1 | ☐ |
| 3.11 | What-if simulator ("drop worker X, see impact") | v2 | ☐ |

## 4. Dashboard & Reporting

| # | Feature | Milestone | Status |
|---|---|---|---|
| 4.1 | Live roster (who is clocked in, which station, how long) | MVP | ☐ |
| 4.2 | KPI strip (on-floor count, open shifts, missed clock-ins today) | MVP | ☐ |
| 4.3 | Timesheet view per worker (shifts between two dates) | MVP | ☐ |
| 4.4 | CSV export of timesheets for payroll | MVP | ☐ |
| 4.5 | Attendance report (late / early / missed vs. scheduled) | v1 | ☐ |
| 4.6 | Scheduled daily digest email | v1 | ☐ |
| 4.7 | Historical replay slider ("rewind to 2 h ago") | v2 | ☐ |

## 5. Auth, RBAC, Admin

| # | Feature | Milestone | Status |
|---|---|---|---|
| 5.1 | Session login (bcrypt + cookie) | MVP | ☐ |
| 5.2 | Three roles enforced in middleware (manager / supervisor / worker) | MVP | ☐ |
| 5.3 | User admin page (create / disable, assign worker row) | MVP | ☐ |
| 5.4 | Password reset by admin | v1 | ☐ |
| 5.5 | Audit log viewer | v1 | ☐ |
| 5.6 | 2FA (TOTP) for manager role | v2 | ☐ |
| 5.7 | SSO (Google / Microsoft) | v2 | ☐ |

## 6. Realtime Infrastructure

| # | Feature | Milestone | Status |
|---|---|---|---|
| 6.1 | Socket.IO rooms: `floor:global`, `station:*`, `schedule`, `user:<id>`, `role:supervisor` | MVP | ☐ |
| 6.2 | Room auth gating (role check on join) | MVP | ☐ |
| 6.3 | Reconnect-with-replay (missed-events window) | v2 | ☐ |
| 6.4 | Redis adapter for horizontal scale | v2 | ☐ |

## 7. Platform & Ops

| # | Feature | Milestone | Status |
|---|---|---|---|
| 7.1 | `docker compose up` boots full dev stack | MVP | ☐ |
| 7.2 | Seed script for demo data | MVP | ☐ |
| 7.3 | GitHub Actions CI (lint + test) | MVP | ☐ |
| 7.4 | Simulator service for demo clock events | MVP | ☐ |
| 7.5 | Pino → journald in prod | v1 | ☐ |
| 7.6 | Nightly DB backup to S3-compatible store | v2 | ☐ |

---

## Milestone groupings

**MVP (course deliverable)**
Clock-in/out 1.1–1.5; Worker scheduling 2.1–2.4; Manager generator 3.1–3.5; Dashboard 4.1–4.4; Auth 5.1–5.3; Realtime 6.1–6.2; Platform 7.1–7.4.

**v1 (polish)** — everything tagged v1 above.
**v2 (stretch)** — everything tagged v2 above.
