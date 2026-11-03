---
description: CURRENT STATE MODE — reconstruye con evidencia cómo funciona algo hoy (technical-discovery)
argument-hint: <pregunta sobre un sistema, repositorio o flujo>
---

# /discover — CURRENT STATE MODE

Entrada:

$ARGUMENTS

Pregunta: *¿cómo funciona realmente esto hoy?* El owner de la investigación es el agent `technical-discovery`, que aplica `skill://technical-discovery`. Tú, **Main Session** y Control Tower, delimitas la pregunta (repositorio y escala, `technical-discovery` §4), aplicas el protocolo de entrada al repositorio que la gobernanza de este workspace defina, si existe (p. ej. en su `AGENTS.md`), delegas e integras el resultado. Una pregunta estrecha puede responderse aplicando la skill en esta sesión (`delivery-lifecycle` §4). Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Fronteras:

- Reconstruye `CURRENT_STATE`; no define `TARGET_STATE`. Discovery no es diseño: no implementa, no refactoriza y no decide arquitectura.
- Separa hecho, inferencia, desconocido y contradicción (`technical-discovery` §5 y §6); lo que no puede verificarse queda como desconocido, no se responde por suposición.

Termina con la salida canónica de su escala (`technical-discovery` §11). Puede recomendar `/spec`, `/design` o `/diagnose`; no los ejecuta.
