# System Architecture

Container-level view of ShiftDeck: processes, how they talk, and the trust boundary between the demo simulator and the operator-facing stack.

```mermaid
flowchart LR
    subgraph Worker["Worker (kiosk or phone)"]
        UIk["React: Clock Kiosk + My Schedule"]
        WSk["socket.io-client"]
    end

    subgraph Mgr["Manager / Supervisor"]
        UIm["React: Roster + Schedule Builder + Swap Inbox"]
        WSm["socket.io-client"]
    end

    subgraph Server["Application Host"]
        API["Express REST API"]
        HUB["Socket.IO Hub<br/>(rooms: floor:global, station:*,<br/>schedule, user:*, role:supervisor)"]
        AUTH["Session + RBAC<br/>Middleware"]
        SVC["Domain Services<br/>Shift · Schedule · Swap · TimeOff · Availability"]
        REPO["Repositories<br/>(pg pool)"]
    end

    DB[("PostgreSQL 16<br/>shiftdeck schema")]

    Sim["Simulator<br/>(demo only)"]

    UIk -- "HTTPS REST" --> API
    UIm -- "HTTPS REST" --> API
    WSk <-- "WebSocket" --> HUB
    WSm <-- "WebSocket" --> HUB
    API --> AUTH --> SVC --> REPO --> DB
    SVC -- "broadcast" --> HUB
    Sim -- "POST /sim/tick" --> API

    classDef store fill:#eef,stroke:#447
    class DB store
```

## Trust boundary

- **Browser side:** only REST + WebSocket, both over TLS in production. No direct DB access.
- **Simulator:** dev-only. The `/sim/*` routes are mounted only when `NODE_ENV=development`. There is no device-bridge equivalent in this scope — all realtime pressure comes from humans tapping badges.

## Scaling notes

- The `pg` pool is per-process; the hub currently runs single-node. Horizontal scale would add a Redis adapter for Socket.IO and move session storage out of memory into the same Redis.
- The hot path is clock-in and clock-out. Both are a single INSERT / UPDATE plus a broadcast — no telemetry fire-hose to shed.
