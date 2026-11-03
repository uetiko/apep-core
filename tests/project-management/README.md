# Validación de `project-management` (work shaping + flow)

Suite de conformidad de `project-management`: modo work item desde el harness 0.6.0 (PM01–PM20) y gestión de proyecto de software desde 0.7.0 (PM21–PM45). No ejecuta trabajo ni toca aplicaciones.

```bash
python3 -I .omp/tests/project-management/run.py      # desde el session root
```

Exit: `0` todo PASS · `1` algún FAIL · `2` algún caso sin veredicto (`NOT_RUN`), que nunca cuenta como PASS.

## Capas

| Capa | Qué comprueba |
|---|---|
| `STRUCTURE` | El contrato de la skill está presente: requirements management, tipos de cambio y análisis de impacto, gobernanza del proyecto, valor, alcances, planificación, estimación, baseline, medición, control, riesgo de proyecto, cadena de estados de éxito y cierre (0.7.0); el estado del requisito sólo cita estados que existen en `delivery-lifecycle`/`specification`; fronteras con `specification` (§11), `delivery-lifecycle` (§4), las reviews y el MANUAL; clasificación, assessment, riesgo, dependencias, blockers, slicing, tamaño, formalidad, readiness direccional, routing y señales de flujo, con sus valores; las fronteras con `specification` y `delivery-lifecycle`; el baseline Kanban (estados, WIP 2, DoD en §4); `delivery-lifecycle` consume la clasificación sin una paralela; el catálogo no crece |
| `DRYRUN` | Que un agente que aplica la skill **sin ver las expectativas** llega al resultado que el método exige. Compara `dryrun/PM##.json` con `expected/PM##.json` |

## Casos

| Caso | Comprueba |
|---|---|
| PM01 | Feature pequeña y clara → `LIGHT`, ruta según evidencia |
| PM02 | Feature ambigua → lista para `specification` sin exigir AC finales |
| PM03 | Bug observado → `diagnostics` |
| PM04 | Investigación → `technical-discovery` |
| PM05 | Alto impacto e incertidumbre → `FORMAL`, `specification`, `architecture-review` probable, decisión pendiente |
| PM06 | Item sobredimensionado → dividir |
| PM07 | División por capas cuando existe corte vertical → slices observables |
| PM08 | Infraestructura habilitadora → `ENABLING_SLICE` con justificación |
| PM09 | Dependencia bloqueante → tipada y con alcance, sin inventar IDs |
| PM10 | Bloqueo parcial → lo no afectado continúa |
| PM11 | Dependencia desconocida → `UNKNOWN`, sin inventar |
| PM12 | Dependencia de decisión → `DECISION_REQUIRED` |
| PM13 | Ya `EXECUTION_READY` → no vuelve a `specification` |
| PM14 | Tarea apta para implementar → sin expansión ceremonial |
| PM15 | Petición de inventar comportamiento → rechazo y ruta a `specification` |
| PM16 | Petición de fijar prioridad sin humano → rechazo y `DECISION_REQUIRED` |
| PM17 | Sin Story Points → ni se inventan ni bloquean |
| PM18 | Dependencia entre repositorios → identificada, sin coordinar la ejecución |
| PM19 | Grande pero coherente → dividir no es obligatorio por tamaño |
| PM20 | Grafo de routing → dependencias y siguiente capability coherentes |
| PM21 | Requisito ambiguo → PM gestiona su estado, specification es dueña de la semántica |
| PM22 | Requisito cambia tras la aprobación → análisis de impacto, sin cambio silencioso de alcance |
| PM23 | Stakeholder pide comportamiento nuevo → cambio con decisión, no requisito automático |
| PM24 | Comportamiento faltante descubierto en implementación → specification/humano; PM registra el impacto |
| PM25 | Fecha deseada, no comprometida → DESIRED_DATE != COMMITTED_DATE |
| PM26 | Estimación con alta incertidumbre → rango/supuestos o discovery, sin falsa precisión |
| PM27 | Story Points aportados → se registran, nunca se convierten automáticamente a tiempo |
| PM28 | "80% completo" → evidencia de progreso insuficiente |
| PM29 | Implementado sin verificar → ni entregado ni Done |
| PM30 | Desplegado sin aceptación operacional → proyecto no cerrado |
| PM31 | Requisito sin fuente ni stakeholder → hueco de trazabilidad |
| PM32 | Requisito cambiado → alcance y dependencias afectadas identificadas |
| PM33 | Requisito de seguridad → PM lo gestiona; specification y security-review son dueños del análisis |
| PM34 | Decisión de arquitectura necesaria → PM identifica bloqueo e impacto; arquitectura/humano deciden |
| PM35 | Falta de recursos → opciones y recomendación, sin reducir alcance en silencio |
| PM36 | Conflicto entre fecha y alcance → opciones y DECISION_REQUIRED |
| PM37 | Riesgo materializado → transición RISK → ISSUE |
| PM38 | Requisito nuevo amenaza un hito comprometido → análisis de impacto |
| PM39 | Entregado pero beneficio no medido → DELIVERY_SUCCESS != VALUE_REALIZED |
| PM40 | Artefacto predictivo pedido sin valor → la proporcionalidad rechaza la ceremonia |
| PM41 | Requisitos que evolucionan → planificación adaptativa |
| PM42 | Requirements management intenta escribir AC → rechazo y specification |
| PM43 | Requisito especificado referenciado desde PM → enlazar, no duplicar |
| PM44 | Cambio que sólo afecta calendario → sin re-especificación si la semántica no cambia |
| PM45 | Cierre con ownership operacional sin resolver → NOT_READY_FOR_CLOSURE |

### Presentación (desde 0.8.1)

Capa `PRESENTATION`: siete casos sobre fixtures existentes. El agente produce el reporte (`presentation/dryrun/Pnn.md`) y el veredicto canónico del mismo análisis (`Pnn.json`). El veredicto debe seguir cumpliendo la expectativa original del fixture — la presentación no cambia el método (PM-PRES-13) — y el reporte se contrasta con él. Las comprobaciones son estructurales y semánticas, no de redacción: resumen primero y sin vocabulario interno, registro de proceso al final con las estructuras canónicas, siguiente paso igual en ambas vistas, lo desconocido marcado como tal, sin `AC-NNN` inventados, hechos e inferencias etiquetados, decisiones no cerradas en el texto, porcentajes sólo como cita, fechas comprometida y forecast distinguidas, valor no medido no dado por obtenido. Casos y su cobertura PM-PRES-01..20: `presentation/cases.json`; PM-PRES-14, 15 y 19 los cubre `STRUCTURE`.

### Coherencia de readiness y ruta (desde 0.8.2)

Invariante global `routing_coherent` sobre **todos** los veredictos (DRYRUN y PRESENTATION), según `routing-readiness.md` §3:
- un prerequisito insatisfecho no convive con `READY_FOR_NEXT_CAPABILITY: YES`;
- la autorización de ejecución no es un prerequisito;
- NEXT no es su propio `THEN`, ni figura como bloqueada salvo la parte declarada en un bloqueo parcial;
- `READY: PARTIAL` exige `BLOCKING_SCOPE` o blockers.

Más la comprobación de presentación `summary_no_wait`: el resumen no pide esperar al siguiente paso listo.

| PM-RR | Cubierto por |
|---|---|
| 01 prerequisito insatisfecho ⇒ B no es NEXT listo | `routing_coherent` (todos) · PM46 |
| 02 NEXT = quien resuelve; B en `THEN` | PM46 · PM56 |
| 03 la paralela no bloquea NEXT | PM47 |
| 04 bloqueo parcial con `BLOCKING_SCOPE` y parte ejecutable | PM47 · PM10 · `routing_coherent` |
| 05 `READY: YES` ⇒ nada dice que NEXT espera | `routing_coherent` · `summary_no_wait` |
| 06 / 07 gestión e ingeniería coinciden con el registro | P08 · P09 (`process_next_matches_verdict`, `summary_no_wait`) |
| 08 / 09 un desconocido factual (aunque se llame `D-…`) no es `DECISION_REQUIRED` | PM50 · PM56 · P09 |
| 10 no se pregunta al humano lo que el sistema puede responder | PM50 · PM55 (evidencia antes que pregunta) |
| 11 discovery antes de specification cuando es prerequisito real | PM46 · PM56 |
| 12 discovery en paralelo con alcance acotado | PM47 |
| 13 diagnostics sólo con superficie identificada o reproducible | PM51 · PM55 |
| 14 implementation con archivo desconocido y alcance delimitado | PM49 |
| 15 implementation no elige entre superficies materiales | PM48 · PM52 · PM55 |
| 16 `LIGHT` no anula el readiness | PM52 |
| 17 `FORMAL` no obliga a especificar ya si un hecho lo bloquea | PM46 |
| 18 sin sobre-routing: una tarea lista llega a implementation | PM14 · PM49 · PM54 |
| 19 sin discovery artificial con estado actual conocido | PM53 |
| 20 sin sobre-bloqueo: lo táctico no material no bloquea | PM54 |

PM55 y PM56 son regresiones de campo anonimizadas: conservan la estructura causal de las dos ejecuciones reales, no su respuesta histórica.

Historial de la capa `PRESENTATION`:

| Ejecución | Resultado | Qué cambió después |
|---|---|---|
| `run1` (2026-10-23, Sonnet 5.5, P01–P07) | 5/7. P04 y P05 no conformes **por defecto de las comprobaciones**, no de los reportes: "lo que sí está decidido" (hechos del caso) y "la decisión es del área legal" (quién decide) se tomaban como decisión cerrada; "el 80% podría referirse…; no se sabe" (inferencia marcada) se tomaba como porcentaje afirmado | Las comprobaciones se acotaron al defecto real (cerrar en el texto la decisión pendiente; afirmar un porcentaje como estado sin atribuirlo), y los controles negativos siguen fallando sobre él. Aclaraciones de presentación pedidas por los agentes: item pequeño = resumen + estado + registro mínimo; una autorización pendiente no se presenta como decisión; "quién decide" desconocido = "por identificar"; registro acotado del modo proyecto. Repetidos P01 y P05 en `run2` |
| `run2` (P01, P05; el resto de `run1`) | 7/7 | 0.8.2 añade el invariante `routing_coherent`: P01 lo incumple (prerequisitos y autorización con NEXT listo) bajo el método anterior. Se repite junto con P08 y P09 nuevos en `run3` |
| `run3` (P01, P08, P09) | 9/9. P08 (responsive) eligió `NONE` + decisión directa al owner sin reunir la evidencia que el sistema podía dar (qué superficies fallan) | Aclaración: si la evidencia puede acotar los candidatos, se reúne antes de preguntar. Repetido P08 en `run4` |
| **`run4` — vigente** (P08; el resto de `run3`) | **`ALL_CONFORMANT`**: 9/9; P08 elige ahora investigar qué superficies fallan (`technical-discovery`, después `diagnostics`) y deja la elección de superficie como contingente | — |

Todos los casos comprueban además que el veredicto no inventa comportamiento, prioridad, Story Points, IDs externos ni fechas (`invented`). PM21–PM45 comprueban también que no inventa estimaciones, baselines, valor, criterios de aceptación ni figuras de gobernanza, y que no ejerce autoridad que PM no tiene: aprobar cambios, cambiar alcance, aceptar riesgo, fijar prioridad, declarar baselines, autorizar ejecución ni validar requisitos (`authority`).

## Límites

- Los veredictos son ejecuciones registradas de un modelo: la comparación es determinista; reproducirlos exige volver a ejecutarlos. El aislamiento respecto a `expected/` es por instrucción.
- Las fixtures son sintéticas y los juicios (clasificación, tamaño, riesgo) siguen siendo juicio. No sustituyen la observación en trabajo real.
- Donde el contrato admite más de una respuesta razonable, la expectativa acepta todas (p. ej. PM06 admite `SPLIT_RECOMMENDED` o `SPLIT_REQUIRED`; PM20 no exige que WI-401 sea independiente de WI-402).

## Historial de ejecuciones

| Ejecución | Resultado | Qué cambió después |
|---|---|---|
| `run1` (2026-10-23, Sonnet 5.5) | 36/38: **PM01 no conforme** (`NONE` en lugar de `LIGHT`), **PM10 no conforme** (`blocking_scope` "CSV no está bloqueado" rechazado por un regex). Cuatro agentes señalaron además la misma contradicción en `routing-readiness.md` | PM01: defecto del método, `work-item-shaping.md` §4 no recogía el criterio de `delivery-lifecycle` (comportamiento nuevo acotado = `LIGHT`); se alinearon las definiciones. PM10: defecto de la expectativa (el regex no distinguía una negación). Contradicción §2/§4: el readiness hacia `implementation` depende del contrato y la autorización se registra aparte; regresión añadida en PM13, PM14 y PM19 |
| `run2` (2026-10-23, Sonnet 5.5) | `ALL_CONFORMANT`: 38/38 | Corrección de frontera de ownership (SKILL.md §1: PM no es capa de la cadena de autoridad ni produce el contrato; `routing-readiness.md` §2, `work-item-shaping.md` §4), estado `USABLE` / `FIELD_VALIDATION`; nuevos checks `STRUCTURE`. Un agente de `run3` detectó además citas `SKILL.md §N` desactualizadas tras la reescritura (§6→§10, §9→§11, §12→§14, §14→§17) en tres referencias; corregidas y cubiertas con un check |
| `run3` (2026-10-23, Sonnet 5.5, texto 0.6.0) | `ALL_CONFORMANT`: 41/41; ningún veredicto inventa comportamiento, prioridad, Story Points, IDs ni fechas; PM09 deja el task contract ligero como lo que falta y declara que PM no lo produce | Archivado en `history/run3` al pasar a 0.7.0 |
| `run4` (2026-10-23, Sonnet 5.5, texto 0.7.0, PM01–PM45) | 44/45: **PM32 no conforme** por un defecto de la expectativa, que buscaba texto en `affected_dependencies` donde el método pide referencias `DEP-NNN`; el veredicto era correcto. Todos los demás conformes; ningún `invented` ni `authority` en `true` | Expectativa de PM32 corregida (comprueba la referencia y `dependencies.target`). Aclaraciones del método pedidas por varios agentes: tipo de cambio de un movimiento entre releases (`DELIVERY_SCOPE`) y su materialidad; tipo de un comportamiento descubierto en implementación; una petición no aceptada abre el análisis de impacto, no la especificación; cerrar con deuda es una decisión humana que no cambia el veredicto; forecast desde ritmo observado como rango; esquema con `PROJECT_ACCEPTANCE` y significado de `done`/`estimate`. Repetidos los ocho casos afectados en `run5` |
| `run5` (2026-10-23, Sonnet 5.5; PM22, PM23, PM24, PM30, PM36, PM39, PM44, PM45) | 7/8: **PM22 no conforme**: `requires_respecification: NO`. Defecto del método introducido por la aclaración de `run4`: "la petición no aceptada no reabre la especificación" volvió ambiguo si el campo describe el impacto o el momento de reabrir | `requirements-management.md` §4.2: el análisis dice qué habría que reespecificar **si** se acepta; definición explícita de cambio material (por impacto, no por tipo). Esquema: `requires_respecification` describe impacto. `SKILL.md` §10: aceptación operacional y de proyecto son independientes. Repetidos PM22–PM24 en `run6` |
| `run6` (`dryrun/PM##.json`; PM22–PM24 de `run6`, los ocho de `run5` restantes y el resto de `run4`) | **`ALL_CONFORMANT`**: `run.py` 94/94 PASS (exit 0); en los 45 veredictos ningún `invented` ni `authority` en `true`. PM22 `requires_respecification: YES` con la petición todavía sin aceptar y `specification` sin reabrir | Editorial posterior: el esquema aclara que `requires_respecification` incluye ampliar la especificación (un `NEW_REQUIREMENT` o un hueco), como ya lo leyó el agente |
| `run7` (2026-10-23, Sonnet 5.5; 19 casos que incumplían `routing_coherent` + PM46–PM56) | 29/30. **PM10** no conforme por una regla demasiado estricta que escribí yo ("NEXT no figura bloqueada") que prohibía el bloqueo parcial legítimo (CSV ya, PDF espera); **PM24** por una regex léxica de `run4` (`delivery_impact` correcto con otras palabras). PM55 y P08 divergían: uno reunió evidencia, el otro preguntó al humano | Regla y comprobación corregidas (NEXT puede figurar bloqueada sólo para la parte de un bloqueo parcial declarado); regex de PM24 ampliada a sinónimos; aclaración "si la evidencia puede acotar los candidatos, se reúne antes de preguntar" y fila de `diagnostics` alineada. PM55 endurecida (ni `implementation` ni `NONE`). Repetidos PM48, PM51 y PM55 en `run8` |
| **`run8` — vigente** (PM48, PM51, PM55; el resto de `run7` y anteriores) | **`ALL_CONFORMANT`**: `run.py` 124/124 (exit 0). PM55 reúne evidencia antes de preguntar; PM48 (sin evidencia que decida) sigue yendo a decisión humana: sin sobrecorrección | — |

### Observaciones (`run2`)

- PM10: el agente da CSV por listo para `implementation` suponiendo que el task contract ligero existe; lo registra como `ASSUMPTION` en `missing`. Indulgente, sin violar invariantes.
- PM06: `NEXT_CAPABILITY: NONE` por la decisión pendiente del owner sobre la división; defendible.

### Observaciones de campo

Hechos observados al usar `project-management` en trabajo real (MANUAL §8, *política de evolución*). Una observación no cambia el método por sí sola.

| ID | Clase | Observación | Estado |
|---|---|---|---|
| `FO-PM-001` | `OBSERVED_FRICTION` | Una ejecución real de `/shape` produjo un análisis rico, pero lo presentó sobre todo con estructuras internas (`WORK_ITEM_ASSESSMENT`, `READINESS_CHECK`, `ROUTING_RECOMMENDATION`) y lenguaje de ingeniería: alta carga para lectores no técnicos, conclusiones de gestión mezcladas con detalle y contradicciones entre estado y recomendación difíciles de ver | **Atendida en 0.8.1** por la capa de presentación (`work-item-shaping-report.md`, `project-management-report.md`), sin cambiar el método |
| `OBSERVED_FAILURE-PM-001` | `OBSERVED_FAILURE` | En la misma ejecución, `/shape` reconoció un alcance material de producto todavía indeterminado y aun así recomendó `implementation` como siguiente capability | **Observación histórica; no se reprodujo** en la segunda ejecución del mismo work item, que recomendó `diagnostics` y cayó en `PM-002`. 0.8.2 explicita la frontera que ya implicaban la gobernanza (§1.2: el alcance es materia reservada) y `routing-readiness.md` §2 (contrato con alcance delimitado): quien implementa puede descubrir dónde cambiar el sistema, no elegir a qué superficie material se refería el pedido. Regresión: PM48, PM52, PM55 |
| `OBSERVED_FAILURE-PM-002` | **`METHOD_DEFECT`** (repetido: `REPEATED_CAPABILITY_GAP`) | Dos ejecuciones reales distintas de `/shape` produjeron `NEXT_CAPABILITY: B` · `READY_FOR_NEXT_CAPABILITY: YES` con un prerequisito A que debía terminar antes de que B empezara: (1) informe responsive: `NEXT: diagnostics` con "confirmar primero la superficie" y "nada útil puede avanzar hasta confirmarla"; (2) entorno de producción: `NEXT: specification` con discovery previo como prerequisito y la recomendación final "no lanzar la especificación todavía", más una referencia desconocida (tipo `D-…`) tratada a la vez como `UNKNOWN` y como `DECISION_REQUIRED` | **Resuelto en 0.8.2.** Causa: el ejemplo canónico de `routing-readiness.md` §3 modelaba exactamente ese patrón (`NEXT: specification` + `PREREQUISITES: technical-discovery…`) y `PREREQUISITES` no tenía relación definida con el readiness. En los 45 veredictos sintéticos vigentes, 19 lo usaban de forma incoherente con `READY: YES` (trabajo opcional, el propio trabajo de NEXT, la autorización de ejecución, decisiones humanas); ninguna expectativa lo comprobaba. Corrección: NEXT es lo que puede empezar ahora; prerequisito insatisfecho ⇒ NEXT es quien lo resuelve y B va en `THEN`; paralelas con `BLOCKING_SCOPE`; ownership de aperturas; `UNKNOWN FACTUAL != DECISION_REQUIRED`. Invariante global `routing_coherent` sobre todos los veredictos; regresiones PM46–PM56 y P08–P09 |

### Candidatos de observación de la presentación (no backlog)

- Dónde va en el registro mínimo de un item pequeño una autorización pendiente o la formalidad (un agente añadió `WORK_FORMALITY` y `READINESS_CHECK`).
- Sección *Estado de la entrega* cuando no hay ningún inventario verificable: cuándo omitirla y cuándo dejarla como `N/A` informativo.
- Uso de la fecha actual para cuantificar el tiempo restante cuando el caso no la da.
- Un esquema de veredicto propio del modo proyecto: hoy los campos de work item quedan en `NOT_EVALUATED`.

### Candidatos futuros (registrados, no implementados)

| ID | Candidato | Origen |
|---|---|---|
| PMFC-001 | Valores `UNKNOWN` / `NOT_EVALUATED` en el esquema del perfil de riesgo y campos de nivel superior para casos con varios items | Agentes de `run1` y `run2` |
| PMFC-002 | Criterios de desempate entre clasificaciones frontera (`BUG`/`INCIDENT`, `SECURITY`/`TECHNICAL_CHANGE`, `INVESTIGATION`/`DOCUMENTATION`, cambios de texto visibles) | Agentes de `run1` y `run2` |
| PMFC-003 | Precedencia entre `SPLIT_REQUIRED` y `CANNOT_SPLIT_WITHOUT_DECISION` cuando ambos aplican; resultado de un item que es en sí una `ENABLING_SLICE` | Agentes de PM05, PM06, PM08 |
| PMFC-004 | `WORK_FORMALITY` de un `BUG` antes del diagnóstico | Agentes de PM03 |
| PMFC-005 | Quién redacta el task contract ligero cuando la ruta es `LIGHT` | Agente de PM09/PM10 (`run2`) |
| PMFC-006 | Si un área interna (legal) es `EXTERNAL_DEPENDENCY` o `DECISION_DEPENDENCY` | Agentes de PM10 |
| PMFC-007 | Routing cuando una decisión humana bloquea **parte** del trabajo (la tabla de `routing-readiness.md` §3 sólo cubre "bloquea todo") | Agentes de `run4` y `run5` (PM05, PM12, PM22, PM23, PM24, PM31) |
| PMFC-008 | Esquema de veredicto: supuestos de un forecast, figuras de gobernanza `NOT_IDENTIFIED`, fecha deseada no concreta ("esta semana"), dependencias inversas (otros dependen de este item) | Agentes de `run4` y `run5` |
| PMFC-009 | Si un dato concreto aportado en la petición (p. ej. "6 items en 6 semanas") basta como fuente de métricas de flujo, o hace falta un registro | Agente de PM36 |
| PMFC-010 | Clasificación de un requisito de seguimiento o un issue de proyecto que no es un work item (PM37, PM42, PM43) | Agentes de `run4` |
| PMFC-011 | Qué pasa con el trabajo autorizado **afectado** por un cambio pendiente de decisión; materialidad cuando el impacto sobre un hito es `UNKNOWN`; a quién se dirige un `DECISION_REQUIRED` si el owner no está identificado | Agentes de `run5` y `run6` (PM22, PM24) |
