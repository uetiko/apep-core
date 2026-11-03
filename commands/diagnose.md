---
description: FAILURE ANALYSIS MODE — determina con evidencia por qué falla algo observado (diagnostics)
argument-hint: <síntoma observado: qué, dónde, cuándo>
---

# /diagnose — FAILURE ANALYSIS MODE

Entrada:

$ARGUMENTS

Pregunta: *¿por qué está fallando?* El owner del análisis es el agent `diagnostics`, que aplica `skill://diagnostics` con su propio rol de modelo. Tú, **Main Session** y Control Tower, delimitas el síntoma y la evidencia disponible, delegas e integras. Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Requiere un **fallo observado** — síntoma, comportamiento anómalo o evidencia de incidente (`diagnostics` §0). Si no lo hay, no es un diagnóstico: recomienda `/discover` para entender cómo funciona, o `/shape`.

Fronteras:

- No diseña features ni hace refactors: busca la causa.
- Recomienda la remediation dentro de su `FIX_BOUNDARY` (`diagnostics` §9) sin aplicarla y sin cambiar la semántica del producto.
- Preserva la evidencia antes de cualquier mutación (`diagnostics` §10).

Termina con su contrato de salida (`diagnostics` §15): `ROOT_CAUSE_CONFIRMED`, `ROOT_CAUSE_HIGH_CONFIDENCE` o `INSUFFICIENT_EVIDENCE`. Puede recomendar `/design`, `/spec` o `/deliver`; no los ejecuta.
