# Traceability Matrix

Step 3 of the project (3.4.1) asks us to trace every requirement to its design, its code and its test cases. This table is filled in as we go: whoever implements or tests a requirement updates its row in the same pull request.

- **Use case / feature:** from the Trace column in [`REQUIREMENTS.md`](./REQUIREMENTS.md).
- **Design:** the control class from report Section 8.1, with methods from the class diagram where they already exist ([`uml/img/class-diagram.svg`](./uml/img/class-diagram.svg)).
- **Screen:** the boundary screen from Section 4.1 (`—` = runs without a screen, e.g. a nightly job).
- **Code / Tests:** file paths and test IDs, added during implementation.

| Req | Priority | Use case / feature | Design (control class / method) | Screen | Code | Tests |
|---|---|---|---|---|---|---|
| FR-1.1 | MVP | UC-01, F 5.1 | AuthController | IR-1.10 |  |  |
| FR-1.1.1 | MVP | UC-01, F 5.1 | AuthController | IR-1.10 |  |  |
| FR-1.1.2 | MVP | UC-01, F 5.1 | AuthController | IR-1.10 |  |  |
| FR-1.2 | MVP | UC-01, F 5.1 | AuthController | IR-1.10 |  |  |
| FR-1.3 | MVP | UC-01, F 5.2 | AuthController | — |  |  |
| FR-1.4 | MVP | F 5.2 | AuthController (role check middleware) | — |  |  |
| FR-1.5 | MVP | UC-22, F 5.3 | AccountController | IR-1.9 |  |  |
| FR-1.6 | MVP | UC-22, F 5.3 | AccountController | IR-1.9 |  |  |
| FR-1.7 | MVP | UC-22, F 5.3 | AccountController | IR-1.9 |  |  |
| FR-1.8 | v1 | UC-22, F 5.4 | AccountController | IR-1.9 |  |  |
| FR-2.1 | MVP | UC-02, F 1.1 | ClockController.handleBadgeTap() | IR-1.1 |  |  |
| FR-2.1.1 | MVP | UC-04, F 1.1 | ClockController.handleBadgeTap() → Worker.findActiveByBadge() | IR-1.1 |  |  |
| FR-2.1.2 | MVP | UC-02, UC-03, F 1.1, F 1.2, F 1.3 | ClockController.handleBadgeTap() → Shift.findOpenShift() | IR-1.1 |  |  |
| FR-2.1.3 | MVP | UC-02, F 1.1 | ClockController.clockIn() → new Shift(...) | IR-1.1 |  |  |
| FR-2.1.4 | MVP | UC-02, F 1.5 | ClockController.clockIn() → ScheduledShift.findMatching() | IR-1.1 |  |  |
| FR-2.1.5 | MVP | UC-05, F 1.5 | ClockController.clockIn() | IR-1.1 |  |  |
| FR-2.1.6 | MVP | UC-02, F 1.5 | ClockController.computeMinutesLate(), ClockKioskUI.showWelcome() | IR-1.1 |  |  |
| FR-2.2 | MVP | UC-03, F 1.2 | ClockController.handleBadgeTap() | IR-1.1 |  |  |
| FR-2.2.1 | MVP | UC-03, F 1.2 | ClockController.clockOut() → Shift.close() | IR-1.1 |  |  |
| FR-2.2.2 | MVP | UC-03, F 1.2 | ClockKioskUI.showClockOut() | IR-1.1 |  |  |
| FR-2.2.3 | — | — | *Removed (covered by FR-2.1.2)* | — | — | — |
| FR-2.3 | MVP | UC-15, F 1.4 | ClockController | IR-1.7 |  |  |
| FR-2.4 | MVP | UC-02, F 1.5 | Shift.setFlag(), ScheduledShift.getTimes() | — |  |  |
| FR-2.5 | v1 | F 1.6 | ClockController | — |  |  |
| FR-2.6 | v1 | F 1.7 | ClockController | IR-1.7 |  |  |
| FR-2.7 | v1 | F 1.8 | ClockController | — |  |  |
| FR-3.1 | MVP | UC-06, F 2.1 | ShiftClaimController | IR-1.2 |  |  |
| FR-3.2 | MVP | UC-07, F 2.2 | ShiftClaimController | IR-1.3 |  |  |
| FR-3.3 | MVP | UC-07, F 2.2 | ShiftClaimController | IR-1.3 |  |  |
| FR-3.3.1 | MVP | UC-07, F 2.2 | ShiftClaimController | IR-1.3 |  |  |
| FR-3.3.2 | MVP | UC-07, F 3.2 | ShiftClaimController | IR-1.3 |  |  |
| FR-3.4 | v1 | UC-11, F 2.5 | TimeOffController | IR-1.12 |  |  |
| FR-3.4.1 | v1 | UC-11, F 2.5 | TimeOffController | IR-1.12 |  |  |
| FR-3.5 | v1 | UC-12, F 2.5 | TimeOffController | IR-1.5 |  |  |
| FR-3.6 | MVP | UC-13, F 2.6, F 3.2 | AvailabilityController | IR-1.11 |  |  |
| FR-3.7 | v1 | UC-06, F 2.7 | ShiftClaimController | IR-1.2 |  |  |
| FR-4.1 | MVP | UC-08, F 2.3 | SwapController | IR-1.2, IR-1.4 |  |  |
| FR-4.1.1 | MVP | UC-08, F 2.3 | SwapController | IR-1.2, IR-1.4 |  |  |
| FR-4.1.2 | MVP | UC-08, F 2.3 | SwapController | IR-1.2, IR-1.4 |  |  |
| FR-4.1.3 | MVP | UC-08, F 2.3 | SwapController | IR-1.2, IR-1.4 |  |  |
| FR-4.2 | MVP | UC-09, F 2.3 | SwapController | IR-1.4 |  |  |
| FR-4.2.1 | MVP | UC-09, F 2.3 | SwapController | IR-1.4 |  |  |
| FR-4.2.2 | MVP | UC-09, F 2.3 | SwapController | IR-1.4 |  |  |
| FR-4.3 | MVP | UC-10, F 2.3 | SwapController | IR-1.5 |  |  |
| FR-4.3.1 | MVP | UC-10, F 3.2 | SwapController | IR-1.5 |  |  |
| FR-4.3.2 | MVP | UC-10, F 2.3 | SwapController | IR-1.5 |  |  |
| FR-4.3.3 | MVP | UC-10, F 2.3 | SwapController | IR-1.5 |  |  |
| FR-4.4 | MVP | UC-08, F 2.3 | SwapController | IR-1.4 |  |  |
| FR-4.5 | MVP | UC-08, F 2.3 | SwapController | IR-1.4 |  |  |
| FR-5.1 | MVP | UC-16, F 3.1 | ScheduleController | IR-1.6 |  |  |
| FR-5.1.1 | MVP | UC-16, F 3.1 | ScheduleController | IR-1.6 |  |  |
| FR-5.1.2 | MVP | UC-16, F 3.1 | ScheduleController | IR-1.6 |  |  |
| FR-5.2 | MVP | UC-23, F 3.2 | AccountController | IR-1.9 |  |  |
| FR-5.3 | MVP | UC-17, F 3.3 | ScheduleController | IR-1.6 |  |  |
| FR-5.3.1 | MVP | UC-17, F 3.3 | ScheduleController | IR-1.6 |  |  |
| FR-5.3.2 | MVP | UC-17, F 3.3 | ScheduleController | IR-1.6 |  |  |
| FR-5.3.3 | MVP | UC-17, F 3.3 | ScheduleController | IR-1.6 |  |  |
| FR-5.4 | MVP | UC-18, F 3.5 | ScheduleController | IR-1.6 |  |  |
| FR-5.5 | MVP | UC-19, F 3.4 | ScheduleController | IR-1.6 |  |  |
| FR-5.6 | v1 | UC-17, F 3.10 | ScheduleController | IR-1.6 |  |  |
| FR-5.7 | v1 | UC-17, F 3.8 | ScheduleController | IR-1.6 |  |  |
| FR-6.1 | MVP | UC-14, F 4.1 | RosterController | IR-1.7 |  |  |
| FR-6.2 | MVP | UC-14, F 4.2 | RosterController | IR-1.7 |  |  |
| FR-6.3 | MVP | UC-21, F 4.3 | TimesheetController | IR-1.8 |  |  |
| FR-6.4 | MVP | UC-20, F 4.4 | TimesheetController | IR-1.8 |  |  |
| FR-6.5 | v1 | F 4.5 | TimesheetController | IR-1.8 |  |  |

Non-functional requirements are traced in the test plan once it exists (performance and security checks rather than single classes).
