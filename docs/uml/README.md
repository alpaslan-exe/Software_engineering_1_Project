# UML Diagrams — ShiftDeck

All diagrams are authored in [Mermaid](https://mermaid.js.org/) and render inline on GitHub.

## Structure

| Kind | Diagram | File |
|---|---|---|
| Structural | System architecture | [`architecture.md`](./architecture.md) |
| Structural | Deployment topology | [`deployment.md`](./deployment.md) |
| Structural | Domain class diagram | [`class-diagram.md`](./class-diagram.md) |
| Structural | Database ER diagram | [`er-diagram.md`](./er-diagram.md) |
| Structural | Full schema (columns + constraints + indexes) | [`schema.md`](./schema.md) |
| Behavioral | Use cases | [`use-cases.md`](./use-cases.md) |
| Behavioral | Sequence — worker clock-in | [`seq-clock-in.md`](./seq-clock-in.md) |
| Behavioral | Sequence — shift swap request | [`seq-swap-request.md`](./seq-swap-request.md) |
| State | Shift (clock-in → clock-out) | [`state-shift.md`](./state-shift.md) |
| State | Swap request | [`state-swap-request.md`](./state-swap-request.md) |
| Activity | Shift lifecycle | [`activity-shift.md`](./activity-shift.md) |
| Activity | Schedule generator pipeline | [`activity-scheduling.md`](./activity-scheduling.md) |

## Legend

- **Structural** — what the system *is*: components, classes, tables.
- **Behavioral** — what the system *does* in time: use cases, sequences.
- **State** — what each entity *can be*: lifecycle rules, guards, transitions.
- **Activity** — how work *flows* through the system: branches, loops, swim-lanes.
