# ShiftDeck — Employee Clock-In / Clock-Out & Scheduling

> **CIS 375 — Software Engineering I — Final Project**
> A focused web app for employee time-tracking: workers punch in and out, see their own schedule, trade shifts, and request time-off; managers build the weekly schedule from a demand template and watch who is on the floor in real time.

[![Rust](https://img.shields.io/badge/Backend-Rust-000000?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#11-license)

---

## 1. Problem

Even small shops run time-tracking on an index card, a spreadsheet, and a group chat. The result: forgotten clock-outs, missed shift coverage, swap requests buried in DMs, and a payroll run that takes a full day to reconcile. ShiftDeck replaces the index card and the group chat with one web app:

- **Workers** punch in and out, see their upcoming schedule, pick up open shifts, trade shifts with a coworker, and request time-off.
- **Managers** build a weekly schedule from a reusable demand template, review coverage before publishing, and watch a live roster of who is currently clocked in.

The original pitch was broader (maintenance + machinery + live feeds); after review the team scoped the project down to the clock-in / clock-out slice.


## 2. Stack

| Layer | Tech |
|---|---|
| Backend | **Rust** (web framework chosen in the architecture phase) |
| Frontend | **JavaScript** single-page app (framework chosen in the architecture phase) |
| Realtime | WebSocket push from the API to open roster / queue screens (NFR-2.2) |
| Database | **PostgreSQL 16** with versioned SQL migrations |
| Auth | Session cookies, salted one-way password hashes (NFR-4.1), role-based (manager / supervisor / worker), 30-minute idle timeout (NFR-4.3) |
| Email | SMTP; a local test mail server in Docker Compose for development (IR-3.1) |
| Simulator | Dev-only tool that generates demo clock-in/out events (C3: disabled in production) |
| Dev / CI | Docker Compose (NFR-5.1), GitHub Actions running lint + tests on every push (NFR-5.2) |

Constraint C2 (REQUIREMENTS §1.4): Rust for the server, PostgreSQL 16 for storage. Library choices (web framework, database crate, frontend framework, test tools) are recorded here once the team decides them.

## 3. Architecture at a Glance

```
┌──────────────────┐     HTTPS/REST + WebSocket    ┌────────────────────┐
│   Web client     │ ────────────────────────────► │   Rust API         │
│   (JavaScript)   │ ◄──── realtime events ─────── │  + realtime hub    │
└──────────────────┘                               └─────────┬──────────┘
                                                             │ SQL
                                                             │
┌──────────────────┐                               ┌─────────▼──────────┐
│  Simulator       │ ─── POST /sim/clock events ─► │   PostgreSQL 16    │
│  (demo only)     │                               │  (shiftdeck)       │
└──────────────────┘                               └────────────────────┘
```

Requirements specification in [`docs/REQUIREMENTS.md`](./docs/REQUIREMENTS.md). Full feature matrix in [`docs/FEATURES.md`](./docs/FEATURES.md). UI mockups in [`docs/MOCKUPS.md`](./docs/MOCKUPS.md). Requirement → design → code → test tracking in [`docs/TRACEABILITY.md`](./docs/TRACEABILITY.md).

> **Source of truth.** The Step 1–2 report is the master copy of the requirements and design. Everything in `docs/` mirrors it. If you change a requirement or diagram, change the report and the repo together in the same pull request.

## 4. UML

All diagrams, with sources and re-render instructions: [`docs/uml/`](./docs/uml).

- Use case diagram + descriptions (UC-01 … UC-23) — [`docs/uml/use-cases.md`](./docs/uml/use-cases.md)
- Sequence diagrams — [clock in](./docs/uml/img/sequence-clock-in.svg), [clock out](./docs/uml/img/sequence-clock-out.svg)
- Class diagram — [`docs/uml/img/class-diagram.svg`](./docs/uml/img/class-diagram.svg)
- Dialog maps — [kiosk](./docs/uml/img/dialog-map-kiosk.svg), [web application](./docs/uml/img/dialog-map-web.svg)

## 5. Repository Layout

```
.
├── apps/
│   ├── api/            # Rust API server (internal layout set in the architecture phase)
│   │   ├── src/
│   │   │   ├── routes/         # boundary: HTTP endpoints
│   │   │   ├── realtime/       # boundary: WebSocket push
│   │   │   ├── domain/         # control: ClockController, SwapController, …
│   │   │   ├── db/             # entity: repositories for each table
│   │   │   └── auth/           # sessions, role checks
│   │   └── migrations/
│   ├── web/            # JavaScript SPA (worker + supervisor + manager views)
│   │   └── src/
│   │       ├── pages/          # one page per screen in REQUIREMENTS §4.1:
│   │       │                   #   ClockKiosk, LogIn, WorkerHome, MySchedule,
│   │       │                   #   OpenShifts, SwapInbox, TimeOff, Availability,
│   │       │                   #   SupervisorQueue, ScheduleBuilder, LiveRoster,
│   │       │                   #   Timesheets, UserAdmin
│   │       ├── components/
│   │       ├── hooks/
│   │       └── api/            # client wrappers for the REST API
│   └── simulator/      # synthetic clock events for the demo
├── docs/
│   ├── REQUIREMENTS.md
│   ├── FEATURES.md
│   ├── MOCKUPS.md       # + mockups/ (screen images)
│   ├── TRACEABILITY.md
│   └── uml/             # src/ (diagram sources) + img/ (SVG, PNG)
├── docker-compose.yml   # (added in the project setup PR)
└── README.md
```

## 6. Data Model (short form)

| Table | Purpose |
|---|---|
| `users` | account record; `role` ∈ {manager, supervisor, worker} |
| `workers` | HR-side worker row (name, email, badge ID, active, weekly hour cap); FK → `users` for ones that log in |
| `stations` | physical location / department / station the worker is punching into |
| `shifts` | **actual** clock-in/clock-out rows (one per punch pair) |
| `demand_templates` + `demand_slots` | manager-authored demand (station × day-of-week × hour → head-count) |
| `availability` | worker's declared preferred / available / unavailable windows |
| `time_off_requests` | PTO rows with approval chain |
| `schedule_runs` | one row per generation; inputs hash + coverage metrics |
| `scheduled_shifts` | **planned** shifts (`scheduled`/`open`/`superseded`/`canceled`/`completed`) |
| `swap_requests` | two-slot trade proposals with counterpart + supervisor approval |

> **Planned vs. actual.** `scheduled_shifts` is the schedule a manager publishes; `shifts` is what actually happened on the floor. Clock-in resolves a worker to a `scheduled_shift` when one exists for that window, which is how late / early / missed can be flagged.

## 7. API Surface (selected)

| Method | Path | Notes |
|---|---|---|
| `POST` | `/auth/login` | session cookie |
| `POST` | `/auth/logout` | |
| `GET`  | `/me` | current user + role |
| `GET`  | `/workers` / `/workers/:id` | roster |
| `POST` | `/kiosk/badge-tap` | body: `{ badgeId, stationId }`. One endpoint for both directions (FR-2.1.2): clocks the worker **out** if they have an open shift, **in** otherwise. Returns `{ action: "clock_in" \| "clock_out", firstName, minutesLate?, duration? }`; unknown badge → `404` with `"Unknown badge"`. Implemented by `ClockController.handleBadgeTap()`. |
| `POST` | `/shifts/:id/force-close` | supervisor only; body: `{ reason }` (FR-2.3) |
| `GET`  | `/shifts?from&to&workerId=` | timesheet query |
| `GET`  | `/me/schedule?weekStart=` | worker's own schedule for the week |
| `GET`  | `/schedule/open-shifts` | open-shift marketplace |
| `POST` | `/schedule/open-shifts/:id/claim` | worker claims an open slot |
| `POST` | `/swaps` | open a swap request |
| `PATCH`| `/swaps/:id` | counterpart decision / supervisor approval / cancel |
| `GET`  | `/availability` / `POST` `/availability` | worker availability intake |
| `POST` | `/time-off` / `PATCH` `/time-off/:id` | request + approval |
| `POST` | `/demand-templates` | manager builds a demand template |
| `POST` | `/schedule/runs` | kick off a generation (body: `templateId`, `weekStart`) |
| `GET`  | `/schedule/runs/:id` | preview coverage + unfilled list |
| `POST` | `/schedule/runs/:id/publish` | lock + notify |
| `POST` | `/sim/tick` | **dev-only** simulator trigger |

### Realtime channels

| Room | Payload | Consumers |
|---|---|---|
| `floor:global` | roster-change banners | all |
| `station:<id>` | per-station roster + clock events | station view |
| `schedule` | schedule run published, open-shift claimed, slot superseded | schedule editor |
| `user:<id>` | swap incoming / approved / denied, time-off decision | logged-in worker |
| `role:supervisor` | swaps + time-off requests pending supervisor approval | supervisor queue |

## 8. Running Locally

Set up in the project setup PR, after the architecture phase picks the frameworks. Target: one `docker compose up` starts the database, the API, the web client and a test mail server (NFR-5.1).

Planned seed accounts (dev only; the seed step must refuse to run in production):

| Role | Username | Password |
|---|---|---|
| Manager | `manager` | `manager` |
| Supervisor | `super` | `super` |
| Worker | `worker1` | `worker1` |

## 9. Testing

Backend tests run with `cargo test`; frontend tests with the test runner chosen for the web client. CI runs lint and all tests on every push to `main` and on pull requests (NFR-5.2). Step 3 test cases (equivalence classes, boundary values, basis paths) are tracked in [`docs/TRACEABILITY.md`](./docs/TRACEABILITY.md).

## 10. Team

CIS 375, Fall 2026 — University of Michigan–Dearborn.

## 11. License

MIT (the `LICENSE` file is added in the project setup PR).
