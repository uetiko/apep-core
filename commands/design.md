---
description: DESIGN VALIDATION MODE — valida si un diseño o cambio respeta las fronteras y contratos del sistema (architecture-review)
argument-hint: <diseño, decisión, cambio planificado o Execution Contract>
---

# /design — DESIGN VALIDATION MODE

Entrada:

$ARGUMENTS

Pregunta: *¿este diseño o cambio respeta las fronteras y contratos del sistema?* El owner es el agent `architecture-review`, que aplica `skill://architecture-review` a un diseño propuesto, una decisión, un cambio planificado, un Execution Contract o un cambio que toca fronteras. Tú, **Main Session** y Control Tower, delimitas qué se valida, delegas e integras. Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Fronteras:

- Evalúa y no decide: una decisión arquitectónica material es `DECISION_REQUIRED` para el humano (`architecture-review` §9). Una recomendación no es una decisión.
- No inventa la semántica de los requisitos (es de `specification`), no implementa y no diseña la arquitectura de reemplazo (`architecture-review` §11).

Termina con los estados de `architecture-review` §9 y sus findings (§10).
