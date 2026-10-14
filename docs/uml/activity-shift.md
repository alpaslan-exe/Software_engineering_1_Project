# Activity Diagram — Shift Lifecycle

Worker-side view of a day on the floor. Starts at badge-in, ends either at a clean clock-out or at the nightly reaper closing a forgotten shift.

```mermaid
flowchart TD
    Start([Worker arrives]) --> Tap[Tap badge at kiosk]
    Tap --> Lookup{Badge valid?}
    Lookup -- no --> Deny[Deny + buzz] --> EndA([End])
    Lookup -- yes --> Open{Already clocked in?}
    Open -- yes --> Err[Show "already on shift"<br/>+ station] --> EndB([End])
    Open -- no --> StationQ{Station assigned<br/>for this shift?}
    StationQ -- no --> Assign[Supervisor assigns<br/>station]
    StationQ -- yes --> Insert
    Assign --> Insert[Insert shifts row<br/>state=OPEN]
    Insert --> Broadcast[Broadcast roster:changed<br/>on floor:global]
    Broadcast --> Work[Worker on station]
    Work --> Event{Event?}
    Event -- break --> Break[Pause: no row change]
    Break --> Work
    Event -- station move --> Move[Supervisor closes current<br/>shift + opens new one]
    Move --> Work
    Event -- end of day --> Out[Tap badge → clock-out]
    Out --> Close[UPDATE shifts<br/>SET clock_out = now]
    Close --> BroadcastOut[Broadcast roster:changed]
    BroadcastOut --> EndC([End])
    Event -- forgot --> Timeout[16 h passes]
    Timeout --> AutoClose[Nightly reaper sets<br/>state=AUTO_CLOSED]
    AutoClose --> AuditFlag[Flag for payroll review]
    AuditFlag --> EndD([End])
```
