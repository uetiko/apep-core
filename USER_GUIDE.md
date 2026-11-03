# USER GUIDE — Apep Core

Cómo empezar, qué puedes pedir y cuánto delegar en el harness.

**Este documento enseña a usar el harness. No define governance ni metodología.** Ante discrepancia mandan las fuentes normativas y el MANUAL:

```
ENGINEERING_GOVERNANCE.md · rules/ · AGENTS.md · skills     (normativo)
  → MANUAL.md                                                 (referencia operacional)
    → USER_GUIDE.md · COOKBOOK.md                             (uso y recetas)

THE USER GUIDE TEACHES THE SYSTEM.
THE MANUAL EXPLAINS THE SYSTEM.
THE COOKBOOK SOLVES PROBLEMS WITH THE SYSTEM.
THIS GUIDE ILLUSTRATES. IT DOES NOT LEGISLATE.
```

| Quieres | Lee |
|---|---|
| Arrancar el harness | [README.md](README.md) |
| Aprender a usarlo | esta guía |
| Resolver un problema concreto con una receta | [COOKBOOK.md](COOKBOOK.md) |
| Entender su modelo operativo, estados, autoridad y lifecycle | [MANUAL.md](MANUAL.md) |
| La governance normativa | [`ENGINEERING_GOVERNANCE.md`](docs/governance/ENGINEERING_GOVERNANCE.md) |

---

## 1. Empieza aquí

No necesitas conocer los commands, las skills ni los agents para usar el harness. Arranca OMP desde la raíz de tu proyecto ([README.md](README.md)) y trae lo que tengas:

- una necesidad;
- un ticket;
- un fallo;
- una pregunta;
- un diseño;
- un diff;
- un PR;
- un proyecto que no sabes cómo ordenar.

Escríbelo como se lo contarías a un compañero. La sesión en la que escribes — la **Control Tower** — interpreta la intención, elige la metodología, delega cuando conviene y te devuelve las decisiones que siguen siendo tuyas.

```
BRING WHAT YOU HAVE.

A NEED. A TICKET. A FAILURE. A QUESTION.
A DESIGN. A DIFF. A PR.

THE HARNESS HELPS DETERMINE WHAT COMES NEXT.
```

```
WHEN IN DOUBT:
START WITH THE CONTROL TOWER.
DESCRIBE THE PROBLEM, NOT THE TOOL.
```

```
YOU DO NOT NEED TO KNOW THE PROCESS
BEFORE YOU CAN USE THE PROCESS.

USE FIRST. UNDERSTAND INTERNALS LATER.
```

## 2. Cosas que puedes hacer desde el primer día

Ninguno de estos ejemplos nombra una capability. Todos funcionan tal cual.

**Dar forma a un ticket**

```
Tengo este ticket, pero no sé si está suficientemente definido.
Ayúdame a revisar qué falta antes de programarlo.
```

**Investigar un fallo**

```
Algo está fallando en QA.
No cambies nada todavía.
Primero quiero saber qué está pasando.
```

**Entender código existente**

```
Necesito cambiar este módulo,
pero no conozco bien cómo funciona actualmente.
Investígalo antes de proponer cambios.
```

**Dar forma a una iniciativa grande**

```
Tenemos que levantar producción.
No sé si esto es una tarea o varias,
qué dependencias tiene ni qué hay que decidir primero.
```

**Gestionar varios trabajos**

```
Tengo estos trabajos pendientes.
Dime cuáles pueden avanzar,
cuáles están bloqueados
y qué decisiones faltan.
```

**Implementar algo ya autorizado**

```
Esta especificación ya está aprobada.
Impleméntala y verifica el resultado.
No hagas commit ni publiques nada.
```

**Revisar un PR**

```
Revisa este PR.
Dime si está listo,
pero no apruebes ni hagas merge sin mi autorización.
```

No elegiste ninguna capability. La Control Tower interpreta la intención, elige la metodología adecuada, delega cuando corresponde y te devuelve las decisiones que siguen siendo humanas: el alcance, la semántica de negocio, la arquitectura, la autorización para ejecutar y toda operación Git (MANUAL §1, *Autoridad humana*).

## 3. Lo que no necesitas preparar antes

Para empezar **no** hace falta tener:

- un prompt perfecto;
- la especificación terminada;
- todos los criterios de aceptación;
- el repositorio exacto;
- la causa raíz;
- la solución técnica;
- el command o el agent correctos;
- un plan completo.

Puedes empezar con una idea, un síntoma, una necesidad, un ticket incompleto, una pregunta, una propuesta, código ya escrito o un PR. Lo que falta se investiga — si es un hecho — o se te pregunta — si es una decisión.

```
THE HARNESS CAN INVESTIGATE FACTS AND RECOMMEND.
IT CANNOT TAKE MATERIAL HUMAN DECISIONS FOR YOU.
```

## 4. Formas válidas de empezar

Cinco entradas para la misma intención de fondo. Todas son válidas.

**1. Conversación natural**

```
Tengo que agregar exportación CSV,
pero el ticket sólo dice eso.
Ayúdame a darle forma.
```

**2. Work mode** — un command que dice qué quieres conseguir:

```
/shape Agregar exportación CSV al reporte de cartera.
```

**3. Skill directa** — la metodología, sin el work mode:

```
/skill:project-management
Compara estas cuatro iniciativas
y analiza dependencias, riesgo y readiness.
```

**4. Agent** — un worker especializado con su propio contexto:

```
Usa technical-discovery para reconstruir
el flujo completo de autenticación.
```

**5. Plan mode** — cuando lo que falta es cómo abordar el trabajo:

```
/plan
Tenemos que migrar este módulo.
Antes de hacer nada quiero ordenar
la investigación, las dependencias y la estrategia.
```

La diferencia es cuánto quieres dirigir tú y cuánto quieres que el harness enrute por ti. Si dudas, la primera siempre funciona.

## 5. ¿Cuánto quieres delegar?

```
QUIERO CONVERSAR Y TOMAR DECISIONES                → Control Tower
QUIERO PEDIR UNA CAPABILITY CONCRETA               → Work mode
QUIERO APLICAR UNA METODOLOGÍA CONCRETA            → Skill
QUIERO DELEGAR TRABAJO ESPECIALIZADO               → Agent
QUIERO DELEGAR EL LIFECYCLE DE UN ITEM DELIMITADO  → delivery-orchestrator
```

En la práctica:

- **Control Tower.** Vas viendo resultados y decidiendo el siguiente paso. Es lo normal mientras el trabajo todavía está tomando forma.
- **Work mode.** Ya sabes qué tipo de ayuda quieres ("dale forma", "diagnostica", "revisa el PR"). El command carga la metodología y los workers que tocan.
- **Skill.** Quieres una metodología concreta aplicada a algo que no encaja con un work mode, o sin el recorrido que el work mode propone.
- **Agent.** El trabajo tiene volumen o conviene aislarlo: reconstruir un flujo que cruza componentes, implementar, revisar un diff.
- **`delivery-orchestrator`.** El work item ya está delimitado y quieres que el harness conduzca el recorrido completo y vuelva sólo cuando haga falta tu decisión.

No es una escala de autoridad: en las cinco, las decisiones materiales siguen siendo tuyas. Es una escala de cuánto conduces tú.

## 6. Conversaciones que crecen

No hace falta conocer la ruta completa al empezar. Estas tres conversaciones empiezan con una frase y crecen según lo que se descubre.

### A — Un ticket ambiguo

```
Tengo este ticket: "El reporte no es responsive". ¿Me ayudas?
```

La Control Tower le da forma (`/shape`): es un `BUG`, de formalidad `LIGHT`. Lo primero no es programar sino localizar y reproducir el fallo — incluida la duda de qué superficie es "el reporte", que el sistema puede averiguar por sí mismo. Siguiente paso: `diagnostics`.

Con la superficie y la causa encontradas:

```
Ya encontramos la superficie y la causa. Quiero corregirlo.
```

Ahora sí: un task contract ligero (qué se cambia, dónde, cómo se comprueba, en qué rama), tu autorización, y `/deliver` lo implementa, lo verifica y lo revisa hasta `INTEGRATION_READY`. El commit y el PR los autorizas tú.

Si la evidencia hubiera dejado varias superficies igualmente válidas, elegir una habría sido decisión tuya, no del implementador.

```
YOU DO NOT NEED TO KNOW THE WHOLE ROUTE BEFORE YOU START.
```

### B — Una iniciativa grande

```
Tenemos que levantar PROD y empezar a promover lo estable de QA.
```

El harness descubre qué es eso: `INFRASTRUCTURE`, `FORMAL`, `TOO_LARGE_TO_EXECUTE`, `SPLIT_REQUIRED`. Es un frente, no una tarea. Faltan hechos de los que depende la definición — qué hay realmente en QA y en PROD, referencias que nadie reconoce, documentación desactualizada —, así que el siguiente paso recomendado es investigar (`technical-discovery`), y después especificar slice a slice. Implementar queda bloqueado mientras no haya contrato.

```
YOU CAN BRING UNFORMED WORK.
SHAPING IS PART OF THE SYSTEM.
```

### C — No conozco el proyecto

```
Me pidieron revisar por qué esta Lambda tarda 25 segundos.
No conozco este proyecto ni sé por dónde empezar.
```

Hay un síntoma observado: el centro es `diagnostics`. Si para seguir la cadena hace falta entender primero el flujo, la Control Tower intercala `technical-discovery`. El resultado es una causa con su evidencia — o `INSUFFICIENT_EVIDENCE` y qué faltaría medir — y una recomendación. Ahí se detiene: corregir es otro paso, con su propio alcance, que decides tú.

```
BRING THE PROBLEM.
THE HARNESS HELPS STRUCTURE THE WORK.
```

## 7. Pedir sólo una parte

El harness no es sólo una fábrica autónoma. Puedes invocar una capability acotada y detenerte ahí:

```
Sólo quiero entender el estado actual. No propongas cambios.
```

```
Sólo quiero saber si este ticket está listo. No lo implementes.
```

```
Haz el diagnóstico. No corrijas nada.
```

```
Revisa el diseño. No escribas código.
```

```
Prepara el commit y el PR. No ejecutes operaciones Git.
```

```
Resume los riesgos para dirección.
Incluye detalle técnico sólo cuando sostenga una conclusión.
```

```
THE HARNESS IS NOT ONLY AN AUTONOMOUS SOFTWARE FACTORY.
YOU CAN INVOKE ONE BOUNDED CAPABILITY AND STOP THERE.
```

## 8. Delegar el recorrido completo

El caso opuesto:

```
Este work item ya está suficientemente delimitado.
Quiero llevarlo hasta INTEGRATION_READY.
Detente sólo ante una decisión material o un gate humano.
```

Eso es delegar en `delivery-orchestrator`. Es apropiado cuando el trabajo es un work item — no una idea ni un frente — y su alcance ya está claro. El orchestrator clasifica, decide qué capability sigue, delega en los workers, verifica, revisa y prepara commit y PR. Vuelve a ti ante un gate real o con el paquete `INTEGRATION_READY`. No hace commit, push ni merge (MANUAL §4, *`delivery-orchestrator`*).

| Control Tower | `delivery-orchestrator` |
|---|---|
| Quieres ir viendo y decidiendo | Quieres delegar el recorrido de un item ya delimitado |
| Vas a combinar capabilities y mirar los resultados entre pasos | Te basta con que vuelva por gates reales |
| El trabajo todavía está tomando forma | El trabajo ya tiene forma |

```
CONTROL TOWER != DELIVERY ORCHESTRATOR
THE ORCHESTRATOR CHOOSES THE NEXT CAPABILITY.
IT DOES NOT ACQUIRE THAT CAPABILITY'S AUTHORITY.
```

## 9. Recetas

Las situaciones concretas — un ticket que no sabes si está listo, una Lambda lenta, un preflight que no da `PASS`, un lote de PRs — viven en el [COOKBOOK.md](COOKBOOK.md): una receta por problema, con qué escribir, qué esperar y dónde decides tú. Su *Índice por problema* es la entrada más rápida.

Lo que esta guía sí te deja como criterio:

```
USE A CAPABILITY WHEN IT REDUCES UNCERTAINTY,
PROTECTS A BOUNDARY, OR PRODUCES NEEDED EVIDENCE.
```

Un cambio pequeño y claro no necesita `/shape`, `/spec` ni `/design`; un frente grande sí necesita forma antes de construirse. Las recetas muestran los dos extremos y lo que hay entre medias.

## 10. Ejemplos según lo que haces

Mismo modelo operativo, distintos puntos de entrada. No hay un proceso por rol.

| Rol | Por ejemplo |
|---|---|
| Developer | *"Tengo este bug. Quiero saber si está suficientemente definido antes de tocar código."* |
| QA | *"Este comportamiento falla sólo en QA. Ayúdame a reunir evidencia y delimitar la reproducción."* |
| Product / PM | *"Tenemos esta necesidad. No sé si está lista para ingeniería. Dale forma y dime qué decisiones faltan."* |
| Tech Lead | *"Tenemos estas opciones de arquitectura. Quiero revisar boundaries y dependencias antes de decidir."* |
| Engineering Manager | *"Tengo siete trabajos abiertos. Quiero blockers, dependencias, riesgos y qué puede avanzar ahora."* |
| Dirección | *"Necesito saber qué impide que PROD esté listo, qué decisiones necesitan autoridad y cuál es la secuencia recomendada."* |

Los resultados de dar forma y de gestión de proyecto empiezan por un resumen en lenguaje de gestión, siguen con el detalle de ingeniería y terminan con el registro de proceso: el mismo análisis para lectores distintos (MANUAL §5, *Cómo se presentan los resultados*).

```
SAME OPERATING MODEL.
DIFFERENT ENTRYPOINTS.
```

## 11. Cheat sheet de commands

Ahora que sabes qué puedes pedir, ésta es la correspondencia con los commands. Semántica completa: MANUAL §7 (*Apep Work Modes*); situación → capability: MANUAL §17.

| Si quieres… | Usa | Detrás |
|---|---|---|
| No sabes por dónde empezar | la conversación | Control Tower |
| Dar forma a una necesidad, idea, ticket o bug | `/shape` | `project-management`, work item |
| Gestionar un proyecto o un frente | `/project` | `project-management`, proyecto |
| Entender cómo funciona algo hoy | `/discover` | `technical-discovery` |
| Definir qué debe hacer el sistema | `/spec` | Línea 1 — Specification Factory |
| Encontrar la causa de algo que falló | `/diagnose` | `diagnostics` |
| Validar un diseño o sus fronteras | `/design` | `architecture-review` |
| Materializar un contrato autorizado | `/deliver` | Línea 2 — Delivery Factory |
| Revisar lo que se implementó | `/review` | `implementation-review` |
| Procesar el Pull Request remoto | `/pr` | `pr-review` |
| Pensar cómo abordar un trabajo complejo | `/plan` | Modo nativo de OMP |
| Aplicar una metodología directamente | `/skill:<skill>` | La skill |
| Delegar el lifecycle de un item delimitado | agent `delivery-orchestrator` | `delivery-lifecycle` |

Un work mode es una entrada de UX: no añade método, autoridad ni modelo.

## 12. `/plan`, skills y agents en la práctica

### ¿Cuándo uso `/plan`?

```
/plan     = ¿CÓMO ABORDAMOS EL TRABAJO?
/spec     = ¿QUÉ DEBE HACER EL SISTEMA?
/deliver  = MATERIALIZA LO QUE AUTORIZASTE.
```

Cuando no sabes cómo atacar el objetivo, hay que ordenar la investigación, hay dependencias o hay que decidir qué va en paralelo:

```
/plan
Necesito investigar por qué esta Lambda tarda 25 segundos. Quiero definir
primero qué evidencia buscar, qué dependencias hay y qué podemos investigar
en paralelo.
```

No para definir el comportamiento del producto (eso es `/spec`), ni para reabrir un contrato ya autorizado (MANUAL §6).

### ¿Cuándo uso una skill directamente?

Cuando quieres la metodología sin el recorrido de un work mode:

```
/skill:project-management
Analiza estas cuatro iniciativas: dependencias, riesgo, cuál puede avanzar
y qué decisiones faltan. No quiero ejecutar nada.
```

```
/skill:architecture-review
Evalúa esta propuesta de separar Report Engine en otro servicio.
No diseñes el reemplazo ni implementes nada.
```

```
/skill:git-workflow
Determina rama base, destino y flujo esperado para este cambio.
No ejecutes operaciones Git.
```

Invocar una skill no crea autoridad ni la convierte en agent (MANUAL §7).

### ¿Cuándo delego en un agent?

Cuando el trabajo cruza archivos o componentes, tiene volumen o conviene aislar su evidencia del contexto de la sesión:

```
Usa technical-discovery para reconstruir el flujo completo desde
POST /client/discovery hasta el inicio de Step Functions.
```

*"¿Qué hace esta función?"* normalmente no lo necesita: se contesta en la sesión.

```
MAIN SESSION  → lo local, lo pequeño, la síntesis y la decisión
AGENT         → lo aislado, el volumen, lo especializado
```

Fronteras de cada agent y tabla *Cuándo usar Main Session y cuándo delegar*: MANUAL §4 y MANUAL §13.

## 13. Anti-patrones de uso

| Anti-patrón | Por qué no |
|---|---|
| `/shape` → `/spec` → `/design` → `/deliver` → `/review` → `/pr` para cada ticket | `CEREMONY != GOVERNANCE`: cada paso necesita una incertidumbre, una frontera o una evidencia que lo justifique |
| *"/discover dime cuál debería ser nuestra arquitectura"* | Discovery reconstruye lo que hay; el diseño lo valida `/design` y lo decides tú |
| *"/diagnose busca problemas potenciales"* | Sin un fallo observado no hay diagnóstico: la pregunta es "¿cómo funciona?" (`/discover`) |
| *"/deliver crea un sistema nuevo de permisos"* sin contrato autorizado | `/deliver` materializa un contrato; la idea pasa antes por `/shape` y `/spec` |
| *"implementation: elige tú si también modificamos Report Studio"* | La autonomía táctica no incluye cambiar el alcance material (`ENGINEERING_GOVERNANCE.md` §1.3) |

**Cuándo no usar cada capability:**

| Capability | No la uses para |
|---|---|
| `/shape` | Un cambio local ya perfectamente determinado, sólo por ceremonia |
| `/spec` | Una errata, o para reconstruir el estado actual |
| `/discover` | Decidir qué arquitectura adoptar |
| `/diagnose` | "Buscar posibles problemas" sin un síntoma observado |
| `/deliver` | Convertir en código una idea que nadie especificó ni autorizó |
| `/review` | El PR remoto: eso es `/pr` |
| `/pr` | Revisar una implementación local: eso es `/review` |
| `/plan` | Reabrir un contrato ya autorizado |

Anti-patrones del proceso, con su razón: MANUAL §22.

## 14. Dónde leer más

| Pregunta | Dónde |
|---|---|
| ¿Qué es la Control Tower y qué no debe hacer? | MANUAL §4 |
| ¿Cómo fluye un work item, qué es la Línea 2, cuáles son los gates humanos? | MANUAL §5 |
| ¿Qué hace cada work mode y cada skill? | MANUAL §7 |
| ¿Cómo se llega a `EXECUTION_READY`? | MANUAL §8 |
| ¿Qué pregunta responde cada review? ¿Cómo funciona `/pr`? | MANUAL §12 |
| ¿Qué agents hay y con qué fronteras? | MANUAL §13 |
| Situación → capability | MANUAL §17 |
| Prompts de control por capability | MANUAL §18 |
| Git, commit y PR | MANUAL §20 |
| Autonomía y approvals | MANUAL §23 |
| Limitaciones conocidas | MANUAL §24 |
| Una receta para un problema concreto | [COOKBOOK.md](COOKBOOK.md), *Índice por problema* |
| Regenerar los ebooks | MANUAL §1, *Ebooks* |
