# Database Schema

Companion to the [ER diagram](./er-diagram.md). The ER view shows cardinalities; this view shows every column, every constraint, and every index you would see with `\d+` in `psql`.

```mermaid
classDiagram
    class users {
        +uuid id PK
        text username UK
        text password_hash
        text role
        timestamptz created_at
        timestamptz updated_at
        «check» role IN ('manager','supervisor','worker')
    }
    class workers {
        +uuid id PK
        uuid user_id FK → users.id ON DELETE SET NULL
        text first_name
        text last_name
        text badge_id UK
        bool active
        timestamptz created_at
    }
    class stations {
        +uuid id PK
        text code UK
        text name
        text zone
    }
    class shifts {
        +uuid id PK
        uuid worker_id FK → workers.id
        uuid station_id FK → stations.id
        uuid scheduled_shift_id FK → scheduled_shifts.id
        timestamptz clock_in
        timestamptz clock_out
        text close_reason
        «check» clock_out IS NULL OR clock_out >= clock_in
        «partial unique» (worker_id) WHERE clock_out IS NULL
        «index» BTREE(worker_id, clock_in DESC)
    }
    class demand_templates {
        +uuid id PK
        text name
        date effective_from
        date effective_to
    }
    class demand_slots {
        +uuid id PK
        uuid template_id FK → demand_templates.id ON DELETE CASCADE
        uuid station_id FK → stations.id
        smallint dow
        time starts_at
        time ends_at
        smallint head_count
        «check» dow BETWEEN 0 AND 6
        «check» ends_at > starts_at
        «check» head_count > 0
    }
    class availability {
        +uuid id PK
        uuid worker_id FK → workers.id ON DELETE CASCADE
        smallint dow
        time starts_at
        time ends_at
        text preference
        «check» preference IN ('available','preferred','unavailable')
        «unique» (worker_id, dow, starts_at)
    }
    class time_off_requests {
        +uuid id PK
        uuid worker_id FK → workers.id
        date starts_on
        date ends_on
        text reason
        text state
        timestamptz decided_at
        uuid decided_by FK → users.id
        «check» ends_on >= starts_on
        «check» state IN ('pending','approved','denied','canceled')
    }
    class schedule_runs {
        +uuid id PK
        uuid template_id FK → demand_templates.id
        date week_start
        text inputs_sha
        text state
        real coverage_pct
        int unfilled_count
        uuid created_by FK → users.id
        timestamptz created_at
        timestamptz published_at
        «check» state IN ('pending','previewed','published','archived')
        «partial unique» (template_id, week_start) WHERE state='published'
    }
    class scheduled_shifts {
        +uuid id PK
        uuid schedule_run_id FK → schedule_runs.id
        uuid worker_id FK → workers.id
        uuid station_id FK → stations.id
        timestamptz starts_at
        timestamptz ends_at
        text state
        uuid superseded_by FK → scheduled_shifts.id
        «check» ends_at > starts_at
        «check» state IN ('scheduled','open','superseded','canceled','completed')
        «partial unique» (worker_id, starts_at) WHERE state IN ('scheduled','open') AND worker_id IS NOT NULL
        «partial index» WHERE worker_id IS NULL AND state='open'
    }
    class swap_requests {
        +uuid id PK
        uuid from_slot_id FK → scheduled_shifts.id
        uuid to_slot_id FK → scheduled_shifts.id
        uuid requested_by FK → users.id
        uuid counterpart FK → users.id
        uuid approver FK → users.id
        text state
        timestamptz created_at
        timestamptz decided_at
        «check» state IN ('awaiting_counterpart','awaiting_supervisor','approved','declined_by_counterpart','denied_by_supervisor','canceled','stale')
        «partial index» WHERE state LIKE 'awaiting_%'
    }

    users "1" --> "0..1" workers
    workers "1" --> "0..*" shifts
    stations "1" --> "0..*" shifts
    scheduled_shifts "1" --> "0..1" shifts
    demand_templates "1" --> "0..*" demand_slots
    stations "1" --> "0..*" demand_slots
    workers "1" --> "0..*" availability
    workers "1" --> "0..*" time_off_requests
    demand_templates "1" --> "0..*" schedule_runs
    schedule_runs "1" --> "0..*" scheduled_shifts
    workers "1" --> "0..*" scheduled_shifts
    stations "1" --> "0..*" scheduled_shifts
    scheduled_shifts "1" --> "0..*" swap_requests : from
    scheduled_shifts "1" --> "0..*" swap_requests : to
    users "1" --> "0..*" swap_requests : actor
```

## Migration order

```
001_init_users.sql
002_workers_stations.sql
003_demand_templates_slots.sql
004_availability_timeoff.sql
005_schedule_runs_shifts.sql
006_shifts_clockevents.sql
007_swap_requests.sql
```

Each file is additive and reversible. `node-pg-migrate` tracks applied names in `pgmigrations`.
