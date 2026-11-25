# UML Diagrams — ShiftDeck

These diagrams match Sections 6–10 of the Step 1–2 report (final, consistency-checked version). The report is the master copy: if a diagram changes, update the source here and the image in the report together.

| Kind | Report section | Image | Source |
|---|---|---|---|
| Use case diagram + descriptions (UC-01 … UC-23) | 6.1, 6.2 | [`img/use-cases.svg`](./img/use-cases.svg) | [`src/use_case_diagram.py`](./src/use_case_diagram.py), text in [`use-cases.md`](./use-cases.md) |
| Sequence diagram — clock in | 7.1 | [`img/sequence-clock-in.svg`](./img/sequence-clock-in.svg) | [`src/sequence_diagrams.py`](./src/sequence_diagrams.py) |
| Sequence diagram — clock out | 7.2 | [`img/sequence-clock-out.svg`](./img/sequence-clock-out.svg) | [`src/sequence_diagrams.py`](./src/sequence_diagrams.py) |
| Class diagram (entity, boundary, control) | 8.2 | [`img/class-diagram.svg`](./img/class-diagram.svg) | [`src/class-diagram.puml`](./src/class-diagram.puml) |
| Dialog map — clock kiosk | 10.1 | [`img/dialog-map-kiosk.svg`](./img/dialog-map-kiosk.svg) | [`src/dialog-map-kiosk.puml`](./src/dialog-map-kiosk.puml) |
| Dialog map — web application | 10.2 | [`img/dialog-map-web.svg`](./img/dialog-map-web.svg) | [`src/dialog-map-web.puml`](./src/dialog-map-web.puml) |

Each image is committed as SVG (sharp at any zoom) and PNG (for pasting into the report).

## Key design decisions the diagrams encode

- **One badge tap toggles clock-in / clock-out.** The kiosk calls a single `ClockController.handleBadgeTap(badgeID, stationID)`; the controller decides in or out from whether the worker has an open shift (FR-2.1.2). There is no "Already clocked in" or "Not clocked in" message.
- **In-screen actions are internal transitions.** In the web dialog map, actions that keep you on the same screen are listed inside the state (`event [guard] / action`). Log out and the 30-minute idle timeout leave the `Logged In` composite state from any screen.
- **Planned vs. actual shifts are associated, not inherited.** `Shift` *realizes* 0..1 `ScheduledShift`; `TimeSheet` and `LiveRoster` aggregate `Shift`s.

## Re-rendering

PlantUML diagrams (needs Java):

```bash
cd docs/uml/src
java -jar plantuml.jar -tsvg -o ../img class-diagram.puml dialog-map-kiosk.puml dialog-map-web.puml
```

Download `plantuml.jar` from <https://plantuml.com/download>.

Python diagrams (standard library only, write SVG):

```bash
cd docs/uml/src
python3 use_case_diagram.py ../img/use-cases.svg
python3 sequence_diagrams.py ../img
```

PNG copies: `rsvg-convert -w 1800 -o name.png name.svg` (librsvg), or export the SVG from any browser.
