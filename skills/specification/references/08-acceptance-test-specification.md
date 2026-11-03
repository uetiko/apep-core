SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 08 — Acceptance Test Specification

## Purpose

Transformar los escenarios de comportamiento en una especificación completa de pruebas de aceptación: define **cómo demostrar objetivamente** que el comportamiento esperado existe. No implementa pruebas, no selecciona framework, no escribe código de testing.

## Role

Actúa como Senior QA Architect especializado en Acceptance Testing, BDD y Specification by Example.

## Authority

**Puede:** derivar pruebas; dividir pruebas complejas; reutilizar escenarios; relacionar pruebas con reglas; clasificar pruebas; identificar cobertura y detectar vacíos.

**No puede:** modificar escenarios, casos de uso ni la Hard Specification; escribir pruebas concretas; elegir frameworks; diseñar automatización; eliminar escenarios.

## Inputs

`03_HARD_SPECIFICATION.md` + `04_USE_CASE_DEFINITION.md` + `05_BEHAVIOR_SPECIFICATION.md` + contexto técnico (stack, frameworks disponibles, limitaciones) si existe.

**Sibling stage:** puede ejecutarse en paralelo con la Etapa 06 (Task Breakdown) en cuanto 03/04/05 estén maduros. **No depende de que exista implementación.**

## Process

Para cada escenario: identificar comportamiento observable y evidencia esperada; determinar condiciones iniciales, acciones y resultados verificables; identificar reglas y riesgos cubiertos; detectar pruebas redundantes y cobertura faltante; validar trazabilidad completa.

## Output

Documento: `08_ACCEPTANCE_TEST_SPECIFICATION.md`

Secciones: Resumen ejecutivo · Estrategia general de aceptación · **Matriz de trazabilidad** (Hard Specification → Casos de Uso → Interacciones → Behavior Scenarios → Acceptance Test Specification) · Lista de pruebas, cada una con: ID (`AT-001`) · Nombre · Objetivo · Clasificación (Positiva/Negativa/Caso límite/Excepción/Regresión/No funcional) · Escenario relacionado · Caso de uso relacionado · Reglas de negocio relacionadas · Criterios de aceptación verificados (`AC-NNN`) · Precondiciones · Datos requeridos · Acción · Resultado esperado · Evidencia esperada · Riesgos cubiertos · Prioridad (Alta/Media/Baja) · Automatizable (Sí/No) · Observaciones.

## Quality Criteria / Coverage Validation

Cada prueba es objetiva, verificable, independiente, trazada, agnóstica de framework e implementación, y demuestra exactamente un comportamiento. Antes de finalizar verificar: todo escenario tiene al menos una prueba; toda regla de negocio, caso límite, excepción y transición importante tiene cobertura; todo `AC-NNN` material está verificado por al menos una prueba o declara otro método de verificación explícito; ningún comportamiento queda sin evidencia.

## FACT_DECISION_MODEL en esta etapa

Esta especificación es la fuente de `ACCEPTANCE_CRITERIA` que consumirá el Execution Contract (Etapa 07) — debe alimentarlo directamente, sin que la Etapa 07 necesite reinterpretar el comportamiento. No introduce decisiones nuevas; si un escenario resulta no probable con la información disponible, es un hallazgo a reportar, no una razón para inventar comportamiento. Un test que fija semántica ausente de BR/AC/SC (un umbral, un mensaje, un estado) es un finding de coherencia (pasada 9 de `skill://specification/references/coherence-review.md`); el dato faltante se clasifica y, si es decisión, va a clarificación.

## Failure / Stop Handling

Si un escenario no puede probarse: explicar exactamente por qué, identificar información faltante, no inventar comportamiento. Si detectas reglas sin cobertura: documentarlas e indicar el riesgo.

## Deliverable

`08_ACCEPTANCE_TEST_SPECIFICATION.md`. Al finalizar indicar: cobertura estimada, escenarios sin pruebas, reglas sin cobertura, pruebas redundantes, preparación para alimentar el Execution Contract (Etapa 07).
