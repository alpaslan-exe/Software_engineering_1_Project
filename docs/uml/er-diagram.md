# Entity-Relationship Diagram

Postgres schema `shiftdeck`. UUID primary keys, `created_at` / `updated_at` on every table (omitted here for clarity).

```mermaid
erDiagram
    USERS ||--o| WORKERS : "login for"
    WORKERS ||--o{ SHIFTS : "logs"
    STATIONS ||--o{ SHIFTS : "hosts"
    STATIONS ||--o{ SCHEDULED_SHIFTS : "hosts"
    STATIONS ||--o{ DEMAND_SLOTS : "declared for"
    DEMAND_TEMPLATES ||--o{ DEMAND_SLOTS : "contains"
    DEMAND_TEMPLATES ||--o{ SCHEDULE_RUNS : "input to"
    SCHEDULE_RUNS ||--o{ SCHEDULED_SHIFTS : "produced"
    WORKERS ||--o{ SCHEDULED_SHIFTS : "assigned"
    WORKERS ||--o{ AVAILABILITY : "declares"
    WORKERS ||--o{ TIME_OFF_REQUESTS : "requests"
    SCHEDULED_SHIFTS ||--o| SHIFTS : "realized by"
    SCHEDULED_SHIFTS ||--o{ SWAP_REQUESTS : "subject of (from)"
    SCHEDULED_SHIFTS ||--o{ SWAP_REQUESTS : "subject of (to)"
    USERS ||--o{ SWAP_REQUESTS : "requested by"
    USERS ||--o{ SWAP_REQUESTS : "counterpart"
    USERS ||--o{ SWAP_REQUESTS : "approver"
    USERS ||--o{ TIME_OFF_REQUESTS : "decided by"

    USERS {
        uuid id PK
        text username UK
        text password_hash
        text role "manager|supervisor|worker"
    }

    WORKERS {
        uuid id PK
        uuid user_id FK
        text first_name
        text last_name
        text badge_id UK
        bool active
    }

    STATIONS {
        uuid id PK
        text code UK
        text name
        text zone
    }

    SHIFTS {
        uuid id PK
        uuid worker_id FK
        uuid station_id FK
        uuid scheduled_shift_id FK "nullable (walk-in)"
        timestamptz clock_in
        timestamptz clock_out "nullable"
        text close_reason
    }

    DEMAND_TEMPLATES {
        uuid id PK
        text name
        date effective_from
        date effective_to
    }

    DEMAND_SLOTS {
        uuid id PK
        uuid template_id FK
        uuid station_id FK
        int dow "0=Sunday..6=Saturday"
        time starts_at
        time ends_at
        int head_count
    }

    AVAILABILITY {
        uuid id PK
        uuid worker_id FK
        int dow
        time starts_at
        time ends_at
        text preference "available|preferred|unavailable"
    }

    TIME_OFF_REQUESTS {
        uuid id PK
        uuid worker_id FK
        date starts_on
        date ends_on
        text reason
        text state "pending|approved|denied|canceled"
    }

    SCHEDULE_RUNS {
        uuid id PK
        uuid template_id FK
        date week_start "Monday ISO"
        text inputs_sha
        text state "pending|previewed|published|archived"
        float4 coverage_pct
        int unfilled_count
        uuid created_by FK
        timestamptz created_at
        timestamptz published_at
    }

    SCHEDULED_SHIFTS {
        uuid id PK
        uuid schedule_run_id FK
        uuid worker_id FK "nullable (open shift)"
        uuid station_id FK
        timestamptz starts_at
        timestamptz ends_at
        text state "scheduled|open|superseded|canceled|completed"
        uuid superseded_by FK "nullable, SELF"
    }

    SWAP_REQUESTS {
        uuid id PK
        uuid from_slot_id FK
        uuid to_slot_id FK
        uuid requested_by FK
        uuid counterpart FK
        uuid approver FK "nullable"
        text state "awaiting_counterpart|awaiting_supervisor|approved|declined_by_counterpart|denied_by_supervisor|canceled|stale"
        timestamptz created_at
        timestamptz decided_at
    }
```

## Indexing & retention

- `shifts` — partial unique index `(worker_id) WHERE clock_out IS NULL` blocks double clock-ins; btree `(worker_id, clock_in DESC)` for the timesheet query.
- `scheduled_shifts` — unique index `(worker_id, starts_at) WHERE state IN ('scheduled','open') AND worker_id IS NOT NULL` to block double-booking; btree `(schedule_run_id, state)` for publish queries; partial index `WHERE worker_id IS NULL AND state='open'` for the open-shift marketplace.
- `swap_requests` — partial index `WHERE state IN ('awaiting_counterpart','awaiting_supervisor')` for inbox queries.
- `shifts` are permanent (payroll). `scheduled_shifts` is permanent (history + audit of what was planned vs. what happened).
