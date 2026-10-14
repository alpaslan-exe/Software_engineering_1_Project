# Sequence — Shift Swap Request

Worker A asks to trade their Thursday 2–10 PM slot for Worker B's Friday 6 AM–2 PM slot. B must accept; a supervisor must approve the final trade.

```mermaid
sequenceDiagram
    autonumber
    actor A as Worker A
    actor B as Worker B
    actor Sup as Supervisor
    participant UI as Web App (React)
    participant API as Express API
    participant Svc as ScheduleService
    participant Repo as Repositories
    participant DB as PostgreSQL
    participant Hub as Socket.IO Hub

    A->>UI: Pick my slot + target slot (B's)
    UI->>API: POST /swaps {fromSlotId, toSlotId}
    API->>Svc: openSwap(a, fromSlot, toSlot)
    Svc->>Repo: validate both slots not locked, A owns from, B owns to
    Repo->>DB: SELECT scheduled_shifts WHERE id IN ($from,$to)
    DB-->>Repo: 2 rows
    Repo-->>Svc: ok
    Svc->>Repo: insert swap_requests(state=awaiting_counterpart)
    Repo->>DB: INSERT ... RETURNING *
    DB-->>Repo: SwapRequest
    Svc->>Hub: broadcast("user:"+B.id, "swap:incoming", payload)
    Svc-->>API: SwapRequest
    API-->>UI: 201 Created
    Hub-->>B: toast "A wants to swap"

    B->>UI: Open swap, click Accept
    UI->>API: PATCH /swaps/:id {decision:"accept"}
    API->>Svc: counterpartDecide(id, B, accept)
    Svc->>Repo: update swap_requests SET state='awaiting_supervisor'
    Repo->>DB: UPDATE ...
    Svc->>Hub: broadcast("role:supervisor", "swap:pending")

    Sup->>UI: Open supervisor queue, click Approve
    UI->>API: PATCH /swaps/:id {decision:"approve"}
    API->>Svc: supervisorDecide(id, sup, approve)
    Svc->>Svc: begin tx
    Svc->>Repo: swap worker_id columns on both slots
    Repo->>DB: UPDATE scheduled_shifts (slot A → B, slot B → A)
    Svc->>Repo: supersede paired rows if needed
    Svc->>Repo: update swap_requests SET state='approved'
    Svc->>Svc: commit tx
    Svc->>Hub: broadcast("user:"+A.id, "swap:approved")
    Svc->>Hub: broadcast("user:"+B.id, "swap:approved")
    Svc->>Hub: broadcast("tickets:schedule", "schedule:changed")
    Svc-->>API: SwapRequest(approved)
    API-->>UI: 200 OK
```

## Rejection branches

- **B declines** → `state=declined_by_counterpart`; A notified; no slot changes.
- **Supervisor denies** → `state=denied_by_supervisor`; both notified; no slot changes.
- **Slot locked** between request and approval → `state=stale`; request must be re-opened on the new slot.
