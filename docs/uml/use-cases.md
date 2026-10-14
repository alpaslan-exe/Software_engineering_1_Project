# Use Cases

Three human actors (plus a simulator for demos). Mermaid has no dedicated use-case shape; the diagram is drawn with a flowchart grouped by the system boundary.

```mermaid
flowchart LR
    Manager((Manager))
    Supervisor((Supervisor))
    Worker((Worker))
    Sim((Simulator<br/>dev only))

    subgraph Sys["ShiftDeck"]
        UC1[View live roster]
        UC2[Clock in / out]
        UC3[View my schedule]
        UC4[Claim open shift]
        UC5[Request swap]
        UC6[Approve swap<br/>counterpart]
        UC7[Approve swap<br/>supervisor]
        UC8[Request time-off]
        UC9[Decide time-off]
        UC10[Edit demand template]
        UC11[Set availability]
        UC12[Generate weekly schedule]
        UC13[Publish schedule]
        UC14[Export timesheet CSV]
        UC15[Force clock-out]
    end

    Worker --> UC2
    Worker --> UC3
    Worker --> UC4
    Worker --> UC5
    Worker --> UC6
    Worker --> UC8
    Worker --> UC11
    Supervisor --> UC1
    Supervisor --> UC7
    Supervisor --> UC9
    Supervisor --> UC15
    Manager --> UC1
    Manager --> UC10
    Manager --> UC12
    Manager --> UC13
    Manager --> UC14
    Sim --> UC2
```

## Primary flows

- **Clock-in (Worker).** Worker taps their badge; API opens a `shifts` row, matches it to the next `scheduled_shifts` row for that worker/station, hub broadcasts the roster change.
- **Clock-out (Worker).** Taps again; API closes the row with duration + late/early flags.
- **Swap (Worker → Worker → Supervisor).** A opens a request against B's slot. B accepts. Supervisor approves. Slots are atomically re-assigned.
- **Schedule build (Manager).** Build or edit demand template → kick off a run → review coverage → publish. Workers are notified of their new schedule.
- **Timesheet export (Manager).** Pick date range + worker set → download CSV for payroll.
