# Activity Diagram — Schedule Generator

How the weekly schedule is built, reviewed, and published. Driven by a `schedule_runs` row so every published schedule can be traced to its inputs.

```mermaid
flowchart TD
    Start([Manager clicks "Generate week N"]) --> Load[Load inputs:<br/>- demand_template for week N<br/>- worker availability<br/>- hours cap per worker<br/>- open time-off rows]
    Load --> Val{Inputs complete?}
    Val -- no --> Fix[Prompt manager to fill gaps]
    Fix --> Load
    Val -- yes --> Snap[Insert schedule_runs row<br/>status=pending, inputs hashed]
    Snap --> Pass1[Pass 1: greedy fill<br/>station x hour slot by seniority]
    Pass1 --> Pass2[Pass 2: constraint repair<br/>- resolve double-booked workers<br/>- cap daily + weekly hours]
    Pass2 --> Pass3[Pass 3: optimizer<br/>- minimize unfilled slots<br/>- prefer worker preferences]
    Pass3 --> Metric[Compute coverage %<br/>+ unfilled slots list]
    Metric --> Preview[Render preview UI:<br/>coverage heat-map,<br/>per-worker summary]
    Preview --> Review{Manager approves?}
    Review -- no --> Edit[Drag-to-swap editor]
    Edit --> Metric
    Review -- yes --> Lock[Insert scheduled_shifts rows<br/>status=published,<br/>schedule_runs.status=published]
    Lock --> Notify[Broadcast scheduled_shift:published<br/>+ email each affected worker]
    Notify --> End([End])
```

## Determinism

- Inputs are hashed into `schedule_runs.inputs_sha`; re-running with the same hash must produce the same output.
- Random tie-breaks seed off `schedule_runs.id` (UUID v7), so a reproduced run from the same inputs produces the same output.

## Post-publish mutation

A published schedule is immutable at the row level. Changes happen through:
- **Swap requests** — two workers trade; approval chain closes one slot and reopens the paired one.
- **Open-shift drops** — supervisor marks a slot `open`, any eligible worker claims.
- **Supervisor override** — writes a new `scheduled_shifts` row and marks the prior row `superseded`, keeping history intact.
