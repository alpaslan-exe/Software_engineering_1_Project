# Sequence — Worker Clock-In

Flow starts when a worker taps their badge at the kiosk. Ends when every manager with the roster open sees the new on-floor count tick up without a page refresh.

```mermaid
sequenceDiagram
    autonumber
    actor Worker
    participant UI as Kiosk UI (React)
    participant API as Express API
    participant Auth as RBAC Middleware
    participant Svc as ShiftService
    participant Repo as Repositories
    participant DB as PostgreSQL
    participant Hub as Socket.IO Hub
    participant Mgr as Manager Roster

    Worker->>UI: Tap badge (badgeId, stationId)
    UI->>API: POST /shifts/clock-in {badgeId, stationId}
    API->>Auth: validate session + role
    Auth-->>API: ok (role=worker|kiosk)
    API->>Svc: clockIn(badgeId, stationId)
    Svc->>Repo: findWorkerByBadge(badgeId)
    Repo->>DB: SELECT ... FROM workers WHERE badge_id=$1
    DB-->>Repo: worker row
    Repo-->>Svc: Worker
    Svc->>Repo: findOpenShift(workerId)
    Repo-->>Svc: null (none open)
    Svc->>Repo: findScheduledShiftForNow(workerId, stationId)
    Repo->>DB: SELECT scheduled_shifts WHERE worker_id=$1 AND station_id=$2<br/>AND state='scheduled' AND now() BETWEEN starts_at AND ends_at
    DB-->>Repo: ScheduledShift (or null)
    Repo-->>Svc: ScheduledShift?
    Svc->>Repo: insertShift(workerId, stationId, scheduledShiftId, now)
    Repo->>DB: INSERT INTO shifts ... RETURNING *
    DB-->>Repo: Shift row
    Repo-->>Svc: Shift
    Svc->>Hub: broadcast("station:"+stationId, "worker:clock_in", payload)
    Svc->>Hub: broadcast("floor:global", "roster:changed", {+1})
    Svc-->>API: Shift
    API-->>UI: 201 Created {shift, lateByMin, scheduled?}
    UI-->>Worker: "Welcome back, {name}" (+ "You are N min late" if applicable)
    Hub-->>Mgr: worker:clock_in → UI increments on-floor count
```

## Error branches

- **Already clocked in** — `findOpenShift` returns a shift; service throws `ConflictError`; API responds `409`.
- **Unknown badge** — repo returns null; service throws `NotFoundError`; API responds `404`.
- **No scheduled shift at this time** — `scheduledShiftId` is left null and the shift is flagged `walk_in` so attendance reports can show it.
