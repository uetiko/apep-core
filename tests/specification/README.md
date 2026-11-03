# Validación de la Línea 1 (`specification`)

Fixtures y dry-runs deterministas de la Línea 1 desde el harness 0.5.0. No ejecutan la Línea 2 ni tocan ninguna aplicación.

```bash
python3 -I .omp/tests/specification/run.py      # desde el session root
```

Exit: `0` todo PASS · `1` algún FAIL · `2` algún caso sin veredicto registrado (`NOT_RUN`), que nunca cuenta como PASS.

## Capas

| Capa | Qué comprueba | Cómo |
|---|---|---|
| `STRUCTURE` | Que el contrato de la skill está presente: C1–C4 y la regla de readiness intactos, las cuatro referencias nuevas con sus dimensiones, checks, pasadas y campos, los diez estados, y el catálogo sin skills ni agents nuevos | Búsqueda textual sobre `.omp/skills/specification/` |
| `MECHANICAL` | Lo que se puede comprobar sin juicio: integridad de referencias (C2) y señales léxicas de SQ5 / SQ10 sobre las fixtures | Extracción de IDs y léxico (`run.py`) |
| `DRYRUN` | Que un agente que aplica la skill **sin ver las expectativas** llega al resultado que la metodología exige | Compara `dryrun/T##.json` con `expected/T##.json` y, en T11 y T15, inspecciona los artefactos producidos en `dryrun/out/` |

## Casos

| Caso | Comprueba |
|---|---|
| T01 | Un requisito claro no genera preguntas y avanza a especificar |
| T02 | Un unknown factual verificable va a discovery (con evidencia) y no se pregunta al humano |
| T03 | Una ambigüedad material produce `CLARIFICATION_REQUIRED` con preguntas interrogativas completas |
| T04 | Una assumption táctica se registra con su razón y no pide decisión |
| T05 | Una decisión de negocio disfrazada de assumption se rechaza (A6) y se pregunta |
| T06 | Un requisito vago hace fallar SQ5 |
| T07 | El HOW prematuro hace fallar SQ4 |
| T08 | BR y AC contradictorios hacen fallar la coherencia, sin elegir versión |
| T09 | Una tarea que introduce comportamiento hace fallar la coherencia (`AC_TO_TASK`) |
| T10 | Un test de aceptación que inventa semántica hace fallar la coherencia (`AC_TO_ACCEPTANCE_TEST`) |
| T11 | Una respuesta aplicada queda en el ledger como `APPLIED` y los artefactos dejan de contradecirla |
| T12 | Una clarificación material abierta deja la spec `NOT_EXECUTION_READY` |
| T13 | Un item abierto no material (`ASM-001`) pasa C1 registrado y la spec llega a `EXECUTION_READY` |
| T14 | C2 pasa y la coherencia falla: `REFERENCE_INTEGRITY != SEMANTIC_COHERENCE` |
| T15 | Camino completo: necesidad cruda → clarificación → spec → quality, coherence y C1–C4 PASS → `EXECUTION_READY`, sin requisitos cuyo origen sea una inferencia del agente |
| T16 | Una respuesta "fuera de alcance" sobre algo de lo que depende el alcance no cierra la apertura: no hay `EXECUTION_READY` ni se rellena con inferencias |

## Historial de ejecuciones

`dryrun/history/` conserva las ejecuciones anteriores como evidencia; no se comparan.

| Ejecución | Resultado | Qué cambió después |
|---|---|---|
| `run1` (2026-10-23, Sonnet 5.5, T01–T15) | T01–T14 conformes. **T15 fue un falso `EXECUTION_READY`**: el oráculo respondió "si es regla de negocio, déjala fuera de alcance" a cuándo empieza la pausa, y el agente fijó él mismo la regla (BR-011, `SOURCE: … INFERENCE`), la declaró no material y pasó el gate. Las aserciones de entonces no lo detectaban | Metodología: una respuesta sólo cierra lo que dice; "fuera de alcance" no cierra lo que el alcance necesita; una inferencia nunca es `SOURCE` de un requisito material; la coherencia (pasada 12) lo marca `HIGH`. Pruebas: guard mecánico `provenance_no_inference`, oráculo de T15 completado y T16 nuevo con el oráculo original. Además se aclararon los estados tras un intake limpio o un `FAIL`, el tratamiento del comportamiento añadido aguas abajo, la granularidad de los findings y la creación de AC al aplicar una respuesta, todo señalado como ambiguo por los agentes |
| `run2` (2026-10-23, Sonnet 5.5, T01–T16, texto corregido tras `run1`) | 97/97 PASS en `run.py`, pero **T15 no era un `EXECUTION_READY` legítimo**: el agente trató el comodín del oráculo ("si es regla de negocio, fuera de alcance") como una reducción de alcance explícita, y cerró cinco casos alcanzables (p. ej. cancelar con una pausa programada) con una `STOP_CONDITION` del contrato. En T16 otro agente leyó la misma regla al revés: dos lecturas opuestas del mismo texto | Metodología: una regla genérica no es una decisión explícita sobre una parte concreta; una condición de parada no sustituye el comportamiento de un caso alcanzable (C1 lo trata como material). Pruebas: guard heurístico sobre `STOP_CONDITIONS` del tipo "detenerse si hace falta definir…" en T15/T16, y oráculo de T15 completado con esos casos. T01–T14 no se repitieron: estas reglas no cambian sus casos |
| `run3` (T15, T16) | T16 conforme. T15 en `NOT_EXECUTION_READY`, **correcto con ese oráculo**: la métrica de éxito presuponía que la pausa se ofrece en el flujo de cancelación, pero el owner nunca lo dijo; el agente retiró la regla en vez de inferirla y bloqueó | Defecto de la fixture, no de la metodología: el oráculo de T15 se completó con los casos que quedaban (dónde se ofrece, varias suscripciones, pago vencido, cancelación programada, textos de email). Metodología: se explicitó que una presuposición no es una respuesta, cómo dividir una respuesta parcial, el tratamiento del comportamiento existente que cita el owner y el registro de las aperturas que se dejan para etapas posteriores |
| `run4` (T15) | 99/99 en `run.py`, pero **no conforme**: CLAR-005 quedó `APPLIED` con "el importe no se respondió … es el del proceso de cobro existente". El owner no había citado ese proceso para el importe; la parte sin responder debía dividirse y quedar `OPEN` | Metodología: sólo cuenta como comportamiento existente lo que el owner o la evidencia identifican como tal, y una entrada `APPLIED` nunca registra algo sin responder. Pruebas: guard sobre el ledger (T11, T15) que detecta esa ejecución. Fixture: oráculo de T15 completado (importe al reanudar, condiciones simultáneas, otros estados, medición) |
| `run5` (T15) | **Conforme**: `EXECUTION_READY` con 13 `CLAR-NNN` aplicadas, provenance sin inferencias y sin casos alcanzables sin definir. El guard del ledger de `run4` saltó sobre CLAR-013, una **delegación explícita** del owner sobre un punto clasificado como no material y cerrado como ASM-001, que la metodología acepta | Defecto de la expectativa: el guard confundía "sin respuesta" con "respondida por delegación". Se sustituyó por `ledger_no_unanswered_applied`, que exceptúa sólo la delegación registrada sobre algo no material y sigue detectando CLAR-005 de `run4` |
| `suite1` (T01–T14, T16 sobre el texto definitivo; T15 = `run5`) | 100/101. **T12 no conforme**: `final_state: CLARIFICATION_REQUIRED` en lugar de `NOT_EXECUTION_READY`, con el gate ya evaluado | Defecto de la metodología introducido en el cierre: la regla de transición de SKILL §12 chocaba con la Etapa 07 una vez ejecutado el gate. Se fijó la precedencia (tras el gate, el estado es el que emite el gate) y se volvieron a ejecutar T11–T14 |
| **`suite2` — vigente** (`dryrun/T##.json`, 2026-10-23, Sonnet 5.5): T01–T10 y T16 de `suite1`, T11–T14 vueltos a ejecutar tras la corrección de §12, T15 = `run5` | **`ALL_CONFORMANT`**: `run.py` 101/101 PASS, exit 0 | — |

### Resultado vigente por caso

| Caso | Esperado | Observado | Divergencia |
|---|---|---|---|
| T01 | 0 preguntas, `SPECIFYING` | 0 preguntas, `SPECIFYING` | — |
| T02 | Discovery con evidencia, 0 preguntas | FACT de `AccountStatementController.php:6-18`, 0 preguntas | — |
| T03 | `CLARIFICATION_REQUIRED`, decisión material | `CLARIFICATION_REQUIRED`, 2 `CLAR` independientes (las dependientes, después) | — |
| T04 | ASM registrada, 0 preguntas | ASM-001 con A1–A8, 0 preguntas | — |
| T05 | Assumption rechazada (A6) y pregunta | Rechazada (A2, A4, A6, A7), 1 `CLAR` | — |
| T06 | Quality `FAIL` con SQ5 | `FAIL` SQ3, SQ5, SQ7 | — |
| T07 | Quality `FAIL` con SQ4 | `FAIL` SQ4 | — |
| T08 | Coherence `FAIL`, contradicción material sin elegir versión | `FAIL`, COH-001 `SEMANTIC_CONTRADICTION` `HIGH` → `CLARIFICATION_REQUIRED` | — |
| T09 | Coherence `FAIL` (`AC_TO_TASK`) | `FAIL`, 2 findings `AC_TO_TASK` `HIGH` | — |
| T10 | Coherence `FAIL` (`AC_TO_ACCEPTANCE_TEST`) | `FAIL`, 2 findings `AC_TO_ACCEPTANCE_TEST` `HIGH` | — |
| T11 | `CLAR-001` `APPLIED`, artefactos sin contradicción | `APPLIED`, BR-002 a 30 días, AC/SC nuevos para el límite | — |
| T12 | `NOT_EXECUTION_READY` por `CLAR-002` | `NOT_EXECUTION_READY`, bloqueo por `CLAR-002` (C1, C3) | — (en `suite1` sí la hubo, ver arriba) |
| T13 | `EXECUTION_READY` con ASM-001 no material | `EXECUTION_READY`, quality y coherence `PASS` | — |
| T14 | C2 `PASS`, coherencia `FAIL`, no ready | C2 `PASS`, `COH-001` `HIGH`, `NOT_EXECUTION_READY` | — |
| T15 | Camino completo a `EXECUTION_READY` sin inferencias | 13 `CLAR` aplicadas, quality, coherence y C1–C4 `PASS`, `EXECUTION_READY` | — |
| T16 | No `EXECUTION_READY`, sin inferencias | `CLARIFICATION_REQUIRED`, 2 `CLAR` materiales abiertas | — |

## Observaciones de campo

`FIELD_OBSERVATION` registra hechos observados al usar el harness que no cambian por sí solos la gobernanza (`USE GRADUALLY. OBSERVE REAL BEHAVIOR. EVOLVE FROM EVIDENCE.`).

### FO-001 — `WORKSPACE_BOUNDARY_VIOLATION`

| Campo | Contenido |
|---|---|
| Clasificación | `FIELD_OBSERVATION` |
| Impacto | `NON_MATERIAL_IN_OBSERVED_RUN` |
| Qué ocurrió | Durante `run2`, el agente que ejecutó T06–T10 escribió un script auxiliar en un directorio temporal del sistema (8945 bytes) para generar sus veredictos JSON. Ese directorio está fuera del workspace autorizado y fuera del scratchpad de la sesión |
| Por qué está fuera del comportamiento deseado | Regla de frontera del workspace: ninguna operación del agente se dirige fuera del workspace sin autorización explícita. El prompt del dry-run lo prohibía para la lectura, pero no nombraba un lugar para auxiliares |
| Impacto observado | Ninguno sobre el resultado: el script sólo escribió JSON dentro del workspace y no leyó nada fuera. El archivo sigue existiendo; no se borró, porque borrarlo también es operar fuera del workspace sin autorización |
| Mitigación aplicada | Sólo operativa, en los prompts de dry-run desde `run3`: un directorio para auxiliares dentro de `dryrun/out/<caso>/` y obligación de borrarlos. Las ejecuciones `run3` y `run4` no repitieron la conducta. Sin cambio de gobernanza |
| Área futura de hardening | Cómo se transmite la frontera del workspace a los subagentes (brief estándar con directorio de trabajo), y si la capa de herramientas puede restringir escrituras fuera del árbol |
| Criterio de promoción a cambio material | Repetición en trabajo real, o un caso con impacto real (lectura o escritura de datos fuera del workspace, o efecto sobre otro repositorio o el home) |

```
ONE OBSERVATION != AUTOMATIC GOVERNANCE CHANGE.
```

## Candidatos futuros

Ideas surgidas durante la validación que **no** fueron necesarias para la conformidad de 0.5.0. Se registran y no se implementan; su promoción exige evidencia de uso real (`MANUAL.md` §8, *política de evolución*).

| ID | Candidato | Origen |
|---|---|---|
| FC-001 | Si una métrica de éxito de negocio implica un requisito de instrumentación en la entrega | Agentes de T15 (`run2`–`run4`) y T16 |
| FC-002 | Distinguir en `VERDICT_SCHEMA` y en los resultados un quality/coherence incremental de uno formal | Agentes de T11 (`run1`, `run2`) |
| FC-003 | Ubicación exacta de `SPEC_QUALITY_RESULT` y `SPEC_COHERENCE_RESULT` dentro del contrato 07 ("exactamente estas secciones") | Agente de T15 (`run4`) |
| FC-004 | Criterio explícito para omitir la Etapa 04 con un actor y varias interacciones | Agentes de T15 |
| FC-005 | Estado del ledger para una respuesta recibida cuando todavía no existe artefacto donde aplicarla | Agente de T16 (`run3`) |
| FC-006 | Búsqueda léxica de C1/C3 por palabra completa (falsos positivos por subcadena: "independiente", "a definirlos") | Agentes de T15 |
| FC-007 | Protocolo de oráculo que no exponga respuestas antes de escribir las preguntas de seguimiento | Agentes de T15 (el oráculo sólo puede leerse entero) |
| FC-008 | Si una elección de UI observable pero sin regla de negocio puede cerrarse por delegación explícita del owner | Agente de T15 (`run4`) |

## Cómo se produce un veredicto de dry-run

1. Un agente recibe sólo la skill (`.omp/skills/specification/`), la gobernanza y la fixture, y tiene prohibido leer `expected/`, `run.py` y los veredictos de otros casos.
2. Aplica la metodología y escribe `dryrun/T##.json` según `VERDICT_SCHEMA.md`. En T15 escribe sus preguntas **antes** de consultar `fixtures/T15-stakeholder-oracle.md`, que hace de stakeholder.
3. `run.py` compara el veredicto con las aserciones de `expected/T##.json`.

## Límites

- Los veredictos de `DRYRUN` son la salida de **una** ejecución de un modelo, registrada. Reproducir el resultado exige volver a ejecutar el dry-run; la comparación sí es determinista. Un modelo distinto, u otra ejecución, puede producir otro veredicto: eso es exactamente lo que estas pruebas detectan.
- El aislamiento del agente respecto a `expected/` es por instrucción, no técnico.
- `MECHANICAL` no evalúa semántica: C2 sólo prueba que los IDs existen, y una señal léxica no es un `FAIL` de SQ5 por sí sola. La coherencia y la materialidad siguen siendo juicio registrado.
- Las fixtures son sintéticas. No sustituyen la observación de la Línea 1 en trabajo real (`USE GRADUALLY. OBSERVE REAL BEHAVIOR. EVOLVE FROM EVIDENCE.`).
