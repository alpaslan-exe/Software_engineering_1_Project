# UML Diagrams — ShiftDeck

The analysis diagrams (use case, class, analysis objects, sequence, state, activity) follow the UML notation used in the CIS 375 lecture slides. They are written in [PlantUML](https://plantuml.com/) under [`src/`](./src) and rendered to PNG under [`img/`](./img). The architecture, deployment and database diagrams are design-level views and stay in Mermaid, which renders inline on GitHub.

## Analysis (course notation)

| Kind | Diagram | File |
|---|---|---|
| Use case | Actors, use cases UC-01…UC-20, include / extend / generalization | [`use-cases.md`](./use-cases.md) |
| Class | Conceptual domain model with multiplicities | [`class-diagram.md`](./class-diagram.md) |
| Class | Boundary / control / entity analysis objects | [`analysis-objects.md`](./analysis-objects.md) |
| Sequence | Clock in (UC-02) | [`seq-clock-in.md`](./seq-clock-in.md) |
| Sequence | Shift swap (UC-08, UC-09, UC-10) | [`seq-swap-request.md`](./seq-swap-request.md) |
| State machine | Shift | [`state-shift.md`](./state-shift.md) |
| State machine | Swap request | [`state-swap-request.md`](./state-swap-request.md) |
| Activity | Work a shift | [`activity-shift.md`](./activity-shift.md) |
| Activity | Generate weekly schedule | [`activity-scheduling.md`](./activity-scheduling.md) |

## Design (Mermaid)

| Kind | Diagram | File |
|---|---|---|
| Structural | System architecture | [`architecture.md`](./architecture.md) |
| Structural | Deployment topology | [`deployment.md`](./deployment.md) |
| Structural | Database ER diagram | [`er-diagram.md`](./er-diagram.md) |
| Structural | Full schema (columns + constraints + indexes) | [`schema.md`](./schema.md) |

## Notation

- **Use case:** stick-figure actors outside the system boundary. `<<include>>` points from the base use case to the included one. `<<extend>>` points from the extension to the base use case.
- **Class:** name / attributes / operations compartments. Associations are labelled and carry multiplicity at both ends. A filled diamond marks composition.
- **Sequence:** lifelines are `:Class` or `name: Class` objects with boundary, control and entity icons. Messages are numbered. `alt` / `opt` / `loop` fragments carry `[guard]` conditions.
- **State machine:** rounded states with `entry / do / exit` behaviour. Transitions are labelled `event [guard] / action`.
- **Activity:** rounded actions, decision and merge diamonds with `[guard]` labels, fork / join bars, and a frame naming the activity.

## Re-rendering

Rendering needs Java and Graphviz (`brew install graphviz`).

```bash
cd docs/uml
java -jar plantuml.jar -tpng -o ../img src/*.puml
```

Download `plantuml.jar` from <https://plantuml.com/download>. The diagrams were rendered with PlantUML 1.2024.7.
