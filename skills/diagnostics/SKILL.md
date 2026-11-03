---
name: diagnostics
description: Metodología causal, basada en evidencia, para determinar por qué ocurrió un fallo, bug o incidente ya observado — o para demostrar con precisión qué evidencia falta para determinarlo responsablemente. Parte siempre de un fallo observado, nunca de una pregunta sobre cómo funciona un sistema. Úsalo cuando se pida diagnosticar un error, investigar la causa raíz de un fallo, entender por qué algo se rompió, o mediante invocación explícita (`/skill:diagnostics`). No es el modo normal de trabajo del workspace — no se activa para entender cómo funciona un sistema sin que haya un fallo observado (eso es `technical-discovery`), para decidir qué debería hacer el sistema (`specification`), para ejecutar un fix ya autorizado (`implementation`), ni para revisar cumplimiento de un cambio (`governance-review`). No parchea automáticamente lo que encuentra.
---

# Diagnostics

Este skill es un **método de diagnóstico causal** — no un workflow de producto, no una auditoría, y no una vía directa a la corrección. Dado un fallo observado, obtiene evidencia suficiente para explicar su causa, o declara honestamente que la evidencia disponible no alcanza.

## 0. Activation contract

**Diagnostics parte siempre de un fallo observado.** Sin un fallo concreto ya observado, este skill no aplica.

Cuenta como fallo observado: un error, una anomalía, un comportamiento inesperado, una divergencia entre real y esperado, un test que falla, un fallo de runtime, una anomalía de datos/estado, o un incidente concreto.

La frontera con `technical-discovery` se decide por la pregunta principal:

| Pregunta principal | Capability |
|---|---|
| `¿Cómo funciona esto actualmente?` | `technical-discovery` |
| `¿Por qué ocurrió este fallo observado?` | `diagnostics` |

Diagnostics **MUST NOT** usarse como sustituto de technical discovery. Si aún no hay un fallo que explicar, lo que hace falta es reconstruir el `CURRENT_STATE`, no diagnosticar. Diagnostics puede *consumir* discovery previo; no lo reemplaza ni lo ejecuta por su cuenta a escala de sistema (§5).

Tampoco lo actives para: decidir qué debería hacer el sistema (`specification`), ejecutar una corrección ya autorizada (`implementation`), o revisar cumplimiento de gobernanza de un cambio (`governance-review`). No lo uses como excusa para parchear de inmediato un síntoma — ver §9 (`REMEDIATION_BOUNDARY`).

## 0.1 Contrato obligatorio de cierre

> **Un diagnóstico está completo sólo cuando demuestra la causa con evidencia suficiente, o demuestra con precisión por qué la evidencia disponible no permite determinarla.**

Toda ejecución termina cumpliendo **A** o **B**:

- **A — Causa demostrada.** Mecanismo causal explicado y respaldado, y su relación con el fallo concreto establecida al nivel de confianza declarado (§8).
- **B — Brecha de evidencia demostrada.** Qué hipótesis siguen vivas, qué observación concreta las discriminaría, y por qué esa observación no está razonablemente disponible.

**B no es un fracaso.** Es un resultado de primera clase.

Un diagnóstico **MUST NOT** cerrarse únicamente porque: se investigó mucho · se encontró algo raro · se reprodujo un fallo compatible · apareció un archivo sospechoso · un test pasó · una explicación "parece probable".

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE       (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE   (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → DIAGNOSTICS           (este skill)
      → consumidor          (implementation / specification / decisión humana)
```

No es gobernanza independiente ni tiene autoridad de decisión propia. No contradice los invariantes de autoridad del workspace (`ENGINEERING_GOVERNANCE.md` §1, §2, §16). Su resultado (causa raíz, impacto, fix boundary) es evidencia que otro proceso puede consumir — no invoca automáticamente `implementation` ni ninguna corrección. Es executor-neutral, igual que `technical-discovery`.

## 2. Pregunta gobernante

`¿Por qué ocurrió este fallo observado?`

Distinta de la de `technical-discovery` (`¿cómo funciona realmente esto?`), de `specification` (`¿qué debería hacer el sistema?`), de `implementation` (`ejecuta el cambio ya delimitado`) y de review (`¿el cambio cumple?`). Diagnostics puede consumir hallazgos de `technical-discovery` sobre cómo funciona el sistema, pero su objetivo propio es siempre causal: explicar un fallo, no describir un funcionamiento.

## 3. Invariantes diagnósticos

1. **`SYMPTOM != ROOT_CAUSE`** — el fallo observable es punto de partida, no explicación causal.
2. **`ERROR_LOCATION != ROOT_CAUSE`** — la línea que lanza la excepción no demuestra por sí sola dónde nació el defecto.
3. **`PROXIMITY != CAUSALITY`** — cercanía temporal, espacial, de archivo o de stack trace no demuestra causalidad.
4. **`RECENT_CHANGE != ROOT_CAUSE`** — un cambio reciente eleva una hipótesis; no la convierte en conclusión.
5. **`CORRELATION != CAUSATION`**.
6. **`TEST_GREEN != RUNTIME_CORRECT`** — tests verdes son evidencia de lo que realmente ejercitan, no del comportamiento real completo.
7. **`LOG_MESSAGE != TRUTH`** y **`LOG_MESSAGE != SYSTEM_STATE`** — un log es evidencia de lo que el sistema reportó, no autoridad infalible sobre la causa ni descripción fiable del estado real en ese momento.
8. **Reproducción es evidencia, no dogma** — la reproducción controlada es evidencia de alto valor cuando es razonablemente posible y segura, pero no es condición obligatoria para toda causa raíz.
9. **No patch before causal evidence** — no se pasa automáticamente del síntoma a una modificación. Un cambio exploratorio sólo se ejecuta con autorización explícita y se mantiene semánticamente separado de una corrección confirmada (§9).
10. **Evidence before inference** — nunca presentar una inferencia como hecho observado. Lo que es razonablemente observable con las herramientas disponibles se **observa**, no se razona (§4.3).
11. **Un hallazgo adyacente no expande automáticamente el alcance del diagnóstico** — se reporta, no se persigue (§11).
12. **`FAILURE_LOCATION != FAULT_DOMAIN`** — el archivo, componente o línea donde el fallo se hace visible no es automáticamente el propietario causal del defecto (§4.1).
13. **`COMPATIBLE_EXPLANATION != INCIDENT_ATTRIBUTION`** — demostrar que un mecanismo *puede* producir el síntoma no demuestra que produjo **este** incidente. Son dos afirmaciones distintas y requieren evidencia distinta (§8.1).
14. **`REPRODUCED_MECHANISM != HISTORICAL_PROOF`** — reproducir el fallo hoy demuestra que el mecanismo existe y es capaz de producirlo; no demuestra por sí solo que ése fue el mecanismo que actuó en la ocurrencia histórica diagnosticada.
15. **`SUPPORTED != CONFIRMED`** — evidencia compatible con una hipótesis no la confirma mientras no haya discriminado a sus competidoras (`references/hypothesis-driven-diagnosis.md`).
16. **Anti-supuestos de baseline** (§4.2) — **`SOURCE_CODE_CURRENT != RUNTIME_DEPLOYED`** · **`CONFIG_PRESENT != CONFIG_LOADED`** · **`SCHEMA_LOCAL != SCHEMA_EXPECTED_BY_CODE`**.
17. **No mutar para teorizar** — no se modifica un componente sospechoso únicamente para probar una teoría cuando existe una forma observacional o controlada de discriminarla. Mutar es el último recurso, no el primero, y requiere autorización cuando toca estado real (§9, §13).
18. **Continuity over perfection** — el diagnóstico busca evidencia causal *suficiente* para habilitar la siguiente decisión segura; no necesita agotar toda incógnita relacionada. Suficiencia causal prevalece sobre comprensión exhaustiva cuando las incógnitas restantes no afectan materialmente la siguiente decisión — esto no es una licencia para relajar evidencia, es un límite de alcance.

## 4. Modelo de evidencia

Reutiliza sin modificar la taxonomía epistemológica de `technical-discovery` (`skill://technical-discovery/SKILL.md` §5): `FACT` · `INFERENCE` · `HYPOTHESIS` · `DECLARED_INTENT` · `UNKNOWN` · `CONTRADICTION`.

Diagnostics añade una **dimensión causal distinta**, que no se mezcla con la anterior:

| Categoría | Significa |
|---|---|
| `SYMPTOM` | El comportamiento/fallo observable que motiva el diagnóstico. |
| `TRIGGER` | El evento inmediato que activó el fallo. |
| `CONTRIBUTING_FACTOR` | Una condición que facilitó o amplificó el incidente pero que, por sí sola, no explica completamente la causa. |
| `ROOT_CAUSE` | La condición causal cuya presencia explica el fallo y cuya ausencia lo habría evitado dentro del scope analizado; su corrección/remoción evita razonablemente la recurrencia dentro del boundary analizado. |

No fuerces que todo diagnóstico tenga las cuatro categorías causales, y no inventes `TRIGGER` o `CONTRIBUTING_FACTOR` sólo para llenar el formato — omítelos cuando la evidencia no los sostenga.

### 4.1 Failure boundary, first divergence y fault domain

Tres conceptos distintos que **no** deben fusionarse:

| Concepto | Responde | Qué es |
|---|---|---|
| `FAILURE_BOUNDARY` | ¿Dónde se hace **visible** el fallo? | Primer límite observable donde el sistema deja de cumplir el comportamiento esperado. |
| `FIRST_DIVERGENCE` | ¿Dónde empieza a **desviarse**? | Primer punto observable donde el comportamiento real se separa del esperado, del contrato aplicable, del estado válido esperado, de una referencia comparable, o de un input/output previo conocido. |
| `FAULT_DOMAIN` | ¿Dónde **vive la causa**? | Componente, subsistema, configuración, estado o dependencia donde reside causalmente el defecto o la condición que origina el fallo. |

Buscar `FIRST_DIVERGENCE` cuando sea razonablemente posible: acota la cadena causal y suele estar aguas arriba del `FAILURE_BOUNDARY`. **Encontrar `FIRST_DIVERGENCE` no equivale a encontrar `ROOT_CAUSE`** — es un delimitador, no una conclusión.

El `FAULT_DOMAIN` se determina con evidencia de mecanismo, nunca por proximidad al síntoma (§3.2, §3.3, §3.12).

### 4.2 Baseline de realidad

Cuando una diferencia en estos campos pueda **cambiar materialmente la conclusión**, el baseline correspondiente debe establecerse con evidencia antes de concluir. Proporcional: no todos los campos aplican a todo diagnóstico, y un bug local determinista no necesita ninguno.

Para `INCIDENT_DIAGNOSIS`, evalúa: versión del código fuente · branch/HEAD cuando exista Git aplicable (`RULES.md` reglas 13 y 18: baseline por repositorio, nunca mezclado) · versión realmente desplegada en runtime · configuración efectiva · estado de datos relevante · estado del schema · entorno · identidad de ejecución/request/job · timestamp o intervalo relevante.

Anti-supuestos que este baseline existe para evitar (§3.16):

- **`SOURCE_CODE_CURRENT != RUNTIME_DEPLOYED`** — el código que lees no es necesariamente el que se ejecutó.
- **`CONFIG_PRESENT != CONFIG_LOADED`** — que un valor exista en un archivo o template no prueba que el proceso lo cargó.
- **`SCHEMA_LOCAL != SCHEMA_EXPECTED_BY_CODE`** — el schema local/migrado no es necesariamente el que el código asume ni el que el entorno del fallo tenía.

Si un baseline material no puede establecerse, eso no se rellena por inferencia: se declara `UNKNOWN` y se evalúa su impacto en el resultado (§8).

### 4.3 Disciplina de evidencia

Lo razonablemente observable se **observa**. No sustituyas una observación disponible por razonamiento (§3.10). Según aplique y esté disponible: Git (branch, HEAD, historia, diff acotados — §12) · filesystem (archivos y configuración declarada) · búsqueda de código/LSP (símbolos, callers, usos) · test runner (reproducción controlada) · consultas de sólo lectura a datos/schema · herramientas de runtime/cloud (artefacto desplegado, configuración efectiva, estado) · logs (evidencia temporal del evento) · tooling de build/dependencias.

Nunca inventes evidencia que no obtuviste. Una observación que no pudiste hacer es un `UNKNOWN`, no una suposición.

### 4.4 Cadena causal

Cuando la evidencia lo permita, reconstruye:

```
SYMPTOM → FIRST_DIVERGENCE → FAILURE_MECHANISM → NECESSARY_CONDITION → CAUSAL_ORIGIN → ROOT_CAUSE
```

| Elemento | Significa |
|---|---|
| `SYMPTOM` | Lo observado. |
| `FIRST_DIVERGENCE` | Primer punto conocido donde real y esperado divergen (§4.1). |
| `FAILURE_MECHANISM` | El proceso técnico concreto por el cual el estado defectuoso produce el síntoma. Es el núcleo explicativo: sin mecanismo no hay diagnóstico, sólo correlación. |
| `NECESSARY_CONDITION` | Condición necesaria para que ese mecanismo ocurra, cuando pueda determinarse. |
| `CAUSAL_ORIGIN` | Evento, estado o decisión operacional que introdujo la condición causal. |
| `ROOT_CAUSE` | Causa suficientemente profunda cuya presencia explica el fallo observado y cuya ausencia lo habría evitado dentro del scope analizado. |

**No exijas artificialmente todos los niveles.** Cuando la evidencia no permita determinar uno, se omite o se marca `UNKNOWN` — **MUST NOT** inventarse para completar una plantilla. Un `FAILURE_MECHANISM` demostrado con `CAUSAL_ORIGIN` desconocido es un resultado honesto y frecuentemente suficiente.

### 4.5 Dominio causal

Cuando la evidencia permita clasificar, declara el dominio donde reside la causa:

`CODE_DEFECT` · `DATA_STATE` · `CONFIGURATION` · `ENVIRONMENT` · `DEPENDENCY` · `SCHEMA_DRIFT` · `DEPLOYMENT_DRIFT` · `PERMISSION_OR_CREDENTIAL` · `CONTRACT_MISMATCH` · `TIMING_OR_CONCURRENCY` · `UNKNOWN`

**La clasificación describe el dominio; NO sustituye la explicación causal concreta.**

```
INVÁLIDO:  ROOT_CAUSE: CONFIGURATION

VÁLIDO:    DOMAIN: CONFIGURATION
           ROOT_CAUSE: <explicación causal específica, con el mecanismo
                        y la evidencia que la sostiene>
```

Un `DOMAIN` sin `ROOT_CAUSE` explicado es una etiqueta, no un diagnóstico.

## 5. Escalas — controlan formalidad y alcance

| Escala | Uso | Notas |
|---|---|---|
| `TARGETED_DIAGNOSIS` (default) | Error suficientemente delimitado: excepción, query fallida, test roto, dato incorrecto, configuración puntual, error reproducible localizado. | La mayoría de diagnósticos caen aquí. |
| `FLOW_DIAGNOSIS` | Fallo cuyo síntoma atraviesa varias capas/componentes (productor → artefacto → consumidor; API → aplicación → persistencia; pipeline multietapa). | Traza verticalmente el camino real; no lee el repositorio horizontalmente. |
| `INCIDENT_DIAGNOSIS` | Fallo operacional o distribuido: deploy, CI/CD, cloud, colas, contenedores, networking, retries, timeouts, race conditions, eventual consistency, configuration drift. | Ver `references/distributed-and-ci-incidents.md`. |

**No existe `SYSTEM_DIAGNOSIS`.** Si la pregunta requiere comprender globalmente un sistema antes de poder siquiera formular un fallo causal concreto, esa necesidad pertenece a `technical-discovery` — no se absorbe aquí.

**No escales `TARGETED → FLOW → INCIDENT` automáticamente.** Empieza en la escala que el fallo delimitado justifica. La escala sólo se amplía cuando la evidencia demuestra que la causa **no puede determinarse dentro de la frontera actual** — y ese ensanchamiento se declara explícitamente, con la evidencia que lo motivó. Ampliar por comodidad, por exhaustividad o "por si acaso" es scope expansion silencioso (§11, `RULES.md` regla 5).

La formalidad es proporcional a incertidumbre, impacto, número de componentes, costo/riesgo de experimentar, y costo de una conclusión equivocada. Un bug trivial no exige la ceremonia de un incidente.

## 6. Lifecycle (proporcional, no checklist obligatorio)

```
 1. Establecer el fallo observado                       (§0 activation contract)
 2. Establecer el comportamiento esperado               (cuando defina la desviación)
 3. Establecer el baseline de realidad material         (§4.2)
 4. Establecer el failure boundary / last known-good    (§4.1)
 5. Localizar la first divergence cuando sea posible    (§4.1)
 6. Trazar el camino que falla, verticalmente
 7. Generar las hipótesis mínimas necesarias            (§7)
 8. Buscar evidencia discriminante                      (§7)
 9. Falsificar explicaciones competidoras si es material
10. Explicar el failure mechanism                       (§4.4)
11. Determinar el fault domain                          (§4.1)
12. Reconstruir la cadena causal hasta donde llegue     (§4.4)
13. Clasificar el dominio causal cuando aporte          (§4.5)
14. Establecer mechanism confidence e incident attribution (§8.1)
15. Determinar el boundary de impacto
16. Determinar el fault owner y el fix boundary         (§9)
17. Detenerse antes de remediation no autorizada        (§9, §13)
18. Cerrar cumpliendo A o B del contrato obligatorio    (§0.1)
```

No todas las etapas requieren igual profundidad — la escala (§5) decide cuánto peso recibe cada una. Una explicación verificable de forma determinista y directa no requiere múltiples hipótesis (§7, `hypothesis-driven-diagnosis.md`).

**La numeración es un orden causal, no un protocolo secuencial.** Las etapas 3-6 son en su mayoría independientes entre sí: el baseline, el failure boundary y el camino que falla se establecen con observaciones que no dependen unas de otras. Recolectarlas de una en una, esperando cada resultado antes de pedir el siguiente, multiplica el tiempo del diagnóstico sin añadir una sola conclusión.

### 6.1 Recolección de evidencia — eficiencia

`EVIDENCE_QUALITY != NUMBER_OF_ROUND_TRIPS`. Un diagnóstico bien hecho no es uno lento.

1. **Agrupa las observaciones independientes en una sola tanda.** Si el siguiente comando no depende del resultado del anterior, van juntos. Baseline Git, estado de servicios, versión efectiva, logs del intervalo y contenido de los archivos sospechosos son, casi siempre, independientes entre sí. Encadena en serie sólo cuando una observación *determina cuál es* la siguiente.

2. **Empieza por la observación de mayor poder discriminante, no por la más cómoda.** La pregunta rectora es §7: *¿qué observación daría resultados distintos según qué hipótesis sea cierta?* Recolectar contexto abundante y poco discriminante es trabajo que no cierra el diagnóstico.

3. **Cierra en cuanto la evidencia sea suficiente.** El contrato (§0.1) exige demostrar la causa o demostrar qué falta — no agotar el espacio de observación. Seguir recolectando después de tener mecanismo y atribución es ceremonia (§15).

4. **Usa el parámetro `cwd` de la tool `bash`, nunca `cd <repo> && <cmd>`.** Un comando compuesto no pregunta por sí mismo: una cadena plana de `&&` se auto-aprueba si ningún segmento ni la cadena completa alcanza un gate. Pero `cd` es un builtin que cambia el estado del shell y saca la cadena de la vía por segmentos: los allows de patrón dejan de aplicar, así que una excepción como `rm -rf dist` pregunta tras `cd x &&`. El comando, su alcance y su gate son idénticos por ambas vías. Semántica completa: MANUAL §23 (*Comandos compuestos*) y `.omp/AGENTS.md` §10.

5. **Prefiere la tool dedicada cuando exista.** `read`, `grep`, `glob` y `ast_grep` devuelven resultados estructurados y no pasan por el gate de `bash`.

6. **Si un comando pide aprobación, no busques un rodeo.** Repórtalo como hecho y continúa cuando se apruebe. Reescribir la operación para eludir el gate está prohibido (`RULES.md` regla 19, `ENGINEERING_GOVERNANCE.md` §17.8) — y la mayoría de las veces el prompt significa que la operación no era observacional.

Nada de esto relaja §3.17 (observar antes que mutar), §10 (preservar evidencia antes de mutar) ni §13 (STOP conditions). La eficiencia es sobre *cómo* se recoge la evidencia observacional, nunca sobre ampliar qué se permite ejecutar.

## 7. Evidencia discriminante, no confirmación

Cuando exista incertidumbre material, las hipótesis relevantes deben hacerse **explícitas**, con estado declarado: `OPEN` · `SUPPORTED` · `REJECTED` · `CONFIRMED` · `UNTESTABLE`.

La metodología favorece preguntas del tipo *"¿qué observación daría resultados distintos si H1 fuera cierta frente a H2?"* — no *"formular H1 y buscar sólo evidencia que la confirme"*. Prefiere siempre evidencia que **discrimine** entre hipótesis competidoras sobre evidencia meramente compatible con todas ellas.

`SUPPORTED` **MUST NOT** promoverse a `CONFIRMED` sin evidencia discriminante suficiente (§3.15). No se asignan porcentajes ni scores probabilísticos.

Ver `references/hypothesis-driven-diagnosis.md` para la técnica completa (estructura del ledger, sesgos a evitar, selección de experimentos seguros).

## 8. Confianza de causa raíz — únicos resultados terminales

Todo resultado se sostiene sobre **dos** afirmaciones distintas (§8.1). Los tres resultados terminales son:

**`ROOT_CAUSE_CONFIRMED`** — existe evidencia suficiente para demostrar **ambas** cosas:
1. el mecanismo causal (`FAILURE_MECHANISM`, §4.4), y
2. su relación con el fallo o incidente concreto diagnosticado.

**MUST NOT** declararse mientras la atribución al incidente siga siendo inferida. Mecanismo demostrado + atribución inferida es `ROOT_CAUSE_HIGH_CONFIDENCE`, no `CONFIRMED`.

**`ROOT_CAUSE_HIGH_CONFIDENCE`** — el mecanismo causal está demostrado y la evidencia disponible apunta fuertemente a que explica el incidente, pero falta una pieza de atribución directa que no pudo obtenerse razonablemente (inaccesible, excesivamente costosa, insegura o destructiva de evidencia). Es el cierre honesto cuando el mecanismo es sólido pero el vínculo con la ocurrencia concreta no es directamente observable.

**`INSUFFICIENT_EVIDENCE`** — no hay evidencia suficiente para distinguir responsablemente entre las hipótesis relevantes restantes, o para atribuir la causa al incidente. Elegir una explicación sería especulativo.

`INSUFFICIENT_EVIDENCE` es un **resultado válido, no un fracaso**. Cumple la obligación B del contrato de cierre (§0.1) siempre que declare qué hipótesis siguen vivas, qué observación las discriminaría y por qué no está disponible. Nunca se fuerza una causa para producir una respuesta más satisfactoria.

No se usan porcentajes ni scoring probabilístico de confianza.

### 8.1 Mechanism confidence vs. incident attribution

Son dos dimensiones independientes:

| Dimensión | Pregunta |
|---|---|
| `MECHANISM_CONFIDENCE` | ¿Está demostrado que este mecanismo produce este síntoma? |
| `INCIDENT_ATTRIBUTION_CONFIDENCE` | ¿Está demostrado que este mecanismo produjo **esta** ocurrencia? |

Cuando ambas difieran materialmente, el informe **MUST** declararlas por separado:

```
MECHANISM_CONFIDENCE: CONFIRMED
INCIDENT_ATTRIBUTION_CONFIDENCE: HIGH
RESULT: ROOT_CAUSE_HIGH_CONFIDENCE
```

Cuando no aporte información — mecanismo y atribución sostenidos por la misma evidencia — no impongas la doble dimensión: declara sólo `RESULT`.

Evidencia típica de atribución (no de mecanismo): correlation/execution IDs que atan el evento al incidente, timestamps dentro del intervalo del fallo, identidad de ejecución, estado observado en el momento del incidente, configuración efectiva de esa ejecución concreta. Ver `references/distributed-and-ci-incidents.md`.

## 9. Remediation boundary

**`DIAGNOSIS != REMEDIATION`.** Diagnostics termina conceptualmente en `ROOT_CAUSE` · `FAULT_OWNER` · `IMPACT` · `FIX_BOUNDARY`. Puede producir `RECOMMENDED_REMEDIATION`, pero esa sección es una **propuesta**, no una autorización de implementación — diagnóstico e implementación son fases separadas.

Cuando la evidencia lo sostenga, el resultado señala:

| Campo | Qué es | Qué NO es |
|---|---|---|
| `FAULT_OWNER` | Componente, subsistema, configuración o entorno que **posee causalmente** el problema (§4.1, `FAULT_DOMAIN`). | Un owner humano o equipo, salvo que eso sea conocido y verificable. |
| `FIX_BOUNDARY` | Frontera donde tendría que ocurrir una corrección posterior. | Autorización para implementarla, ni delimitación de un scope ya aprobado. |

Durante un diagnóstico **MUST NOT** modificarse código, tests, configuración, schemas, infraestructura, datos ni estado de deployment para aplicar un fix, salvo autorización humana explícita y separada. Tampoco se modifica un componente sospechoso sólo para comprobar una hipótesis cuando existe una forma observacional o controlada de discriminarla (§3.17). Una reproducción controlada puede usar mecanismos no destructivos compatibles con la gobernanza.

Si la reparación implica decisiones de arquitectura, contrato, API, schema, persistencia, infraestructura, seguridad, lifecycle, compatibilidad, negocio, scope o deuda técnica aceptada, y esa decisión no está ya cerrada, produce `DECISION_REQUIRED` (`ENGINEERING_GOVERNANCE.md` §1.4). Si el fix es táctico, inequívoco, y ya existe autorización explícita para modificar, puede delegarse después a `implementation` — este skill, por sí mismo, no concede esa autorización.

## 10. Preservar evidencia antes de mutar

Antes de reproducir, restart, redeploy, retry, requeue, rollback, limpiar cache, truncar, borrar o resetear cualquier estado relevante: evalúa si la operación destruiría evidencia todavía necesaria. Si hay riesgo material, recopila esa evidencia primero, o detente si la operación no está autorizada (§13, condiciones 1–3). Ver `references/runtime-and-logs.md` para la política completa.

## 11. Hallazgos adyacentes — anti scope creep

Un diagnóstico **MUST NOT** ampliarse automáticamente por encontrar: deuda técnica · anomalías adyacentes · errores no causales · configuraciones cuestionables · tests débiles · oportunidades de refactor · otros incidentes.

Estos hallazgos **pueden reportarse** cuando sean relevantes, pero sólo se **incorporan** al diagnóstico si:

1. pueden explicar materialmente el fallo investigado, o
2. son necesarios para discriminar entre hipótesis vivas.

Fuera de esos dos casos, se reportan y permanecen intactos (`RULES.md` regla 5; `ENGINEERING_GOVERNANCE.md` §9.4). Encontrar algo mejorable nunca es autorización para perseguirlo ni para corregirlo.

## 12. Historial (Git) — acotado, no arqueología horizontal

Patrón: `failure boundary → archivo/símbolo/configuración relevante → git log/blame/show acotado a esa frontera`. Nunca archaeology horizontal de todo el repositorio por defecto. Un commit reciente no demuestra `ROOT_CAUSE` sin evidencia adicional (§3.4). Para la técnica de consulta acotada, reutiliza `skill://technical-discovery/references/history-and-archaeology.md` — mismo principio ("el historial explica procedencia, no reemplaza la verdad ejecutable actual"), aplicado aquí a delimitar el failure boundary en vez de a explicar arquitectura.

## 13. STOP conditions

Detente en la parte afectada — sin improvisar, preservando lo ya establecido, recopilando evidencia disponible, explicando la dependencia/contradicción exacta y qué evidencia/acceso/decisión permitiría continuar — cuando:

1. continuar o "probar" una hipótesis requeriría destruir evidencia todavía necesaria;
2. sería necesario modificar producción únicamente para demostrar una hipótesis y no hay autorización explícita;
3. la siguiente acción es destructiva/mutante y carece de autorización;
4. existen evidencias materiales que sostienen causas incompatibles y no hay forma accesible/segura de discriminarlas;
5. la causa no puede determinarse responsablemente con la evidencia accesible;
6. continuar requiere credenciales, permisos, acceso, datos o infraestructura no disponibles;
7. el diagnóstico alcanza una decisión de arquitectura/producto/contrato/scope no cerrada humanamente;
8. continuar exigiría inventar configuración, valores, estado o comportamiento;
9. la única forma aparente de continuar implica modificar un componente fuera de alcance.

## 14. Progressive disclosure — qué cargar y cuándo

| Escala | Cargar |
|---|---|
| `TARGETED_DIAGNOSIS` | `SKILL.md`; la reference asociada al tipo de fallo sólo si aporta valor concreto. |
| `FLOW_DIAGNOSIS` | `SKILL.md`; `hypothesis-driven-diagnosis.md` cuando existan explicaciones alternativas; `runtime-and-logs.md`/`data-and-state-diagnosis.md` según por dónde pasa el flujo. |
| `INCIDENT_DIAGNOSIS` | `SKILL.md`; `distributed-and-ci-incidents.md`; `runtime-and-logs.md`; otras sólo si el incidente cruza esas fronteras. |

No cargues las cuatro referencias en cada diagnóstico.

## 15. Output contract

`RESULT` (`ROOT_CAUSE_CONFIRMED`/`ROOT_CAUSE_HIGH_CONFIDENCE`/`INSUFFICIENT_EVIDENCE`) · `SYMPTOM` · `OBSERVED_BEHAVIOR` · `EXPECTED_BEHAVIOR` · `BASELINE` · `FAILURE_BOUNDARY` · `FIRST_DIVERGENCE` · `FAULT_DOMAIN` · `FACTS` · `HYPOTHESES` · `EVIDENCE` · `CONTRADICTIONS` · `FAILURE_MECHANISM` · `NECESSARY_CONDITION` · `CAUSAL_ORIGIN` · `ROOT_CAUSE` · `DOMAIN` · `TRIGGER` · `CONTRIBUTING_FACTORS` · `MECHANISM_CONFIDENCE` · `INCIDENT_ATTRIBUTION_CONFIDENCE` · `IMPACT` · `FAULT_OWNER` · `FIX_BOUNDARY` · `RECOMMENDED_REMEDIATION` · `DECISIONS_REQUIRED` · `UNKNOWNS` · `MISSING_EVIDENCE` · `NEXT_ACTION`.

Ninguna sección es obligatoria salvo `RESULT` cuando el diagnóstico llega a un cierre. Omite lo que no aplique — `HYPOTHESES` no hace falta cuando no fue necesario formular alternativas; `MECHANISM_CONFIDENCE`/`INCIDENT_ATTRIBUTION_CONFIDENCE` sólo cuando difieran materialmente (§8.1); no fabriques categorías vacías para completar la plantilla. El resultado debe ser compacto y verificable, no ceremonial.

**Excepción:** cuando `RESULT` es `INSUFFICIENT_EVIDENCE`, `MISSING_EVIDENCE` es obligatorio — es lo que convierte ese resultado en el cierre honesto de la obligación B (§0.1) y no en un abandono. Debe nombrar las hipótesis vivas, la observación que las discriminaría y por qué no está razonablemente disponible.
