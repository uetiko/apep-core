---
name: delivery-lifecycle
description: Máquina de estados y reglas de routing para llevar un work item de principio a fin (clasificar → readiness → discovery/specification si hacen falta → branch preflight → implementation → verificación → reviews que aporten → commit/PR preparados → INTEGRATION_READY) decidiendo qué capability toca en cada fase, sin que el humano dirija fase por fase. La ejecuta el agent delivery-orchestrator o la Main Session (/skill:delivery-lifecycle). Orquesta, no absorbe — no sustituye a project-management, git-workflow, specification, implementation ni a las reviews, y no decide materias reservadas, merge, tag ni release.
---

# Delivery Lifecycle

Metodología de coordinación. Decide **qué capability toca y cuándo**; el trabajo de cada fase lo hace la capability correspondiente.

```
ORCHESTRATE, DO NOT ABSORB.
AUTONOMY != AUTHORITY.
THE ORCHESTRATOR DECIDES WHICH CAPABILITY. IT NEVER DECIDES A RESERVED MATTER.
```

Desde que hay contrato autorizado, este lifecycle es la **Línea 2 — Delivery Factory**: la contraparte de la Línea 1 de `specification`.

```
LINE 1 REMOVES MATERIAL AMBIGUITY.
LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT.
IMPLEMENTATION MAY CHOOSE HOW. IMPLEMENTATION MAY NOT CHANGE WHAT.
```

## 0. Quién la ejecuta

| Ejecutor | Cuándo | Diferencia |
|---|---|---|
| agent `delivery-orchestrator` | Lifecycle delegado completo | Corre headless: no puede preguntar en vivo; se detiene, entrega `LIFECYCLE_STATE` y se reanuda cuando la Main Session le envía la decisión (`hub`). Requiere `tools.approval.task: allow` para delegar |
| Main Session (`/skill:delivery-lifecycle`) | Lifecycle interactivo | Puede preguntar en vivo y es la única que puede ejecutar operaciones con gate (commit, push…) tras tu autorización |

La Main Session sigue siendo la Control Tower por defecto. Este skill no la reemplaza.

## 1. Entrada

Work item u objetivo · contexto disponible · decisiones humanas ya cerradas · restricciones explícitas. **No exige Execution Contract**: conducir hasta tenerlo, cuando haga falta, es parte del lifecycle.

## 2. Estados

| Estado | Significa |
|---|---|
| `RECEIVED` | Work item recibido |
| `CLASSIFIED` | Clasificación hecha (§3) |
| `READY` | DoR suficiente **para la siguiente capability** (`project-management`, `READINESS_CHECK` direccional). No implica listo para implementar |
| `DISCOVERY_REQUIRED` | Falta `CURRENT_STATE` material |
| `SPECIFICATION_REQUIRED` | Falta especificación / contrato proporcional. En `FORMAL` sólo se sale con `EXECUTION_READY` de `specification` (`READINESS_RESULT` con `execution_ready: YES`); `NOT_EXECUTION_READY` → `AWAITING_AUTHORIZATION` (decisiones o clarificaciones pendientes) o `BLOCKED`. Los estados internos de la Línea 1 (`INTAKE`, `CLARIFICATION_REQUIRED`, `SPEC_QUALITY_REVIEW`…, `specification` §12) viven dentro de este estado |
| `BRANCH_READY` | `BRANCH_PREFLIGHT` en `MATCH`, o rama autorizada |
| `EXECUTION_PREFLIGHT` | Autorización de ejecución recibida; se fijan `AUTHORIZED_EXECUTION_SNAPSHOT`, `EXECUTION_BASELINE` y espacio de ejecución antes de la primera escritura (`skill://delivery-lifecycle/references/execution-preflight.md`). Sólo con `EXECUTION_PREFLIGHT_RESULT: PASS` se pasa a `IMPLEMENTING`; `AUTHORIZATION_STALE` → `AWAITING_AUTHORIZATION` |
| `AWAITING_AUTHORIZATION` | Gate humano pendiente que el humano resuelve decidiendo o autorizando: `DECISION_REQUIRED`, rama, ejecución, operación con gate (worktree, commit, PR), `AUTHORIZATION_STALE` |
| `IMPLEMENTING` | `implementation` trabajando |
| `VERIFYING` | Evidencia de verificación en revisión |
| `REVIEWING` | Reviews aplicables en curso, incluida la convergencia por AC en `FORMAL` |
| `REMEDIATION_REQUIRED` | Finding o AC fuera de `PASS` clasificado `FIX_ALREADY_AUTHORIZED` (§5) |
| `COMMIT_READY` | `COMMIT_MESSAGE` preparado |
| `PR_READY` | `PR_TITLE` + `PR_BODY` preparados |
| `INTEGRATION_READY` | Fin normal del lifecycle automático: `DELIVERY_EVIDENCE` con `integration_ready: YES` (§6). No es `COMPLETE` ni autoriza commit, push, PR ni merge |
| `BLOCKED` | No se puede continuar sin evidencia nueva o sin resolver una contradicción: `STOP_REPORT` / `DECISION_CONTRADICTION` / `REMEDIATION_EXHAUSTED`. Una decisión humana pendiente es `AWAITING_AUTHORIZATION` |
| `COMPLETE` | Lo declara el humano, nunca el orchestrator, después de `INTEGRATION_READY`. Distinto de `RESULT: COMPLETE` en el reporte de un worker (trabajo del contrato terminado con evidencia) |

Las transiciones son condicionales: un item recorre sólo los estados que su clasificación exige.

```
RECEIVED → CLASSIFIED → READY ─┬─ [CURRENT_STATE insuficiente] → DISCOVERY_REQUIRED ─┐
                               ├─ [spec LIGHT/FORMAL]           → SPECIFICATION_REQUIRED ┤
                               └────────────────────────────────────────────────────────┴→ BRANCH_READY
BRANCH_READY → [¿autorización de ejecución?] → EXECUTION_PREFLIGHT → [PASS] → IMPLEMENTING → VERIFYING → REVIEWING
EXECUTION_PREFLIGHT → [BLOCKED · DECISION_REQUIRED · AUTHORIZATION_STALE] → AWAITING_AUTHORIZATION | BLOCKED
REVIEWING ─┬─ [FIX_ALREADY_AUTHORIZED] → REMEDIATION_REQUIRED → IMPLEMENTING (una vez) → VERIFYING → REVIEWING (focalizado)
           ├─ [DECISION_REQUIRED] → AWAITING_AUTHORIZATION
           ├─ [REMEDIATION_EXHAUSTED · DECISION_CONTRADICTION] → BLOCKED
           └─ [DELIVERY_EVIDENCE con integration_ready: YES] → COMMIT_READY → PR_READY → INTEGRATION_READY
cualquier estado → AWAITING_AUTHORIZATION | BLOCKED
```

## 3. Clasificación

La clasificación **la produce `project-management`** (modo work item, `skill://project-management/references/work-item-shaping.md`); este lifecycle la consume y no mantiene otra paralela. En un micro cambio cabe en una línea.

| Eje | Valores | Fuente |
|---|---|---|
| `WORK_ITEM_CLASSIFICATION` | `FEATURE` · `BUG` · `TECHNICAL_CHANGE` · `REFACTOR` · `INVESTIGATION` · `INCIDENT` · `INFRASTRUCTURE` · `SECURITY` · `DOCUMENTATION` · `PROCESS` · `UNKNOWN` | PM, por intención y evidencia |
| `RISK` | `WORK_RISK_PROFILE` (cualitativo) | PM |
| `SCOPE` | `targeted` · `flow` · `system` · `multi-repo` | PM (`BLAST_RADIUS`, dependencias `CROSS_REPOSITORY`) |
| `KNOWN_STATE` | `sufficient` · `insufficient` | Este lifecycle |
| `SPECIFICATION_NEED` | `NONE` · `LIGHT` · `FORMAL` | PM (`WORK_FORMALITY`) |

El tipo de rama (`feature/`, `fix/`, `bugfix/`, `hotfix/`) no es esta clasificación: lo decide `git-workflow` §4 con la gobernanza del repositorio. No se inventa información faltante: si un eje no es determinable, se marca y se pregunta sólo si bloquea la siguiente decisión. `INVESTIGATION` termina en un reporte, no en implementation. Un **fallo observado** (`BUG` con causa desconocida, `INCIDENT`) no entra en este lifecycle: va a `diagnostics` (§10).

## 4. Routing

### project-management
Usar (modo work item: clasificación, `WORK_ITEM_ASSESSMENT`, `READINESS_CHECK` direccional, `ROUTING_RECOMMENDATION`) cuando la forma del trabajo, su siguiente capability o su readiness no son evidentes, hay dependencias o bloqueos, el item es grande o mezcla intenciones, el scope es ambiguo, hay WIP relevante (máx. 2 activas por persona) o riesgo material. En un micro cambio cabe en dos líneas. PM **recomienda** el routing; este lifecycle decide y ejecuta la transición. Kanban sigue siendo el sistema.

### technical-discovery
Sólo con `KNOWN_STATE: insufficient` y cuando la falta es **material** para decidir o implementar. `DISCOVERY != REQUIRED PHASE`. Volumen o frontera read-only → agent `technical-discovery`; pregunta estrecha → aplicar la skill en el propio contexto.

### specification
| `SPECIFICATION_NEED` | Cuándo | Qué se produce |
|---|---|---|
| `NONE` | Micro cambio local, reversible y verificable, sin comportamiento nuevo (definiciones en `skill://project-management/references/work-item-shaping.md` §4) | Task contract ligero: objetivo, scope, AC, rama |
| `LIGHT` | Comportamiento nuevo acotado, varios AC | Task contract con invariantes y AC explícitos |
| `FORMAL` | Decisiones materiales, contratos, APIs, persistencia, schema, infraestructura, seguridad, compatibilidad, coste de reversión alto | Pipeline de `specification` desde la necesidad tal como llega (intake y ambiguity assessment) hasta Execution Contract, revisión de calidad y de coherencia y readiness gate C1–C4 (`SPEC_COMPLETE` → `SPEC_QUALITY_RESULT` → `SPEC_COHERENCE_RESULT` → `READINESS_RESULT` → `EXECUTION_READY`). El estado `READY` de este lifecycle (DoR) no es `EXECUTION_READY` |

`EXECUTION_READY != AUTHORIZED`. No formalizar por formalizar.

Una necesidad `FORMAL` todavía ambigua **no** tiene que refinarse antes de entrar en `specification`: reducir su ambigüedad es trabajo de la Línea 1. Dentro de ella, un hecho que falta va a `technical-discovery` con una pregunta concreta (esto no reabre `DISCOVERY_REQUIRED` del lifecycle salvo que el `CURRENT_STATE` completo sea insuficiente), y una decisión material vuelve al humano como `CLAR-NNN` en formato `DECISION_REQUIRED`.

### git-workflow
Antes de cualquier escritura productiva: lee `.omp/skills/git-workflow/SKILL.md` §2–§4 y produce su `BRANCH_PREFLIGHT` — repo, rama actual, tipo, base, destino; `dev` es la rama de integración. El nombre propuesto sigue literalmente `<tipo>/<ID>/<titulo-kebab>` (p. ej. `fix/US-999/rechazar-release-candidate`), con `/` entre tipo, ID y título. Nunca implementar porque "ya estamos en una rama". Si hay que crear o cambiar de rama y no está autorizado → `AWAITING_AUTHORIZATION` con `CURRENT_BRANCH`, `EXPECTED_BRANCH`, `PROPOSED_COMMAND`. No se escribe hasta resolverlo.

### implementation
Con autorización suficiente (contrato aprobado o encargo explícito del humano) y `EXECUTION_PREFLIGHT_RESULT: PASS` (`skill://delivery-lifecycle/references/execution-preflight.md` §2), delegar al agent `implementation` con un contrato autocontenido: objetivo, repo, rama, espacio de ejecución, `AUTHORIZED_EXECUTION_SNAPSHOT`, `EXECUTION_BASELINE`, scope, fuera de scope, decisiones cerradas, invariantes, AC, qué preparar (commit/PR). **El orchestrator no escribe código productivo**: `implementation` es el único que escribe producto. Conserva su bucle `INSPECT → EDIT → VERIFY → FIX → RETEST`; nunca se pregunta al humano si ejecutar tests. Entrega `IMPLEMENTATION_RESULT`, que es su declaración, no la prueba (`SELF-VERIFICATION != INDEPENDENT CONFORMANCE`).

Multi-writer sólo con fronteras de escritura explícitas y disjuntas (MANUAL §14).

### Reviews
`REVIEW ONLY WHERE A REVIEW QUESTION EXISTS.`

| Review | Cuándo |
|---|---|
| `implementation-review` | Por defecto en cambios productivos materiales. En `FORMAL`, con `AC_CONVERGENCE_RESULT` sobre cada `AC-NNN` material (`skill://implementation-review/references/ac-convergence.md`) |
| `architecture-review` | Sólo si toca boundaries, contratos u ownership |
| `security-review` | Sólo si toca superficie material de seguridad |
| `governance-review` | Cuando hay que comprobar scope/autoridad (diff amplio, contrato ligero, señales de desvío) |
| `pr-review` | Sólo cuando existe un PR remoto real. Aquí sólo revisa y prepara; su ciclo de vida con mutaciones (publicar, aprobar, mergear, sincronizar, notificar) corre en la Main Session (`pr-review` §19) |

Un micro cambio de bajo riesgo puede cerrar con la revisión de diff de `code-quality` más una `implementation-review` breve.

## 5. Remediation

`REVIEW_FINDING != AUTHORIZATION_TO_FIX`. Quien ejecuta este lifecycle clasifica cada finding, y cada AC material fuera de `PASS`: `FIX_ALREADY_AUTHORIZED` (inequívocamente dentro del contrato, sin cambio de semántica ni de alcance ni decisión material: vuelve a `implementation` con el finding concreto) · `DECISION_REQUIRED` · `OUT_OF_SCOPE` (se reporta, no se toca) · `CONTRACT_CONTRADICTION` (`DECISION_CONTRADICTION` hacia `specification`). Criterios: `skill://delivery-lifecycle/references/delivery-evidence.md` §3.

Máximo una vuelta: `fix → retest → re-review independiente → convergencia`. Si persiste un finding bloqueante o un AC material fuera de `PASS`: `REMEDIATION_EXHAUSTED` → `BLOCKED` con evidencia; si la causa es un fallo que `implementation` no consigue explicar, puede recomendarse `diagnostics` (§10), y decide el humano. Sin pulido infinito: `CONTINUITY OVER PERFECTION`. La remediation repara la implementación; nunca reescribe el contrato.

## 6. Commit, PR, integración

- `COMMIT_READY`: `COMMIT_MESSAGE` según `git-workflow` (`<tipo>(<componente>): <descripción>` en español, ≤ 72).
- `PR_READY`: `PR_TITLE` (`<tipo>(<componente>): <descripción>`, sin ticket) y `PR_BODY` con la plantilla oficial; **sólo pruebas realmente ejecutadas**; sin ticket → justificación + enlace, nunca un ID inventado.
- Ejecutar `git commit`, push o publicar el PR exige autorización. Dentro de un subagent esos comandos se **rechazan** por la capa de herramientas: el orchestrator los deja preparados y la Main Session los ejecuta si tú los autorizas.
- El lifecycle automático termina en `INTEGRATION_READY` cuando `DELIVERY_EVIDENCE` pasa su gate (`skill://delivery-lifecycle/references/delivery-evidence.md` §4–§5): fingerprint del contrato sin cambios · verificación registrada sin fallos introducidos abiertos · review sin bloqueo · en `FORMAL`, todo AC material en `PASS` · commit y PR preparados (o ejecutados si se autorizó). Un AC material fuera de `PASS` deja `integration_ready: NO`; el requisito no se suaviza para cerrar.
- `INTEGRATION_READY != COMPLETE` y no autoriza commit, push, publicación del PR ni merge. La integración remota es del ciclo de `pr-review` (`/pr`); merge, tag y release son autoridad humana.
- El worktree de ejecución se limpia sólo con la evidencia capturada, sin trabajo sin commitear y con el handoff de integración terminado (`references/execution-preflight.md` §4).

## 7. Gates humanos

Se interrumpe **sólo** por: decisión reservada pendiente (`DECISION_REQUIRED`) · operación material con gate · contradicción (`DECISION_CONTRADICTION`) · ampliación de alcance · evidencia insuficiente que bloquea · integración/release.

**No** se interrumpe por: lecturas, búsquedas, tests, lint, formatter, type-check, build, preparación local de dependencias, Docker local, reintentos de tests, elección de worker, elección de reviews, orden interno del lifecycle.

## 8. Proporcionalidad — rutas típicas

| Caso | Ruta |
|---|---|
| Micro fix | READY → BRANCH → IMPLEMENT/TEST → review breve → COMMIT/PR prep |
| Feature mediana | READY → spec LIGHT → BRANCH → IMPLEMENT/TEST → implementation-review → COMMIT/PR prep |
| Cambio arquitectónico | READY → discovery → spec FORMAL → decisiones humanas → architecture-review (preflight) → BRANCH → autorización → EXECUTION_PREFLIGHT (snapshot, baseline, worktree) → IMPLEMENT/TEST → architecture-review + implementation-review con convergencia por AC → DELIVERY_EVIDENCE → COMMIT/PR prep |
| Investigación | READY → discovery → reporte |
| Incidente | fallo observado → `diagnostics` (§10) |

## 9. Multi-agent

Paralelizar sólo si `COORDINATION_COST < EXPECTED_PARALLELIZATION_VALUE` y hay fronteras claras. El ejecutor del lifecycle es el **único synthesis owner**: no hay votación entre agents; manda la evidencia (MANUAL §14).

## 10. Diagnostics no es una fase

`diagnostics` sólo entra ante un **fallo observado** — incluido un fallo que `implementation` no consigue explicar dentro de su ciclo. Nunca se ejecuta "por si acaso" ni como paso del camino normal. `DIAGNOSIS != REMEDIATION`: la corrección vuelve a entrar con su propio contrato.

## 11. Estado visible

```
LIFECYCLE_STATE
  work_item:          <ID | sin ticket> — <título>
  classification:     <WORK_ITEM_CLASSIFICATION · RISK · SCOPE · KNOWN_STATE · SPECIFICATION_NEED>
  routing:            <ROUTING_RECOMMENDATION de project-management · seguida | no seguida + razón>
  current_state:      <estado>
  completed:          <estados recorridos, una línea>
  next:               <siguiente transición y capability>
  blocked_by:         NONE | <gate>
  decisions_required: NONE | <lista>
  evidence:           <rutas / ids de agent / comandos con resultado; desde EXECUTION_PREFLIGHT, DELIVERY_EVIDENCE>
```

Reportar al humano sólo cuando: hace falta una decisión · hay bloqueo · termina una fase material · termina el lifecycle. No un informe por transición.

## 12. Fallos de worker

- Distinguir `WORKER_FAILURE` (el worker no terminó: timeout, error de herramienta, salida vacía) de `WORK_FAILURE` (terminó con `STOP_REPORT`/`DECISION_REQUIRED` o evidencia negativa).
- `WORKER_FAILURE` claramente transitorio → **un** reintento con el mismo contrato. Si se repite → `BLOCKED` con `STOP_REPORT`.
- `WORK_FAILURE` → se trata como resultado, no se reintenta.
- Conservar siempre `LIFECYCLE_STATE` y la evidencia producida (ids `agent://…`, rutas, diffs): un bloqueo nunca pierde trabajo ya hecho.

## 13. Referencias y estado de la Línea 2

| Tarea | Cargar |
|---|---|
| Antes de la primera escritura: snapshot autorizado, preflight, baseline, worktree y su limpieza | `skill://delivery-lifecycle/references/execution-preflight.md` |
| Verificación, atribución de fallos, remediation, `DELIVERY_EVIDENCE` y gate de `INTEGRATION_READY` | `skill://delivery-lifecycle/references/delivery-evidence.md` |
| Convergencia por `AC-NNN` (owner: `implementation-review`) | `skill://implementation-review/references/ac-convergence.md` |

`LINE 2 STATUS: USABLE` · `MATURITY: FIELD_VALIDATION` (harness 0.8.0). Validada con 24 escenarios sintéticos (`.omp/tests/delivery/`); 0 ejecuciones en trabajo real. `NO MORE LINE 2 FEATURES BY IDEA ALONE`: cambia sólo por `OBSERVED_FAILURE`, `OBSERVED_FRICTION` o `REPEATED_CAPABILITY_GAP`, con evidencia, como la Línea 1. `GOOD ENOUGH TO USE. NOW LET REAL DELIVERY BREAK IT.`
