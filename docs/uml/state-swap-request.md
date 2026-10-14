# State Machine — Shift Swap Request

Every `swap_requests` row moves through this lifecycle. Approvals need two consents: the counterpart worker, then a supervisor.

```mermaid
stateDiagram-v2
    [*] --> AWAITING_COUNTERPART : A opens request
    AWAITING_COUNTERPART --> AWAITING_SUPERVISOR : B accepts
    AWAITING_COUNTERPART --> DECLINED_BY_COUNTERPART : B declines
    AWAITING_COUNTERPART --> CANCELED : A cancels
    AWAITING_SUPERVISOR --> APPROVED : supervisor approves
    AWAITING_SUPERVISOR --> DENIED_BY_SUPERVISOR : supervisor denies
    AWAITING_SUPERVISOR --> CANCELED : A or B cancels
    AWAITING_SUPERVISOR --> STALE : slot locked/edited by generator
    AWAITING_COUNTERPART --> STALE : slot locked/edited by generator
    APPROVED --> [*]
    DECLINED_BY_COUNTERPART --> [*]
    DENIED_BY_SUPERVISOR --> [*]
    CANCELED --> [*]
    STALE --> [*]
```

## Guards

| Transition | Guard |
|---|---|
| any → `AWAITING_SUPERVISOR` | both slots still exist, same week, not yet started |
| `AWAITING_SUPERVISOR → APPROVED` | neither worker now exceeds weekly hour cap after swap |
| any → `STALE` | at least one slot's `generation_run_id` changed since request opened |

## Side effects

- `APPROVED` writes the swap in a single transaction and broadcasts `swap:approved` on the two worker rooms and `schedule:changed` on the global schedule room.
- Any terminal state writes a `ticket_events`-style row in `swap_events` for audit.
