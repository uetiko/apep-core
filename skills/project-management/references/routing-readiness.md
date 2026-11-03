# Readiness direccional y routing

Referencia del modo *work item* de `project-management` (`SKILL.md` §6). Responde: ¿está el trabajo listo para **lo siguiente**, y qué es lo siguiente?

```
READY MEANS READY FOR THE NEXT CAPABILITY,
NOT READY FOR EVERYTHING.

READY != EXECUTION_READY
READY != AUTHORIZED_TO_EXECUTE
```

## 1. Readiness con destino

`READY` sin destino no significa nada útil: casi todo está listo para algo y casi nada está listo para todo. El readiness se evalúa **respecto de la siguiente capability**:

```
READINESS_CHECK
  READY:                      YES | NO | PARTIAL
  NEXT_CAPABILITY:            project-management | technical-discovery | diagnostics | specification
                              | architecture-review | implementation | review | integration | NONE
  READY_FOR_NEXT_CAPABILITY:  YES | NO
  OPEN:                       <aperturas que son el trabajo de la siguiente capability> | NONE
  BLOCKERS:                   NONE | <tipo · alcance, dependency-model.md §3>
  REASON:                     <por qué>
```

- `NEXT_CAPABILITY` es la capability que **puede empezar ahora**, no la que probablemente vendrá después (`NEXT_CAPABILITY != EVENTUAL_CAPABILITY`).
- `READY_FOR_NEXT_CAPABILITY: YES` significa que esa capability puede empezar ahora con la información que necesita. La única excepción es la autorización de ejecución hacia `implementation`, que es un gate aparte (§2).
- `READY: PARTIAL` cuando una parte del item puede avanzar y otra no; `BLOCKERS` dice cuál, y la ruta dice qué parte avanza (`BLOCKING_SCOPE`, §3).
- `OPEN` **no** son blockers. Son las aperturas que la siguiente capability existe para cerrar.

Ejemplo:

```
READY:                      YES
NEXT_CAPABILITY:            specification
READY_FOR_NEXT_CAPABILITY:  YES
OPEN:                       semántica de retención · comportamiento de autorización
BLOCKERS:                   NONE
REASON:                     el resultado buscado y el owner están claros; lo que falta es comportamiento, que es lo que specification resuelve
```

Las aperturas de retención y autorización no bloquean la entrada a `specification`: son su trabajo (Línea 1).

## 2. Qué exige cada destino

| Destino | Listo cuando | **No** exige |
|---|---|---|
| `technical-discovery` | Hay una pregunta concreta sobre el `CURRENT_STATE` y el sistema o repositorio es accesible | Saber qué se va a cambiar |
| `diagnostics` | Hay un fallo observado concreto (qué, dónde, cuándo, esperado frente a real). "Dónde" puede ser una superficie que el propio diagnóstico localiza o reproduce con la evidencia accesible | Hipótesis de causa |
| `specification` | El resultado buscado es entendible, hay un owner o contexto identificable que pueda responder clarificaciones, el alcance inicial basta para empezar, y ninguna contradicción impide saber qué se intenta resolver | AC completos, casos límite, Execution Contract, ambigüedad cero, decisiones cerradas |
| `architecture-review` | Hay un cambio o estado concreto y una pregunta arquitectónica (fronteras, contratos, dependencias) | Una arquitectura alternativa |
| `implementation` | Existe un contrato autocontenido: `EXECUTION_READY` en `FORMAL`, o el task contract ligero en `NONE`/`LIGHT` (objetivo, alcance, AC, rama) que recoge el encargo y las decisiones ya cerradas por el humano. El alcance está **delimitado**: quien implementa puede descubrir dónde cambiar el sistema, pero no elegir a qué superficie de producto material se refería el pedido. PM comprueba que existe; no lo produce ni lo completa con decisiones propias (`SKILL.md` §1) | Autorización: se registra aparte (abajo) · conocer el archivo o componente exacto |
| `review` | Hay una implementación verificada y una pregunta de review que la justifique | Que la implementación esté perfecta |
| `integration` | Implementación verificada, reviews suficientes, commit/PR preparados | Merge (es humano) |

**Readiness hacia `implementation` y autorización son cosas distintas** (`READY != AUTHORIZED_TO_EXECUTE`). Con el contrato completo, `READY_FOR_NEXT_CAPABILITY: YES` aunque falte la autorización. La autorización que falta se registra como `AUTHORIZATION_DEPENDENCY` y blocker `BLOCKED_BY_AUTHORIZATION` sobre la ejecución (`dependency-model.md`), no como falta de readiness. Si el contrato no está completo (p. ej. una Hard Specification aprobada que todavía no es `EXECUTION_READY`), el item no está listo para `implementation`: está listo, en todo caso, para seguir en `specification`.

Un item que ya es `EXECUTION_READY` **no vuelve** a `specification` sin evidencia nueva (una contradicción, un cambio de alcance, un hecho que invalida una decisión). Una tarea ya apta para implementación no se expande con PM ceremonial: el readiness cabe en dos líneas.

## 3. `ROUTING_RECOMMENDATION`

```
ROUTING_RECOMMENDATION
  NEXT_CAPABILITY:        <capability que puede empezar ahora>
  WHY:                    <la razón, en una línea>
  PREREQUISITES:          NONE | <condición para empezar NEXT · SATISFIED>
  THEN:                   NONE | <capability que espera el resultado de NEXT>
  PARALLEL_CAPABILITIES:  NONE | <capability que avanza a la vez sin impedir que NEXT empiece>
  BLOCKING_SCOPE:         NONE | <qué parte de NEXT espera a la paralela · qué parte avanza ya>
  BLOCKED_CAPABILITIES:   NONE | <capability que no puede empezar por otra causa, y cuál>
```

```
IF A MUST FINISH BEFORE B CAN START, THEN B IS NOT THE IMMEDIATE NEXT CAPABILITY.
READY FOR B MEANS B CAN ACTUALLY START NOW.
PREREQUISITE != PARALLEL_SUPPORT.
```

| Campo | Qué es | Qué **no** es |
|---|---|---|
| `PREREQUISITES` | Condiciones que deben cumplirse **antes** de que NEXT empiece. Con NEXT listo, todas están satisfechas | Trabajo de la propia NEXT, trabajo opcional o en paralelo, la autorización de ejecución (es un blocker, §2) |
| `THEN` | Lo que vendrá cuando NEXT termine | Una capability lista ahora |
| `PARALLEL_CAPABILITIES` + `BLOCKING_SCOPE` | Trabajo que corre a la vez porque NEXT puede empezar sin él; `BLOCKING_SCOPE` dice qué parte de NEXT lo espera y qué parte avanza | Un prerequisito: si NEXT no puede empezar sin él, no es paralelo |
| `BLOCKED_CAPABILITIES` | Lo que no puede empezar por otra causa: falta de contrato, decisión, autorización | Lo que simplemente viene después de NEXT (eso es `THEN`) |

**Coherencia.** Los campos de readiness y de ruta describen una sola realidad:

- Un prerequisito **insatisfecho** de B nunca convive con `NEXT_CAPABILITY: B` y `READY_FOR_NEXT_CAPABILITY: YES`. Si lo resuelve otra capability A, la ruta es `NEXT: A · THEN: B`. Si sólo puede resolverlo una persona (una decisión, un dato que nadie más tiene), es `DECISION_REQUIRED` o un blocker, y `READY_FOR_NEXT_CAPABILITY: NO`.
- Si sólo una parte de B depende de la apertura, B puede ser NEXT: la capability que la resuelve va en paralelo y `BLOCKING_SCOPE` dice qué parte espera y qué parte avanza.
- NEXT no aparece como su propio prerequisito ni como `THEN`. Sólo aparece en `BLOCKED_CAPABILITIES` para la parte que `BLOCKING_SCOPE` declara bloqueada, con `READY: PARTIAL` (p. ej. se implementa ya la exportación CSV y la PDF espera una respuesta externa).
- Ningún texto del reporte dice que NEXT debe esperar cuando `READY_FOR_NEXT_CAPABILITY` es `YES`. Si ambas cosas parecen ciertas, la ruta está mal expresada y se corrige la ruta.

Ejemplos:

```
# Un hecho bloquea la definición: hay que conocerlo para poder especificar
NEXT_CAPABILITY:        technical-discovery
WHY:                    sin la versión actual del schema no puede definirse el contrato
PREREQUISITES:          NONE
THEN:                   specification
PARALLEL_CAPABILITIES:  NONE
BLOCKED_CAPABILITIES:   implementation (no hay contrato)

# El hecho sólo afecta a una parte: la definición empieza ya
NEXT_CAPABILITY:        specification
WHY:                    el comportamiento material sigue sin definir
PREREQUISITES:          NONE
THEN:                   NONE
PARALLEL_CAPABILITIES:  technical-discovery: comportamiento actual de persistencia
BLOCKING_SCOPE:         espera la sección de persistencia; el resto de la especificación avanza
BLOCKED_CAPABILITIES:   implementation (no hay contrato)
```

**Quién resuelve cada apertura.** Orientación, no una secuencia fija: decide la evidencia del caso.

| Apertura | La resuelve |
|---|---|
| Un hecho del estado actual que el sistema puede mostrar (código, configuración, rutas, tests, historial, runtime) | `technical-discovery` |
| La causa de un fallo observado sobre una superficie identificada o reproducible | `diagnostics` |
| El comportamiento material del producto | `specification`, con la clarificación del humano |
| Una elección material de alcance o una decisión reservada que la evidencia no puede tomar (p. ej. varias superficies de producto cumplen el pedido y elegir una cambia el alcance) | Humano: `DECISION_REQUIRED`. Si la evidencia puede **acotar** los candidatos — qué superficies fallan hoy, cuáles existen —, primero se reúne esa evidencia y la pregunta al humano queda sólo para lo que siga abierto. Qué falla hoy es un hecho; a qué se refería el pedido, cuando varias opciones siguen siendo válidas, es alcance |
| Dónde está el código que hay que cambiar, con el alcance ya delimitado | `implementation` |

```
DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US.
UNKNOWN FACTUAL != DECISION_REQUIRED.
```

Un hecho que el sistema puede establecer se busca antes de preguntar. Un identificador que parece el de una decisión pero cuyo significado no se conoce es un `UNKNOWN` factual hasta que la evidencia diga qué es — un hecho, una decisión ya cerrada, una decisión abierta, una referencia obsoleta, una contradicción (`dependency-model.md` §1) —; no entra en `DECISIONS_REQUIRED` por su nombre.

**PM recomienda; la Control Tower decide.** La transición la ejecuta la Main Session o `delivery-orchestrator` (`delivery-lifecycle`), que pueden seguir otra ruta con su razón. PM no invoca capabilities ni mueve estados.

| Señal | Ruta habitual |
|---|---|
| `BUG` con fallo observado y causa desconocida | `diagnostics` |
| "¿Cómo funciona hoy…?" | `technical-discovery` |
| `FEATURE` con comportamiento sin definir | `specification` |
| `INCIDENT` | `diagnostics` y ruta de incidente |
| `REFACTOR` sin cambio funcional | ruta técnica (`architecture-review` si toca fronteras) |
| `SECURITY` | `security-review` cuando aplica |
| `EXECUTION_READY` + autorización | `implementation` |
| Decisión humana pendiente que bloquea todo | `NONE` + `DECISION_REQUIRED` |

## 4. Fuera de PM

PM no fija prioridad (`SKILL.md` §2): si hace falta ordenar trabajo por valor, lo presenta como `DECISION_REQUIRED` con las opciones y su evidencia. No autoriza ejecución: `READY_FOR_NEXT_CAPABILITY: YES` hacia `implementation` sólo dice que el contrato está; la autorización es humana y, mientras falte, es un blocker de la ejecución (§2).
