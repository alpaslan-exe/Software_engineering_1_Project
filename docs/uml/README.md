# UML Diagrams — ShiftDeck

| Kind | Diagram | File |
|---|---|---|
| Use case | Actors, use cases UC-01…UC-23, include / extend / generalization | [`use-cases.md`](./use-cases.md) |

The diagram follows the UML notation used in the CIS 375 lecture slides: stick-figure actors outside the system boundary, `<<include>>` pointing from the base use case to the included one, and `<<extend>>` pointing from the extension to the base use case.

It is written in [PlantUML](https://plantuml.com/) in [`src/use-cases.puml`](./src/use-cases.puml) and rendered to [`img/use-cases.png`](./img/use-cases.png).

## Re-rendering

Rendering needs Java and Graphviz (`brew install graphviz`).

```bash
cd docs/uml
java -jar plantuml.jar -tpng -o ../img src/use-cases.puml
```

Download `plantuml.jar` from <https://plantuml.com/download>. The diagram was rendered with PlantUML 1.2024.7.
