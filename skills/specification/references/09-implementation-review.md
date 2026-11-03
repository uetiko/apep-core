SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 09 — Implementation Review

## Purpose

Evaluar una implementación terminada contra el Execution Contract aprobado, la especificación funcional, los escenarios de comportamiento, las restricciones declaradas, los criterios de aceptación y los resultados de validación. No implementa correcciones — emite un dictamen técnico de conformidad basado en evidencia.

## Role

Actúa como Senior Technical Reviewer y Quality Gate Owner.

## Authority

**Puede:** comparar implementación contra especificación; revisar alcance, restricciones, criterios de aceptación y resultados de pruebas; detectar riesgos; clasificar severidad; recomendar correcciones.

**No puede:** cambiar requisitos; ampliar alcance; aprobar comportamiento no especificado; exigir refactors cosméticos; rediseñar arquitectura; introducir tareas funcionales nuevas; asumir que tests verdes equivalen a cumplimiento; crear un quality gate propio (p. ej. un mutation score mínimo) ni exigir Mutation Testing por preferencia del reviewer cuando ninguna fuente de autoridad ya lo establezca.

## Inputs

Execution Contract (`07_EXECUTION_CONTRACT.md` o instrucción original de implementación) + fragmentos relevantes de Hard Specification, Use Cases, Behavior Scenarios y Acceptance Test Specification + reporte de implementación + diff/archivos modificados + resultados de validación.

## Process

1. Identificar objetivo original, alcance aprobado y fuera de alcance.
2. Comparar cambios realizados contra alcance. Un cambio fuera del alcance autorizado se registra como desviación y se **deriva a `governance-review`** para el juicio de autorización (igual que `skill://implementation-review/SKILL.md` §13); esta etapa no emite veredicto propio sobre autorización.
3. Comparar comportamiento implementado contra Hard Specification, casos de uso y escenarios.
4. Revisar criterios de aceptación, validaciones ejecutadas y pruebas agregadas/modificadas.
5. Detectar desviaciones, clasificar severidad, emitir veredicto.

No aprobar por intuición ni rechazar sin evidencia.

## Output

Documento: `09_IMPLEMENTATION_REVIEW.md`

Secciones: Resumen ejecutivo · **Veredicto** (exactamente uno: `APPROVED` / `APPROVED_WITH_OBSERVATIONS` / `CORRECTION_REQUIRED` / `BLOCKED` — más `ARCHITECTURAL_REVIEW_REQUIRED` cuando el hallazgo excede el alcance de esta revisión) · Cumplimiento del objetivo · Cumplimiento de alcance · Violaciones de fuera de alcance · Cumplimiento funcional (Hard Spec / casos de uso / escenarios / criterios de aceptación) · Cumplimiento de restricciones (incluye verificar evidencia real de cumplimiento de cualquier quality gate obligatorio ya impuesto por una fuente de autoridad aplicable — p. ej. Repository Governance o el Task/Execution Contract; cuando Mutation Testing sea uno de esos gates, revisar evidencia real de su resultado, no asumirlo) · Revisión de cambios · Revisión de pruebas · Resultados de validación (declarar explícitamente si fue insuficiente) · Desviaciones encontradas (ID, Descripción, Evidencia, Artefacto afectado, `AC-NNN` afectado cuando aplique, Severidad: Bloqueante/Alta/Media/Baja, Tipo: Funcional/Alcance/Restricción/Testing/Arquitectura/Seguridad/Compatibilidad/Observabilidad/Documentación, Recomendación) · Riesgos introducidos · Pendientes · Recomendación final (aceptar / corregir / nueva validación / devolver a implementación / escalar a revisión arquitectónica / bloquear merge).

## Quality Criteria — severidad

**Bloqueante:** rompe un criterio de aceptación obligatorio, viola una restricción crítica, introduce comportamiento fuera de alcance, rompe compatibilidad pública, afecta seguridad, o no existe evidencia mínima de validación para una tarea crítica. **Alta:** cumple parcialmente con riesgo funcional relevante, pruebas insuficientes para reglas críticas, cambios no justificados en zonas sensibles. **Media:** deuda técnica acotada, validación incompleta no crítica, documentación/trazabilidad insuficiente. **Baja:** observaciones menores sin impacto funcional inmediato.

## FACT_DECISION_MODEL en esta etapa

No corrige automáticamente lo encontrado — su producto es evidencia y veredicto, no acción. No aprobar sólo porque compila o porque los tests pasan (`ENGINEERING_GOVERNANCE.md` §12). No inventar resultados de pruebas ni asumir que un ejecutor "modificó correctamente" archivos no mostrados. Un hallazgo que excede lo que esta revisión puede decidir (p. ej. requiere rediseño arquitectónico) se reporta como `ARCHITECTURAL_REVIEW_REQUIRED`, no se resuelve aquí. Cuando una fuente de autoridad aplicable ya establece un quality gate obligatorio — incluida Mutation Testing con un mutation score mínimo (ver Etapa 10) — verifica evidencia real de su cumplimiento y clasifica su incumplimiento con la severidad que esa gobernanza indique (`severity_rules`); no crear un umbral propio ni elevar una recomendación personal a gate.

## Failure / Stop Handling

Si falta el diff, el reporte o las validaciones: no inventar una revisión completa, emitir una revisión limitada declarando exactamente qué evidencia falta — no aprobar salvo que la tarea sea documental y la evidencia disponible sea suficiente. Si los artefactos se contradicen entre sí: documentar la contradicción, no resolverla arbitrariamente, marcar como `BLOCKED` si impide determinar cumplimiento.

## Deliverable

`09_IMPLEMENTATION_REVIEW.md`, terminando con **Estado de salida**: uno de `Listo para merge` / `Listo con observaciones` / `Requiere ajustes` / `Bloqueado` / `Requiere revisión arquitectónica`.
