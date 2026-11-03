# COOKBOOK — Apep Core

Recetas para problemas recurrentes al trabajar con el harness.

| Si buscas | Lee |
|---|---|
| Por dónde empezar | [README.md](README.md) |
| Aprender a usar el harness | [USER_GUIDE.md](USER_GUIDE.md) |
| La semántica formal: estados, autoridad, lifecycle | [MANUAL.md](MANUAL.md) |
| La governance normativa | [`ENGINEERING_GOVERNANCE.md`](docs/governance/ENGINEERING_GOVERNANCE.md) |

---

# Prefacio

### Qué es este libro

Una colección de recetas. Cada una parte de un problema que aparece una y otra vez al trabajar con Apep Core — un ticket que no sabes si está listo, una Lambda que tarda demasiado, un preflight que se niega a empezar, un lote de PRs con uno bloqueado — y muestra cómo resolverlo con lo que el harness ya ofrece.

Este libro **no** es:

- la governance: la autoridad está en `ENGINEERING_GOVERNANCE.md`, las reglas (`rules/`) y las skills;
- el MANUAL: el MANUAL explica cómo funciona el sistema; aquí sólo se cita;
- una especificación del harness;
- un pipeline obligatorio: ninguna receta dice que todo trabajo deba recorrer esos pasos;
- una introducción a OMP.

```
THE USER GUIDE TEACHES THE SYSTEM.
THE MANUAL EXPLAINS THE SYSTEM.
THE COOKBOOK SOLVES PROBLEMS WITH THE SYSTEM.
```

### A quién está dirigido

A quien trabaja con el harness, haya participado o no en su diseño: developers, QA, Tech Leads, Product y PM, Engineering Managers. No se presupone conocer sus internals. Las recetas usan el mismo modelo operativo para todos; lo que cambia es el problema con el que llegas.

### Qué se presupone

Que puedes arrancar OMP desde la raíz de tu proyecto, que sabes que la sesión en la que escribes es la **Control Tower**, que sabes dónde está el MANUAL y que las decisiones materiales — alcance, semántica de negocio, arquitectura, autorización para ejecutar, toda operación Git — siguen siendo tuyas.

Si todo eso es nuevo: empieza por [USER_GUIDE.md](USER_GUIDE.md).

### Cómo leer este libro

```
YOU DO NOT NEED TO READ THIS BOOK LINEARLY.
```

1. Reconoce tu problema — en el *Índice por problema*, al final, o por el título de las recetas.
2. Ve a la receta.
3. Aplica la **Solución**: qué escribir y qué esperar.
4. Lee la **Discusión** para entender por qué funciona, qué no resuelve y dónde decides tú.
5. Sigue las referencias sólo cuando necesites más profundidad.

Cada receta se sostiene sola. Cuando depende de algo que se explica en otro sitio, lo cita en lugar de repetirlo.

### Anatomía de una receta

```
PROBLEMA     la situación, tal como la vives
SOLUCIÓN     qué escribes, qué hace el harness, qué recibes, dónde se detiene
DISCUSIÓN    por qué funciona, qué frontera protege, variantes, límites, qué decides tú
VÉASE TAMBIÉN  (opcional) otras recetas y secciones del MANUAL
```

Problema, Solución y Discusión están siempre. *Véase también* aparece cuando ayuda.

```
PROBLEM FIRST. CAPABILITY SECOND.
```

### Convenciones

- Lo que escribes va en bloques de texto, tal cual podrías escribirlo:

  ```text
  Tengo este ticket, pero no sé si está listo.
  ```

- Las salidas del harness se muestran **conceptuales y abreviadas**: los campos que importan para la receta, no el artefacto completo.
- `/shape`, `/spec`, … son commands; `project-management`, `diagnostics`, … son capabilities (skills o agents).
- *MANUAL §N* remite a la sección del MANUAL con la semántica formal. *Receta N.M* remite a otra receta de este libro.
- `FACT` es algo observado; `INFERENCE`, algo deducido; `UNKNOWN`, algo que la evidencia no permite saber; `DECISION_REQUIRED`, una decisión que es tuya. Aparecen cuando la distinción importa.
- Los casos reales están resumidos y sin datos sensibles. El de *Orbit Chat* es ilustrativo.

### Gobernanza y precedencia

```
THE COOKBOOK ILLUSTRATES. IT DOES NOT LEGISLATE.
```

Ante cualquier discrepancia:

```
ENGINEERING_GOVERNANCE.md · rules/ · AGENTS.md · skills     (normativo)
  → MANUAL.md                                                 (referencia operacional)
    → USER_GUIDE.md · COOKBOOK.md                             (uso y recetas)
```

Si una receta contradice una skill, manda la skill y se corrige la receta.

---

# Parte I — Conducir el harness

## 1. Control Tower

### 1.1 No sé qué command necesito

#### Problema

Tienes algo entre manos — un fallo, una petición, una duda sobre cómo funciona un módulo — y no sabes si es trabajo de `/shape`, de `/discover` o de otra cosa. Tampoco quieres aprenderte el catálogo antes de empezar.

#### Solución

Descríbelo en la sesión como se lo contarías a un compañero, con lo que sepas y lo que no quieres que ocurra:

```text
El export de cartera a veces sale vacío en QA. No sé si es el filtro
o los datos. No cambies nada todavía; quiero entender qué pasa.
```

La Control Tower reconoce la intención — aquí hay un fallo observado, así que el centro es `diagnostics` — y te dice qué va a hacer antes de hacerlo. Recibes el resultado de esa capability y una recomendación de siguiente paso. Para seguir, contesta sobre ese resultado:

```text
Vale. Con esa causa, ¿qué haría falta para corregirlo?
```

La sesión conserva el objetivo y lo que ya se averiguó; no hace falta repetirlo.

#### Discusión

Funciona porque la Control Tower hace composición, routing y síntesis (MANUAL §4): elige la metodología, delega cuando conviene e integra lo que vuelve. Lo que no hace es decidir por ti: si el siguiente paso cambia el alcance o exige autorización, te lo devuelve.

Los commands siguen siendo útiles cuando ya sabes qué quieres (receta 1.2): son entradas más directas, no más correctas.

No hagas: escribir una cadena de commands "por si acaso" — `/shape`, luego `/spec`, luego `/design` — para algo que una conversación resuelve. `CEREMONY != GOVERNANCE`.

#### Véase también

- Receta 15.1 — cuándo la sesión delega en un agent.
- MANUAL §17 — situación → capability.

### 1.2 Quiero pedir sólo una parte y detenerme ahí

#### Problema

Necesitas una cosa concreta — entender el estado actual, saber si un ticket está listo, un diagnóstico — y te preocupa que el harness "siga de largo" y proponga cambios o empiece a implementar.

#### Solución

Di qué quieres y dónde se detiene:

```text
Sólo quiero entender cómo se calcula hoy la comisión. No propongas cambios.
```

```text
Haz el diagnóstico. No corrijas nada.
```

```text
Revisa el diseño. No escribas código.
```

O usa el command de esa capability, que ya termina en su frontera:

```text
/discover ¿cómo se calcula hoy la comisión en backend/?
```

Recibes el resultado de esa capability y, como mucho, una recomendación de siguiente paso que no se ejecuta.

#### Discusión

Cada capability tiene su final natural: `/discover` termina en el estado actual, `/diagnose` en una causa o en evidencia insuficiente, `/spec` en `EXECUTION_READY`, `/deliver` en `INTEGRATION_READY`. Ninguna encadena la siguiente por su cuenta: `MODE RECOMMENDATION != AUTOMATIC AUTHORITY TRANSITION`.

La instrucción explícita ("no corrijas") sigue valiendo la pena: delimita el encargo y deja claro qué autorizas.

```
THE HARNESS IS NOT ONLY AN AUTONOMOUS SOFTWARE FACTORY.
YOU CAN INVOKE ONE BOUNDED CAPABILITY AND STOP THERE.
```

#### Véase también

- Receta 3.1 — el caso opuesto: delegar el recorrido completo.

### 1.3 Me devolvieron un `DECISION_REQUIRED`

#### Problema

El harness se detuvo y te presenta un bloque `DECISION_REQUIRED` con hechos, opciones, consecuencias y una recomendación. No sabes si basta con decir "ok", ni qué pasa con el resto del trabajo mientras decides.

#### Solución

Lee primero `BLOCKING_SCOPE`: dice qué está parado y qué sigue avanzando. Después responde con la decisión, en una línea, y su razón si la hay:

```text
DECISION: opción B.
RAZÓN: preferimos el coste de migración ahora antes que arrastrar el contrato dual.
Esto cierra la decisión. Continúa con lo que quedó bloqueado; el resto no cambia.
```

Si ninguna opción te sirve, dilo y explica por qué; si te falta información, pide la evidencia concreta que necesitas:

```text
Antes de decidir: ¿cuántos clientes usan hoy el contrato antiguo?
```

#### Discusión

Un `DECISION_REQUIRED` aparece cuando continuar exige elegir entre comportamientos, aceptar un riesgo o cambiar alcance: algo reservado a una persona (`ENGINEERING_GOVERNANCE.md` §1.4). La `RECOMMENDATION` es una recomendación; aceptarla es tu decisión, y "ok" a secas es ambiguo cuando hay varias opciones.

Pedir un hecho no es esquivar la decisión: si el sistema puede averiguarlo, debió averiguarlo antes de preguntarte (`DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US`). Si ves una pregunta que es en realidad un hecho, señálalo.

No hagas: contestar "decide tú" sobre algo material. No transfiere la decisión: queda abierta.

#### Véase también

- Receta 8.2 — preguntas de la especificación (`CLAR-NNN`).
- Receta 3.2 — la misma situación con el orchestrator.

## 2. Planificar el abordaje

### 2.1 No sé cómo abordar un trabajo complejo

#### Problema

El objetivo está claro — "averiguar por qué esta Lambda tarda 25 segundos", "migrar este módulo" — pero no sabes por dónde atacarlo: qué investigar primero, qué depende de qué, qué se puede hacer a la vez.

#### Solución

Activa el plan mode de OMP y describe el objetivo y lo que te preocupa:

```text
/plan
Necesito investigar por qué esta Lambda tarda 25 segundos. Quiero definir
primero qué evidencia buscar, qué dependencias hay y qué podemos investigar
en paralelo.
```

El agente propone un plan antes de ejecutar: pasos, orden, dependencias, qué va en paralelo y qué capability usar en cada uno. Lo revisas, lo corriges y lo apruebas antes de que se ejecute nada.

#### Discusión

```
/plan     = ¿CÓMO ABORDAMOS EL TRABAJO?
/spec     = ¿QUÉ DEBE HACER EL SISTEMA?
/deliver  = MATERIALIZA LO QUE AUTORIZASTE.
```

`/plan` reduce incertidumbre de abordaje. No define comportamiento del producto (eso es `/spec`) y no es una fase obligatoria: para un cambio local ya entendido sólo añade una ronda.

Si lo que necesitas ordenar son **work items** — qué puede empezar ya, qué espera a otro, qué está bloqueado —, eso es gestión del trabajo: receta 5.1.

No hagas: usar `/plan` para reabrir un Execution Contract ya autorizado. Un contrato se reabre por evidencia nueva (`DECISION_CONTRADICTION`) o por tu decisión explícita, no replanificando (MANUAL §6).

#### Véase también

- Receta 15.2 — investigaciones en paralelo con agents.
- MANUAL §6.

## 3. Delegar el recorrido en `delivery-orchestrator`

### 3.1 El work item ya está claro y quiero delegar todo el recorrido

#### Problema

Tienes un work item delimitado — se sabe qué hay que hacer, en qué repositorio y con qué alcance — y no quieres ir pidiendo cada paso. Quieres que vuelva cuando haga falta tu decisión, o terminado.

#### Solución

Delégalo en `delivery-orchestrator` con el contexto, las decisiones ya cerradas y lo que autorizas:

```text
Delega a delivery-orchestrator: implementa US-472 — validar el contexto de
acceso en Discovery, repo backend/. Autorizada la work branch que proponga
desde dev. Lleva el lifecycle hasta INTEGRATION_READY; para en cualquier
decisión reservada.
```

El orchestrator clasifica, decide qué capability sigue, delega en los workers, verifica, revisa y prepara commit y PR. Vuelve con un `LIFECYCLE_STATE`: o un gate que resolver, o el paquete de integración (evidencia, findings, `COMMIT_MESSAGE`, `PR_TITLE`, `PR_BODY`).

#### Discusión

Conviene cuando el trabajo ya tiene forma. Si todavía estás decidiendo qué hacer, quédate en la Control Tower: el orchestrator corre sin poder preguntarte en vivo y cada duda se convierte en una parada.

| Quédate en la Control Tower | Delega en `delivery-orchestrator` |
|---|---|
| Quieres ir viendo y decidiendo | El item ya está delimitado |
| Vas a mirar los resultados entre pasos | Te basta con que vuelva por gates reales |

Delegar el recorrido no delega autoridad: lo que autorizas es lo que escribes ("la work branch que proponga desde `dev`"). Commit, push y PR los ejecuta la Main Session sólo si los autorizas después.

```
THE ORCHESTRATOR CHOOSES THE NEXT CAPABILITY.
IT DOES NOT ACQUIRE THAT CAPABILITY'S AUTHORITY.
```

No hagas: delegarle una idea ("haz un sistema de permisos nuevo") esperando que la especifique y la decida. Se detendrá en la primera decisión material, como debe.

#### Véase también

- Receta 3.2 — cuando se detiene.
- MANUAL §4, *`delivery-orchestrator`*.

### 3.2 El orchestrator se detuvo en un gate

#### Problema

Delegaste un work item y el orchestrator volvió a mitad de camino con un `LIFECYCLE_STATE` en `blocked_by`. No sabes cómo continuar sin empezar de nuevo.

#### Solución

Lee tres campos del `LIFECYCLE_STATE`: `blocked_by` (qué gate), `decisions_required` (qué te toca) y `completed` (lo ya hecho, que no se pierde). Responde a la Main Session con la decisión o la autorización:

```text
Autorizo crear feature/US-472/validar-contexto desde dev. Reanuda.
```

La Main Session reanuda al orchestrator con tu respuesta y el estado conservado.

#### Discusión

El orchestrator corre headless: no puede preguntarte en vivo, así que se detiene y devuelve su estado. La Main Session es el puente de autoridad: te presenta el gate, recoge tu respuesta y lo reanuda (`delivery-lifecycle` §0).

Sólo se detiene por gates reales: una decisión reservada, una operación con gate, una contradicción, una ampliación de alcance, evidencia insuficiente que bloquea o la integración (`delivery-lifecycle` §7). No se detiene para pedirte permiso para leer, ejecutar tests o elegir un worker. Si se detuvo por algo así, es un defecto que conviene reportar.

Si un worker no terminó (timeout, error de herramienta), el orchestrator lo reintenta una vez; si vuelve a fallar, se detiene en `BLOCKED` con su `STOP_REPORT` y la evidencia ya producida. Decides tú si reintentar o investigar la causa.

#### Véase también

- Receta 1.3 — cómo responder un `DECISION_REQUIRED`.

---

# Parte II — Dar forma y entender el trabajo

## 4. Dar forma a un work item

### 4.1 Tengo un ticket y no sé si está listo

#### Problema

Tienes un ticket cuya intención se entiende, pero no sabes si está listo para que alguien lo implemente: si es un bug o una feature, si es grande, si falta definir algo, si depende de otra cosa.

#### Solución

```text
/shape EXPORT-112: "Agregar exportación CSV al reporte de cartera."
```

o, sin command:

```text
Tengo este ticket. Ayúdame a ver qué falta antes de programarlo.
```

Recibes primero un resumen en lenguaje corriente y después el registro de proceso. Para un item pequeño y claro cabe en cuatro líneas:

```
TYPE:             FEATURE
DESIRED_OUTCOME:  el usuario descarga la cartera filtrada en CSV
SIZE_SIGNAL:      SMALL
NEXT_CAPABILITY:  specification   (falta qué columnas y qué filtros)
```

Para uno mayor añade riesgo, dependencias, formalidad (`NONE`, `LIGHT`, `FORMAL`) y el `READINESS_CHECK` hacia el siguiente paso.

#### Discusión

`/shape` responde "¿qué trabajo es éste y cómo debe entrar al sistema?". Clasifica (`BUG`, `FEATURE`, `TECHNICAL_CHANGE`, `INFRASTRUCTURE`…) por intención y evidencia, no por el título del ticket: un "bug" que pide comportamiento nuevo es una feature.

No escribe criterios de aceptación ni inventa comportamiento: si falta comportamiento, su respuesta es que el siguiente paso es definirlo (`PM MUST NOT INVENT PRODUCT SEMANTICS`). Tampoco fija prioridad ni autoriza ejecución.

"Listo" siempre es *listo para algo*: un ticket puede estar listo para especificarse y no para implementarse.

No hagas: pasar por `/shape` un cambio local ya perfectamente determinado — una errata, un label. Ahí `/shape` es ceremonia.

#### Véase también

- Receta 4.3 — cuando el siguiente paso depende de hechos.
- MANUAL §5, *Work shaping*.

### 4.2 La petición es demasiado grande para ser una tarea

#### Problema

Te piden algo que suena a una tarea pero huele a proyecto. Ejemplo: *"Empezar PROD en AWS con CDK y promover lo estable de QA."* No sabes si es uno o diez trabajos, ni por dónde empezar.

#### Solución

```text
/shape Empezar PROD en AWS con CDK y promover lo estable de QA.
```

Salida conceptual:

```
TYPE:               INFRASTRUCTURE
WORK_FORMALITY:     FORMAL
SIZE_SIGNAL:        TOO_LARGE_TO_EXECUTE
SLICING:            SPLIT_REQUIRED
NEXT_CAPABILITY:    technical-discovery
WHY:                la definición depende de qué existe hoy en QA y en PROD
THEN:               specification, por slice
BLOCKED_CAPABILITIES: implementation — no hay contrato
```

Junto con slices propuestos (por ejemplo, red y cuentas, datos, servicios, promoción) y las decisiones que sólo tú puedes tomar.

#### Discusión

`SPLIT_REQUIRED` dice que no se puede ejecutar como una pieza: hay que cortar antes de especificar. Las slices son una propuesta; el corte final es tuyo.

El siguiente paso es investigar, no especificar, porque especificar PROD sin saber qué hay en QA sería inventar el estado actual. Si ese inventario ya existiera y estuviera vigente, `/spec` sería el siguiente paso directamente: la ruta depende de la evidencia, no del tipo de trabajo.

`project-management` da forma; no construye infraestructura ni decide arquitectura.

No hagas: pedir directamente "implementa PROD". No hay contrato que materializar, y cada decisión de infraestructura acabaría tomándola quien escribe el código.

#### Véase también

- Receta 6.3 — comparar QA y PROD.
- Receta 16.2 — el recorrido completo de este caso.

### 4.3 El siguiente paso depende de hechos que nadie conoce

#### Problema

Al dar forma a un trabajo aparecen preguntas — qué servicio lo hace hoy, qué versión está desplegada, si un módulo sigue en uso — de las que depende cómo seguir. Nadie las sabe de memoria.

#### Solución

No las contestes de memoria ni esperes a tenerlas: deja que `/shape` las clasifique. Si son hechos, la ruta lo refleja:

```
NEXT_CAPABILITY:         technical-discovery
WHY:                     no se sabe qué servicio genera hoy el archivo
READY_FOR_NEXT_CAPABILITY: YES
THEN:                    specification
```

Y continúa:

```text
Adelante con el discovery que propones.
```

#### Discusión

```
THE NEXT CAPABILITY IS THE ONE THAT CAN START NOW.
IF A MUST FINISH BEFORE B CAN START, THEN B IS NOT THE IMMEDIATE NEXT CAPABILITY.
UNKNOWN FACTUAL != DECISION_REQUIRED.
```

Esta regla nació de dos ejecuciones reales en las que `/shape` recomendaba especificar mientras decía que antes había que investigar. Ahora el siguiente paso es siempre lo que puede empezar ya; lo que espera va en `THEN`, y lo que avanza a la vez en `PARALLEL_CAPABILITIES`.

Si una parte del siguiente paso puede empezar y otra no, lo verás como bloqueo parcial con su `BLOCKING_SCOPE`: qué espera y qué avanza ya. Eso es "lo que está realmente bloqueado".

No hagas: tratar un desconocido factual como una decisión tuya. Si te preguntan algo que el sistema puede comprobar, pide que lo compruebe.

#### Véase también

- Receta 6.1 — el discovery que sigue.

### 4.4 Un bug con el comportamiento esperado claro

#### Problema

Caso real de field validation: *"el reporte no es responsive"*. El ticket dice qué debe pasar — cards y textos que se adaptan a escritorio, tablet y celular, con zoom de 50 % a 200 %, sin scroll horizontal ni solapes — pero no dice qué pantalla es "el reporte" ni por qué falla.

#### Solución

```text
/shape WI-918: "El reporte no es responsive". Cards y textos deben
adaptarse a escritorio, tablet y celular, zoom 50–200 %, sin scroll
horizontal, solapes ni cortes.
```

Salida conceptual:

```
TYPE:            BUG
WORK_FORMALITY:  LIGHT
NEXT_CAPABILITY: diagnostics
WHY:             regresión observada con esperado explícito; hay que reproducir
                 y localizar qué superficies fallan y por qué
THEN:            implementation
```

#### Discusión

No hace falta `/spec`: el comportamiento esperado ya está escrito en el ticket con suficiente precisión. Lo que falta es saber dónde y por qué falla, y eso es diagnóstico.

La duda de qué superficie es "el reporte" no se te pregunta de entrada: el sistema puede reproducir las candidatas y ver cuáles fallan. Sólo si la evidencia deja varias superficies igualmente válidas, elegir cuál se corrige es decisión tuya. Esa regla — reunir evidencia antes de preguntar — también salió de field validation.

No hagas: dejar que el implementador elija la superficie, ni saltar a implementar sin reproducir.

#### Véase también

- Receta 16.1 — el recorrido completo de este caso.

### 4.5 `/shape` me pide una decisión

#### Problema

Le diste forma a un trabajo y el resultado no recomienda un siguiente paso: termina en `DECISION_REQUIRED`. Esperabas una ruta.

#### Solución

Mira qué decisión es y si de verdad es tuya. Si es una elección real — entre dos alcances, aceptar un riesgo, qué va primero —, decide (receta 1.3). Si la "decisión" es en realidad un hecho que el sistema puede averiguar, devuélvela:

```text
Eso no es una decisión: comprueba en el repositorio qué superficies
usan ese componente y vuelve con la ruta.
```

#### Discusión

`/shape` termina en `DECISION_REQUIRED` cuando lo que falta para seguir es una decisión humana genuina. Las autorizaciones pendientes — ejecutar, crear una rama — no son decisiones de este tipo: aparecen como "pendiente de autorización" en el resumen o la ruta.

Una decisión pendiente no siempre lo bloquea todo: su `BLOCKING_SCOPE` dice qué espera y qué puede avanzar mientras tanto.

#### Véase también

- Receta 1.3.

### 4.6 Tengo que presentar el resultado a dirección

#### Problema

Le diste forma a un trabajo importante y necesitas llevarlo a una reunión con dirección o con producto. El registro técnico es útil para ingeniería, pero ilegible para ellos.

#### Solución

No hace falta nada especial: los resultados de `/shape` y `/project` ya empiezan por un resumen en lenguaje de gestión y terminan en el registro de proceso. Si necesitas ajustar el tono o el foco, pídelo:

```text
Resume esto para dirección: qué está en juego, qué lo bloquea, qué
decisiones necesitan y qué recomendamos. Detalle técnico sólo cuando
sostenga una conclusión.
```

#### Discusión

```
THE METHOD DETERMINES WHAT IS TRUE.
THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED.
```

Las tres vistas — gestión, ingeniería, registro — son el mismo análisis para lectores distintos. Por eso el resumen no puede decir algo que el registro no sostiene: no añade fechas, porcentajes, prioridades ni valor que nadie dio, y una recomendación no aparece como decisión.

No hagas: pedir que "suene más positivo" o que "ponga una fecha". Lo desconocido sigue siendo desconocido en cualquier vista.

#### Véase también

- MANUAL §5, *Cómo se presentan los resultados*.

## 5. Gestionar un proyecto o un frente

### 5.1 Tengo varios trabajos y no sé cuál puede avanzar

#### Problema

Hay siete trabajos abiertos en un frente. Unos dependen de otros, alguno espera una decisión, otro espera a un equipo externo. Necesitas saber qué puede empezar ya y qué está realmente bloqueado.

#### Solución

```text
/project Frente "PROD": estos son los trabajos abiertos y lo que sé de
cada uno. Quiero dependencias, blockers reales, riesgos y qué puede
avanzar ahora. No quiero ejecutar nada.
```

Recibes un estado ejecutivo, las dependencias (internas, externas, de decisión), qué está bloqueado y por qué, y las decisiones pendientes con quién decide.

#### Discusión

Un blocker real es una dependencia que impide empezar; "sería mejor esperar" no lo es. El análisis distingue ambos y separa los hechos de las inferencias.

`/project` gestiona el trabajo; no define comportamiento ni prioriza por ti. Si un trabajo necesita definirse, lo dirá (siguiente paso: `specification`) en lugar de escribir sus requisitos.

Variante: para comparar iniciativas sin la estructura de un proyecto, receta 14.1.

#### Véase también

- Receta 4.3 — siguiente paso, `THEN` y paralelos para un solo item.

### 5.2 Me piden una fecha, o me dicen que "vamos al 80 %"

#### Problema

Alguien pregunta "¿llegamos para el 15?" o reporta "vamos al 80 %". Necesitas una respuesta honesta, no un semáforo.

#### Solución

```text
/project ¿Llegamos con la migración para el 15 de noviembre?
Esto es lo que hay hecho y lo que falta.
```

La respuesta separa las fechas:

```
DESIRED_DATE:    15-nov (la pide producto)
FORECAST:        NOT_AVAILABLE — sin estimación ni histórico
COMMITTED_DATE:  ninguna — nadie con autoridad la comprometió
```

y describe el avance en estados verificables (cuántos items listos, en curso, en revisión, entregados) en lugar de un porcentaje.

#### Discusión

`DESIRED_DATE != COMMITTED_DATE`. El forecast sólo existe con evidencia y lleva su confianza y supuestos. Un "80 %" se cita como lo que es — una afirmación sin estados verificables detrás —, no como estado.

Si la fecha deseada choca con el alcance o la capacidad, la salida son opciones y un `DECISION_REQUIRED`: reducir alcance, mover la fecha, añadir capacidad. Elegir es de quien tiene autoridad.

No hagas: pedir que "ponga una fecha razonable". Una fecha inventada es peor que un `NOT_AVAILABLE`.

#### Véase también

- Receta 4.6 — presentar a dirección.

### 5.3 Cambió un requisito a mitad del proyecto

#### Problema

Producto pide un cambio sobre algo ya acordado — otro campo en el export, otra regla de cálculo — cuando el trabajo ya está en curso. Necesitas saber qué toca antes de aceptarlo o rechazarlo.

#### Solución

```text
/project Producto pide que el export incluya también los clientes dados
de baja. ¿Qué impacto tiene sobre lo acordado?
```

Recibes un `CHANGE_IMPACT_ANALYSIS`: requisitos y alcance afectados, dependencias, impacto en fechas comprometidas, opciones y quién decide.

#### Discusión

```
CHANGE ANALYSIS != CHANGE AUTHORIZATION.
REQUIREMENTS MANAGEMENT != REQUIREMENTS ENGINEERING.
```

`/project` analiza el impacto; aceptar el cambio es una decisión. Y gestiona el requisito como trabajo — su estado, sus cambios —, pero no redefine qué significa: si el cambio altera comportamiento, la definición vuelve a `specification` y los criterios de aceptación se actualizan allí.

No hagas: pedirle a `/project` que reescriba los criterios de aceptación con el cambio.

#### Véase también

- Receta 8.4 — cuando el cambio contradice una decisión cerrada.

## 6. Entender el estado actual

### 6.1 Necesito entender un flujo de punta a punta

#### Problema

Vas a tocar algo que cruza varios componentes — un endpoint que acaba lanzando un pipeline — y nadie sabe exactamente qué pasa entre medias, ni a veces en qué repositorio vive cada parte.

#### Solución

```text
/discover Reconstruye el flujo completo desde POST /client/discovery hasta
el inicio de Step Functions: qué componentes participan, qué datos pasan,
qué se persiste y qué pasa ante error.
```

Si no sabes el repositorio, dilo: el primer paso será localizarlo. Recibes un `FLOW_DISCOVERY`: frontera de entrada, camino de ejecución, contratos y datos, efectos, comportamiento ante error, dependencias externas, contradicciones y desconocidos.

#### Discusión

Discovery sigue la ejecución real, no lee el repositorio entero: elige la escala más estrecha que responde la pregunta (`TARGETED`, `FLOW` o `SYSTEM`, `technical-discovery` §4). Una pregunta puntual — "¿qué hace esta función?" — no necesita un `FLOW_DISCOVERY` ni un agent.

```
DISCOVERY RECONSTRUCTS CURRENT_STATE.
DISCOVERY DOES NOT DEFINE TARGET_STATE.
```

El resultado distingue `FACT` (observado), `INFERENCE`, `DECLARED_INTENT` (lo que dice la documentación o un comentario) y `UNKNOWN`. Lo que no pudo verificarse queda como desconocido, no se rellena.

#### Véase también

- Receta 15.1 — cuándo esto va a un agent.
- Receta 16.2 — de aquí a especificar el cambio.

### 6.2 No sé si la documentación — o el ticket — dicen la verdad

#### Problema

Tu decisión depende de algo que "todo el mundo sabe" o que dice un README, un ticket o un comentario. Sospechas que puede estar desactualizado.

Caso real: un ticket sobre un reporte grande que no terminaba por memoria afirmaba la configuración de memoria del contenedor y que otro componente "ya estaba optimizado en memoria". Las dos cosas condicionaban la solución.

#### Solución

Pide que se contraste contra la fuente de verdad:

```text
/discover El ticket dice que Explorer corre con 24 GB/4 CPU y que Social
Listener ya está optimizado en memoria. Verifica ambas cosas contra la
configuración desplegada y el código. Separa lo que dice el ticket de lo
que observas.
```

#### Discusión

En el caso real, discovery encontró que la cifra del ticket era la configuración **que falló**, no la vigente, y que "optimizado" era en realidad una subida de capacidad, no una reducción de consumo. Las dos conclusiones cambiaron lo que había que especificar.

Discovery no trata como equivalentes documentación y verdad de runtime, ni intención declarada y comportamiento observado. Cuando dos fuentes relevantes no casan, lo reporta como `CONTRADICTION`: es un estado de la evidencia, no algo que discovery resuelva eligiendo una.

No hagas: pedir que "asuma lo que dice el README" para ir más rápido.

#### Véase también

- Receta 8.1 — cómo siguió este caso en la especificación.

### 6.3 Necesito comparar QA y PROD

#### Problema

Antes de promover algo a producción, o para entender por qué algo funciona en QA y no en PROD, necesitas saber en qué difieren de verdad los dos entornos.

#### Solución

```text
/discover Inventario comparado de QA y PROD para el pipeline de reportes:
servicios, configuración de cómputo y memoria, variables relevantes y
versiones desplegadas. Sólo lectura. Marca lo que no puedas verificar.
```

#### Discusión

Es discovery de sistema guiado por una pregunta concreta. Sólo puede verificar lo que el acceso disponible permite: lo que no pudo leer queda `UNKNOWN`, con qué haría falta para cerrarlo.

Si la pregunta es "¿por qué falla en PROD?", hay un fallo observado: eso es diagnóstico (receta 7.3), que puede consumir este inventario.

No hagas: pedir que proponga la configuración de PROD. Eso es una decisión de infraestructura, no estado actual.

#### Véase también

- Receta 4.2 — el frente PROD.

## 7. Diagnosticar un fallo observado

### 7.1 Algo tarda demasiado

#### Problema

Un endpoint, un chat, una Lambda tarda muchísimo y no sabes dónde se va el tiempo. Ejemplo ilustrativo: *"Orbit Chat tarda más de 25 segundos."* Antes de cambiar nada quieres saber la causa.

#### Solución

Da el síntoma con lo que sepas: qué, dónde, cuándo, desde cuándo.

```text
/diagnose Orbit Chat tarda más de 25 s por respuesta en QA desde la semana
pasada. Antes tardaba unos 5 s. No cambies nada.
```

El diagnóstico busca dónde diverge el comportamiento real del esperado, sigue la cadena causal y termina en uno de tres resultados:

```
ROOT_CAUSE_CONFIRMED | ROOT_CAUSE_HIGH_CONFIDENCE | INSUFFICIENT_EVIDENCE
```

con `FAULT_OWNER` (qué componente posee la causa), `FIX_BOUNDARY` (dónde tendría que ir la corrección) y, si procede, una remediation recomendada.

#### Discusión

Diagnostics empieza siempre por un fallo observado: "tarda 25 s y antes 5 s" lo es. Si sólo quieres saber cómo funciona el chat, sin fallo que explicar, eso es `/discover`. Si para seguir la cadena hace falta entender el flujo, la Control Tower intercala discovery.

La escala es la más estrecha que el fallo justifica — `TARGETED`, `FLOW` o `INCIDENT` (`diagnostics` §5) — y sólo se amplía con evidencia.

```
DIAGNOSIS != REMEDIATION.
```

No hagas: `/diagnose busca problemas potenciales en el chat`. Sin fallo no hay diagnóstico.

#### Véase también

- Receta 7.4 — qué hacer con la causa.

### 7.2 Un proceso muere por memoria

#### Problema

Caso real: un reporte de QA de unas 245.000 menciones falló dos veces en Explorer — primero por falta de memoria del contenedor, después con un bloqueo de cuatro horas sin consumo de CPU.

#### Solución

```text
/diagnose El reporte <execution_id> falló en Explorer en QA: primero OOM
(ver evento de ECS), luego un bloqueo de ~4 h sin CPU en el reintento.
Preserva la evidencia. No reinicies ni redespliegues nada.
```

#### Discusión

En el caso real, el mecanismo de memoria fue que el preprocesamiento de lenguaje natural dimensionaba lotes y número de procesos según el tamaño del corpus y la CPU disponible, sin límite superior. El bloqueo era **otro** mecanismo, distinto, que el ticket no mencionaba: un fallo con dos síntomas puede tener dos causas.

Dos cosas importan en esta clase de fallo:

- **Preservar evidencia antes de mutar.** Reiniciar, reencolar o redesplegar puede borrar justo lo que discrimina entre hipótesis (`diagnostics` §10). Por eso el prompt lo prohíbe.
- **Mecanismo frente a atribución.** Demostrar que un mecanismo produce OOM no demuestra que produjo *este* OOM. Si falta el vínculo directo con la ejecución concreta, el resultado honesto es `ROOT_CAUSE_HIGH_CONFIDENCE` (`diagnostics` §8).

Si el fallo sólo ocurre en un entorno, la diferencia de configuración entre entornos es evidencia: receta 6.3.

#### Véase también

- Receta 16.3 — de este diagnóstico a la corrección.

### 7.3 Hay varias causas posibles y la evidencia no alcanza

#### Problema

El fallo es intermitente, o hay tres explicaciones plausibles y cada persona defiende una. Necesitas saber cuál es, no la más convincente.

#### Solución

```text
/diagnose El timeout del pipeline de reportes aparece en 1 de cada 10
ejecuciones. Hipótesis que se manejan: cola saturada, cold start, consulta
lenta. Quiero la evidencia que discrimine entre ellas.
```

Si la evidencia disponible discrimina, recibes la causa. Si no:

```
RESULT:              INSUFFICIENT_EVIDENCE
LIVE_HYPOTHESES:     cold start · consulta lenta
DISCRIMINATING:      tiempos por etapa con correlation id de una ejecución lenta
WHY_NOT_AVAILABLE:   los logs de etapa no se conservan más de 24 h
```

#### Discusión

El diagnóstico busca evidencia que **distinga** entre hipótesis, no evidencia que confirme la favorita. Reproducir un fallo compatible no prueba la causa.

`INSUFFICIENT_EVIDENCE` es un resultado válido, no un fracaso: dice qué observación cerraría la pregunta. Lo siguiente es tuyo: habilitar esa observación (más logs, una ventana de captura) y volver a diagnosticar, o aceptar el riesgo.

No hagas: pedir "elige la más probable y arréglala". Forzar una causa produce una corrección que puede no corregir nada.

#### Véase también

- MANUAL §11.

### 7.4 Ya tengo la causa: ¿y ahora?

#### Problema

El diagnóstico terminó con una causa y una remediation recomendada. Quieres arreglarlo, pero no sabes si basta con decir "corrígelo".

#### Solución

Lee `FIX_BOUNDARY`: dice dónde tendría que ir la corrección. Decide el alcance y da forma a la corrección en proporción:

- **Pequeña, local, sin comportamiento nuevo:** autoriza un encargo ligero.

  ```text
  Corrige el cálculo del lote dentro de FIX_BOUNDARY, rama fix/RPT-311 desde
  dev. Verifica con los tests del módulo. Sin commit.
  ```

- **Cambia comportamiento, contratos o infraestructura:** pasa por `/shape` o `/spec` antes de `/deliver`.

#### Discusión

```
DIAGNOSIS != REMEDIATION.
```

La remediation recomendada es una propuesta. El diagnóstico no concede autorización para aplicarla, y si la corrección implica una decisión de arquitectura, infraestructura o alcance no cerrada, el propio diagnóstico la devuelve como `DECISION_REQUIRED` (`diagnostics` §9).

No hagas: aplicar el arreglo "ya que estamos" dentro del diagnóstico. Una corrección sin contrato no tiene criterio de aceptación contra el que verificarse.

#### Véase también

- Receta 10.1 — ejecutar el contrato.
- Receta 16.3.

---

# Parte III — Definir y diseñar

## 8. Especificar el comportamiento

### 8.1 Tengo una necesidad todavía ambigua

#### Problema

Tienes un ticket crudo que mezcla el problema con una posible solución y con datos de contexto que no sabes si son ciertos. Caso real: *"Que un reporte grande no se caiga por falta de memoria"*, con criterios de aceptación mezclados y un PR mencionado como si fuera la solución.

#### Solución

Dáselo tal cual a la especificación:

```text
/spec Ticket RPT-204: "Que un reporte grande no se caiga por falta de memoria".
<texto completo del ticket>
```

La Línea 1 normaliza primero la entrada — separa problema de solución propuesta —, clasifica cada apertura (hecho verificable, decisión material o detalle táctico) y sólo después avanza por las etapas que hagan falta.

#### Discusión

En el caso real, de doce aperturas, diez eran hechos que se resolvieron con discovery sin preguntar a nadie: la causa raíz, el estado real del PR mencionado (no se había mergeado; se mergeó otra corrección más completa), la configuración vigente, la topología del pipeline. Sólo dos eran decisiones de negocio e infraestructura, y esas dos se preguntaron.

```
CLASSIFY BEFORE ASKING.
DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US.
```

No hace falta que limpies el ticket antes: separar problema de solución es parte del trabajo.

No hagas: pedir "especifica la solución del PR". La solución propuesta es un dato, no el problema.

#### Véase también

- Receta 8.2 — las preguntas que sí te llegan.
- Receta 6.2.

### 8.2 La especificación me hace preguntas

#### Problema

La especificación se detuvo con una o varias preguntas `CLAR-NNN`. Quieres contestar bien, sin abrir dudas nuevas ni dejar huecos.

#### Solución

Cada pregunta trae por qué importa, opciones y una recomendación. Contesta por ID, una decisión por pregunta:

```text
CLAR-003: B. Una cuenta suspendida no recibe pagos nuevos; los ya
programados se cancelan.
CLAR-004: fuera de alcance para esta versión.
```

Si sólo puedes contestar una parte, dilo: la parte respondida se aplica y el resto queda abierta como pregunta nueva.

#### Discusión

Las respuestas se registran en un ledger y se aplican a los artefactos sustituyendo el texto que contradicen.

```
HISTORY LIVES IN THE LEDGER. CURRENT TRUTH LIVES IN THE ARTIFACTS.
```

Una respuesta sólo cierra lo que dice: al aplicarla no se añaden reglas, umbrales ni permisos que no contenga. "Fuera de alcance" no cierra algo de lo que depende lo que sí está en alcance: si es el caso, te lo vuelven a preguntar explicando la dependencia.

"Decídelo tú" vale para algo no material, que se registra como supuesto (`ASM-NNN`); sobre algo material no transfiere la decisión.

#### Véase también

- Receta 1.3.
- MANUAL §8, *Clarificación*.

### 8.3 La especificación no quedó lista del todo

#### Problema

La especificación terminó en `NOT_EXECUTION_READY`, pero buena parte del trabajo parece clara. No sabes si puedes empezar con algo o hay que esperar a todo.

#### Solución

Lee los `blocking_reasons` y el `BLOCKING_SCOPE`: dicen qué parte está bloqueada y por qué. En el caso real de memoria, un criterio de aceptación y partes de dos tareas eran ejecutables ya; sólo la porción que dependía de dos decisiones estaba bloqueada.

Puedes decidir lo pendiente:

```text
CLAR-A: la verificación incluye Report Engine. CLAR-B: no tocar el sizing
aprobado en esta iteración. Continúa hasta el gate.
```

o autorizar sólo la parte ya especificada, si el contrato la delimita.

#### Discusión

```
EXECUTION_READY != AUTHORIZED_TO_EXECUTE.
```

El bloqueo no es binario: el gate dice exactamente qué falta. En el caso real había una tentación evidente de declarar éxito — la causa estaba identificada y la corrección desplegada —, y el gate lo impidió: lo que faltaba era una decisión humana sobre el alcance de la verificación, no más investigación.

Incluso un `EXECUTION_READY` completo no autoriza a nadie a implementar: hace falta tu autorización explícita.

No hagas: pedir que "lo marque como listo, que ya está casi". El gate no se suaviza para cerrar.

#### Véase también

- Receta 10.1.

### 8.4 La evidencia contradice algo ya decidido

#### Problema

Decidiste algo — un comportamiento, una restricción — y ahora la investigación o la implementación muestran que no encaja con la realidad: la API no devuelve lo que se suponía, el dato no existe.

#### Solución

El harness lo reporta como `DECISION_CONTRADICTION`: qué se decidió, qué muestra la evidencia y por qué no son compatibles. Decide si mantienes, cambias o retiras la decisión:

```text
Mantengo la decisión; el dato se obtendrá de la tabla de auditoría.
Actualiza la especificación y vuelve al gate.
```

#### Discusión

Un contrato autorizado no se reescribe en silencio para ajustarse a lo encontrado, ni se ignora la evidencia para cumplir el contrato. La contradicción vuelve a quien decidió.

Es el único camino legítimo — junto con tu decisión explícita de cambiar — para reabrir algo cerrado. `/plan` no lo es (receta 2.1).

#### Véase también

- Receta 10.4 — contradicciones que aparecen al revisar.

### 8.5 No sé si esto necesita especificación

#### Problema

Tienes un cambio entre manos y dudas: ¿pasa por `/spec` o es demasiado pequeño? ¿Y si ya existe una especificación a medias?

#### Solución

Pregúntalo:

```text
/shape Cambiar el texto de ayuda del filtro de fechas en el reporte.
```

La formalidad sale en el resultado:

| Formalidad | Cuándo, a grandes rasgos | Qué hace falta |
|---|---|---|
| `NONE` | Micro cambio local, reversible, sin comportamiento nuevo | Un encargo breve |
| `LIGHT` | Comportamiento acotado y claro | Un task contract ligero |
| `FORMAL` | Comportamiento material, contratos, varios componentes | Especificación hasta `EXECUTION_READY` |

Si ya hay una especificación a medias, dilo; `/spec` empieza en la etapa que la evidencia permite:

```text
/spec Continúa specs/membership-pause/: ya hay problem definition aprobada.
```

#### Discusión

La formalidad es proporcional a la incertidumbre, el impacto, las dependencias y el coste de revertir. Una errata no se especifica; reconstruir el estado actual tampoco es especificar (es `/discover`).

Al continuar una especificación existente, `/spec` verifica que las etapas previas existen de verdad antes de saltárselas: si falta algo, lo dice en lugar de fingir que está.

#### Véase también

- MANUAL §8.

## 9. Validar un diseño

### 9.1 Quiero validar una propuesta antes de construirla

#### Problema

Hay una propuesta de diseño sobre la mesa — "separar Report Engine en otro servicio" — y quieres saber si respeta las fronteras del sistema antes de invertir en especificarla e implementarla.

#### Solución

```text
/design Evalúa esta propuesta de separar Report Engine en otro servicio:
<propuesta>. Quiero saber qué fronteras toca, qué acoplamiento introduce
o elimina y qué contratos cambian. No diseñes el reemplazo.
```

El resultado es uno o varios estados — `ARCHITECTURE_OK`, `ARCHITECTURAL_RISK`, `ARCHITECTURAL_CONTRADICTION`, `INSUFFICIENT_EVIDENCE`, `DECISION_REQUIRED` — con findings que citan la decisión, frontera o contrato contra el que se evalúa.

#### Discusión

Architecture review evalúa; no decide ni diseña. No inventa capas, servicios, colas ni adaptadores como solución (`architecture-review` §11): su recomendación es de proceso — revisar una decisión, obtener evidencia, formalizarla, volver a especificación.

Si todavía no sabes cómo está construido lo que vas a cambiar, empieza por discovery: revisar arquitectura sobre suposiciones produce findings sobre suposiciones.

No hagas: revisar arquitectura de un cambio local que no toca fronteras. Ahí no aporta.

#### Véase también

- Receta 9.2.

### 9.2 Tengo dos alternativas y quiero decidir yo

#### Problema

Hay dos opciones de diseño y quieres un análisis serio de ambas, sin que el agente elija por ti ni te empuje hacia una.

#### Solución

```text
/design Compara A (cola entre Explorer y Report Engine) y B (llamada directa
con reintentos) contra las fronteras y contratos actuales. Para cada una:
riesgos, contradicciones y qué decisiones implica. No elijas.
```

#### Discusión

El análisis termina en hechos sobre cada opción y, cuando la elección es material, en `DECISION_REQUIRED` con opciones, trade-offs y consecuencias. Puede incluir una recomendación; sigue siendo tuya la decisión.

Evaluar opciones de diseño es una tarea que tienes que pedir explícitamente: por defecto, architecture review no propone diseños.

La decisión tomada no implementa nada: sigue el camino `decisión → especificación → implementación`.

---

# Parte IV — Construir y verificar

## 10. Ejecutar un contrato

### 10.1 Tengo un contrato autorizado y quiero llevarlo hasta integración

#### Problema

La especificación está en `EXECUTION_READY` — o tienes un task contract ligero — y quieres que se implemente, se verifique y se revise, sin que nadie haga commit ni publique nada.

#### Solución

Autoriza explícitamente la ejecución y el espacio de trabajo:

```text
/deliver Execution Contract specs/membership-pause/07, autorizado: ejecútalo.
Repo backend/, rama feature/MEM-88/pausa desde dev (autorizada).
```

Para un `LIGHT`:

```text
/deliver Task contract: en el reporte, las cards se apilan en una columna
por debajo de 768 px y los textos no se cortan. Repo frontend/, rama
fix/WI-918/responsive. Verifica en los tres viewports. Sin commit.
```

`/deliver` fija el contrato autorizado y su huella, la baseline y el espacio de ejecución (un worktree en `FORMAL`), implementa, verifica, revisa con evidencia propia y, en `FORMAL`, converge contra cada criterio de aceptación. Termina en `INTEGRATION_READY` o en el gate que lo detuvo.

#### Discusión

```
EXECUTION_READY != AUTHORIZED_TO_EXECUTE.
IMPLEMENTATION APPROVAL != GIT APPROVAL.
INTEGRATION_READY != COMPLETE.
```

`/deliver` no autoriza nada por existir. Tu autorización cubre la ejecución del contrato exacto que leíste; si después el contrato cambia, la autorización caduca (receta 10.2).

En `FORMAL` el worktree es obligatorio y lo crea la Main Session; en `LIGHT` se recomienda; en `NONE` basta la work branch si el checkout está limpio.

No hagas: `/deliver crea un sistema nuevo de permisos` sin contrato. `/deliver` materializa contratos; las ideas pasan antes por `/shape` y `/spec`.

#### Véase también

- Receta 10.5 — qué hacer al llegar.
- MANUAL §5, *Línea 2*.

### 10.2 El preflight no da `PASS`

#### Problema

Autorizaste la ejecución y `/deliver` se detuvo antes de escribir una línea: `EXECUTION_PREFLIGHT_RESULT` en `BLOCKED` o `AUTHORIZATION_STALE`.

#### Solución

El resultado dice qué comprobación falló. Las más comunes:

| Motivo | Qué haces |
|---|---|
| El checkout tiene cambios que no son de esta ejecución | Autoriza un worktree para aislarla; el harness no mueve tus cambios |
| La rama no es la del contrato y no hay autorización para crearla | Autoriza la rama que propone, o indica otra |
| La huella del contrato no coincide con la autorizada (`AUTHORIZATION_STALE`) | Revisa qué cambió y vuelve a autorizar la versión actual |
| No hay autorización humana de ejecución | Dala explícitamente |

```text
Los cambios del checkout son míos y no van aquí. Autorizo el worktree
.worktrees/exec-MEM-88 sobre feature/MEM-88/pausa.
```

#### Discusión

El preflight existe para que nada se escriba sobre una base incierta. Un working tree con cambios ajenos no se toca: ni stash, ni checkout forzado, ni restore. Si estorba y no hay espacio aislado posible, el resultado es `BLOCKED` con su `STOP_REPORT`.

`AUTHORIZATION_STALE` protege tu autorización: autorizaste un contrato concreto, y si sus archivos cambiaron después, ejecutar sería ejecutar algo que no leíste.

No hagas: pedir "limpia el working tree y sigue".

#### Véase también

- Receta 12.1 — determinar la rama.

### 10.3 Fallan tests durante la implementación

#### Problema

La implementación termina y hay tests en rojo. No sabes si los rompió el cambio o ya estaban rotos.

#### Solución

No hace falta pedir nada especial: cada fallo llega atribuido contra la baseline congelada antes de empezar.

```
PREEXISTING_FAILURE    fallaba igual antes del cambio
INTRODUCED_FAILURE     pasaba antes y falla con el cambio
UNKNOWN_ATTRIBUTION    no se midió antes, o la evidencia no permite decidir
```

Si quieres más detalle sobre alguno:

```text
Muéstrame la evidencia de que test_export_empty ya fallaba en la baseline.
```

#### Discusión

Un `INTRODUCED_FAILURE` se corrige dentro del contrato. Un `PREEXISTING_FAILURE` se reporta y no se corrige, salvo que el contrato lo incluya. Un `UNKNOWN_ATTRIBUTION` nunca se presenta como preexistente para poder cerrar.

```
NO SE BORRA, SALTA NI RELAJA UN TEST PARA OBTENER VERDE.
```

Si un test protege lo contrario de lo que el contrato pide, corregirlo hacia el contrato no es debilitar evidencia: es parte de cumplirlo.

#### Véase también

- Receta 11.1.

### 10.4 La revisión encontró un problema, o un criterio quedó sin evidencia

#### Problema

La revisión independiente encontró un finding `BLOCKING`, o la convergencia dejó un criterio de aceptación en `UNVERIFIED`, `UNIMPLEMENTED` o `CONTRADICTED`. No sabes si se corrige solo o te toca decidir.

#### Solución

Cada finding llega clasificado:

| Clase | Qué pasa |
|---|---|
| `FIX_ALREADY_AUTHORIZED` | Está dentro del contrato: vuelve a implementación sin preguntarte |
| `DECISION_REQUIRED` | Corregirlo exige elegir: te llega a ti |
| `OUT_OF_SCOPE` | Fuera del contrato y del cambio: se reporta, no se toca |
| `CONTRACT_CONTRADICTION` | El contrato es imposible tal como está: vuelve a especificación y a ti |

Hay **una** vuelta de corrección. Si después sigue un finding bloqueante o un criterio material fuera de `PASS`, el resultado es `REMEDIATION_EXHAUSTED`, con su evidencia, y decides tú:

```text
Acepto mover AC-007 a la siguiente iteración; actualiza el contrato y
vuelve a especificación para eso. El resto, adelante.
```

#### Discusión

```
REVIEW_FINDING != AUTHORIZATION_TO_FIX.
REMEDIATION MAY REPAIR IMPLEMENTATION. IT MAY NOT REWRITE THE CONTRACT.
```

Un criterio `UNVERIFIED` suele arreglarse aportando la evidencia que el contrato ya exige; no es comportamiento nuevo.

Ojo con el vocabulario: en una revisión local los findings son `BLOCKING`, `MAJOR` o `MINOR`. `MUST_FIX` es la clase de un PR remoto (receta 13.1).

No hagas: pedir "otra vuelta más, que ya casi está". El límite existe para que las decisiones que tocan no se escondan en reintentos.

#### Véase también

- Receta 11.2 — cambios fuera de alcance en el diff.

### 10.5 Llegamos a `INTEGRATION_READY`: ¿y ahora?

#### Problema

`/deliver` terminó en `INTEGRATION_READY` con un `DELIVERY_EVIDENCE`, un mensaje de commit y un PR preparados. No sabes qué falta para dar el trabajo por terminado.

#### Solución

Revisa el paquete: `files_changed`, la verificación, la revisión, la convergencia por criterio de aceptación, los findings sin resolver y la deuda descubierta. Después autoriza, por separado, lo que quieras:

```text
Autorizo el commit con el mensaje preparado. Push a origin y PR hacia dev.
```

#### Discusión

```
INTEGRATION_READY != COMPLETE
INTEGRATION_READY != AUTHORIZED_TO_COMMIT / PUSH / PUBLISH_PR / MERGE
```

Cada operación Git es una autorización distinta: autorizar el commit no autoriza el push, y el push no autoriza el merge. La Main Session las ejecuta; el ciclo del PR remoto es `/pr`; `COMPLETE` lo declaras tú.

#### Véase también

- Receta 12.2.
- Receta 13.2.

## 11. Revisar una implementación

### 11.1 ¿Lo implementado cumple de verdad?

#### Problema

Tienes una implementación — tuya, de un compañero, de un agent — y los tests pasan. Necesitas saber si cumple lo que se pidió, no sólo si compila.

#### Solución

```text
/review La rama feature/MEM-88/pausa contra specs/membership-pause/07.
```

La revisión separa tres cosas: lo esperado (contrato o especificación), lo implementado (el diff efectivo) y lo verificado (la evidencia). Termina en `REVIEW_PASS`, `REVIEW_PASS_WITH_FINDINGS`, `REVIEW_BLOCKED` o `INSUFFICIENT_EVIDENCE`, y con especificación formal añade el estado de cada criterio de aceptación.

#### Discusión

```
IMPLEMENTED != VERIFIED != CONFORMANT.
SELF-VERIFICATION != INDEPENDENT CONFORMANCE.
```

Que los tests pasen no prueba que prueben lo que importa: un comportamiento afirmado y no demostrado es un finding (`UNVERIFIED_BEHAVIOR`). Sin contrato ni expectativa autoritativa, la revisión lo declara como evidencia faltante. La falta de evidencia nunca es `REVIEW_PASS`.

Un cambio `LIGHT` se revisa contra su task contract, sin exigir un inventario de criterios formal.

No hagas: usar `/review` para un PR remoto que quieres comentar o aprobar. Eso es `/pr` (receta 13.1).

#### Véase también

- MANUAL §12.1.

### 11.2 El diff trae cosas que nadie pidió

#### Problema

Revisando un cambio ves algo que no estaba en el encargo: un refactor "de paso", un parámetro nuevo, una pantalla tocada que no tocaba.

#### Solución

La revisión lo marca como `OUT_OF_SCOPE_CHANGE` (ajeno al contrato) o `UNREQUESTED_BEHAVIOR` (comportamiento añadido que nadie pidió) y lo deriva a `governance-review`. Decides tú:

```text
Retira el refactor de ExportService; lo abriremos como item aparte.
El parámetro nuevo se queda: añádelo al contrato.
```

#### Discusión

Un cambio fuera de alcance en el diff deja el trabajo en `integration_ready: NO` hasta que decides retirarlo o incorporarlo. No es un detalle de estilo: es alcance no autorizado.

Es distinto de un problema ajeno que se descubre por el camino (deuda, un defecto en otro módulo): ese se reporta y no se toca.

```
OUT-OF-SCOPE DISCOVERY IS REPORTED, NOT ABSORBED.
```

No hagas: `implementation: elige tú si también modificamos Report Studio`. La autonomía táctica no incluye cambiar el alcance material (`ENGINEERING_GOVERNANCE.md` §1.3).

---

# Parte V — Integrar

## 12. Ramas, commits y PRs

### 12.1 No sé en qué rama va este trabajo

#### Problema

Vas a empezar a implementar y estás en `dev`, o en la rama de otro ticket, o no sabes cuál es la base correcta.

#### Solución

```text
/skill:git-workflow
Determina rama base, work branch esperada y destino del PR para WI-918
(bug) en frontend/. No ejecutes operaciones Git.
```

Recibes un `BRANCH_PREFLIGHT`:

```
CURRENT_BRANCH:        dev
WORKING_TREE:          clean
EXPECTED_BASE:         dev
EXPECTED_WORK_BRANCH:  fix/WI-918/<descripción>
PR_TARGET:             dev
BRANCH_STATUS:         ON_PERMANENT_BRANCH
NEXT_GIT_ACTION:       AUTHORIZATION_REQUIRED: git switch -c fix/WI-918/responsive dev
```

#### Discusión

El preflight es Git de sólo lectura: siempre se puede pedir. Crear o cambiar de rama exige tu autorización, aunque la herramienta no pregunte (`POLICY_PERMITS != TOOL_LAYER_AUTO_APPROVES`).

En una rama permanente (`main`, `dev`, `qa`, `release-candidate`) no se implementa; en la rama de otro work item tampoco: no se mezclan intenciones. Si falta el ID del work item o el tipo, se te pide en lugar de inventarlo.

Si hay cambios que no son tuyos en el working tree, no se mueven para poder cambiar de rama (receta 10.2).

#### Véase también

- MANUAL §20.

### 12.2 Quiero el commit y el PR preparados, no ejecutados

#### Problema

Quieres revisar el mensaje de commit y la descripción del PR antes de que exista nada, o vas a hacer el commit tú mismo.

#### Solución

```text
Prepara el commit y el PR para estos cambios. No ejecutes operaciones Git.
```

Recibes un `COMMIT_MESSAGE` y un `PR_DRAFT` (título y cuerpo) con la trazabilidad del work item, y el `NEXT_GIT_ACTION` que haría falta con su estado de autorización.

#### Discusión

Preparar no autoriza ejecutar. Cuando quieras que se ejecute, autorízalo por operación (receta 10.5). La versión de un release nunca la decide el agente: llega como `VERSION_PROPOSAL`.

## 13. Pull Requests

### 13.1 Quiero revisar un PR sin publicar nada

#### Problema

Te toca revisar un PR y quieres un análisis serio antes de comentar nada en el remote.

#### Solución

```text
/pr 127
```

Sin más instrucciones, sólo se revisa. Recibes un `PR_REVIEW_REPORT` con findings (`MUST_FIX`, `SHOULD_IMPROVE`, `SUGGESTION`), un outcome (`APPROVE`, `APPROVE_WITH_COMMENTS`, `CHANGES_REQUIRED`, `INSUFFICIENT_EVIDENCE`), los comentarios propuestos y las acciones disponibles:

```
OUTCOME: CHANGES_REQUIRED
COMMENTS_TO_POST:  C1 (MUST_FIX) · C2 (SUGGESTION)
ACTIONS_AVAILABLE:
  PUBLISH_COMMENTS:     AVAILABLE (C1, C2)
  APPROVE:              NOT_AVAILABLE: hay un MUST_FIX
  AUTHOR_NOTIFICATION:  AVAILABLE
```

#### Discusión

Listar una acción no la ejecuta. Revisar es implícito; publicar, aprobar, mergear, sincronizar y notificar son autoridades independientes que no se implican entre sí.

Un `MUST_FIX` basta para `CHANGES_REQUIRED`. Una `SUGGESTION` nunca bloquea la aprobación.

No hagas: usar `/review` para esto. `/review` revisa una implementación local contra su contrato; `/pr` conduce el PR remoto.

#### Véase también

- MANUAL §12.5.

### 13.2 Quiero autorizar acciones sobre un PR o un lote

#### Problema

Revisaste varios PRs y quieres que se publiquen ciertos comentarios, se aprueben los que estén bien, se mergeen algunos y se avise a los autores de los que tienen `MUST_FIX`, sin confirmar cada comando.

#### Solución

Fija el conjunto y las acciones en una frase:

```text
/pr 127 131 140
Publica los comentarios, aprueba los que queden en APPROVE y mergea el
131 si es elegible. Avisa a los autores con MUST_FIX.
```

Cada PR se procesa por separado. Al final recibes un `BATCH_RESULT` con lo que se hizo en cada uno, lo que no y por qué, verificado contra el estado remoto.

#### Discusión

```
AUTHORIZED_SET IS CLOSED.  AUTHORIZED_ACTIONS ARE CLOSED.
AUTHORIZE THE EFFECT, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.
AUTHORIZED != ELIGIBLE.
```

Una acción autorizada sobre un PR no elegible — un merge sin la aprobación que pide la regla — se registra con su blocker y no se ejecuta. Un PR bloqueado no detiene el resto del lote. Tras cada mutación se relee el estado real: un exit 0 no es evidencia.

Si la instrucción es ambigua ("encárgate de los PRs"), sólo se revisa y se te pide la precisión que falta.

Sincronización y notificaciones son capabilities opcionales del provider configurado por la composición (por ejemplo, un organization plugin): si el provider no las soporta, aparecen como `NOT_AVAILABLE` y el resto del ciclo no cambia.

#### Véase también

- `pr-review` §19.2.

### 13.3 El PR no se puede mergear porque su destino avanzó

#### Problema

La revisión del PR salió bien, pero no se puede mergear: la rama destino avanzó desde que se abrió y hay conflictos, o el método de merge exige fast-forward.

#### Solución

Si el PR lo necesita, la revisión lo muestra como `SYNC_REMEDIATION` disponible. Autorízala:

```text
Autorizo la sincronización del 131.
```

El harness abre un PR auxiliar que integra el destino en la rama del PR — una reconciliación mecánica —, lo mergea si es elegible y revalida el PR original. Las approval rules pendientes se satisfacen después de sincronizar: aprobar antes quedaría invalidado por el cambio.

#### Discusión

La sincronización es una capability opcional del provider: sólo está disponible si el provider configurado la soporta. Sólo aplica cuando el único blocker es la desincronización: si hay un `MUST_FIX` u otro blocker, el PR se reporta con ese blocker. La sincronización se limita a reconciliar; si un conflicto exige decidir qué comportamiento queda, eso no es mecánico y vuelve como `DECISION_REQUIRED`.

```
SYNC_REMEDIATION != FUNCTIONAL_REMEDIATION.
```

```
SYNC AUTHORIZATION != GENERAL GIT WRITE AUTHORITY.
```

---

# Parte VI — Uso avanzado

## 14. Skills directamente

### 14.1 Quiero análisis de gestión sin el recorrido de `/shape`

#### Problema

Tienes cuatro iniciativas en una lista y quieres compararlas — dependencias, riesgo, cuál puede avanzar, qué decisiones faltan — pero no son work items que vayan a entrar al sistema todavía.

#### Solución

```text
/skill:project-management
Analiza estas cuatro iniciativas: dependencias, riesgo, cuál puede avanzar
y qué decisiones faltan. No quiero ejecutar nada.
```

#### Discusión

Por qué una skill directa aquí: `/shape` está pensado para dar forma a un item y recomendar cómo entra; `/project`, para gestionar un frente. Para una comparación puntual, la metodología basta y no necesitas su recorrido.

Invocar una skill no crea autoridad: sigue sin priorizar por ti ni aceptar riesgos.

Lo mismo vale para otras skills sin work mode propio: `/skill:git-workflow` (receta 12.1) o `/skill:delivery-lifecycle` para conducir tú el lifecycle paso a paso en la sesión, en lugar de delegarlo.

`code-quality` no se invoca: se aplica siempre que se escribe código.

### 14.2 Quiero una revisión de seguridad de un cambio concreto

#### Problema

Un cambio toca autenticación, permisos, secretos o entrada externa, y quieres saber si introduce un riesgo demostrable antes de integrarlo.

#### Solución

```text
/skill:security-review
Revisa el diff de feature/AUTH-31 contra dev. Superficie: validación del
token en el middleware de acceso.
```

Termina en `SECURITY_PASS`, `SECURITY_PASS_WITH_FINDINGS`, `SECURITY_BLOCKED` o `INSUFFICIENT_EVIDENCE`.

#### Discusión

Por qué una skill directa: no hay work mode de seguridad. `/review` y `/pr` derivan a seguridad cuando ven superficie, pero si sabes de antemano que la pregunta es de seguridad, ir directo ahorra un paso.

Necesita un cambio concreto revisable. No es pentesting, ni auditoría general, ni una campaña de hardening, y `SECURITY_PASS` no significa que el sistema sea seguro: significa que no se encontró riesgo material en lo revisado.

## 15. Agents directamente

### 15.1 ¿Lo hago en la sesión o lo delego?

#### Problema

Tienes una pregunta técnica y no sabes si pedirla en la conversación o delegarla en un agent. O notas que la sesión se está llenando de output y ya cuesta seguir el hilo.

#### Solución

```text
Usa technical-discovery para reconstruir el flujo completo desde
POST /client/discovery hasta el inicio de Step Functions.
```

frente a:

```text
¿Qué hace esta función?
```

La primera va a un agent; la segunda se contesta en la sesión.

#### Discusión

```
AGENT = WHO + TOOLS + BOUNDARIES
SKILL = HOW

MAIN SESSION  → lo local, lo pequeño, la síntesis y la decisión
AGENT         → lo aislado, el volumen, lo especializado
```

Delega cuando el trabajo cruza componentes, tiene volumen, conviene aislar su evidencia, o necesita las herramientas de un worker concreto: `implementation` es el único que escribe código; una revisión aislada (`architecture-review`, `governance-review`) no hereda los sesgos de la conversación.

Si la Main Session está investigando un flujo entero, especificándolo, implementándolo y revisándolo, ha perdido las fronteras que dan valor al harness: delega el volumen y quédate con la síntesis.

#### Véase también

- MANUAL §4, *Cuándo usar Main Session y cuándo delegar*; MANUAL §13.

### 15.2 Quiero investigar varias cosas en paralelo

#### Problema

Hay tres preguntas independientes — qué hace el servicio A, qué hace el B, qué configuración tiene la cola — y no quieres esperar a una para empezar la siguiente. También te preocupa qué pasa si las respuestas no casan.

#### Solución

Delimita cada worker para que no se pisen, y di quién sintetiza:

```text
En paralelo, con technical-discovery:
1) servicio A: qué publica en la cola y con qué contrato;
2) servicio B: qué consume y qué hace ante un mensaje inválido;
3) la cola: configuración de reintentos y DLQ en QA.
Sintetiza tú y marca cualquier contradicción entre los tres.
```

#### Discusión

Paralelizar compensa cuando el coste de coordinar es menor que el valor de ir en paralelo y las fronteras son claras. Tres workers sobre el mismo archivo no son paralelismo: son overlap.

La Main Session es el synthesis owner. Si dos workers se contradicen, no hay votación: manda la evidencia, y si la evidencia no decide, la contradicción se reporta como tal.

#### Véase también

- MANUAL §14.

## 16. Composición de capabilities

Estas recetas combinan varias capabilities. Ninguna es un pipeline obligatorio: cada paso está porque reduce una incertidumbre, protege una frontera o produce evidencia que hace falta.

```
USE A CAPABILITY WHEN IT REDUCES UNCERTAINTY,
PROTECTS A BOUNDARY, OR PRODUCES NEEDED EVIDENCE.
```

### 16.1 Del ticket ambiguo a la corrección

#### Problema

Tienes el ticket *"el reporte no es responsive"* y quieres llevarlo hasta un cambio listo para integrar, sin saltarte pasos que hagan falta ni añadir los que no.

#### Solución

```
/shape        BUG · LIGHT · siguiente: diagnostics · después: implementation
/diagnose     qué superficies fallan, en qué viewports, por qué
(tú)          decides la superficie si la evidencia deja varias
(tú)          autorizas el task contract y la rama
/deliver      implementa, verifica en los tres viewports, revisa → INTEGRATION_READY
(tú)          autorizas commit, push y PR
```

#### Discusión

| Paso | Por qué está |
|---|---|
| `/shape` | Saber qué clase de trabajo es y por dónde entra |
| `/diagnose` | Hay un fallo observado y no se sabe dónde ni por qué |
| `/deliver` | Hay un contrato — ligero — que materializar con evidencia |

Por qué **no** está `/spec`: el comportamiento esperado ya estaba escrito en el ticket. Por qué no está `/design`: no toca fronteras.

#### Véase también

- Recetas 4.4, 10.1.

### 16.2 De una iniciativa grande a slices ejecutables

#### Problema

Tienes el frente *"PROD en AWS con CDK"* y quieres convertirlo en trabajo que se pueda ejecutar con contratos.

#### Solución

```
/shape        INFRASTRUCTURE · FORMAL · TOO_LARGE_TO_EXECUTE · SPLIT_REQUIRED
/discover     inventario QA frente a PROD, referencias desconocidas, documentación vigente
(tú)          decides el corte en slices y las decisiones de infraestructura
/spec         por slice, hasta EXECUTION_READY
(tú)          autorizas cada contrato
/deliver      por slice
```

#### Discusión

| Paso | Por qué está |
|---|---|
| `/shape` | Descubrir que no es una tarea y proponer slices |
| `/discover` | La definición depende de hechos que nadie tenía |
| `/spec` por slice | Cada slice cambia infraestructura material: necesita contrato |
| `/deliver` por slice | Cada contrato autorizado se ejecuta y se verifica por separado |

`/project` puede acompañar todo el frente para seguir dependencias, riesgos y decisiones entre slices.

#### Véase también

- Recetas 4.2, 6.3, 5.1.

### 16.3 Un fallo por memoria: de la causa al PR

#### Problema

*"Explorer está fallando por memoria. No sé si es código o infraestructura. Quiero arreglarlo correctamente."*

#### Solución

```
/diagnose     causa raíz con evidencia, o qué falta para saberla
/shape        alcance, riesgo y formalidad de la corrección
/spec         si la corrección cambia comportamiento o contratos materiales
(tú)          autorizas la ejecución
/deliver      implementación, verificación, convergencia por criterio
(tú)          autorizas commit, push y PR
/pr           ciclo del PR remoto
```

**ESTO ES UN EJEMPLO, NO EL PIPELINE OBLIGATORIO.**

#### Discusión

| Paso | Por qué está |
|---|---|
| `/diagnose` | Hay síntoma; no se sabe si la causa es código o infraestructura |
| `/shape` | La corrección puede ser local o tocar memoria, configuración e infraestructura |
| `/spec` | Sólo si cambia comportamiento material; un ajuste de configuración ya decidido no lo necesita |
| Tu autorización | `EXECUTION_READY` no es autorización |
| `/deliver` | Ejecuta exactamente el contrato que autorizaste |
| `/pr` | `INTEGRATION_READY` no es merge |

En el caso real, la especificación terminó con bloqueo parcial: la causa estaba corregida, pero faltaban dos decisiones sobre el alcance de la verificación y el sizing aprobado (receta 8.3).

#### Véase también

- Recetas 7.2, 8.1, 8.3.

---

# Índices

## Índice por problema

| Si te pasa esto | Mira |
|---|---|
| No sé por dónde empezar | 1.1 |
| Quiero sólo una parte, sin que siga de largo | 1.2 |
| Me piden una decisión | 1.3, 4.5, 8.2 |
| No sé cómo atacar un trabajo complejo | 2.1 |
| Quiero delegar todo el recorrido / se detuvo | 3.1, 3.2 |
| No sé si un ticket está listo | 4.1, 8.5 |
| Es demasiado grande | 4.2, 16.2 |
| Faltan hechos para decidir cómo seguir | 4.3, 6.1 |
| Un bug con el esperado claro | 4.4, 16.1 |
| Tengo que contárselo a dirección | 4.6, 5.2 |
| Varios trabajos, dependencias, blockers | 5.1 |
| Fechas, forecast, "vamos al 80 %" | 5.2 |
| Cambió un requisito | 5.3 |
| No entiendo cómo funciona | 6.1 |
| La documentación o el ticket pueden mentir | 6.2 |
| QA y PROD se comportan distinto | 6.3, 7.2 |
| Algo es lento | 7.1 |
| Algo muere por memoria | 7.2, 16.3 |
| Fallo intermitente, varias causas | 7.3 |
| Ya sé la causa | 7.4 |
| Necesidad ambigua | 8.1 |
| La especificación no quedó lista | 8.3 |
| Lo decidido choca con la realidad | 8.4 |
| Validar un diseño o elegir entre opciones | 9.1, 9.2 |
| Implementar un contrato | 10.1 |
| No arranca la ejecución | 10.2 |
| Tests en rojo | 10.3 |
| La revisión encontró algo | 10.4, 11.2 |
| Terminó: ¿y ahora? | 10.5 |
| Revisar una implementación | 11.1 |
| Rama equivocada | 12.1 |
| Commit y PR preparados | 12.2 |
| Revisar, aprobar o mergear PRs | 13.1, 13.2 |
| PR desincronizado | 13.3 |
| Seguridad de un cambio | 14.2 |
| ¿Sesión o agent? Trabajo en paralelo | 15.1, 15.2 |

## Índice por command y capability

| Command / capability | Recetas |
|---|---|
| Control Tower (conversación) | 1.1, 1.2, 1.3 |
| `/plan` | 2.1 |
| `delivery-orchestrator` | 3.1, 3.2 |
| `/shape` | 4.1–4.6, 8.5, 16.1–16.3 |
| `/project` | 5.1, 5.2, 5.3 |
| `/discover` | 6.1, 6.2, 6.3, 16.2 |
| `/diagnose` | 7.1–7.4, 16.1, 16.3 |
| `/spec` | 8.1–8.5, 16.2, 16.3 |
| `/design` | 9.1, 9.2 |
| `/deliver` | 10.1–10.5, 16.1–16.3 |
| `/review` | 11.1, 11.2 |
| `git-workflow` | 12.1, 12.2 |
| `/pr` | 13.1, 13.2, 13.3, 16.3 |
| Skills directas | 12.1, 14.1, 14.2 |
| Agents | 6.1, 15.1, 15.2 |

## Anti-patrones, de un vistazo

Cada uno aparece en la receta donde es útil; aquí sólo se enumeran.

| No hagas | Por qué | Receta |
|---|---|---|
| Encadenar todos los commands para cada ticket | `CEREMONY != GOVERNANCE` | 1.1, 16 |
| Pedir a discovery que decida la arquitectura | Reconstruye lo que hay; no define lo que debería haber | 6.1, 9.1 |
| Diagnosticar sin un fallo observado | Sin síntoma no hay diagnóstico | 7.1 |
| Arreglar dentro del diagnóstico | `DIAGNOSIS != REMEDIATION` | 7.4 |
| `/deliver` sobre una idea sin contrato | `/deliver` materializa contratos | 10.1 |
| Dejar que implementation elija alcance material | La autonomía táctica no cambia el alcance | 11.2 |
| Usar `/plan` para reabrir un contrato | Se reabre por evidencia o por tu decisión | 2.1 |
| Pedir una fecha "razonable" | Una fecha inventada no es un forecast | 5.2 |
| Limpiar el working tree para que la ejecución arranque | Los cambios ajenos no se mueven | 10.2 |
