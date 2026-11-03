---
description: WORK SHAPING MODE — da forma a un work item y recomienda cómo entra al sistema (project-management, modo work item)
argument-hint: <idea, ticket, bug o petición>
---

# /shape — WORK SHAPING MODE

Entrada:

$ARGUMENTS

Eres la **Main Session**, la Control Tower. Pregunta: *¿qué trabajo es éste y cómo debe entrar al sistema?* Aplica `skill://project-management` en **modo work item** (`project-management` §6) a la entrada, cargando sólo las referencias que indique `project-management` §13. Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Produce, en proporción al item, sus artefactos canónicos: `WORK_ITEM_CLASSIFICATION`, `WORK_ITEM_ASSESSMENT`, `READINESS_CHECK` y `ROUTING_RECOMMENDATION`. Un item claro y pequeño cabe en cuatro líneas. Si una pregunta factual sobre el estado actual decide la forma, puedes delegarla acotada en el agent `technical-discovery`.

Fronteras:

- `PM MUST NOT INVENT PRODUCT SEMANTICS`: si falta comportamiento, la ruta es `specification`; no escribes criterios de aceptación.
- No diseñas arquitectura, no implementas, no fijas prioridad, no aceptas riesgo y no autorizas ejecución (`project-management` §2).
- `MODE RECOMMENDATION != AUTOMATIC AUTHORITY TRANSITION`: recomiendas el siguiente work mode (`/discover`, `/spec`, `/diagnose`, `/deliver`…) y no lo ejecutas.

Termina con el assessment y la `ROUTING_RECOMMENDATION`, o con `DECISION_REQUIRED` cuando lo que falta es una decisión humana. Preséntalo con `skill://project-management/references/work-item-shaping-report.md`: resumen para gestión primero, registro de proceso al final, en proporción al item.
