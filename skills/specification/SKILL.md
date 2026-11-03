---
name: specification
description: Convierte progresivamente una necesidad — incluso una idea, un problema, un ticket breve o un requisito informal todavía ambiguo — en una especificación formal y, eventualmente, en un Execution Contract que sólo se declara EXECUTION_READY tras un readiness gate verificable. Normaliza la entrada, evalúa la ambigüedad, investiga los hechos verificables (technical-discovery), pregunta al humano sólo las decisiones materiales y registra las respuestas (clarification ledger), y pasa por definición del problema, especificación funcional (Hard Specification), casos de uso, comportamiento observable (Specification by Example), task breakdown, pruebas de aceptación, revisión de calidad y de coherencia y readiness gate C1–C4. Úsalo sólo cuando el usuario pida explícitamente convertir una necesidad/idea/requerimiento en una especificación formal, o invóquese explícitamente vía /skill:specification, o cuando delivery-lifecycle lo enrute en un lifecycle delegado por clasificación FORMAL. No es el modo normal de trabajo de ingeniería del workspace — no se activa para debugging, consultas técnicas, code review ordinario, fixes pequeños, investigación puntual, ejecución de una tarea ya refinada, inspección de tests, o troubleshooting.
---

# Specification Workflow

Este skill es un **router, controlador de workflow, recordatorio de autoridad, selector de entry point y gatekeeper**. No contiene el detalle de cada etapa — eso vive en `references/`, y se lee sólo lo que la etapa actual requiere (progressive disclosure).

## 0. Cuándo NO usar este skill

No lo actives para: debugging, consultas técnicas, code review ordinario, fixes pequeños, investigación puntual, ejecución de una tarea ya refinada, inspección de tests, troubleshooting, ni ninguna tarea de ingeniería ordinaria del workspace. No infieras silenciosamente que una tarea de ingeniería cualquiera requiere este workflow. Actívalo únicamente cuando el usuario pida —o cuando `delivery-lifecycle` lo enrute en un lifecycle delegado al clasificar el trabajo como `SPECIFICATION_NEED: FORMAL`— convertir una necesidad, idea, requerimiento o stakeholder input en una especificación formal, o mediante invocación explícita (`/skill:specification` cuando los skill commands estén habilitados).

La necesidad **no tiene que llegar refinada**: reducir su ambigüedad es trabajo de este skill (§4.1). Lo que no hace es investigar sin pregunta: los hechos que faltan se buscan con una pregunta concreta de discovery, nunca explorando por si acaso.

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE        (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE    (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → SPECIFICATION WORKFLOW  (este skill)
      → TASK CONTRACT          (el Execution Contract concreto que este workflow produce)
        → IMPLEMENTATION
```

Este skill no es una gobernanza independiente. No puede contradecir los invariantes de autoridad del workspace (`ENGINEERING_GOVERNANCE.md` §1, §2, §16) ni la gobernanza del repositorio en el que se esté trabajando. Ante conflicto entre este workflow y una gobernanza superior, prevalece la superior — repórtalo, no lo resuelvas en silencio.

La lectura de artefactos, código, contratos y evidencia necesaria para cerrar una etapa cae dentro del `OPERATIONAL_AUTONOMY_ENVELOPE` (`ENGINEERING_GOVERNANCE.md` §17, `RULES.md` regla 19): complétala **sin pedir aprobación repetida por cada operación de sólo lectura**. El envelope es observacional y no toca §6: el gate de ejecución sigue intacto y `EXECUTION_READY` sigue sin ser autorización (§17.5, §17.7).

La metodología de este skill fue adaptada de material de referencia interno no distribuido con este plugin; la autoridad de comportamiento del agente es siempre esta skill y la gobernanza del workspace, nunca ese material de origen.

## 2. Principio central — el workflow transforma información, no autoridad

```
EVIDENCE → ANALYSIS → PROPOSAL → HUMAN DECISION → SPECIFICATION → EXECUTION CONTRACT → HUMAN AUTHORIZATION → IMPLEMENTATION
```

Nunca:

- `PROPOSAL → DECISION` automático.
- `EXECUTION_READY → IMPLEMENTATION` automático.

Tres estados que nunca se usan como sinónimos (detalle en `skill://specification/references/07-execution-contract.md`):

```
SPEC_COMPLETE  !=  EXECUTION_READY  !=  AUTHORIZED_TO_EXECUTE
```

- `SPEC_COMPLETE`: las etapas aplicables terminaron y sus artefactos existen.
- `EXECUTION_READY`: la especificación pasó el readiness gate C1–C4 de la Etapa 07 (`READINESS_RESULT` con `execution_ready: YES`).
- `AUTHORIZED_TO_EXECUTE`: existe autoridad humana / task contract para iniciar la ejecución. Ver §6.

## 3. Modelo FACT/DECISION

Usa conceptualmente, en cualquier etapa: `FACT` · `INFERENCE` · `HYPOTHESIS` · `PROPOSAL` · `RECOMMENDATION` · `DECISION_REQUIRED` · `DECISION` · `INVARIANT`. Una inferencia suficientemente respaldada puede informar una propuesta; no se convierte automáticamente en decisión cuando la materia pertenece a autoridad humana (arquitectura, contratos externos, APIs, schemas, persistencia, lifecycle, seguridad, infraestructura, compatibilidad, semántica de negocio, alcance, aceptación consciente de deuda, cambios destructivos — ver `ENGINEERING_GOVERNANCE.md` §1.2). Silencio humano no es autorización.

Toda apertura que aparezca en cualquier etapa se clasifica **antes** de preguntar: `FACT` · `UNKNOWN` factual · `ASSUMPTION` · `AMBIGUITY` · `CONTRADICTION` · `DECISION_REQUIRED` (`skill://specification/references/ambiguity-assessment.md` §3). Un hecho verificable se investiga (`technical-discovery`); una ambigüedad material vuelve al humano (`skill://specification/references/clarification-loop.md`); una apertura no material sólo se cierra con una assumption registrada si cumple los ocho criterios de la política de assumptions (§4 de esa referencia, basada en `ENGINEERING_GOVERNANCE.md` §1.3).

```
DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US.
DO NOT LET THE SYSTEM DECIDE WHAT ONLY THE HUMAN MAY DECIDE.
```

Cuando una etapa deba detenerse, usa los formatos ya definidos por la gobernanza de workspace: `DECISION_REQUIRED` (§1.4) cuando falta una decisión humana; `STOP_REPORT` (§14.2) para cualquier otra causa de parada; `DECISION_CONTRADICTION` (§16) si una decisión ya cerrada contradice un hecho verificado. No inventes un formato nuevo.

## 4. Etapas, dependencias y gates

| Etapa | Nombre | Consume | Produce | Referencia |
|---|---|---|---|---|
| — | Intake + Ambiguity Assessment (transversal) | la necesidad tal como llega; cualquier artefacto en curso | normalización de intake, clasificación de aperturas, `ASM-NNN`, preguntas de discovery | `skill://specification/references/ambiguity-assessment.md` |
| — | Clarification Loop (transversal) | aperturas materiales | `CLAR-NNN` en `CLARIFICATION_LEDGER.md`, artefactos actualizados | `skill://specification/references/clarification-loop.md` |
| 01 | Stakeholder Discovery | input crudo del stakeholder | `01_STAKEHOLDER_DISCOVERY.md` | `skill://specification/references/01-stakeholder-discovery.md` |
| 02 | Problem Definition | 01 | `02_PROBLEM_DEFINITION.md` (+ madurez) | `skill://specification/references/02-problem-definition.md` |
| 03 | Hard Specification | 02 | `03_HARD_SPECIFICATION.md` | `skill://specification/references/03-hard-specification.md` |
| 04 | Use Case Definition | 03 | `04_USE_CASE_DEFINITION.md` | `skill://specification/references/04-use-case-definition.md` |
| 05 | Behavior Specification | 03 + 04 | `05_BEHAVIOR_SPECIFICATION.md` | `skill://specification/references/05-behavior-specification.md` |
| 06 | Task Breakdown | 03 + 04 + 05 | `06_TASK_BREAKDOWN.md` | `skill://specification/references/06-task-breakdown.md` |
| 08 | Acceptance Test Specification | 03 + 04 + 05 | `08_ACCEPTANCE_TEST_SPECIFICATION.md` | `skill://specification/references/08-acceptance-test-specification.md` |
| 07 | Execution Contract | 03 + 04 + 05 + 06 + 08 (cuando existan) + contexto técnico + decisiones humanas cerradas | `07_EXECUTION_CONTRACT.md` + `SPEC_QUALITY_RESULT` + `SPEC_COHERENCE_RESULT` + `READINESS_RESULT` → `EXECUTION_READY` o `NOT_EXECUTION_READY` | `skill://specification/references/07-execution-contract.md` |
| — | Specification Quality Review | artefactos activos | `SPEC_QUALITY_RESULT` (SQ1–SQ10) | `skill://specification/references/specification-quality.md` |
| — | Specification Coherence Review | artefactos activos + ledger + decisiones + gobernanza | `SPEC_COHERENCE_RESULT` (12 pasadas, `COH-NNN`) | `skill://specification/references/coherence-review.md` |
| 09 | Implementation Review | Execution Contract + implementación real + evidencia de validación | `09_IMPLEMENTATION_REVIEW.md` | `skill://specification/references/09-implementation-review.md` |
| 10 | Mutation Testing Analysis | 09 (o directamente 03/05/08) + tests + implementación | `10_MUTATION_TESTING_ANALYSIS.md` | `skill://specification/references/10-mutation-testing-analysis.md` |

**06 y 08 son sibling stages**: 08 puede ejecutarse en paralelo con 06 en cuanto sus inputs (03, 04, 05) estén maduros — 08 no depende de que exista Task Breakdown.

**07 (Execution Contract) es el gate formal de este pipeline antes de implementación**: genera el contrato (`SPEC_COMPLETE`), ejecuta la revisión de calidad y la de coherencia, y después el readiness gate C1–C4 — open material items, reference/coverage integrity, deferred promise closure, claim/artifact consistency. `QUALITY != COHERENCE != READINESS`: ninguna sustituye a otra. Generar el contrato no basta para `EXECUTION_READY` — ver §6. En trabajo `NONE`/`LIGHT` sin pipeline formal, el gate proporcional es el task contract ligero autorizado (`skill://delivery-lifecycle/SKILL.md` §4).

**09 y 10 son post-implementación.** 10 es un **quality gate opcional**, no obligatorio por defecto (ver §7).

Carga sólo la referencia de la etapa en curso. No cargues las diez si la tarea sólo requiere una. Las referencias transversales se cargan cuando aparece su objeto: `ambiguity-assessment.md` al recibir la necesidad o al encontrar una apertura, `clarification-loop.md` cuando hay que preguntar, `specification-quality.md` y `coherence-review.md` al revisar una etapa o en la Etapa 07.

### 4.1 Modelo de la Línea 1

```
LINE 1 REMOVES MATERIAL AMBIGUITY.
LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT.
```

```
RAW / PARTIALLY DEFINED NEED
  ↓
INTAKE NORMALIZATION                (PROBLEM ≠ PROPOSED_SOLUTION)
  ↓
AMBIGUITY ASSESSMENT
  ├─ factual unknown     → technical-discovery → FACT / UNKNOWN → vuelve aquí
  ├─ material ambiguity  → clarification → CLAR-NNN → respuesta aplicada
  └─ tactical ambiguity  → assumption registrada (ASM-NNN)
  ↓
[01 STAKEHOLDER DISCOVERY] → [02 PROBLEM] → 03 HARD SPEC (AC-NNN, provenance)
  ↓
[04 USE CASES] → [05 BEHAVIOR] → [06 TASKS] · [08 ACCEPTANCE TESTS]
  ↓
07 EXECUTION CONTRACT  =  SPEC_COMPLETE
  ↓
SPEC QUALITY (SQ1–SQ10) → SPEC COHERENCE (12 pasadas) → READINESS C1–C4
  ↓
EXECUTION_READY | NOT_EXECUTION_READY
  ↓
█ AUTORIZACIÓN HUMANA █  =  AUTHORIZED_TO_EXECUTE  →  LÍNEA 2
```

Los corchetes son etapas condicionales (§5). El assessment y la clarificación no son un paso único al principio: se repiten en cada etapa en cuanto la evidencia expone una apertura (§13).

## 5. Entry points

No es obligatorio comenzar en la etapa 01. Selecciona el entry point según la evidencia disponible — nunca por conveniencia ni porque una etapa "parezca innecesaria":

| Estado disponible | Entry point |
|---|---|
| Idea, necesidad, problema, ticket breve o requisito informal, todavía ambiguo | Intake + Ambiguity Assessment; después la etapa que corresponda según lo que haya (normalmente 02, o 01 si hay material de stakeholder que preservar) |
| Input crudo de stakeholder, sin estructurar | Etapa 01 (con su normalización de intake) |
| Discovery ya disponible y estructurado | Etapa 02 |
| Problem Definition ya aprobada (madurez Nivel 3-4, sin `DECISION_REQUIRED` abiertos que bloqueen) | Etapa 03 |
| Hard Specification aprobada | Etapa 04 y/o 05 |
| Especificación funcional completa (03+04+05) | Etapa 06 y/o 08 |
| Tarea ya refinada con especificación, casos de uso, comportamiento y aceptación disponibles | Etapa 07 |
| Implementación ya existente | Etapa 09 |
| Se requiere análisis de calidad de tests | Etapa 10 |

**Etapas condicionales consumidas aguas abajo.** Cuando una etapa condicional no se produce (p. ej. 04 en una necesidad con un único actor y una interacción evidente), las etapas que la consumen (05, 06, 08) trabajan con las fuentes que sí existen y declaran la ausencia en su "Derivado de" y en `INPUTS` del contrato 07. La ausencia de un artefacto no requerido no bloquea; inventarlo para completar la cadena, tampoco se hace.

**Proporcionalidad.** Si la entrada ya está suficientemente determinada, la normalización ocupa pocas líneas, el assessment marca las dimensiones como `CLEAR` y no se genera ninguna pregunta: no se ejecutan ceremonias vacías. El intake no obliga a pasar por 01 ni por 02.

Antes de usar un entry point posterior a la etapa 01, **verifica evidencia real de que las precondiciones están satisfechas** — no las asumas ni las inventes. Si falta una precondición, repórtalo exactamente (qué falta y de qué etapa/documento debería provenir) y no avances fingiendo que existe.

## 6. Gate de ejecución obligatorio (MANDATORY_EXECUTION_GATE)

La Etapa 07 sólo puede reportar `STATUS: EXECUTION_READY` cuando su `READINESS_RESULT` cumple la regla de readiness (`SPEC_QUALITY_RESULT` y `SPEC_COHERENCE_RESULT` sin bloqueos materiales, sin `CLAR-NNN` materiales abiertas, sin items abiertos materiales o ambiguos, sin promesas diferidas materiales sin resolver, sin claims contradichos, referencias declaradas válidas y sin `DECISION_REQUIRED` bloqueante). Si no la cumple, reporta `STATUS: NOT_EXECUTION_READY` con sus `blocking_reasons`; no hay transición por juicio de completitud.

Después de reportar `STATUS: EXECUTION_READY`:

**DETENTE.** No implementes. No modifiques código. No ejecutes migraciones. No modifiques tests. No hagas refactors. No continúes automáticamente a implementación.

Espera autorización humana explícita e inequívoca. `EXECUTION_READY` es el resultado del readiness gate, no una autorización. Sólo una instrucción humana posterior puede convertir `EXECUTION_READY` en `AUTHORIZED_TO_EXECUTE`.

## 7. Post-implementación

- **Etapa 09 (Implementation Review):** usable después de una implementación existente. No corrige automáticamente lo que encuentra — produce un veredicto (`APPROVED`, `APPROVED_WITH_OBSERVATIONS`, `CORRECTION_REQUIRED`, `BLOCKED`, `ARCHITECTURAL_REVIEW_REQUIRED`) y reporta.
- **Etapa 10 (Mutation Testing Analysis):** **opcional.** Actívala sólo cuando el usuario lo solicite, exista lógica crítica cuya protección lo justifique, el Execution Contract lo requiera explícitamente, o una decisión humana la active. No la exijas por defecto ni la trates como bloqueante universal. No modifica código ni tests.

## 8. Reglas de adaptación permanentes (aplican a todas las etapas)

1. **Executor-neutral:** ninguna etapa está acoplada a un ejecutor concreto. El Execution Contract puede ser consumido por OMP, Codex, otro agente implementador, o un desarrollador humano.
2. **READY ≠ AUTHORIZED**, en cualquier etapa que use ese vocabulario (`Preparada para Codex`, `EXECUTION_READY`, etc.) — readiness es un juicio sobre madurez, nunca una autorización.
3. **Recomendación del agente ≠ decisión humana**, siempre.
4. **Completitud de una etapa ≠ transición automática** cuando un gate requiere autoridad humana — la madurez es evidencia de readiness, no autorización para avanzar si existe un `DECISION_REQUIRED` abierto en materia de autoridad humana.
5. **Código/arquitectura existente es evidencia, no autoridad** — inspecciónalo y presérvalo deliberadamente donde sea autoritativo, pero no infieras que todo patrón existente es la arquitectura pretendida (`ENGINEERING_GOVERNANCE.md` §6.1).
6. **Ambigüedad se preserva y se reporta — nunca se resuelve en silencio.**
7. **Información crítica faltante → STOP_REPORT o DECISION_REQUIRED**, según corresponda, nunca inventarla.
8. **Criterios de aceptación con identidad estable (`AC-NNN`).** El registro vive en la Hard Specification (Etapa 03); las etapas 04, 05, 06, 07, 08 y 09 los referencian por ID — muchos-a-muchos con BR, UC, SC, TASK y AT, sin exigir 1:1. Un ID referenciado no se renumera ni se reutiliza. Así un AC es referenciable desde tareas, tests de aceptación y, en el futuro, desde la evidencia de implementación y las reviews.
9. **No preguntes al humano lo que el sistema puede decir.** Un hecho verificable en código, configuración, runtime o documentación accesibles se investiga con `technical-discovery` antes de preguntar.
10. **Pregunta el mínimo necesario, y sólo lo material.** Sin máximo fijo de preguntas; una a la vez cuando las respuestas dependen entre sí. Cada respuesta material queda en el ledger y se aplica a los artefactos, sustituyendo el texto que contradice.
11. **La clarificación pregunta qué y por qué, no cómo.** No se pregunta por tecnologías, patrones, estructura de código ni secuenciación si lo que falta es comportamiento; una tecnología ya decidida se registra como `CONSTRAINT` con su fuente (`clarification-loop.md` §5).
12. **Una decisión de negocio disfrazada de assumption bloquea.** Una assumption sólo es válida si cumple los ocho criterios de la política de assumptions.

## 9. Compatibilidad con specs existentes

El registro `AC-NNN` y el readiness gate C1–C4 aplican a specs FORMAL **nuevas o refinadas activamente** a partir del harness 0.3.0. Las specs históricas (p. ej. las existentes en `specs/`) se conservan como evidencia histórica: pueden tener AC sin ID y declaraciones de `EXECUTION_READY` anteriores al gate, y no se migran automáticamente. Si una spec histórica se refina para ejecutarse, se le aplica el contrato vigente (registro AC en 03 y `READINESS_RESULT` en 07) antes de declarar `EXECUTION_READY`.

Desde el harness 0.5.0, las revisiones de calidad y coherencia y el ledger de clarificaciones aplican del mismo modo: a specs nuevas o refinadas activamente. Una spec en curso creada antes de 0.5.0 no necesita reconstruir un ledger de clarificaciones pasadas; sí pasa por quality y coherence antes de declarar `EXECUTION_READY`, y el provenance se exige a los requisitos materiales que se añadan o cambien.

## 10. Dónde viven los artefactos de la tarea

Los documentos que produce cada etapa (`01_STAKEHOLDER_DISCOVERY.md`, ... `10_MUTATION_TESTING_ANALYSIS.md`), y `CLARIFICATION_LEDGER.md` cuando hay clarificaciones, son artefactos de la tarea en curso, no del skill. Este skill no asume ni impone su ubicación final en el repositorio de trabajo — confírmala con el usuario o con el Task Contract antes de escribir el primer artefacto. No los coloques dentro del directorio de este skill (reservado para el propio skill).

## 11. Trazabilidad y provenance

Cada referencia de etapa documenta su `SOURCE` (linaje interno de la metodología, no requerido en tiempo de ejecución) y su `ADAPTATION` (`OMP Specification Skill v0.1`), para permitir comparar la adaptación contra el original cuando sea necesario. Las referencias transversales añadidas en 0.5.0 declaran como `SOURCE` el harness y los mecanismos de Spec Kit que adaptan (§14.1).

**Provenance de requisitos.** Para todo elemento material debe poder responderse "¿de dónde salió esta regla?": las BR materiales llevan `SOURCE` y los AC materiales `DERIVED_FROM` (`skill://specification/references/03-hard-specification.md`). Las respuestas humanas se citan por su `CLAR-NNN`. La relación es muchos-a-muchos; no se exige una cadena `BR → UC → SC → AC → TASK → AT` cuando el dominio no la tiene, pero sí evidencia de origen y de cobertura suficiente para cada requisito material. C2 verifica que las referencias existen; la coherencia (pasada 12) verifica que respaldan lo que dicen.

**Frontera con la gestión de requisitos.** Esta skill es dueña del significado del requisito y de su provenance. El requisito **como trabajo del proyecto** — su estado, su origen como petición, sus cambios y el impacto de esos cambios, la trazabilidad objetivo → requisito — lo gestiona `project-management` (`skill://project-management/references/requirements-management.md`), que referencia los IDs y `AC-NNN` de esta skill sin copiarlos. Cuando una clarificación revela un cambio de alcance, fecha o prioridad del proyecto, se reporta como `PROJECT_DECISION_REQUIRED` en formato `DECISION_REQUIRED`, sin decidirlo aquí.

## 12. Estado de la especificación

No hay una máquina de estados persistente: el estado vive en los artefactos y en la sesión. Para reportarlo:

| Estado | Significa |
|---|---|
| `INTAKE` | Normalizando la entrada |
| `AMBIGUITY_ASSESSMENT` | Clasificando aperturas |
| `CLARIFICATION_REQUIRED` | Hay al menos una `CLAR-NNN` material `OPEN` sin preguntar o sin respuesta |
| `CLARIFYING` | Loop de clarificación en curso (pregunta hecha, respuesta pendiente de aplicar) |
| `SPECIFYING` | Produciendo o corrigiendo artefactos de etapa |
| `SPEC_COMPLETE` | Etapas aplicables terminadas y contrato 07 generado |
| `SPEC_QUALITY_REVIEW` | Revisión de calidad formal en curso |
| `SPEC_COHERENCE_REVIEW` | Revisión de coherencia formal en curso |
| `NOT_EXECUTION_READY` | El gate no se cumple; con `blocking_reasons` |
| `EXECUTION_READY` | El gate se cumple; se espera autorización humana (§6) |

Una necesidad puede volver de cualquier estado a `CLARIFICATION_REQUIRED` o `SPECIFYING` cuando aparece una apertura. Reglas de transición que se aplican siempre:

- Un intake y un assessment sin aperturas materiales terminan en `SPECIFYING`, aunque todavía no exista ningún artefacto de etapa.
- Aplicar una clarificación respondida devuelve a `SPECIFYING` (o a `CLARIFICATION_REQUIRED` si quedan materiales abiertas).
- Antes del gate formal, un `FAIL` de quality o un finding de coherencia que exige decisión lleva a `CLARIFICATION_REQUIRED`; si se corrige localmente sin decisión, a `SPECIFYING`, y después se repite la revisión.
- **Una vez ejecutado el gate de la Etapa 07, el estado es el que emite el gate**: `EXECUTION_READY` o `NOT_EXECUTION_READY`. Las clarificaciones y decisiones pendientes que lo bloquean van en sus `blocking_reasons` y `decisions_required`; el estado no vuelve a `CLARIFICATION_REQUIRED` hasta que se reanuda el trabajo con una respuesta.

Cuando se reporta:

```
SPECIFICATION_STATE
  need:            <necesidad, una línea>
  entry_point:     <etapa · por qué>
  state:           <estado>
  artifacts:       <artefactos existentes y ubicación>
  clarifications:  NONE | <CLAR-NNN · STATUS>
  assumptions:     NONE | <ASM-NNN>
  discovery:       NONE | <pregunta · resultado>
  next:            <siguiente paso>
```

Dentro de `delivery-lifecycle`, todos estos estados corresponden a `SPECIFICATION_REQUIRED`; `CLARIFICATION_REQUIRED` se refleja además en `decisions_required` del `LIFECYCLE_STATE`.

## 13. Detección temprana, gate formal al final

```
DETECT EARLY. REMEDIATE LOCALLY. GATE FORMALLY AT THE END.
```

Ambiguity assessment y clarificación se aplican en cada etapa en el momento en que la evidencia expone una apertura: intake, problem, hard spec, use cases, behavior, AC, tasks, acceptance tests y execution contract. Calidad y coherencia también pueden aplicarse a cada etapa sobre lo que produce (`specification-quality.md` §5, `coherence-review.md` §5); su revisión **formal** ocurre una vez, en la Etapa 07, antes de C1–C4. No es un waterfall: corregir un defecto en la etapa que lo produjo es más barato que descubrirlo en el gate.

## 14. Estado y evolución

`LINE_1_STATUS: USABLE` · `MATURITY: FIELD_VALIDATION` (harness 0.5.0). La metodología no se declara cerrada: se usa en trabajo real y cambia sólo por evidencia (`OBSERVED_FAILURE`, `OBSERVED_FRICTION` o `REPEATED_CAPABILITY_GAP`), nunca por idea sola. Una ocurrencia aislada es una `FIELD_OBSERVATION` (`MANUAL.md` §8, *Estado de la Línea 1 y política de evolución*).

## 14.1 Origen de los mecanismos

Los mecanismos añadidos en 0.5.0 toman como **referencia** el repositorio GitHub Spec Kit (un checkout local del repositorio GitHub Spec Kit, fuera del alcance de este plugin, `67e0f72`). No es una fuente de autoridad ni una dependencia operacional: el harness no lee ese repositorio en tiempo de ejecución, y si Spec Kit contradice la gobernanza Apep, prevalece Apep.

```
TAKE THE MECHANISMS. KEEP THE APEP MODEL.
```

| Adaptado de Spec Kit | Propio del harness |
|---|---|
| Taxonomía de cobertura `Clear / Partial / Missing` y heurística `Impact × Uncertainty` (`clarify`) | Separación `UNKNOWN` factual → discovery frente a decisión → humano |
| Pregunta interrogativa completa, una a la vez, "why it matters", `Recommended` / `Suggested` (`clarify`) | Formato de pregunta = `DECISION_REQUIRED` §1.4; sin máximo de preguntas |
| Registrar cada respuesta e integrarla sustituyendo el texto contradicho (`clarify`) | Ledger `CLAR-NNN` con clasificación, fuente, `AFFECTS` y `SUPERSEDED` |
| "Checklists are unit tests for English" (`checklist`, `specify`) | Checks SQ1–SQ10 con evidencia y materialidad, sin checkboxes autoevaluados |
| Análisis read-only entre artefactos con severidad (`analyze`) | Gobernanza y decisiones cerradas en lugar de constitution; `REFERENCE_INTEGRITY != SEMANTIC_COHERENCE`; nunca elegir una versión de una contradicción material |
| Separar WHAT/WHY de HOW, criterios de éxito medibles (`specify`) | Política de assumptions basada en `ENGINEERING_GOVERNANCE.md` §1.3; provenance; readiness C1–C4; `EXECUTION_READY != AUTHORIZED_TO_EXECUTE` |

No se adoptan: el pipeline fijo `specify → plan → tasks → implement`; los máximos de 3 marcadores o 5 preguntas; rellenar huecos con "informed guesses" o defaults de industria; una constitution paralela; los comandos `/speckit.*`, presets, hooks e instalación; ni la autoevaluación del modelo como evidencia suficiente.
