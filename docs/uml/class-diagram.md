# Domain Class Diagram

Backend domain model. Services expose use-case methods and lean on repositories for persistence; entities are plain data classes mapped to Postgres rows.

```mermaid
classDiagram
    class User {
        +UUID id
        +string username
        +string passwordHash
        +Role role
        +Date createdAt
        +verifyPassword(pw) bool
    }

    class Role {
        <<enumeration>>
        MANAGER
        SUPERVISOR
        WORKER
    }

    class Worker {
        +UUID id
        +string firstName
        +string lastName
        +string badgeId
        +UUID userId
        +boolean active
    }

    class Station {
        +UUID id
        +string code
        +string name
        +string zone
    }

    class Shift {
        +UUID id
        +UUID workerId
        +UUID stationId
        +UUID scheduledShiftId
        +Date clockIn
        +Date clockOut
        +string closeReason
        +durationMinutes() int
        +isOpen() bool
        +latenessMinutes() int
    }

    class DemandTemplate {
        +UUID id
        +string name
        +Date effectiveFrom
        +Date effectiveTo
    }

    class DemandSlot {
        +UUID id
        +UUID templateId
        +UUID stationId
        +int dow
        +time startsAt
        +time endsAt
        +int headCount
    }

    class Availability {
        +UUID id
        +UUID workerId
        +int dow
        +time startsAt
        +time endsAt
        +Preference preference
    }

    class TimeOffRequest {
        +UUID id
        +UUID workerId
        +Date startsOn
        +Date endsOn
        +string reason
        +RequestState state
    }

    class ScheduleRun {
        +UUID id
        +UUID templateId
        +Date weekStart
        +string inputsSha
        +RunState state
        +float coveragePct
        +int unfilledCount
    }

    class ScheduledShift {
        +UUID id
        +UUID scheduleRunId
        +UUID workerId
        +UUID stationId
        +Date startsAt
        +Date endsAt
        +ScheduledState state
        +UUID supersededBy
    }

    class SwapRequest {
        +UUID id
        +UUID fromSlotId
        +UUID toSlotId
        +UUID requestedBy
        +UUID counterpart
        +UUID approver
        +SwapState state
    }

    class ShiftService {
        +clockIn(badgeId, stationId) Shift
        +clockOut(shiftId) Shift
        +activeByStation(stationId) Shift[]
        +timesheet(workerId, from, to) Shift[]
    }

    class ScheduleService {
        +generate(templateId, weekStart) ScheduleRun
        +preview(runId) CoverageReport
        +publish(runId) void
        +claimOpenShift(slotId, workerId) ScheduledShift
    }

    class SwapService {
        +open(fromSlotId, toSlotId, by) SwapRequest
        +counterpartDecide(id, by, accept) SwapRequest
        +supervisorDecide(id, by, approve) SwapRequest
    }

    class RealtimeHub {
        +broadcast(room, event, payload) void
        +joinStation(sock, stationId) void
        +joinUser(sock, userId) void
    }

    User "1" --o "0..1" Worker
    Worker "1" --o "0..*" Shift
    Station "1" --o "0..*" Shift
    Station "1" --o "0..*" ScheduledShift
    Station "1" --o "0..*" DemandSlot
    DemandTemplate "1" --o "0..*" DemandSlot
    DemandTemplate "1" --o "0..*" ScheduleRun
    ScheduleRun "1" --o "0..*" ScheduledShift
    Worker "1" --o "0..*" ScheduledShift
    Worker "1" --o "0..*" Availability
    Worker "1" --o "0..*" TimeOffRequest
    ScheduledShift "1" --o "0..1" Shift : realized by
    ScheduledShift "1" --o "0..*" SwapRequest

    ShiftService ..> Shift
    ShiftService ..> RealtimeHub
    ScheduleService ..> ScheduleRun
    ScheduleService ..> ScheduledShift
    ScheduleService ..> RealtimeHub
    SwapService ..> SwapRequest
    SwapService ..> RealtimeHub
```

## Notes

- `Shift.scheduledShiftId` is nullable — walk-in / unscheduled clock-ins are allowed but flagged.
- Services are the only writers. Routes call services; services call repositories.
- `RealtimeHub` is injected into services so broadcasts and persistence stay in one transaction boundary.
