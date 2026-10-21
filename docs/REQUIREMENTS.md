# ShiftDeck — Software Requirements Specification

CIS 375 Software Engineering I, Fall 2026 — Project Step 1: Requirements Elicitation.

## Conventions

- Each requirement has a unique hierarchical ID: `FR-x.y` for a functional requirement and `FR-x.y.z` for its atomic detail; `NFR-x.y` for non-functional requirements; `IR-x.y` for interface requirements.
- **shall** states a functional capability. **must / must not** states a performance level or constraint. **will** states something the operating environment provides.
- Each functional requirement names who performs it, what the system does, the input, and the output.
- **Priority** follows the milestones in [`FEATURES.md`](./FEATURES.md): **MVP** (course deliverable, demonstrated end-to-end), **v1** (polish), **v2** (stretch).
- **Trace** links each requirement to its use case in [`uml/use-cases.md`](./uml/use-cases.md) (UC-xx) and its feature number in `FEATURES.md` (F x.y).
- **TBD** marks a value the team has not confirmed with the client. TBD values are not guessed.

---

## 1. Product Description

### 1.1 Purpose of the System

ShiftDeck is a web application for employee time-tracking and shift scheduling at small workplaces. Workers clock in and out with a badge at a kiosk, see their own schedule, claim open shifts, trade shifts with coworkers, and request time off. Supervisors approve swaps and time-off and watch who is on the floor in real time. Managers build the weekly schedule from a reusable demand template, review its coverage before publishing, and export timesheets for payroll. ShiftDeck replaces the paper card, spreadsheet and group chat that small shops use today.

### 1.2 Scope of the System

In scope: badge clock-in and clock-out, live roster, worker self-service scheduling (own schedule, open shifts, swaps, time-off, availability), manager schedule generation and publishing, timesheet viewing and CSV export, and role-based accounts.

Out of scope: payroll calculation, machinery and maintenance tracking (removed when the project was narrowed), native mobile apps, and single sign-on (v2 stretch).

### 1.3 Users and Stakeholders

| Stakeholder | Interest |
|---|---|
| Worker | Clocks in and out; manages their own schedule, swaps, time-off and availability. |
| Supervisor | Approves swaps and time-off; forces clock-outs; monitors the live roster. |
| Manager | Builds and publishes schedules; manages user accounts; exports timesheets. |
| Payroll staff | Receives timesheet CSV exports; reviews auto-closed shifts. Not a system user. |
| Course instructor | Client for the project; signs off on this specification. |

### 1.4 Assumptions and Constraints

- A1. Each worker has exactly one badge with a unique badge ID.
- A2. Each kiosk is installed at exactly one station and knows its station ID.
- A3. One organization uses one ShiftDeck installation. Multi-tenant use is out of scope.
- C1. The system must run as a browser application; no software installation is required on worker devices.
- C2. The system must use PostgreSQL 16 for persistent storage and Node.js 20 for the server (team technology decision).
- C3. The demo simulator must be disabled in production.

---

## 2. Functional Requirements

### FR-1 Accounts and Log In

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-1.1 | The system shall allow an Employee to log in by entering a username and password. | MVP | UC-01, F 5.1 |
| FR-1.1.1 | If the username and password match an active account, the system shall start a session and display the home screen for that account's role. | MVP | UC-01, F 5.1 |
| FR-1.1.2 | If the username or password does not match, the system shall display "Invalid username or password" and shall not start a session. | MVP | UC-01, F 5.1 |
| FR-1.2 | The system shall allow a logged-in Employee to log out. On log-out the system shall end the session and display the log-in screen. | MVP | UC-01, F 5.1 |
| FR-1.3 | The system shall assign each account exactly one role: Manager, Supervisor, or Worker. | MVP | UC-01, F 5.2 |
| FR-1.4 | The system shall deny any request for a function not permitted to the requester's role and shall display "Not authorized". | MVP | F 5.2 |
| FR-1.5 | The system shall allow a Manager to create an account by entering a username, initial password, and role. | MVP | UC-22, F 5.3 |
| FR-1.6 | The system shall allow a Manager to disable an account. A disabled account shall not be permitted to log in. | MVP | UC-22, F 5.3 |
| FR-1.7 | The system shall allow a Manager to link an account to a worker record. | MVP | UC-22, F 5.3 |
| FR-1.8 | The system shall allow a Manager to reset another account's password. | v1 | UC-22, F 5.4 |

### FR-2 Clock In and Clock Out

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-2.1 | The system shall allow a Worker to clock in by tapping a badge at a station kiosk. Input: badge ID and station ID. | MVP | UC-02, F 1.1 |
| FR-2.1.1 | If the badge ID does not match an active worker, the system shall display "Unknown badge" and shall not record a shift. | MVP | UC-04, F 1.1 |
| FR-2.1.2 | If the worker already has an open shift, the system shall display "Already clocked in" with that shift's station and shall not record a new shift. | MVP | UC-02, F 1.3 |
| FR-2.1.3 | On a valid clock-in, the system shall record an open shift containing the worker, the station, and the clock-in date and time. | MVP | UC-02, F 1.1 |
| FR-2.1.4 | On a valid clock-in, the system shall link the shift to the worker's scheduled shift at that station whose time window contains the clock-in time. | MVP | UC-02, F 1.5 |
| FR-2.1.5 | If no scheduled shift matches, the system shall record the shift as a walk-in. | MVP | UC-05, F 1.5 |
| FR-2.1.6 | On a valid clock-in, the kiosk shall display the worker's first name and, if the clock-in is later than the scheduled start, the number of minutes late. | MVP | UC-02, F 1.5 |
| FR-2.2 | The system shall allow a Worker to clock out by tapping their badge at a kiosk while they have an open shift. | MVP | UC-03, F 1.2 |
| FR-2.2.1 | On clock-out, the system shall record the clock-out date and time on the open shift. | MVP | UC-03, F 1.2 |
| FR-2.2.2 | On clock-out, the kiosk shall display the shift duration in hours and minutes. | MVP | UC-03, F 1.2 |
| FR-2.3 | The system shall allow a Supervisor to force a clock-out of a worker's open shift. Input: the shift and a reason. Output: the shift is closed with the current time and the reason. | MVP | UC-15, F 1.4 |
| FR-2.4 | The system shall flag a linked shift as late, early, or missed by comparing its clock-in and clock-out times with the scheduled shift. The tolerance in minutes is TBD. | MVP | UC-02, F 1.5 |
| FR-2.5 | Once per night, the system shall close every shift that has been open for more than 16 hours, set its clock-out to its clock-in plus 8 hours, and mark it "auto_closed" for payroll review. | v1 | F 1.6 |
| FR-2.6 | The system shall allow a Supervisor to reassign a worker with an open shift to another station. The system shall close the current shift and open a new shift at the new station with the same time. | v1 | F 1.7 |
| FR-2.7 | The system shall flag every closed shift whose duration exceeds 8 hours as overtime. | v1 | F 1.8 |

### FR-3 Worker Schedule Self-Service

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-3.1 | The system shall allow a Worker to view their own scheduled shifts for the next 14 days. Output: date, start time, end time, and station of each shift. | MVP | UC-06, F 2.1 |
| FR-3.2 | The system shall allow a Worker to view the list of open shifts. Output: date, start time, end time, and station of each open shift. | MVP | UC-07, F 2.2 |
| FR-3.3 | The system shall allow a Worker to claim an open shift. Output: the shift is assigned to that worker and removed from the open list. | MVP | UC-07, F 2.2 |
| FR-3.3.1 | The system shall reject a claim that overlaps another of the worker's scheduled shifts and shall display the conflicting shift. | MVP | UC-07, F 2.2 |
| FR-3.3.2 | The system shall reject a claim that would put the worker over their weekly hour cap and shall display the cap. | MVP | UC-07, F 3.2 |
| FR-3.4 | The system shall allow a Worker to submit a time-off request. Input: start date, end date, and reason. Output: a pending request visible to Supervisors. | v1 | UC-11, F 2.5 |
| FR-3.4.1 | The system shall reject a time-off request whose end date is before its start date. | v1 | UC-11, F 2.5 |
| FR-3.5 | The system shall allow a Supervisor to approve or deny a pending time-off request. Output: the request state is updated and the worker is notified. | v1 | UC-12, F 2.5 |
| FR-3.6 | The system shall allow a Worker to declare availability windows. Input: day of week, start time, end time, and preference (available, preferred, or unavailable). | MVP | UC-13, F 2.6, F 3.2 |
| FR-3.7 | The system shall allow a Worker to download their own scheduled shifts as an ICS calendar file. | v1 | UC-06, F 2.7 |

### FR-4 Shift Swaps

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-4.1 | The system shall allow a Worker (requester) to request a swap of one of their scheduled shifts for a coworker's (counterpart's) scheduled shift. Input: the offered shift and the wanted shift. | MVP | UC-08, F 2.3 |
| FR-4.1.1 | The system shall reject the request if the requester does not hold the offered shift or the counterpart does not hold the wanted shift. | MVP | UC-08, F 2.3 |
| FR-4.1.2 | The system shall reject the request if either shift belongs to a locked schedule run or has already started. | MVP | UC-08, F 2.3 |
| FR-4.1.3 | On a valid request, the system shall notify the counterpart. | MVP | UC-08, F 2.3 |
| FR-4.2 | The system shall allow the counterpart to accept or decline the request. | MVP | UC-09, F 2.3 |
| FR-4.2.1 | On decline, the system shall notify the requester and shall leave both shifts unchanged. | MVP | UC-09, F 2.3 |
| FR-4.2.2 | On accept, the system shall add the request to the Supervisor approval queue. | MVP | UC-09, F 2.3 |
| FR-4.3 | The system shall allow a Supervisor to approve or deny an accepted request. | MVP | UC-10, F 2.3 |
| FR-4.3.1 | The system shall deny the request if either worker would exceed their weekly hour cap after the swap. | MVP | UC-10, F 3.2 |
| FR-4.3.2 | On approval, the system shall reassign both shifts in a single operation and shall notify both workers. | MVP | UC-10, F 2.3 |
| FR-4.3.3 | On denial, the system shall notify both workers and shall leave both shifts unchanged. | MVP | UC-10, F 2.3 |
| FR-4.4 | The system shall allow the requester to cancel a request before approval, and the counterpart to cancel it after accepting and before approval. | MVP | UC-08, F 2.3 |
| FR-4.5 | If either shift is changed by the schedule after the request is opened, the system shall mark the request stale and notify both workers. | MVP | UC-08, F 2.3 |

### FR-5 Schedule Generation

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-5.1 | The system shall allow a Manager to create and edit a demand template. Input: template name, effective dates, and a list of demand slots. | MVP | UC-16, F 3.1 |
| FR-5.1.1 | Each demand slot shall state a station, a day of week, a start time, an end time, and a head-count of at least 1. | MVP | UC-16, F 3.1 |
| FR-5.1.2 | The system shall reject a demand slot whose end time is not after its start time. | MVP | UC-16, F 3.1 |
| FR-5.2 | The system shall allow a Manager to set a weekly hour cap for each worker. | MVP | UC-23, F 3.2 |
| FR-5.3 | The system shall allow a Manager to generate a draft schedule. Input: a demand template and a week start date. | MVP | UC-17, F 3.3 |
| FR-5.3.1 | If any worker has no availability or no hour cap, the system shall list the missing inputs and shall not generate the draft. | MVP | UC-17, F 3.3 |
| FR-5.3.2 | The generator shall not assign a worker to a shift that overlaps their approved time-off, falls in a window they marked unavailable, overlaps another of their shifts, or exceeds their weekly hour cap. | MVP | UC-17, F 3.3 |
| FR-5.3.3 | The system shall display the draft with its coverage percentage and the list of unfilled demand slots. | MVP | UC-17, F 3.3 |
| FR-5.4 | The system shall allow a Manager to reassign a shift in the draft by dragging it to another worker, and shall recompute coverage after each change. | MVP | UC-18, F 3.5 |
| FR-5.5 | The system shall allow a Manager to publish a draft. On publish, the system shall lock the schedule run and email every worker who has a shift in it. | MVP | UC-19, F 3.4 |
| FR-5.6 | Generating twice from identical inputs shall produce identical schedules. | v1 | UC-17, F 3.10 |
| FR-5.7 | The system shall display a coverage heat-map of the draft by station and hour, marking under-staffed hours. | v1 | UC-17, F 3.8 |

### FR-6 Roster and Reporting

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| FR-6.1 | The system shall display to Supervisors and Managers a live roster listing each worker currently clocked in, their station, and the time elapsed since clock-in. | MVP | UC-14, F 4.1 |
| FR-6.2 | The roster screen shall display the number of workers on the floor, the number of open shifts, and the number of missed clock-ins for the current day. | MVP | UC-14, F 4.2 |
| FR-6.3 | The system shall allow a Supervisor or Manager to view a worker's timesheet. Input: worker and date range. Output: each shift's date, station, clock-in, clock-out, duration, and flags. | MVP | UC-21, F 4.3 |
| FR-6.4 | The system shall allow a Manager to export timesheets as a CSV file. Input: date range and set of workers. Output: one row per shift with the same columns as FR-6.3. | MVP | UC-20, F 4.4 |
| FR-6.5 | The system shall display an attendance report listing late, early, missed, and walk-in shifts for a date range. | v1 | F 4.5 |

---

## 3. Non-Functional Requirements

| ID | Category | Requirement | Priority | Trace |
|---|---|---|---|---|
| NFR-1.1 | Usability | Every worker screen must be usable without horizontal scrolling on a display 360 pixels wide. | MVP | F 2.4 |
| NFR-1.2 | Usability | A worker must complete a clock-in in no more than one badge tap and no keyboard input. | MVP | F 1.1 |
| NFR-1.3 | Usability | 80% of first-time workers must find and claim an open shift within 2 minutes without help. (Target TBD with client.) | MVP | F 2.2 |
| NFR-2.1 | Performance | The kiosk must display the clock-in or clock-out confirmation within 2 seconds of the badge tap. (TBD with client.) | MVP | F 1.1 |
| NFR-2.2 | Performance | A clock-in or clock-out must appear on every open live-roster screen within 2 seconds, without a page reload. (TBD with client.) | MVP | F 4.1, F 6.1 |
| NFR-2.3 | Performance | Draft generation for 50 workers and one week must finish within 10 seconds. (TBD with client.) | MVP | F 3.3 |
| NFR-3.1 | Reliability | At no time must a worker have more than one open shift. | MVP | F 1.3 |
| NFR-3.2 | Reliability | A swap approval must either reassign both shifts or neither. | MVP | F 2.3 |
| NFR-3.3 | Reliability | A published schedule shift must not be edited in place; a change must create a new shift that supersedes the old one. | v1 | F 3.9 |
| NFR-4.1 | Security | Passwords must be stored only as salted one-way hashes. | MVP | F 5.1 |
| NFR-4.2 | Security | All browser–server traffic must be encrypted with TLS in production. | MVP | — |
| NFR-4.3 | Security | A session must expire after a period of inactivity (duration TBD). | MVP | F 5.1 |
| NFR-4.4 | Security | The database must not be reachable from the public internet. | MVP | — |
| NFR-5.1 | Supportability | The full development stack must start with a single `docker compose up` command. | MVP | F 7.1 |
| NFR-5.2 | Supportability | Every push to `main` must run lint and automated tests in CI. | MVP | F 7.3 |
| NFR-6.1 | Portability | The web client must run on the current releases of Chrome, Firefox, Safari, and Edge. | MVP | — |

---

## 4. Interface Requirements

### 4.1 User Interfaces

| ID | Screen | Users | Content |
|---|---|---|---|
| IR-1.1 | Clock Kiosk | Worker | Badge prompt; welcome, lateness, and error messages (FR-2.1, FR-2.2) |
| IR-1.2 | My Schedule | Worker | Next 14 days of the worker's shifts (FR-3.1) |
| IR-1.3 | Open Shifts | Worker | Open shift list with Claim action (FR-3.2, FR-3.3) |
| IR-1.4 | Swap Inbox | Worker | Outgoing and incoming swap requests with Accept / Decline / Cancel (FR-4) |
| IR-1.5 | Supervisor Queue | Supervisor | Pending swaps and time-off requests with Approve / Deny (FR-3.5, FR-4.3) |
| IR-1.6 | Schedule Builder | Manager | Demand template editor, draft preview, coverage, drag-to-reassign, Publish (FR-5) |
| IR-1.7 | Live Roster | Supervisor, Manager | On-floor list and daily counts (FR-6.1, FR-6.2) |
| IR-1.8 | Timesheets | Supervisor, Manager | Timesheet view and CSV export (FR-6.3, FR-6.4) |
| IR-1.9 | User Admin | Manager | Account list with create, disable, link, and reset actions (FR-1.5 – FR-1.8) |

### 4.2 Hardware Interfaces

- IR-2.1 Each kiosk will provide a badge reader that delivers the badge ID to the browser as keyboard input. The reader model is TBD.

### 4.3 Software Interfaces

- IR-3.1 The system shall send schedule notifications through an SMTP email service (provider TBD).
- IR-3.2 The timesheet export shall be a comma-separated file with a header row, readable by common spreadsheet software.
- IR-3.3 The ICS export shall follow RFC 5545 (v1).

---

## 5. Data Dictionary

| Term | Description | Attributes | Relationships |
|---|---|---|---|
| Employee | Any person with a ShiftDeck account. | username, role | Is a Worker, Supervisor, or Manager. |
| Worker | Employee who clocks in and works shifts. | first name, last name, badge ID, active, weekly hour cap | Has 0..* Shifts, Scheduled Shifts, Availability windows, Time-Off Requests. |
| Supervisor | Employee who approves swaps and time-off and forces clock-outs. | (account attributes) | Decides Swap Requests and Time-Off Requests. |
| Manager | Employee who builds schedules, manages accounts, and exports timesheets. | (account attributes) | Owns Demand Templates and Schedule Runs. |
| Badge | Physical card identifying one worker at a kiosk. | badge ID (unique) | Belongs to exactly one Worker. |
| Station | Physical work location where a kiosk is installed. | code (unique), name, zone | Hosts 0..* Shifts, Scheduled Shifts, Demand Slots. |
| Shift | What actually happened: one clock-in / clock-out pair. | clock-in, clock-out, close reason | Belongs to one Worker and one Station; realizes 0..1 Scheduled Shift. |
| Open shift (on the floor) | A Shift with no clock-out yet. | — | At most one per Worker. |
| Walk-in | A Shift that matches no Scheduled Shift. | — | Special case of Shift. |
| Scheduled Shift | A planned shift in a published or draft schedule. | start, end, state (scheduled, open, superseded, canceled, completed) | Belongs to one Schedule Run and one Station; assigned to 0..1 Worker. |
| Open Shift (schedule) | A Scheduled Shift with no worker assigned, available to claim. | — | Special case of Scheduled Shift. |
| Demand Template | Reusable statement of how many workers each station needs. | name, effective from, effective to | Composed of 1..* Demand Slots. |
| Demand Slot | One station's head-count need for a day-of-week and time window. | day of week, start time, end time, head-count | Part of one Demand Template; refers to one Station. |
| Availability | A worker's declared window for one day of the week. | day of week, start time, end time, preference | Belongs to one Worker. |
| Weekly Hour Cap | Maximum hours a worker may be scheduled in one week. | hours | Belongs to one Worker. |
| Time-Off Request | A worker's request to be unscheduled for a date range. | start date, end date, reason, state | Submitted by one Worker; decided by 0..1 Supervisor. |
| Schedule Run | One generation of a weekly schedule. | week start, inputs hash, state, coverage %, unfilled count | Generated from one Demand Template; produces 0..* Scheduled Shifts. |
| Coverage | Percentage of demand-slot head-count filled by a schedule run. | — | Property of a Schedule Run. |
| Swap Request | Proposal to trade two scheduled shifts between two workers. | state, created at, decided at | Refers to two Scheduled Shifts; involves a requester, a counterpart, and 0..1 approving Supervisor. |
| Live Roster | Real-time list of workers currently clocked in. | worker, station, elapsed time | Derived from open Shifts. |
| Timesheet | A worker's shifts over a date range. | per shift: date, station, clock-in, clock-out, duration, flags | Derived from Shifts. |

---

## Appendix A — Open Issues (TBD)

1. Lateness tolerance in minutes before a clock-in is flagged late (FR-2.4).
2. Session inactivity timeout (NFR-4.3).
3. Performance targets NFR-1.3, NFR-2.1 – NFR-2.3 are proposals awaiting client confirmation.
4. Badge reader model and interface (IR-2.1).
5. Email provider (IR-3.1).
6. Whether a Supervisor may also edit schedules, or only Managers.
7. Whether user administration (UC-22) belongs to Managers or a separate admin role.

## Appendix B — Inconsistencies Found in the Repository

Found while cross-referencing the README, `FEATURES.md`, and `docs/uml/`. The redrawn diagrams use the corrected form.

| Issue | Where | Resolution |
|---|---|---|
| A weekly hour cap is required (F 3.2, swap guard) but no table or column stores it. | `schema.md` | Added to the Worker data dictionary entry; the schema needs a column. |
| `shift_events` and `swap_events` audit tables are referenced but not in the schema. | `FEATURES.md` 1.9, old state diagrams | Audit is v1 (F 1.9); tables must be added before then. |
| Swap staleness referred to `generation_run_id`; the column is `schedule_run_id`. | old `state-swap-request.md` | Fixed. |
| Swap approval broadcast to room `tickets:schedule`; the room is `schedule`. | old `seq-swap-request.md` | Fixed. |
| Shift states OPEN / CLOSED / AUTO_CLOSED had no state column; only `close_reason`. | old `state-shift.md` | Auto-close recorded as `close_reason = "auto_closed"`. |
| Clock-in sequence allowed role `kiosk`, but only three roles exist. | old `seq-clock-in.md` | Kiosk authentication is TBD (Appendix A). |
| Schedule generator diagram showed a seniority-based optimizer pass; no seniority attribute exists, and the optimizer is v1 (F 3.6). | old `activity-scheduling.md` | Removed from the MVP flow. |
| Use cases for timesheet view (F 4.3), user admin (F 5.3), and hour caps (F 3.2) were missing. | old `use-cases.md` | Added UC-21, UC-22, UC-23. |
