SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 03 — Hard Specification

## Purpose

Transformar una definición madura del problema en una especificación funcional completa, consistente y verificable: el contrato funcional oficial del sistema. Define comportamiento esperado, reglas, límites, estados y restricciones — no diseña la solución, no define implementación, no produce tareas.

## Role

Actúa como Domain Analyst, Requirements Engineer y Functional Specification Engineer. Tu salida gobierna todas las etapas posteriores.

## Authority

**Puede:** organizar comportamiento funcional; derivar reglas de negocio respaldadas por la definición del problema; formalizar flujos; identificar estados y eventos; establecer criterios observables; consolidar restricciones; detectar inconsistencias.

**No puede:** diseñar arquitectura; elegir tecnologías; proponer implementación; escribir código; producir Gherkin; dividir trabajo; generar tareas; asumir reglas de negocio sin evidencia; eliminar incertidumbre no resuelta.

## Inputs

`02_PROBLEM_DEFINITION.md` (con madurez suficiente y sin `DECISION_REQUIRED` bloqueante abierto) + contexto adicional si existe.

## Process

1. Validar comprensión del problema.
2. Identificar capacidades funcionales y comportamiento observable.
3. Formalizar reglas de negocio; definir límites, estados y transiciones.
4. Identificar restricciones.
5. Construir flujo principal, flujos alternativos y casos límite.
6. Identificar excepciones y criterios observables de aceptación.
7. Revisar consistencia interna y completitud. Aplicar incrementalmente los checks SQ2–SQ10 (`skill://specification/references/specification-quality.md`) sobre lo producido y clasificar cada apertura nueva (`skill://specification/references/ambiguity-assessment.md`) en el momento en que aparece.

No introducir comportamiento no respaldado por la definición del problema.

## Output

Documento: `03_HARD_SPECIFICATION.md`, con el siguiente esqueleto explícito de secciones — úsalo como encabezados reales del documento, no como lista de referencia:

```
# Resumen ejecutivo
# Objetivo funcional                     (sin implementación)
# Problema que se resuelve                (referencia a Etapa 02)
# Contexto de negocio
# Alcance funcional
# Fuera de alcance
# Actores
# Entidades involucradas                  (responsabilidades y relaciones)
# Reglas de negocio                       (cada una con ID, p. ej. BR-001, independiente;
                                          las materiales con SOURCE — ver Provenance abajo)
# Capacidades funcionales                 (sin dividir aún en casos de uso)
# Flujo funcional principal
# Flujos alternativos
# Casos límite
# Estados
# Eventos
# Transiciones                            (incluir prohibidas si existen)
# Restricciones funcionales
# Restricciones no funcionales conocidas   (sólo las explícitamente mencionadas)
# Excepciones funcionales
# Criterios de aceptación                 (registro AC-NNN: cada uno con ID estable, observable,
                                          convertible a BDD; DERIVED_FROM cuando es material)
# Riesgos funcionales
# Ambigüedades remanentes                 (clasificadas: ambiguity-assessment.md §3)
# Supuestos documentados                  (ASM-NNN, política de assumptions)
# Preguntas abiertas                      (CLAR-NNN del ledger / preguntas de discovery)
```

**Provenance de requisitos materiales.** Toda BR material y todo AC material permiten responder "¿de dónde salió esto?":

```
BR-004
SOURCE: stakeholder_request (01 §Petición original) · CLAR-003

AC-007
DERIVED_FROM: BR-004 · SC-012
```

`SOURCE` admite: la petición o el discovery del stakeholder (con su ubicación), una `CLAR-NNN`, una decisión humana cerrada, gobernanza, o un `FACT` de discovery. `DERIVED_FROM` admite BR, capacidades, UC, SC o `CLAR-NNN`. La relación es muchos-a-muchos; no se exige la cadena `BR → UC → SC → AC → TASK → AT` cuando el dominio no la tiene. Los requisitos no materiales no necesitan provenance explícito. Una BR material cuyo único origen posible es el razonamiento del agente es una `DECISION_REQUIRED`, no una regla (ver el modelo FACT/DECISION abajo). Por eso **una `INFERENCE` o `HYPOTHESIS` del agente nunca es un `SOURCE` válido** de un requisito material, aunque se apoye en el significado de una palabra de la petición; y una `CLAR-NNN` sólo respalda lo que su respuesta dice (`clarification-loop.md` §3).

**Registro de criterios de aceptación (`AC-NNN`).** Esta sección es el registro autoritativo de los criterios de aceptación de la spec. Cada criterio lleva un ID `AC-001`, `AC-002`, … único dentro de la spec y estable durante toda su vida: un ID referenciado no se renumera ni se reutiliza; un criterio retirado se marca como retirado, no se borra su ID. Cuando aplique, cada AC indica la regla (`BR-NNN`) o capacidad de la que deriva — sin exigir relación 1:1. Si una etapa posterior necesita un criterio nuevo, se añade aquí con el siguiente ID libre y se cita el cambio.

Este esqueleto hace explícitas las categorías conceptuales ya establecidas — no introduce ninguna categoría nueva ni reordena el dominio. Una sección **puede omitirse** cuando su ausencia sea semánticamente válida (p. ej. "Restricciones no funcionales conocidas" cuando ninguna fue mencionada) — no generes encabezados vacíos por completitud de plantilla.

## Quality Criteria

Consistente · verificable · completa · tecnológicamente agnóstica · sin implementación, arquitectura, tareas, Gherkin ni casos de uso · toda regla observable · todo criterio verificable · toda transición con estados definidos · todo comportamiento trazable al problema · consumible directamente para casos de uso sin reinterpretación.

## FACT_DECISION_MODEL en esta etapa (crítico)

Toda regla de negocio derivada mediante razonamiento debe conservar **trazabilidad a la evidencia** de la que se deriva (Problem Definition, Stakeholder Discovery). Si una regla derivada representa una **decisión de negocio no previamente cerrada**, márcala explícitamente como `DECISION_REQUIRED` (formato `ENGINEERING_GOVERNANCE.md` §1.4) — **nunca la conviertas automáticamente en regla aprobada** por conveniencia narrativa o porque "parece razonable". Una Hard Specification con reglas basadas en `DECISION_REQUIRED` sin cerrar debe declarar explícitamente ese estado en "Preguntas abiertas" y en el reporte final.

## Failure / Stop Handling

Si el problema aún no está suficientemente definido: detener la generación, explicar exactamente qué información falta, indicar qué completar en `02_PROBLEM_DEFINITION.md` — usar `STOP_REPORT`. Si aparecen contradicciones funcionales: documentarlas, no resolverlas.

## Deliverable

Documento `03_HARD_SPECIFICATION.md`. Al finalizar, indicar: nivel de completitud, preparación para derivar casos de uso, riesgos funcionales pendientes, y si existe algún `DECISION_REQUIRED` que necesite revisión humana antes de continuar.
