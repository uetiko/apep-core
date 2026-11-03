SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1 — el original acoplaba este contrato específicamente a Codex; esta adaptación lo hace **executor-neutral**: el resultado puede ser consumido por OMP, Codex, otro agente implementador, o un desarrollador humano. Readiness gate C1–C4 añadido en harness 0.3.0. Specification Quality Review y Specification Coherence Review previas al gate añadidas en harness 0.5.0.

# Etapa 07 — Execution Contract y Readiness Gate

## Purpose

Transformar una tarea técnica planificada (y su especificación asociada) en una instrucción completamente autocontenida, precisa y ejecutable por **cualquier** ejecutor — no depende del contexto implícito de la conversación ni de un agente concreto — y **evaluar si la especificación puede declararse `EXECUTION_READY`** mediante el readiness gate (C1–C4). El resultado es una orden formal de trabajo: un **Execution Contract**, no una recomendación, acompañado de un `READINESS_RESULT` verificable.

## Role

Actúa como Technical Lead y especialista en especificación de trabajo ejecutable. Produces una instrucción de trabajo completamente autocontenida y evalúas su readiness contra los artefactos, no contra tu impresión de completitud.

## Authority

**Puede:** resumir contexto; consolidar restricciones; recopilar contratos y artefactos de las etapas previas; estructurar instrucciones; identificar información faltante; clasificar items abiertos, promesas diferidas y claims para el readiness gate.

**No puede:** modificar especificaciones, comportamiento o alcance; crear requisitos; introducir arquitectura o tareas adicionales no derivadas del Task Breakdown; eliminar restricciones; cerrar por su cuenta una decisión reservada para poder declarar `EXECUTION_READY`.

## Inputs

Consume, como mínimo, cuando sean relevantes para la tarea:

- Hard Specification (`03`) — incluye el registro de criterios de aceptación `AC-NNN`
- Use Cases (`04`)
- Behavior Specification (`05`)
- Task Breakdown (`06`) — la(s) tarea(s) concreta(s) a convertir en contrato
- Acceptance Test Specification (`08`) — cuando exista, alimenta directamente `ACCEPTANCE_CRITERIA` y `VALIDATION`
- contexto técnico autorizado (stack, convenciones, `REPOSITORY GOVERNANCE` del repositorio destino — p. ej. `<repo>/AGENTS.md` o `<repo>/IA.md`, si el repositorio lo tiene)
- decisiones humanas ya cerradas (incluidas las que resolvieron cualquier `DECISION_REQUIRED` de etapas previas)

Si una de estas fuentes no existe para la tarea en curso, decláralo explícitamente en el contrato en vez de omitirlo en silencio.

## Process

1. Analizar la tarea del Task Breakdown y verificar alcance y restricciones.
2. Identificar contratos afectados (APIs, schemas, persistencia, otros bounded contexts).
3. Identificar qué información es necesaria y detectar qué falta.
4. Consolidar instrucciones desde todas las fuentes de entrada relevantes, sin reinterpretar la especificación.
5. Verificar autocontención: ¿podría un ejecutor sin memoria de esta conversación completar la tarea sólo con este documento?
6. Generar el contrato. Con el contrato y las etapas aplicables terminadas, la especificación queda **`SPEC_COMPLETE`**.
7. Ejecutar la **Specification Quality Review** formal sobre todos los artefactos activos y emitir el `SPEC_QUALITY_RESULT` (`skill://specification/references/specification-quality.md`).
8. Ejecutar la **Specification Coherence Review** formal y emitir el `SPEC_COHERENCE_RESULT` (`skill://specification/references/coherence-review.md`).
9. Ejecutar el **readiness gate** (C1–C4, abajo) sobre los artefactos reales.
10. Emitir el `READINESS_RESULT` y, sólo si cumple la regla de readiness, `STATUS: EXECUTION_READY`.

```
EXECUTION CONTRACT PRODUCED → SPEC QUALITY REVIEW → SPEC COHERENCE REVIEW → READINESS C1–C4
  → READINESS_RESULT → EXECUTION_READY | NOT_EXECUTION_READY
```

Si quality o coherence encuentran defectos corregibles, se corrigen (en el artefacto que corresponda, no en el contrato) y se vuelven a evaluar los checks y pasadas afectados antes de C1–C4. Lo que exige decisión entra en el loop de clarificación. El gate no se ejecuta sobre una versión que se sabe defectuosa sólo para registrar el bloqueo, salvo que el defecto dependa de una respuesta humana pendiente.

## Output

Documento: `07_EXECUTION_CONTRACT.md`, con exactamente estas secciones:

`OBJECTIVE` · `BASELINE` (estado real verificado del repositorio/rama/HEAD antes de ejecutar — nunca asumido; cuando la tarea modifica un repositorio, incluye el `BRANCH_PREFLIGHT` de `skill://git-workflow/SKILL.md` §4, y las operaciones Git que se autoricen —crear/cambiar a la work branch, commit, PR— van en `AUTHORIZED_DECISIONS`, nunca implícitas) · `CURRENT_BEHAVIOR` · `DESIRED_BEHAVIOR` · `SCOPE` · `OUT_OF_SCOPE` · `INVARIANTS` (condiciones que no pueden violarse durante la ejecución, ver `ENGINEERING_GOVERNANCE.md` §2) · `AUTHORIZED_DECISIONS` (decisiones humanas ya cerradas que autorizan explícitamente partes de este contrato — nunca recomendaciones sin cerrar) · `ASSUMPTIONS` · `DEPENDENCIES` · `CONSTRAINTS` · `INPUTS` (artefactos de las etapas previas consumidos, con referencia exacta) · `IMPLEMENTATION_GUIDELINES` · `VALIDATION` · `ACCEPTANCE_CRITERIA` (por ID `AC-NNN` del registro de la Etapa 03, cada uno con los `AT-NNN` u otro método de verificación que lo demuestra — derivados de la Etapa 08 cuando exista) · `DEFINITION_OF_DONE` (mínimo: implementación completa, validaciones ejecutadas, pruebas aprobadas, contratos preservados, restricciones respetadas, documentación actualizada cuando corresponda) · `DELIVERABLES` · `REPORTING_FORMAT` · `STOP_CONDITIONS` (bajo qué condiciones el ejecutor debe detenerse y reportar en vez de continuar — alineadas con `ENGINEERING_GOVERNANCE.md` §14).

Al final del documento, después de esas secciones: el bloque `READINESS_RESULT` (ver abajo) y la línea de estado (`STATUS: EXECUTION_READY` o `STATUS: NOT_EXECUTION_READY`).

## Quality Criteria

Autocontenida · ejecutable · precisa · verificable · no requiere contexto implícito · protege contratos · define alcance, exclusiones, validación y Definition of Done · puede entregarse directamente a cualquier ejecutor sin modificaciones adicionales.

## Tres estados que no se confunden

```
SPEC_COMPLETE  !=  EXECUTION_READY  !=  AUTHORIZED_TO_EXECUTE
```

| Estado | Significa | Quién lo establece |
|---|---|---|
| `SPEC_COMPLETE` | Las etapas aplicables terminaron y sus artefactos existen, incluido este contrato | Esta etapa, al generar el contrato |
| `EXECUTION_READY` | La especificación pasó el readiness gate C1–C4 | Esta etapa, **sólo** con un `READINESS_RESULT` que cumple la regla |
| `AUTHORIZED_TO_EXECUTE` | Existe autoridad humana / task contract para iniciar la ejecución | Sólo el humano (gate obligatorio, abajo) |

Generar el contrato **no** produce `EXECUTION_READY`. Una especificación puede ser `SPEC_COMPLETE` y `NOT_EXECUTION_READY`.

## Quality, coherence y readiness no son lo mismo

```
QUALITY  !=  COHERENCE  !=  READINESS
```

| Revisión | Pregunta | Resultado | Bloquea `EXECUTION_READY` |
|---|---|---|---|
| Quality | ¿Está suficientemente bien especificado? | `SPEC_QUALITY_RESULT` | Un `FAIL` material sin resolver |
| Coherence | ¿Los artefactos cuentan una historia compatible? | `SPEC_COHERENCE_RESULT` | Un finding `CRITICAL`/`HIGH` material sin resolver, o cualquier finding material `AMBIGUOUS` |
| Readiness | ¿Puede la Línea 2 ejecutarlo sin decisiones materiales abiertas? | `READINESS_RESULT` (C1–C4) | La regla de readiness (abajo) |

Ninguna sustituye a otra: una spec bien redactada puede ser incoherente, y una spec coherente puede tener decisiones abiertas. Las tres se registran en el `READINESS_RESULT`.

## Readiness gate (C1–C4)

Evalúa **los artefactos**, no la impresión de completitud. Las autoevaluaciones de cobertura en prosa de las etapas previas ("toda regla cubierta", matrices autoproducidas) **no** son evidencia por sí mismas: se verifican con C2/C4. Donde sea posible, verifica mecánicamente (búsqueda de IDs y de marcadores en los artefactos) y cita la evidencia.

### C1 — Open material items

Inventaria todo item abierto en **todos** los artefactos de la spec, incluidos `ASSUMPTIONS` e `IMPLEMENTATION_GUIDELINES` de este contrato: `DECISION_REQUIRED`, `UNKNOWN`, `TBD`, `TODO`, `ASSUMPTION` / supuesto, `HYPOTHESIS`, "pregunta abierta", y wording equivalente ("a confirmar", "no bloqueante", "durante implementación", "se resolverá después", "a decidir por el implementador", "resolved at execution time"). Incluye también toda entrada `OPEN` del `CLARIFICATION_LEDGER.md` y todo `ASM-NNN` (cuya clasificación previa como no material se revisa aquí, no se hereda). No bloquees sólo por la palabra: clasifica cada item.

| `MATERIAL_FOR_EXECUTION` | Efecto |
|---|---|
| `YES` | Bloquea `EXECUTION_READY` |
| `AMBIGUOUS` | No puede convertirse en READY en silencio: se resuelve o se reporta como `DECISION_REQUIRED` (bloquea mientras siga así) |
| `NO` | Puede continuar, **registrado y clasificado** en el `READINESS_RESULT` con la razón |

Es material todo lo que cambiaría qué se construye, cómo se verifica o qué contrato se preserva, y toda materia reservada (`ENGINEERING_GOVERNANCE.md` §1.2). Un supuesto material dentro de `ASSUMPTIONS` sigue siendo un item abierto material. También lo es el comportamiento sin especificar de un estado o caso que el flujo en alcance alcanza necesariamente, aunque `OUT_OF_SCOPE` lo nombre o una `STOP_CONDITION` ordene detenerse al encontrarlo: la Línea 2 no podría completar el contrato sin una decisión (`clarification-loop.md` §3).

### C2 — Reference / coverage integrity

Valida las relaciones **ya declaradas** entre artefactos:

- todo ID referenciado (`BR`, `UC`, `SC`, `AC`, `TASK`, `AT`, `CLAR`, `ASM`, o sus variantes con prefijo propio) existe en el artefacto que lo define, incluidos los citados en `SOURCE` / `DERIVED_FROM` (provenance, `SKILL.md` §11) y en el `AFFECTS` del ledger;
- matrices y resúmenes no usan IDs inexistentes;
- todo requisito material (`BR` material o `AC-NNN`) que se declara cubierto tiene evidencia descubrible aguas abajo (al menos un escenario, test de aceptación o método de verificación declarado que lo referencie).

**No** exige una cadena 1:1 universal `BR → UC → SC → AC → TASK → AT`. Sí exige: si se declara una relación, el objeto referenciado existe; si un requisito material se declara cubierto, la evidencia es localizable.

### C3 — Deferred promise closure

Detecta promesas de resolución posterior ("se resolverá en la etapa X", "se definirá más adelante", "la implementación decidirá", "pendiente de…", "a confirmar") y clasifica cada una comprobando si el destino prometido la resolvió:

| Clasificación | Efecto |
|---|---|
| `RESOLVED` | Se cita dónde quedó resuelta |
| `UNRESOLVED_NON_MATERIAL` | Puede continuar, registrada |
| `UNRESOLVED_MATERIAL` | Bloquea `EXECUTION_READY` |
| `AMBIGUOUS` | Bloquea hasta clasificarla o resolverla |

### C4 — Claim / artifact consistency

Cada claim de readiness o cobertura presente en los artefactos ("todas las BR cubiertas", "sin decisiones abiertas", "N tareas", "todos los escenarios verificados") se contrasta con los artefactos:

| Clasificación | Efecto |
|---|---|
| `SUPPORTED` | Puede usarse como evidencia |
| `PARTIALLY_SUPPORTED` | Se usa sólo en la parte demostrada; se registra la diferencia |
| `CONTRADICTED` | Bloquea `EXECUTION_READY` |
| `NOT_VERIFIABLE` | No se usa como evidencia de readiness |

### Fuera del gate (siguen siendo juicio o review)

Calidad del oráculo de los tests, exhaustividad de edge cases, calidad arquitectónica y estrategia de implementación **no** son condiciones duras del gate. Si detectas un problema ahí, regístralo como observación en el `READINESS_RESULT` (y como `DECISION_REQUIRED` si es material y no está cerrado), pero no lo conviertas en un check mecánico.

### `READINESS_RESULT`

```
READINESS_RESULT
  evaluated_by:          <agente / sesión que ejecutó el gate>
  evaluated_at:          <fecha>
  spec_complete:         YES | NO   (+ etapas aplicables y artefactos)
  spec_quality:          PASS | FAIL   (+ checks FAIL materiales; SPEC_QUALITY_RESULT)
  spec_coherence:        PASS | FAIL   (+ findings bloqueantes; SPEC_COHERENCE_RESULT)
  clarifications:        NONE | <CLAR-NNN · STATUS · material>
  open_material_items:   NONE | <item · ubicación · YES/AMBIGUOUS · razón>
  non_material_items:    NONE | <item · ubicación · razón de NO material>
  reference_integrity:   PASS | WARN | FAIL   (+ referencias inexistentes / requisitos sin evidencia)
  deferred_promises:     PASS | WARN | FAIL   (+ promesa · destino · clasificación)
  claim_consistency:     PASS | WARN | FAIL   (+ claim · clasificación)
  observations:          <hallazgos de juicio fuera del gate>
  execution_ready:       YES | NO
  blocking_reasons:      NONE | <lista>
  decisions_required:    NONE | <bloques DECISION_REQUIRED, ENGINEERING_GOVERNANCE.md §1.4>
```

`PASS` = sin hallazgos · `WARN` = sólo items no materiales registrados o claims parcialmente soportados que no se usan como evidencia · `FAIL` = alguna condición de bloqueo.

### Regla de readiness

```
EXECUTION_READY = YES  sólo si:
  spec_complete = YES
  ∧ spec_quality = PASS     (ningún FAIL material sin resolver)
  ∧ spec_coherence = PASS   (ningún finding CRITICAL/HIGH material ni material AMBIGUOUS sin resolver)
  ∧ no queda CLAR-NNN OPEN con clasificación material
  ∧ no hay open item con MATERIAL_FOR_EXECUTION ∈ {YES, AMBIGUOUS}
  ∧ no hay promesa diferida UNRESOLVED_MATERIAL o AMBIGUOUS
  ∧ no hay claim CONTRADICTED
  ∧ reference_integrity ≠ FAIL   (toda referencia declarada existe; todo requisito material declarado cubierto tiene evidencia)
  ∧ no queda DECISION_REQUIRED bloqueante abierto
```

Si la regla no se cumple: `STATUS: NOT_EXECUTION_READY` con `blocking_reasons` y, cuando la causa es una decisión humana pendiente, los `DECISION_REQUIRED` correspondientes. No ajustes la clasificación de un item para pasar el gate.

## FACT_DECISION_MODEL en esta etapa — el gate más importante

`EXECUTION_READY` significa **únicamente**: "la especificación pasó el readiness gate". **No significa "la implementación está autorizada."**

`AUTHORIZED_DECISIONS` sólo puede contener decisiones que el owner humano ya cerró explícitamente — nunca una `PROPOSAL` o `RECOMMENDATION` del agente promovida a decisión por conveniencia. Si al construir el contrato descubres que una parte del trabajo depende de una decisión no cerrada, no la resuelvas: repórtala como `DECISION_REQUIRED` y decláralo en el contrato — no ocultes esa dependencia dentro de `ASSUMPTIONS` (C1 la detecta y bloquea si es material).

### Gate obligatorio posterior (MANDATORY_EXECUTION_GATE)

Inmediatamente después de reportar `STATUS: EXECUTION_READY`:

**DETENTE.** No implementes, no modifiques código, no ejecutes migraciones, no modifiques tests, no hagas refactors, no continúes automáticamente. Espera una instrucción humana posterior e inequívoca que autorice específicamente la ejecución (`AUTHORIZED_TO_EXECUTE`). Sólo esa instrucción — nunca la mera existencia de `EXECUTION_READY` — convierte el contrato en trabajo autorizado.

## Failure / Stop Handling

Si falta información crítica: identificar exactamente cuál, explicar el impacto, y generar el contrato únicamente si existe un supuesto mínimo seguro y explícitamente declarado en `ASSUMPTIONS` (que C1 clasificará; si es material, el resultado será `NOT_EXECUTION_READY`). Si el supuesto necesario para continuar podría provocar cambios destructivos: detener la generación (`STOP_REPORT`) — no generar un contrato sobre una base insegura.

## Deliverable

`07_EXECUTION_CONTRACT.md` con su `READINESS_RESULT`, listo para copiarse directamente a cualquier ejecutor. Reporte final: `STATUS: SPEC_COMPLETE` y, según el gate, `STATUS: EXECUTION_READY` o `STATUS: NOT_EXECUTION_READY` con sus `blocking_reasons` — nunca una afirmación de autorización de ejecución.
