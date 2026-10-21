# ShiftDeck — Employee Clock-In / Clock-Out & Scheduling

> **CIS 375 — Software Engineering I — Final Project**
> A focused web app for employee time-tracking: workers punch in and out, see their own schedule, trade shifts, and request time-off; managers build the weekly schedule from a demand template and watch who is on the floor in real time.

[![Node.js](https://img.shields.io/badge/Node.js-20.x-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4-010101?logo=socket.io&logoColor=white)](https://socket.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 1. Problem

Even small shops run time-tracking on an index card, a spreadsheet, and a group chat. The result: forgotten clock-outs, missed shift coverage, swap requests buried in DMs, and a payroll run that takes a full day to reconcile. ShiftDeck replaces the index card and the group chat with one web app:

- **Workers** punch in and out, see their upcoming schedule, pick up open shifts, trade shifts with a coworker, and request time-off.
- **Managers** build a weekly schedule from a reusable demand template, review coverage before publishing, and watch a live roster of who is currently clocked in.

The original pitch was broader (maintenance + machinery + live feeds); after review the team scoped the project down to the clock-in / clock-out slice.


## 2. Stack

| Layer | Tech |
|---|---|
| Frontend | React 18 + Vite, React Router, TanStack Query, Tailwind, `socket.io-client` |
| Realtime | Socket.IO over WebSocket |
| Backend | Node.js 20, Express, Zod validation, Pino logging |
| Database | PostgreSQL 16, `pg` driver, migrations via `node-pg-migrate` |
| Auth | Session cookies + bcrypt, role-based (manager / supervisor / worker) |
| Simulator | Node worker that generates demo clock-in/out events |
| Dev / CI | Docker Compose, GitHub Actions, ESLint + Prettier, Vitest + Supertest |

## 3. Architecture at a Glance

```
┌──────────────────┐     HTTPS/REST + WebSocket    ┌────────────────────┐
│   React SPA      │ ────────────────────────────► │   Express API      │
│  worker + mgr    │ ◄──── realtime events ─────── │  + Socket.IO hub   │
└──────────────────┘                               └─────────┬──────────┘
                                                             │ SQL (pg)
                                                             │
┌──────────────────┐                               ┌─────────▼──────────┐
│  Simulator       │ ─── POST /sim/clock events ─► │   PostgreSQL 16    │
│  (demo only)     │                               │  (shiftdeck)       │
└──────────────────┘                               └────────────────────┘
```

The use case diagram lives in [`docs/uml/`](./docs/uml). Full feature matrix in [`docs/FEATURES.md`](./docs/FEATURES.md). Requirements specification in [`docs/REQUIREMENTS.md`](./docs/REQUIREMENTS.md).

## 4. UML

- Use case diagram — [`docs/uml/use-cases.md`](./docs/uml/use-cases.md)

## 5. Repository Layout

```
.
├── apps/
│   ├── api/            # Express + Socket.IO server
│   │   ├── src/
│   │   │   ├── routes/         # REST endpoints
│   │   │   ├── realtime/       # Socket.IO rooms, broadcasters
│   │   │   ├── domain/         # services (Shift, Schedule, Swap, TimeOff)
│   │   │   ├── db/             # pg pool, repository classes
│   │   │   ├── auth/           # sessions, RBAC middleware
│   │   │   └── index.ts
│   │   └── migrations/
│   ├── web/            # React SPA (worker + manager views)
│   │   └── src/
│   │       ├── pages/          # ClockKiosk, MySchedule, OpenShifts,
│   │       │                   #   SwapInbox, ScheduleBuilder, Roster
│   │       ├── components/
│   │       ├── hooks/          # useSocketRoom, useAuth, …
│   │       └── api/            # typed client wrappers
│   └── simulator/      # synthetic clock events for the demo
├── docs/
│   ├── FEATURES.md
│   └── uml/
├── docker-compose.yml
├── package.json        # workspace root
└── README.md
```

## 6. Data Model (short form)

| Table | Purpose |
|---|---|
| `users` | account record; `role` ∈ {manager, supervisor, worker} |
| `workers` | HR-side worker row; FK → `users` for ones that log in |
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
| `POST` | `/shifts/clock-in` | body: `{ badgeId, stationId }` |
| `POST` | `/shifts/clock-out` | body: `{ shiftId }` |
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

### Realtime channels (Socket.IO rooms)

| Room | Payload | Consumers |
|---|---|---|
| `floor:global` | roster-change banners | all |
| `station:<id>` | per-station roster + clock events | station view |
| `schedule` | schedule run published, open-shift claimed, slot superseded | schedule editor |
| `user:<id>` | swap incoming / approved / denied, time-off decision | logged-in worker |
| `role:supervisor` | swaps + time-off requests pending supervisor approval | supervisor queue |

## 8. Running Locally

### Prerequisites
Docker + Docker Compose, Node 20, pnpm.

### Boot everything
```bash
cp .env.example .env
docker compose up -d db          # Postgres
pnpm install
pnpm --filter api migrate:up
pnpm --filter api seed            # loads demo workers + a demand template
pnpm dev                          # concurrently: api, web, simulator
```

Open:
- Web UI — <http://localhost:5173>
- API    — <http://localhost:4000>
- Postgres — `localhost:5432` (user `shiftdeck` / db `shiftdeck`)

### Default seed accounts
| Role | Username | Password |
|---|---|---|
| Manager | `manager` | `manager` |
| Supervisor | `super` | `super` |
| Worker | `worker1` | `worker1` |

(Dev-only; the seed script refuses to run with `NODE_ENV=production`.)

## 9. Testing

```bash
pnpm --filter api test            # unit + supertest integration
pnpm --filter web test            # vitest + React Testing Library
pnpm lint
```

CI runs the same three on every push to `main` and on pull requests.

## 10. Team

CIS 375, Fall 2026 — University of Michigan–Dearborn.

## 11. License

MIT. See [`LICENSE`](./LICENSE).
