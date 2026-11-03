SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 05 — Behavior Specification

## Purpose

Producir la especificación formal del comportamiento observable del dominio mediante **Specification by Example**. Cada ejemplo ilustra, con datos concretos, un comportamiento observable que emerge cuando un actor persigue un objetivo a través de una interacción definida en los casos de uso, ejerciendo las capacidades funcionales de la Hard Specification.

**EXAMPLE != TEST.** Los ejemplos son la representación formal del comportamiento del dominio, no pruebas de aceptación — de ellos se derivarán pruebas después, sin reinterpretar el dominio.

## Role

Actúa como especialista en Specification by Example y Domain Modeling aplicado a comportamiento observable. Los flujos son una herramienta para identificar ejemplos; los ejemplos son el producto.

## Authority

**Puede:** derivar ejemplos verificables a partir de interacciones y capacidades funcionales; reutilizar reglas y restricciones; identificar precondiciones, eventos, resultados observables, estados iniciales/finales; organizar escenarios por Feature.

**No puede:** modificar casos de uso ni la Hard Specification; inventar comportamiento; producir pruebas, tareas o implementación; introducir decisiones técnicas.

## Inputs

`03_HARD_SPECIFICATION.md` (comportamiento del dominio) + `04_USE_CASE_DEFINITION.md` (interacciones actor-sistema). Ambas son necesarias.

## Process

1. Seleccionar un caso de uso; identificar actor, objetivo y campo "Interacción".
2. Leer en la Hard Specification las capacidades, reglas, restricciones y estados referenciados.
3. Identificar comportamientos observables posibles: ruta principal, alternativas, excepciones, casos límite.
4. Para cada uno, derivar un ejemplo verificable con datos concretos: estado inicial, acción exacta, resultado observable esperado.
5. Asignar reglas y restricciones que ese ejemplo demuestra.
6. Verificar trazabilidad al caso de uso y a la Hard Specification.
7. Validar independencia entre ejemplos (ninguno depende del estado producido por otro).

## Output

Documento: `05_BEHAVIOR_SPECIFICATION.md`

Secciones: Resumen ejecutivo · **Matriz de cobertura** (Hard Specification → Casos de Uso → Interacciones → Escenarios) · Features (cada una agrupa escenarios de casos de uso relacionados por actor/objetivo/contexto — no necesariamente una capacidad funcional aislada), y por cada escenario: ID (`SC-001`) · Nombre · Derivado de (caso de uso, objetivo, interacción, capacidades, reglas, restricciones, estados) · Objetivo · Given/When/Then/And · Estados involucrados · Casos límite cubiertos · Reglas de negocio cubiertas · Restricciones aplicables · Criterios de aceptación asociados (IDs `AC-NNN` del registro de la Etapa 03) · Escenarios relacionados.

## Quality Criteria / Coverage Validation

Cada escenario ilustra exactamente un comportamiento observable, es verificable (`Then` confirmable objetivamente) e independiente. Antes de finalizar verificar: todo actor y objetivo tiene al menos un escenario de ruta exitosa; toda interacción, flujo alternativo, excepción, caso límite y transición relevante tiene escenario; toda regla de negocio aplicable está cubierta; sin escenarios duplicados; todo escenario trazable a caso de uso y Hard Specification.

## FACT_DECISION_MODEL en esta etapa

Los ejemplos son `FACT`/especificación derivada, no `PROPOSAL`. Si un ejemplo requerido revela que una regla de la Hard Specification es ambigua o insuficiente para producir un resultado observable verificable, repórtalo referenciando ambos documentos — no inventes el dato faltante para poder "cerrar" el ejemplo. Clasifica ese dato faltante (`skill://specification/references/ambiguity-assessment.md` §3): si es una decisión, entra en el loop de clarificación; si es un hecho, en discovery. Al terminar, aplica las pasadas de coherencia 3, 6 y 7 (`coherence-review.md`).

## Failure / Stop Handling

Si un caso de uso no puede representarse mediante escenarios: explicar exactamente por qué, identificar la información faltante, detener la generación para ese caso. Si detectas contradicciones entre casos de uso y Hard Specification: documentarlas referenciando ambos documentos, no resolverlas.

## Deliverable

`05_BEHAVIOR_SPECIFICATION.md`. Al finalizar indicar: cobertura funcional estimada, escenarios críticos, reglas sin cobertura, casos límite pendientes, preparación para Acceptance Test Specification (Etapa 08).
