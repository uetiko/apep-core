# Project management report — cómo se comunica el modo proyecto

Referencia de presentación de `project-management` (`SKILL.md` §12). No añade método: toma la salida del modo proyecto y la presenta como un **informe de gestión**, no como un dashboard. Comparte con el reporte de work item las reglas de las tres vistas (`work-item-shaping-report.md` §1), la proporcionalidad (`work-item-shaping-report.md` §2) y la presentación de decisiones (`work-item-shaping-report.md` §3, *Decisiones necesarias*); aquí sólo va lo propio del proyecto.

```
THE METHOD DETERMINES WHAT IS TRUE.
THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED.
APPLY THE MANAGEMENT CONCERN, NOT NECESSARILY THE MANAGEMENT ARTIFACT.
```

Responde a la pregunta que se hizo. Un `/project` sobre "¿llegamos con la fecha?" no produce el informe completo: produce el estado ejecutivo, la planificación y las decisiones. No es reporting periódico ni compara contra un estado anterior que no esté disponible.

## 1. Estructura

```markdown
# <Proyecto o frente>

## Estado ejecutivo                       (siempre)
## Valor y resultados                     (si aplica)
## Alcance y requisitos                   (si aplica)
## Estado de la entrega                   (si aplica)
## Riesgos e issues                       (si aplica)
## Dependencias                           (si aplica)
## Planificación y forecast               (si aplica y hay evidencia)
## Calidad y readiness                    (si aplica)
## Decisiones necesarias                  (si hay decisiones humanas pendientes)
## Acciones recomendadas                  (si aplica)
## Anexo de evidencia                     (si aplica)
## Registro de proceso                    (siempre)
```

### Estado ejecutivo

El resumen de gestión del proyecto, con las mismas reglas que el resumen de un work item (`work-item-shaping-report.md` §3): estado general **verificable**, resultado o valor perseguido, cambio material desde el último estado *disponible* (si no hay uno, no se compara), principal riesgo y decisiones necesarias. Sin semáforos sin evidencia y sin `ON_TRACK` sin baseline, estado actual y evidencia (`planning-and-control.md` §7).

### Valor y resultados

Outputs, outcomes y, sólo si alguien los definió y hay evidencia, beneficio y valor (`project-governance.md` §3). Un beneficio no medido se dice así (`EVIDENCE_PENDING`, `OUT_OF_HORIZON`, `NOT_DEFINED`), no se da por obtenido.

### Alcance y requisitos

Dentro, fuera, estado de los requisitos, cambios y su análisis de impacto, decisiones pendientes (`requirements-management.md`). Los criterios de aceptación se referencian, no se copian ni se escriben.

### Estado de la entrega

Cuántos work items o requisitos están en cada estado **verificable** — listo, en curso, en revisión, entregado, desplegado, aceptado en operación — según la evidencia disponible (`software-project-management.md` §2, `SKILL.md` §10). **Nunca un porcentaje de avance inventado.** Si alguien reportó uno, se cita como lo que es — una afirmación sin estados verificables detrás —, no como estado.

### Riesgos e issues

Riesgo o issue, impacto, respuesta propuesta y quién decide si se conoce (`risk-and-issue-management.md`). Un riesgo materializado es un issue.

### Dependencias

Internas, externas, entre equipos, entre repositorios y de decisión (`dependency-model.md`).

### Planificación y forecast

Sólo con evidencia, y con las tres fechas separadas (`planning-and-control.md` §3): **deseada** (alguien la quiere), **forecast** (lo que la evidencia hace probable, con su confianza y sus supuestos) y **comprometida** (sólo si alguien con autoridad la comprometió). Si no hay base para un forecast, `NOT_AVAILABLE`.

### Calidad y readiness

Estados verificables que vienen de las capabilities responsables (reviews, readiness de la especificación, preparación operativa). Este informe los compone; no emite veredictos de calidad propios.

### Decisiones necesarias

Igual que en el work item: cada una es un `DECISION_REQUIRED` canónico presentado para gestión (`work-item-shaping-report.md` §3).

### Acciones recomendadas

Qué recomienda hacer la gestión, con su razón. Recomendaciones, no decisiones.

### Anexo de evidencia

Detalle técnico y fuentes, con hechos separados de inferencias.

### Registro de proceso

La salida canónica del modo proyecto (`SKILL.md` §12) — la forma acotada (`OBJECTIVE · CURRENT_STATE · DEPENDENCIES · RISKS · ISSUES · DECISIONS_REQUIRED · NEXT_ACTION`) para una pregunta acotada — con sus nombres y valores — `DEVIATION`, `CHANGE_IMPACT_ANALYSIS`, `PROJECT_GOVERNANCE_MODEL`, `CLOSURE_READINESS` y lo que aplique —, completa y sin reescribir.
