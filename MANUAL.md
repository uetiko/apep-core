# MANUAL — Apep Core Engineering Harness v0.1.0

Manual operativo de Apep Core, el harness de ingeniería para OMP reutilizable e independiente de cualquier organización: qué es, cómo se arranca, qué capabilities tiene, qué autonomía y qué límites de autoridad aplican, y cómo fluye una tarea desde la idea hasta el PR.

**Versión de Apep Core: 0.1.0** (`VERSION`, junto a este manual) — primera separación material de la metodología como paquete OMP independiente (`CHANGELOG.md`). Entrega 11 skills (`project-management` como **work shaping + flow management** y **gestión de proyectos de software**; la Línea 1 como **Specification Factory** —acepta necesidades todavía ambiguas, clasifica cada apertura, investiga los hechos, te pregunta sólo las decisiones materiales con un ledger de clarificaciones y revisa calidad y coherencia antes del readiness gate C1–C4—; la Línea 2 como **Delivery Factory** —contrato autorizado → ejecución controlada → verificación → conformidad independiente por AC → `DELIVERY_EVIDENCE`—; `pr-review` y `git-workflow` como modelos genéricos independientes del provider; y las skills de discovery, diagnostics, reviews y calidad de código), 6 agents, 9 work modes (slash commands) y 1 archivo de reglas sticky. Lo que depende de una organización —un provider remoto concreto, un modelo de ramas propio, reglas específicas de un workspace— lo aporta un plugin de organización (§1, *Composición*).

Documento **operacional, no normativo**. Describe el estado vigente; la historia de cómo se llegó aquí está en [CHANGELOG.md](CHANGELOG.md). Entrada breve: [README.md](README.md).

> **EL MANUAL DESCRIBE EL HARNESS. EL MANUAL NO DEFINE EL HARNESS.** Si discrepa de las fuentes normativas, se corrige el manual.

**Para aprender a usarlo:** [USER_GUIDE.md](USER_GUIDE.md). **Recetas por problema:** [COOKBOOK.md](COOKBOOK.md). Este manual es la **referencia** del modelo operativo; la guía y el cookbook enseñan y resuelven con ejemplos, y no definen nada. Ante discrepancia: fuentes normativas → MANUAL → USER_GUIDE y COOKBOOK.

---

## 1. Propósito, principios y precedencia

### Qué es

OMP (Oh My Pi, `omp/18.2.11`, la versión contra la que se verificaron los hechos de runtime de este manual) es el runtime. Apep Core —un plugin de OMP— es la compilación operativa de `docs/governance/ENGINEERING_GOVERNANCE.md` sobre ese runtime. Coordina:

| Pieza | Dónde vive | Papel |
|---|---|---|
| Governance | `docs/governance/ENGINEERING_GOVERNANCE.md`, reglas sticky (`rules/engineering-discipline.md`), `AGENTS.md` del proyecto consumidor | Qué está permitido y quién decide |
| Main Session | La conversación interactiva | Control Tower: interpreta, delega, sintetiza (§4) |
| Skills | `skills/` del plugin | Metodología cargable (§7) |
| Agents | `agents/` del plugin | Workers especializados (§13) |
| Tools | OMP (`read`, `edit`, `bash`, `eval`, `task`…) | Ejecutan, con su capa de approvals (§23) |
| Execution Contracts | `specification` / task contract | Fijan scope, decisiones cerradas e invariantes (§8) |
| Verification | `code-quality`, `implementation`, reviews | Evidencia antes de `COMPLETE` (§21) |

```
THE HARNESS GOVERNS INTENT.
THE EXECUTION CONTRACT GOVERNS SCOPE.
TOOLS EXECUTE WITHIN THAT AUTHORITY.

AUTONOMY != AUTHORITY
```

OMP aporta la maquinaria; la metodología la fija este proceso. Cuando el comportamiento por defecto de OMP y la governance divergen, manda la governance. Ejemplo: el default de OMP para `tools.approvalMode` es `yolo`; Apep Core recomienda `write` (§23) y no puede imponerlo, porque un plugin no entrega settings. `yolo` no es un modo deseado en un proyecto que adopte este harness.

### Composición: Apep Core y plugins de organización

```
REMOVE THE ORGANIZATION PLUGIN → APEP CORE REMAINS A VALID ENGINEERING HARNESS
```

Apep Core es la capa pública: sólo contiene lo que tiene sentido fuera de cualquier organización (mecanismo y metodología, no contexto de cliente, ni identificadores, topología o nombres de repositorios concretos). Lo organizacional se compone encima con un **plugin de organización**, que es quien aporta:

- el **provider** concreto de `pr-review`: la mecánica contra un remote (CodeCommit, GitHub u otro), su clasificación de operaciones, la sincronización y las notificaciones opcionales (§12.5);
- el **modelo de ramas** concreto de `git-workflow` (ramas permanentes, convenciones propias; §20);
- las **reglas de organización** que Apep Core no define: frontera de workspace, autoridad de un repositorio designado y raíz de sesión. En la numeración de las reglas sticky son las 14, 15 y 16; **Apep Core no las tiene** (§1, *Precedencia*).

Cuando este manual dice «el provider configurado» o «el plugin de organización» se refiere a esa composición. Con sólo Apep Core, `pr-review` y `git-workflow` siguen siendo válidas como metodología —revisión sobre evidencia aportada, preflight de ramas con `POLICY_APPLICABILITY: UNVERIFIED`—, pero ninguna materializa mutaciones remotas ni asume un modelo de ramas.

### Versión y madurez

**0.1.0 = primera separación material de Apep Core**, extraído de un harness de ingeniería de organización (baseline 0.8.2) como paquete OMP independiente. La versión de Apep Core es la de `VERSION`; la baseline heredada se cita sólo como procedencia (`CHANGELOG.md`) y no es su historial de versiones.

| Incremento | Cuándo |
|---|---|
| `PATCH` | Correcciones, documentación y alineación que no alteran autoridad ni semántica del lifecycle |
| `MINOR` | Capability, agent o skill nuevos, o ampliación deliberada de autonomía |
| `MAJOR` | Cambio incompatible de governance, modelo de autoridad, semántica del lifecycle o de lo que se espera del operador |

La versión vive en `VERSION`; cada versión tiene su sección en [CHANGELOG.md](CHANGELOG.md).

**Ebooks.** `MANUAL.epub`, `USER_GUIDE.epub` y `COOKBOOK.epub` se generan desde su Markdown, que es la fuente canónica, y nunca se editan a mano. El tooling vive en `ebook/` dentro del paquete y el script funciona desde cualquier directorio:

```bash
ebook/build-ebooks.sh manual       # MANUAL.epub
ebook/build-ebooks.sh user-guide   # USER_GUIDE.epub
ebook/build-ebooks.sh cookbook     # COOKBOOK.epub
ebook/build-ebooks.sh governance   # ENGINEERING_GOVERNANCE.epub
ebook/build-ebooks.sh all          # los cuatro
```

Cada EPUB queda junto a su fuente. Los documentos del harness toman la versión de `VERSION`; la governance conserva la suya, la de su primer encabezado, y el script la busca en `docs/governance/ENGINEERING_GOVERNANCE.md` relativo al directorio padre del paquete (si no existe ahí, informa `NOT_PRESENT` y no la genera). La fecha es la del día (`EBOOK_DATE=AAAA-MM-DD` la fija), valida cada EPUB antes de sustituir al anterior y no toca el Markdown. Toda la configuración vive en `ebook/`: opciones de pandoc (`epub.yaml`), hoja de estilos compartida (`kindle.css`), dos filtros de presentación (`local-links.lua`, `wide-tables.lua`) y el validador (`validate_epub.py`). El resultado es un EPUB 3 reflowable pensado para pantallas e-ink estrechas: el lector controla fuente, tamaño, márgenes e interlineado; el código se envuelve sin scroll horizontal; las tablas anchas se presentan como fichas con los mismos rótulos y contenido.

```
MARKDOWN IS CANONICAL. EPUB IS GENERATED. DO NOT EDIT EPUB MANUALLY.
```

**Línea 1 (Specification Factory): `USABLE`, en `FIELD_VALIDATION`** (§8). `GOOD ENOUGH TO USE. NOW LET REAL WORK BREAK IT.`

**Línea 2 (Delivery Factory): `USABLE`, en `FIELD_VALIDATION`** (§5). `GOOD ENOUGH TO USE. NOW LET REAL DELIVERY BREAK IT.`

| Capability | Estado | Evidencia en el paquete |
|---|---|---|
| `project-management` | `USABLE` · `FIELD_VALIDATION` | Suite sintética `tests/project-management/` |
| Línea 1 — Specification Factory | `USABLE` · `FIELD_VALIDATION` | Suite sintética `tests/specification/` (fixtures y dry-runs registrados). Las observaciones de campo y los candidatos futuros se registran en su `README.md`; no hay evidencia de campo registrada para Apep Core como paquete independiente |
| Línea 2 — Delivery Factory | `USABLE` · `FIELD_VALIDATION` | Escenarios sintéticos en `tests/delivery/`: validación metodológica, no de campo. **Sin ejecuciones en trabajo real registradas para Apep Core** |
| Ciclo de PR (`pr-review`, `/pr`) | `USABLE` (contrato genérico) · `FIELD_VALIDATION` | El contrato de autoridad y de ciclo es agnóstico del provider; la mecánica concreta depende del provider configurado y de su validación |
| Approvals | Patrón recomendado, no enforcement | `tests/approvals/`: matriz mínima y genérica que el proyecto consumidor ejecuta contra su propia config (§23) |

No se declara nada `COMPLETE`, `FINAL` ni probado en producción. El harness no lleva un contador de ejecuciones: estas son las suites y los registros que el paquete contiene, no una métrica viva.

```
                   PROJECT MANAGEMENT  →  WORK SHAPING
                          │
╔═════════════════════════▼══════════════════════════╗
║ LINE 1 — SPECIFICATION FACTORY                     ║
║ NEED → REDUCE MATERIAL AMBIGUITY → EXECUTION_READY ║
╚═════════════════════════╤══════════════════════════╝
                 HUMAN AUTHORIZATION
╔═════════════════════════▼══════════════════════════╗
║ LINE 2 — DELIVERY FACTORY                          ║
║ AUTHORIZED CONTRACT → CONTROLLED EXECUTION         ║
║ → VERIFICATION → INDEPENDENT CONFORMANCE           ║
║ → AC CONVERGENCE → DELIVERY_EVIDENCE               ║
║ → INTEGRATION_READY                                ║
╚═════════════════════════╤══════════════════════════╝
                   HUMAN AUTHORITY
╔═════════════════════════▼══════════════════════════╗
║ PR LIFECYCLE                                       ║
║ REVIEW → APPROVAL → MERGE → VERIFY                 ║
╚════════════════════════════════════════════════════╝

PROJECT MANAGEMENT MANAGES THE WORK.
SPECIFICATION DEFINES THE BEHAVIOR.
DELIVERY MATERIALIZES THE CONTRACT.
PR LIFECYCLE MATERIALIZES REMOTE INTEGRATION.
```

**Adopción: field validation.** Apep Core 0.1.0 se adopta gradualmente en trabajo real (`USE GRADUALLY. OBSERVE REAL BEHAVIOR. EVOLVE FROM EVIDENCE.`). Práctica operativa, no regla de governance: el harness cambia por evidencia, no por ocurrencia.

```
OBSERVED FRICTION / FAILURE / CAPABILITY GAP → evidence → classify → PATCH or MINOR when justified
NOT:  IDEA → immediately modify harness
```

### Modelo de enforcement

```
GOVERN INTENT.
BOUND AUTHORITY.
AUTOMATE EXECUTION.
VERIFY RESULTS.

TOOL APPROVALS ARE NOT THE PRIMARY GOVERNANCE MODEL.
```

Los approvals de herramienta son protección **residual** de efectos materiales. Lo que controla qué se hace y quién lo decide es la capa semántica:

| Concern | Enforcement primario |
|---|---|
| Scope | Execution Contract |
| Decisiones reservadas (arquitectura, contratos, APIs, schemas…) | Governance + autoridad humana |
| Calidad de implementación | `code-quality` + agent `implementation` |
| Verificación | `implementation` + tests |
| Routing del lifecycle y selección de workers | `delivery-lifecycle` + `delivery-orchestrator` (o la Main Session) |
| Intención Git (rama, base, destino, mensajes) | `git-workflow` |
| Mutación de index, historia o estado Git compartido | Autoridad humana + gates materiales |
| Mutación remota / cloud | Autoridad humana + gates materiales |
| Decisiones de seguridad | Governance + `security-review` + autoridad humana |

### Precedencia

```
WORKSPACE GOVERNANCE    ENGINEERING_GOVERNANCE.md · reglas sticky · AGENTS.md del proyecto
  → REPOSITORY GOVERNANCE   p. ej. <repo>/AGENTS.md o <repo>/IA.md, al entrar en ese repositorio
    → TASK CONTRACT         Execution Contract / encargo concreto aprobado
      → IMPLEMENTATION
```

Un nivel inferior especializa al superior, nunca contradice en silencio sus invariantes de autoridad. Las skills y los agents operan **dentro** de esta cadena; no son una gobernanza propia.

Las **reglas sticky** se citan en todo el harness como `RULES.md`; el archivo real es [`rules/engineering-discipline.md`](rules/engineering-discipline.md) (`alwaysApply: true`; reglas 1–13 y 17–19). La numeración conserva la de la gobernanza de ingeniería: las reglas 14, 15 y 16 —frontera de workspace, autoridad de repositorio designado y raíz de sesión— son decisiones de organización y **Apep Core no las define**; si un plugin de organización las aporta, vive en su propio archivo de reglas (§1, *Composición*). Cuando este manual se apoya en una de esas materias, lo dice como práctica de workspace u organización, nunca como regla de Core.

### Autoridad humana

El agente puede investigar, leer, comparar, cuestionar, formular hipótesis y recomendar en cualquier momento. **No** puede convertir una recomendación en decisión en las materias reservadas de `ENGINEERING_GOVERNANCE.md` §1.2 —arquitectura, contratos, APIs, semántica de negocio, persistencia, schemas, infraestructura, seguridad, compatibilidad, alcance, entre otras—. La lista canónica es la de §1.2.

No equivalen a autorización: tu silencio, la ausencia de objeción, una recomendación previa del agente, una convención observada en el código o la urgencia. Si quieres que algo se decida, dilo explícitamente.

### Evidence before inference

Toda afirmación se clasifica y nunca se presenta una categoría como otra:

`FACT` (verificado directamente) · `INFERENCE` (razonado, no verificado) · `HYPOTHESIS` · `PROPOSAL` · `RECOMMENDATION` · `DECISION` (cerrada por ti) · `INVARIANT`.

Un `FACT` lo sostiene una observación, no una lectura plausible del código. La correspondencia por defecto entre pregunta y evidencia:

| Para afirmar… | Se observa con |
|---|---|
| Estado del repositorio, qué cambió, quién y cuándo | Git de sólo lectura (`status`, `diff`, `log`, `show`, `blame`) |
| Qué archivos existen, dónde y con qué contenido | Filesystem (`ls`, `cat`, `find`, `stat`) |
| Dónde vive un símbolo, quién lo llama, qué implementa | `grep` · `rg` · `lsp` · `ast_grep` |
| Qué comportamiento está probado | El test runner del repositorio, ejecutado |
| Si compila y tipa | Build y type checker del repositorio (`tsc --noEmit`, `mypy`, …) |
| Si un contrato/schema se cumple | El validador correspondiente, no la lectura del schema |
| Estado real en un proveedor cloud | La CLI del proveedor en modo sólo lectura (`describe-*`, `list-*`, `get-*`…) |
| Estado remoto de un Pull Request | Las lecturas de sólo lectura del provider configurado (§12.5) |

`RULES.md` reglas 11, 12 y 18 son la norma; esta tabla sólo dice con qué herramienta se produce cada tipo de evidencia.

Y una decisión humana, por legítima que sea, **no puede invalidar un hecho externo verificable**. Si una decisión ya cerrada contradice un hecho, el agente para y emite `DECISION_CONTRADICTION` — no reinterpreta la decisión en silencio (`ENGINEERING_GOVERNANCE.md` §16).

### Continuidad sobre perfección

El harness prefiere avanzar con alcance delimitado y evidencia honesta antes que bloquear entero un frente de trabajo. Por eso `DECISION_REQUIRED` lleva un campo `BLOCKING_SCOPE`: separa lo que queda bloqueado de lo que puede continuar. Un `UNKNOWN` declarado es un resultado legítimo; una certeza inventada, no.

### Proporcionalidad

Usa una capability cuando **reduce incertidumbre, protege una frontera o aporta evidencia**. No hay obligación de recorrer todo el lifecycle en cada tarea. Un cambio local, reversible y verificable no necesita `specification` ni `project-management`; las propias skills lo dicen en su descripción ("NO es el modo normal de trabajo del workspace").

El mismo criterio decide **cuántos** workers ejecutan una capability, no sólo cuál se usa: `COORDINATION_COST < EXPECTED_PARALLELIZATION_VALUE` (§14).

---

## 2. Arranque: desde dónde y con qué cargado

### Cómo se arranca

```bash
cd <workspace-root>
omp
```

o, desde cualquier directorio (verificado en runtime):

```bash
omp --cwd <workspace-root>
```

`<workspace-root>` es la raíz del workspace: el directorio que contiene el `.omp/` que gobierna la sesión. El **session root** canónico es esa raíz; los repositorios hijos son **working targets**: se opera sobre ellos durante la sesión, no se arranca en ellos. Cambiar el `cwd` de un comando no cambia el session root.

Que el session root deba ser siempre la raíz del workspace es una convención de **workspace u organización**, no una regla de Apep Core: Core no define una regla de raíz de sesión (§1, *Precedencia*). Si tu organización la formaliza, la aporta su plugin de organización; mientras tanto, la práctica recomendada se recoge en `docs/agents-md-template.md`, la plantilla para tu propio `.omp/AGENTS.md`.

### Context discovery != settings discovery

OMP 18.2.11 resuelve dos cosas distintas desde el directorio de arranque, con reglas distintas (`omp://settings.md`, `omp://context-files.md`):

| Qué | Cómo se descubre | Al arrancar en `<repo>/` (repo hijo), `.omp/` u otro directorio sin `.omp/` propio |
|---|---|---|
| **Settings** (`.omp/config.yml`: approvals, `bash.patterns`, `modelRoles`, `extensions`) | **Sólo `<cwd>/.omp/`.** No hay búsqueda en directorios ancestro | No se carga la config del proyecto: rige la global |
| **Contexto** (`AGENTS.md`, reglas sticky) | Sube desde el cwd hasta la raíz del repositorio Git | Se detiene en la raíz Git del repo hijo: no llega al `.omp/` del workspace |
| **Skills y agents del proyecto** | Siguen al cwd | Se ven las copias globales de `~/.omp/agent/`, que pueden tener los mismos nombres y **contenido distinto** |

**Esto no está resuelto a nivel de herramienta.** Arrancar desde un repo hijo sin `--cwd` pierde config, contexto, skills y agents del proyecto sin avisar. La mitigación vigente es operativa: lanzamiento canónico (`cd` a la raíz o `--cwd`).

`--config <workspace-root>/.omp/config.yml` no sustituye a `--cwd`: carga los approvals como overlay, pero no cambia el session root ni el descubrimiento de contexto.

Crear un `.omp/` local en un repo hijo para compensar es un cambio de configuración durable y requiere decisión humana explícita (`RULES.md` regla 1).

### Activación de Apep Core

Apep Core es un plugin de OMP. `omp plugin link <ruta-a-apep-core>` lo registra correctamente (`omp plugin list` y `omp plugin doctor` lo muestran habilitado, con symlink y lockfile válidos), pero **en omp/18.2.11 la discovery vía `~/.omp/plugins/node_modules` no superficia sus skills, agents, commands ni reglas** (verificado: una sesión nueva tras `link` + `enable` no resolvió `skill://` de un paquete enlazado). El mecanismo `extensions:` de `config.yml` sí los activa (verificado: las skills se resuelven por `skill://` con esa entrada):

```yaml
extensions:
  - <ruta-al-paquete-apep-core>
```

Ambos mecanismos son nativos de OMP (`omp://marketplace.md`, `omp://skills.md`); `extensions:` es el que funciona hoy. Como cualquier setting, se lee sólo de `<cwd>/.omp/config.yml`: rige la misma advertencia de arranque canónico. En la prioridad de discovery, un archivo nativo del proyecto (`.omp/skills`, prioridad 100) gana por nombre a una skill de plugin (90): activar Apep Core es aditivo y no cambia resoluciones nativas existentes.

### Fail-safe global

Cuando no hay config de proyecto rige la global (`~/.omp/agent/config.yml`; compruébala con `omp config get`). Si fija `approvalMode: write`, un arranque incorrecto no cae en `yolo`; pero tampoco trae los gates, skills, reglas ni contexto del proyecto.

Evidencia de runtime (sonda `bash` sin regla, `omp --mode rpc --no-session`, verificada en un workspace multi-repo con config de proyecto que deja `bash` autónomo por defecto):

| Arranque | Flags | Comando sin regla | Contexto del proyecto |
|---|---|---|---|
| raíz | — | ejecutado sin prompt | SÍ |
| `<repo>/` | — | prompt | **NO** |
| `<repo>/`, `.omp/` | `--cwd <workspace-root>` | ejecutado sin prompt | SÍ |
| `<repo>/` | `--config <workspace-root>/.omp/config.yml` | ejecutado sin prompt | **NO** |

### Qué se carga siempre

| Siempre presente | Qué es |
|---|---|
| Reglas sticky (`RULES.md`) | 16 reglas normativas (1–13 y 17–19) vigentes toda la sesión |
| `AGENTS.md` del proyecto | Contexto del proyecto consumidor: repos del workspace, precedencia, protocolo de entrada a un repositorio. Un plugin no puede entregarlo; parte de `docs/agents-md-template.md` |
| `code-quality` | Skill always-on (`RULES.md` regla 17) |
| Metadata de las 11 skills | Nombre y descripción, para el routing por contexto |

### Qué NO se carga solo

- **El cuerpo de las skills**: `SKILL.md` y `references/` se leen bajo demanda (§7).
- **La gobernanza de repositorio** (`<repo>/IA.md`, `<repo>/AGENTS.md` y equivalentes): se lee al entrar en ese repo, según el protocolo de entrada de tu `AGENTS.md`.
- **`ENGINEERING_GOVERNANCE.md` completo**: las reglas sticky son su compilación; el documento se consulta ante ambigüedad.

**No verificado:** si una sesión ya abierta descubre skills añadidas o modificadas en disco después del arranque. Tras cambiar las skills del plugin o del proyecto, arranca una sesión nueva antes de dar el cambio por cargado.

---

## 3. El modelo operativo

Siete cosas distintas que el harness nunca fusiona. Confundirlas es la causa más común de trabajo mal enrutado.

| Concepto | Responde a | Es | NO es |
|---|---|---|---|
| **GOAL** | Qué debe llegar a ser cierto | El resultado que persigues, conservado por la Main Session | Una tarea, ni un prompt |
| **PLAN** | Cómo pienso conseguirlo | Estrategia y orden: dependencias, paralelización, qué investigar antes | Una fase obligatoria del proceso |
| **TASK** | Qué trabajo delimitado se ejecuta ahora | Unidad acotada con scope, decisiones cerradas e invariantes | Un permiso para todo lo adyacente |
| **SKILL** | Cómo se trabaja | Metodología cargable (`skills/`) | Un worker; no ejecuta nada por sí sola |
| **AGENT** | Quién trabaja | Worker con model role y toolset fijados (`agents/`) | Un lugar donde delegar decisiones humanas |
| **TOOL** | Con qué | Capacidad ejecutable (`read`, `edit`, `bash`, `task`, …), con su tier de aprobación | Una autorización: que la herramienta no pregunte no autoriza el cambio |
| **MAIN SESSION** | Quién conduce | Control Tower: conserva el Goal, decide capability, delega, integra | El worker que implementa todo |

Dos primitivas más, de soporte:

| Primitiva | Es | NO es |
|---|---|---|
| **Sticky rules** (`RULES.md`) | Reglas always-on presentes toda la sesión | Algo que se recuerde por prompt |
| **Agent Hub** (`/hub`) | Superficie de supervisión de workers vivos | Un sitio donde rediseñar la tarea |

---

## 4. La Main Session como Control Tower

La conversación principal es tu superficie de conducción. Su trabajo es **coordinar**, no producir todo el output:

- conserva el Goal y el contexto acumulado de la tarea;
- decide qué capability corresponde a cada momento;
- delimita el trabajo y lo delega al worker adecuado;
- integra y reconcilia lo que devuelven los workers;
- detecta contradicciones entre workers, o entre un worker y la evidencia;
- te devuelve a ti las decisiones que son tuyas.

**Dos coordinadores que coexisten:**

| Coordinador | Rol | Úsalo cuando |
|---|---|---|
| **Main Session** | Control Tower interactiva **por defecto** | Quieres conversar, decidir sobre la marcha, explorar, o el trabajo no es un work item completo |
| agent **`delivery-orchestrator`** | Coordinador **opcional** del lifecycle completo de un work item | Quieres entregar "Implementa X" y que el harness clasifique, enrute, delegue, verifique, revise y prepare commit/PR por sí mismo |

No compiten ni se sustituyen. La Main Session sirve para conversar, refinar, decidir, sintetizar en vivo y controlar tú el routing. El orchestrator sirve para un lifecycle ya delimitado: decide el routing, delega workers, mantiene el estado, sintetiza y vuelve a ti sólo por gates reales.

### La Control Tower y el ciclo de vida de PRs

El ciclo de vida de Pull Requests / merge requests del provider configurado (`/pr`, §7; metodología `pr-review`, §12.5) lo coordina **la Main Session**. No lo hace el orchestrator, porque el ciclo ejecuta mutaciones remotas (approval, merge y, si el provider las define, sincronización, PRs auxiliares y notificaciones) que la gobernanza reserva a la Main Session, y en un subagent headless cualquier forma no canónica con gate se rechazaría. La Control Tower:

- fija y enumera `AUTHORIZED_SET` y `AUTHORIZED_ACTIONS` al empezar, y no los amplía;
- coordina `pr-review`, `git-workflow` e `implementation`, este último sólo para la reconciliación mecánica que el provider defina;
- continúa el lote frente a blockers locales, consolida el reporte y coordina las notificaciones que el provider soporte;
- te devuelve `DECISION_REQUIRED` sólo ante materia reservada.

Mantiene, conceptualmente, este estado:

```
CYCLE_ID · AUTHORIZED_SET · AUTHORIZED_ACTIONS · CURRENT_PR
PER_PR_STATE · AUXILIARY_PRS · NOTIFICATIONS · BATCH_RESULT

LIFECYCLE SEMANTICS != PERSISTENT STATE MACHINE IMPLEMENTATION
```

La semántica de estados y transiciones es inequívoca (`skill://pr-review/SKILL.md` §19.5), pero **no existe una máquina de estados persistente**: el estado vive en la sesión y se muestra en el reporte. Lo que se persista además (p. ej. un ledger de notificaciones o la marca de identificación de un PR auxiliar) es del provider configurado, que debe permitir que una ejecución posterior retome lo pendiente sin duplicar efectos (idempotencia, §12.5).

### `delivery-orchestrator`

**Rol:** coordinar el lifecycle de un work item aplicando `skill://delivery-lifecycle/SKILL.md` (cargada por `autoloadSkills`).

```
ORCHESTRATE, DO NOT ABSORB.
```

| Puede | No puede |
|---|---|
| Clasificar el work item | Expandir scope |
| Decidir qué capability sigue | Cerrar decisiones reservadas |
| Delegar en los workers permitidos | Escribir código productivo (no tiene `edit`/`write`) |
| Aplicar en su contexto las skills sin agent (`project-management`, `git-workflow`, `specification`, `implementation-review`, `security-review`, `pr-review`) | Hacer commit, push, merge, tag o release por autoridad propia |
| Mantener `LIFECYCLE_STATE` y sintetizar resultados | Sustituir a la governance o a la autoridad arquitectónica |
| Reintentar **una vez** un worker ante un fallo transitorio | Reintentar indefinidamente |

**No es** implementation, ni autoridad de arquitectura, ni writer de producto, ni reemplazo de la governance.

**Topología efectiva** (`spawns` del agent, `task.maxRecursionDepth: 2`):

```
MAIN SESSION
   │
   └─ delivery-orchestrator            (profundidad 1; sin edit/write)
         ├─ implementation             (único writer de código)
         ├─ technical-discovery
         ├─ architecture-review
         ├─ governance-review
         └─ diagnostics                (sólo ante un fallo observado)
                                       (profundidad 2: no pueden delegar)
```

Los workers no tienen `task`: no se convierten en coordinadores. Verificado en runtime.

**Ciclo con gates:** el orchestrator corre headless y no puede pedirte input en vivo. Ante un gate se detiene y devuelve `LIFECYCLE_STATE`; la Main Session te lo presenta, recoge tu decisión y lo reanuda (`hub`). Las operaciones con gate (commit, push, PR) sólo puede ejecutarlas la Main Session (§13).

**Lo que la Control Tower no debe hacer:** convertirse por inercia en el implementador universal. Si te descubres pidiendo a la sesión principal que investigue un flujo completo, lo especifique, lo implemente y lo revise, has perdido las fronteras de tools y de responsabilidad que dan valor al harness — y el contexto de la sesión se llena de output que luego estorba para coordinar.

**Regla práctica:** la Main Session lee, razona, decide qué delegar e integra. El trabajo de volumen (investigación amplia, implementación, revisión de un diff) va a un agent.

**Cuándo usar Main Session y cuándo delegar:**

| Quédate en la Main Session | Delega a un agent |
|---|---|
| Refinamiento, conversación, decisión | Investigación de volumen o que cruza componentes |
| Skills sin agent asociado (`specification`, `project-management`, `git-workflow`, `implementation-review`, `pr-review`, `security-review`) | Escritura de código (`implementation`) |
| Diagnóstico pequeño y acotado | Diagnóstico de volumen o que cruza runtime/datos/configuración |
| Lectura puntual para confirmar un hecho | Revisión que conviene aislar del contexto de la sesión |

Cuándo conviene delegar **la misma capability a varios workers a la vez**, con qué fronteras y quién se queda con la conclusión: §14. Por defecto, la Main Session es el synthesis owner de toda ejecución multi-agent.

> **Nota sobre `/vibe`:** en OMP, `/vibe` es un modo propio y distinto — convierte la sesión de arriba en *director* de worker sessions persistentes y reduce su toolset a lectura más las herramientas de control de workers. **No es sinónimo de "sesión principal".** Cuando en este manual se habla de Control Tower se habla de la sesión interactiva normal, no de vibe mode. `/plan`, `/vibe` y `/goal` son mutuamente excluyentes: activar uno bloquea los otros. `/vibe` no está incorporado a nuestro proceso (§17).


### Quick Start

**¿Nuevo en el harness?**

1. Arranca OMP desde la raíz del workspace (§2).
2. Si no sabes qué capability necesitas, habla normalmente con la Control Tower.
3. Describe el problema, no la herramienta.
4. Para aprender a usarlo: [USER_GUIDE.md](USER_GUIDE.md). Para un problema concreto: las recetas de [COOKBOOK.md](COOKBOOK.md).

```
WHEN IN DOUBT: START WITH THE CONTROL TOWER.
DESCRIBE THE PROBLEM, NOT THE TOOL.
THERE IS NO SINGLE MANDATORY ENTRYPOINT.
```

Entrada rápida (semántica de cada work mode: §7, *Apep Work Modes*; situación → capability: §17):

```
dar forma                    → /shape
gestionar proyecto           → /project
entender CURRENT_STATE       → /discover
definir comportamiento       → /spec
investigar un fallo          → /diagnose
validar diseño               → /design
ejecutar contrato autorizado → /deliver
revisar implementación       → /review
procesar PR                  → /pr
pensar cómo abordarlo        → /plan
metodología directa          → /skill:<skill>
```

Es una ayuda para elegir, no un routing automático. Las fronteras que la acompañan son de este manual: `/plan` no es `/spec` ni reabre un contrato autorizado (§6); la Control Tower no es el `delivery-orchestrator`, que elige la siguiente capability sin adquirir su autoridad (esta sección); Main Session o agent, según la tabla anterior; anti-patrones del proceso en §22.

```
USER_GUIDE = LEARN TO USE IT                  ¿cómo empiezo, qué escribo, cuánto delego?
MANUAL     = UNDERSTAND THE OPERATING MODEL   ¿qué existe, cómo funciona, qué significa cada estado, qué fronteras tiene?
COOKBOOK   = SOLVE RECURRING PROBLEMS         ¿cómo resuelvo este tipo de problema?
THE USER GUIDE AND THE COOKBOOK ILLUSTRATE. THEY DO NOT LEGISLATE.
```

---

## 5. Delivery workflow y gestión del trabajo

### Lifecycle de una necesidad

```
Idea / Necesidad
  │
  ├─ ¿el work item está Ready? ¿riesgo, dependencias?  → /skill:project-management
  ├─ ¿falta CURRENT_STATE verificable?                 → agent technical-discovery
  ├─ ¿hay que formalizar TARGET_STATE?                 → /skill:specification
  ├─ ¿el cambio toca fronteras/contratos?              → agent architecture-review
  │
  ▼
█ HUMAN GATE █  cierras decisiones no tácticas explícitamente
  │
  ▼
Execution Contract + quality, coherence y readiness gate (specification, si FORMAL)
                     SPEC_COMPLETE → SPEC_QUALITY → SPEC_COHERENCE → READINESS_RESULT → EXECUTION_READY
Branch preflight (git-workflow)   rama · base · destino
  │
  ▼
agent implementation   edit → verify → fix → retest, dentro del contrato (code-quality siempre)
  │
  ▼
Reviews que aporten   implementation-review · security-review · governance-review · architecture-review
  │
  ▼
Commit / PR preparados (git-workflow)  =  INTEGRATION_READY
  │
  ▼
█ HUMAN CLOSE █  COMPLETE lo declaras tú, con la evidencia delante
  │
  ▼
Ejecutar commit / push / publicar PR   SÓLO con autorización (Main Session)
  │
  ▼
pr-review (provider configurado)  →  approve / merge del PR: decide el humano, lo materializa pr-review
                         →  promoción, tag, release — autoridad humana
```

### Lifecycle interactivo o delegado

| Modo | Conduce | Cómo |
|---|---|---|
| **Interactivo** | Main Session | Tú, o la Main Session con `/skill:delivery-lifecycle`, eligen cada paso |
| **Delegado** | `delivery-orchestrator` | El orchestrator decide la ruta y vuelve sólo por gates |

Estados (`skill://delivery-lifecycle/SKILL.md` §2); los corchetes son fases condicionales:

```
RECEIVED → CLASSIFIED → READY → [DISCOVERY] → [SPECIFICATION] → BRANCH_READY
  → [autorización] → EXECUTION_PREFLIGHT → IMPLEMENTING → VERIFYING
  → REVIEWING (+ convergencia por AC en FORMAL) → [REMEDIATION, una vuelta]
  → [DELIVERY_EVIDENCE, integration_ready: YES] → COMMIT_READY → PR_READY → INTEGRATION_READY

en cualquier punto:  → AWAITING_AUTHORIZATION | BLOCKED
COMPLETE sólo lo declara el humano.
```

No es un pipeline rígido: un micro fix salta discovery y specification; una investigación termina en un reporte; un fallo observado va a `diagnostics`, fuera de esta ruta.

### Cuándo vuelve el control al humano

| No te interrumpe | Sí te devuelve el control |
|---|---|
| Elegir y lanzar workers | `DECISION_REQUIRED` |
| Lecturas, búsquedas | `DECISION_CONTRADICTION` |
| Tests, lint, formatter, type-check, build | `STOP_REPORT` |
| Verificación local; ciclo normal fix/retest | Un gate material de herramienta (commit, push, PR, mutación cloud o remota…) |
| Elegir reviews | Ampliación de alcance |
| Transiciones del lifecycle | Evidencia material insuficiente |
| | Integración y release |

### El workflow de un work item

```
WORK ITEM → READY → BRANCH → IMPLEMENT → TEST → REVIEW → COMMIT → PR → INTEGRATION
```

| Paso | Capability | Qué produce | Autonomía | Autoridad humana |
|---|---|---|---|---|
| READY | `project-management` (modo work item) | Clasificación, `WORK_ITEM_ASSESSMENT`, `READINESS_CHECK` **direccional**, `ROUTING_RECOMMENDATION` | Total — es análisis y recomendación | Alcance, prioridad, Story Points, aceptación de riesgo; la transición la decide la Control Tower |
| BRANCH | `git-workflow` §4 | `BRANCH_PREFLIGHT`: rama actual vs. esperada, base, destino | Total en lectura | **Crear / cambiar de rama** |
| Contrato | `specification` (si hace falta) | Execution Contract con el preflight en `BASELINE` | — | **Autoriza la ejecución** |
| IMPLEMENT + TEST | agent `implementation` + `code-quality` | Cambio verificado con evidencia | **Total dentro del contrato** | Sólo eventos materiales (§19) |
| REVIEW | `implementation-review` y demás (§12) | Expected → implemented → verified | Total — observacional | Declara `COMPLETE` |
| COMMIT | `git-workflow` | Mensaje preparado (§20) | Total para preparar | **`git commit`** |
| PR | `git-workflow` | Título y cuerpo con la evidencia real (§20) | Total para preparar | **push y publicación** |
| INTEGRATION | `pr-review`; `git-workflow` (flujo, versión) | Findings; `ACTIONS_AVAILABLE` / `MERGE_READY`; propuesta de versión | Total para revisar, proponer y, ya autorizado, materializar approve/merge en el provider configurado | **approve y merge del PR**, promoción, tag, release |

```
AUTONOMY FOR EXECUTION.
DISCIPLINE FOR INTEGRATION.
THE AGENT SHOULD NOT NEED TO BE REMINDED TO TEST ITS OWN WORK.
```

**Proporcionalidad.** No toda tarea recorre todos los pasos. La formalidad es proporcional a la incertidumbre, el impacto, las dependencias y el coste de revertir. Un fix de una línea en una work branch ya correcta resuelve READY y BRANCH en dos líneas, sin `specification`. Las capabilities cooperan pasándose artefactos (`READINESS_CHECK` → `BRANCH_PREFLIGHT` → Execution Contract → evidencia → `COMMIT_MESSAGE` / `PR_DRAFT`); no se invocan entre sí. Quien decide cuál toca es la Main Session, o el `delivery-orchestrator` si le delegas el lifecycle completo (§4; skill `delivery-lifecycle`).

### Work shaping: dar forma al trabajo antes de moverlo

```
PROJECT MANAGEMENT MANAGES THE WORK.
SPECIFICATION DEFINES THE BEHAVIOR.
DELIVERY MATERIALIZES THE CONTRACT.
```

`project-management` está **sobre** las dos líneas de entrega, no dentro de ninguna: recibe el trabajo, le da forma y recomienda a dónde va. La Control Tower (Main Session o `delivery-orchestrator`) decide la transición.

```
CLASSIFY → SHAPE → RISK → DEPENDENCIES / BLOCKERS → SIZE / SLICE → FORMALITY → READINESS → ROUTING → FLOW
```

| Pieza | Qué es | Referencia |
|---|---|---|
| Clasificación | Por intención y evidencia, no por el título: `FEATURE` · `BUG` · `TECHNICAL_CHANGE` · `REFACTOR` · `INVESTIGATION` · `INCIDENT` · `INFRASTRUCTURE` · `SECURITY` · `DOCUMENTATION` · `PROCESS` · `UNKNOWN`. No es el tipo de rama, que decide `git-workflow` | `work-item-shaping.md` |
| `WORK_ITEM_ASSESSMENT` | Resultado buscado, alcance, actores, dependencias, riesgos, incertidumbres, contorno de aceptación, tamaño, slices, siguiente capability. Sólo con evidencia: lo que falta queda `UNKNOWN` | `work-item-shaping.md` |
| `WORK_RISK_PROFILE` | Impacto, incertidumbre, reversibilidad, radio de impacto, dependencias, sensibilidad de seguridad y datos, riesgo operativo. Cualitativo, sin puntuación; orienta ruta y formalidad, no prioridad | `risk-and-issue-management.md` §1 |
| Dependencias y blockers | `DEP-NNN` tipadas (bloqueante, de secuencia, de información, externa, recurso compartido, entre repositorios, de decisión, de autorización) con estado y alcance; blockers con tipo y `BLOCKING_SCOPE`; `WORK_GRAPH` secuencial / paralelo / condicional, sin scheduler ni persistencia | `dependency-model.md` |
| `SIZE_SIGNAL` y slicing | `SMALL` … `TOO_LARGE_TO_EXECUTE`, nunca horas ni Story Points. Dividir por valor observable cuando se pueda; `ENABLING_SLICE` justificada para infraestructura, habilitadores, migraciones, investigación, seguridad o deuda | `work-slicing.md` |
| `WORK_FORMALITY` | `NONE` / `LIGHT` / `FORMAL`, sin fórmula. Es el `SPECIFICATION_NEED` que consume `delivery-lifecycle` | `work-item-shaping.md` |
| Readiness y routing | Listo **para la siguiente capability** — la que puede empezar ahora —, con `ROUTING_RECOMMENDATION` (siguiente capability, por qué, prerrequisitos ya satisfechos, lo que viene después en `THEN`, paralelas con su `BLOCKING_SCOPE`, bloqueadas) | `routing-readiness.md` |

```
READY MEANS READY FOR THE NEXT CAPABILITY, NOT READY FOR EVERYTHING.
```

```
THE NEXT CAPABILITY IS THE ONE THAT CAN START NOW.
IF A MUST FINISH BEFORE B CAN START, THEN B IS NOT THE IMMEDIATE NEXT CAPABILITY.
```

Si para especificar hace falta antes un hecho que nadie conoce, el siguiente paso es investigarlo (`technical-discovery`) y la especificación va **después** (`THEN`); si ese hecho sólo afecta a una parte, la especificación empieza ya y la investigación corre **en paralelo**, con la parte que espera declarada (`BLOCKING_SCOPE`). Un hecho que el sistema puede mostrar se busca antes de preguntarte (`DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US`), y una referencia desconocida — aunque se llame como una decisión — es un desconocido, no una decisión, hasta saber qué es. Te llega una decisión cuando la evidencia ya no puede elegir: por ejemplo, varias superficies del producto siguen siendo válidas y elegir una cambia el alcance.

Ejemplo: una necesidad ambigua está **lista para `specification`** aunque le falten AC, casos límite y decisiones. Esas aperturas son precisamente el trabajo de la Línea 1, no un motivo para rechazarla. La misma necesidad **no** está lista para `implementation`. Y un item ya `EXECUTION_READY` no vuelve a `specification` sin evidencia nueva.

**PM no es una capa de autoridad.** La cadena es `WORKSPACE GOVERNANCE → REPOSITORY GOVERNANCE → HUMAN DECISIONS / TASK AUTHORITY → TASK OR EXECUTION CONTRACT → IMPLEMENTATION`. PM ayuda a formar y evaluar el trabajo antes del contrato, pero no lo produce. El Execution Contract lo produce `specification` (`FORMAL`). El task contract ligero (`NONE`/`LIGHT`) recoge tu encargo y las decisiones que cerraste, y puede usar evidencia de PM sin darle autoridad sobre comportamiento, alcance material ni ejecución. Tú autorizas, y delivery consume el contrato autorizado.

**Estado:** `PROJECT_MANAGEMENT_STATUS: USABLE` · `MATURITY: FIELD_VALIDATION`. `NO MORE PROJECT-MANAGEMENT FEATURES BY IDEA ALONE`: sólo cambia por fallo, fricción o hueco repetido observados en trabajo real. 

**Lo que PM no hace:** inventar comportamiento de producto (`PM MUST NOT INVENT PRODUCT SEMANTICS`; si falta, la ruta es `specification`), aprobar alcance o cambios, fijar prioridad, aceptar riesgo, declarar válido un requisito, inventar Story Points, estimaciones, baselines o fechas comprometidas, fabricar cronogramas, autorizar ejecución, ejecutar transiciones ni coordinar la ejecución entre repositorios. Tampoco tiene máquina de estados propia: su salida alimenta a `delivery-lifecycle`. Y `specification` no se convierte en tracker de trabajo.

### Gestión de proyecto de software: requisitos, cambios, plan y control

```
PM MANAGES THE REQUIREMENT AS PROJECT WORK.
SPECIFICATION DEFINES WHAT THE REQUIREMENT MEANS.
REQUIREMENT STATUS != REQUIREMENT SEMANTICS.
CHANGE ANALYSIS != CHANGE AUTHORIZATION.
```

El modo proyecto de `project-management` adapta concerns seleccionados de PMBOK® 8 (gobernar y gestionar el proyecto) y de Sommerville (qué cambia cuando el producto es software) al modelo de Apep Core. **No implementa PMBOK ni afirma conformidad**: son fuentes de método, no de autoridad.

| Concern | Qué hace PM | Qué no hace | Referencia |
|---|---|---|---|
| Requirements management | Registra cada requisito con su fuente, stakeholder, objetivo, estado (derivado de los estados existentes, sin máquina propia), cambios y trazabilidad; referencia los IDs y `AC-NNN` de `specification` | Definir qué significa el requisito, escribir AC, declararlo válido | `requirements-management.md` |
| Cambios | Clasifica (requisito nuevo, clarificación, cambio de requisito, de alcance, técnico, defecto, acción correctiva) y produce el `CHANGE_IMPACT_ANALYSIS` | Aprobar el cambio | `requirements-management.md` §4 |
| Gobernanza del proyecto | Hace visible quién patrocina, decide, entrega, acepta y acepta riesgo; si dos figuras son la misma persona, lo dice | Inventar roles; producir RACI por defecto | `project-governance.md` |
| Valor y alcance | Separa output, outcome, beneficio y valor; proyecto, producto, entrega y tarea; detecta drift con evidencia | Inferir beneficios; redefinir alcance | `project-governance.md` |
| Plan, estimación, control | Del resultado al estado verificable; horizonte de planificación; fecha deseada ≠ forecast ≠ comprometida; tamaño, esfuerzo, duración, calendario, coste y confianza separados; desviaciones con opciones | Convertir Story Points en días, estimar sin base, autodeclarar baselines, afirmar `ON_TRACK` sin evidencia | `planning-and-control.md` |
| Software | Progreso por estados verificables, no por porcentajes ni commits; incertidumbre enviada a su owner; calidad compuesta desde sus capabilities; equipo sin ranking de personas; el producto sigue después del cierre | Sustituir reviews; evaluar personas; absorber DevOps | `software-project-management.md` |

```
IMPLEMENTED != VERIFIED != DELIVERED != DEPLOYED != OPERATIONALLY_ACCEPTED != PROJECT_SUCCESS != VALUE_REALIZED
```

Ejemplos de lo que cambia en la práctica: "el módulo va al 80%" no responde si se llega al hito, y PM pide los estados verificables. Un stakeholder que pide un SMS en una demo abre un `NEW_REQUIREMENT` con análisis de impacto y una decisión tuya; no se agrega al requisito. Un proyecto desplegado sin owner operativo está `NOT_READY_FOR_CLOSURE`.

**Proporcionalidad:** `APPLY THE MANAGEMENT CONCERN, NOT NECESSARILY THE MANAGEMENT ARTIFACT`. Charter, RACI, WBS, risk register, plan de comunicaciones o dashboards sólo si su valor de información supera su coste.

### Cómo se presentan los resultados de `project-management`

```
THE METHOD DETERMINES WHAT IS TRUE.
THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED.

RESULTADO CANÓNICO → VISTA DE GESTIÓN → DETALLE DE INGENIERÍA → REGISTRO DE PROCESO
```

`/shape` y `/project` presentan su resultado para lectores mixtos — dirección, gerencia, producto, operaciones, ingeniería —, no sólo para quien conoce el harness. Es **un solo análisis en tres vistas**:

| Vista | Para quién | Qué contiene |
|---|---|---|
| Gestión (primero) | Cualquiera, sin conocer OMP | Qué se pide, por qué importa, estado, qué no sabemos, riesgo, qué está bloqueado y qué avanza, decisiones y recomendación, en lenguaje corriente |
| Detalle de ingeniería | Quien necesita la evidencia | Hechos con su fuente separados de inferencias, slices, restricciones, razón de la ruta |
| Registro de proceso (al final) | El harness y sus auditorías | Las estructuras canónicas sin reescribir: `WORK_ITEM_ASSESSMENT`, `READINESS_CHECK`, `ROUTING_RECOMMENDATION`, `DECISION_REQUIRED`… |

Plantillas: `skill://project-management/references/work-item-shaping-report.md` (work item) y `skill://project-management/references/project-management-report.md` (informe de gestión del proyecto, no un dashboard). No son metodología: no cambian clasificación, readiness ni routing, no crean hechos, alcance, AC, valor, fechas ni decisiones, y lo desconocido sigue siendo desconocido (`EMPTY TEMPLATE SLOT != PERMISSION TO INVENT`). Un item pequeño produce un reporte pequeño. Las decisiones se presentan desde el `DECISION_REQUIRED` canónico, sin semántica nueva.

### Gestión del trabajo: Kanban

Fuente: `skill://project-management/references/work-item-flow.md`.

**Kanban es el sistema operativo.** Correspondencia con el lifecycle: el estado Kanban `Review` (implementación verificada, PR preparado o publicado) cubre `REVIEWING` → `INTEGRATION_READY` de `delivery-lifecycle`; no son el mismo estado.

```
Backlog → Ready → In Progress → Review → Done
```

| Política | Contenido |
|---|---|
| **WIP** | Máximo **2 tareas activas por persona**. Cuentan `In Progress` y `Review` cuando requiere acciones del autor. Una tarea bloqueada sigue visible y marcada como bloqueada; puede justificar tomar otra, sin ocultar el WIP |
| **DoR** (adaptativa, **por destino**) | `SUFFICIENT CLARITY FOR THE NEXT CAPABILITY, NOT CEREMONIAL COMPLETENESS`. Hacia `specification`: resultado entendible, owner que pueda responder, alcance inicial, sin contradicción que impida saber qué se resuelve; **no** exige AC, casos límite ni decisiones cerradas. Hacia `implementation`: contrato con AC, alcance delimitado y decisiones materiales cerradas; la autorización no forma parte del readiness y se registra aparte, como blocker de la ejecución (`READY != AUTHORIZED_TO_EXECUTE`). Story Points sólo si el equipo los usa; si faltan, no se inventan |
| **DoD** (adaptativa) | Cierre del item, no una segunda review: evidencia de AC verificados uno por uno, tests en verde con el comando, reviews aplicables hechas con findings resueltos o aceptados, PR revisado/aprobado cuando corresponda, documentación actualizada si cambia comportamiento, arquitectura o contratos, sin TODOs. Lo que no aplica va como `N/A` + razón |
| **Salud del flujo** | `AGING`, `BLOCKED_TIME`, `WIP_PRESSURE`, `REWORK`, `RETURN_TO_SPECIFICATION`, `RETURN_TO_IMPLEMENTATION`, sólo con evidencia. El harness no guarda timestamps: sin fuente, `NOT_AVAILABLE` |

`Done` lo declara la persona, no el worker. `READY != AUTHORIZED`: que un item esté Ready no autoriza ejecutarlo.

**Scrum y XP aportan prácticas complementarias; no sustituyen a Kanban.**
- De Scrum: refinamiento, criterios de aceptación, inspección y adaptación, feedback temprano.
- De XP: incrementos pequeños, feedback rápido, CI, testing, diseño simple, refactoring disciplinado, TDD cuando reduce incertidumbre.
- No hay sprints obligatorios, velocity targets, roles artificiales ni ceremonias obligatorias.

### Línea 2: Delivery Factory

```
LINE 1 REMOVES MATERIAL AMBIGUITY.
LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT.
IMPLEMENTATION MAY CHOOSE HOW. IMPLEMENTATION MAY NOT CHANGE WHAT.
```

Lo que pasa después de tu autorización es una fábrica verificable, no "implementa y revisa". La conduce `delivery-lifecycle` (`/deliver` o la Main Session) y cada pieza tiene un owner:

```
AUTHORIZED_TO_EXECUTE → EXECUTION_PREFLIGHT (snapshot · baseline · worktree)
  → IMPLEMENT → VERIFY → IMPLEMENTATION_REVIEW → AC_CONVERGENCE
  → REMEDIATION (una vuelta, si cabe en el contrato) → DELIVERY_EVIDENCE → INTEGRATION_READY
```

| Pieza | Qué garantiza | Owner |
|---|---|---|
| `AUTHORIZED_EXECUTION_SNAPSHOT` | Lo que se ejecuta es exactamente lo que autorizaste: `sha256` de los archivos del contrato (07, 03, 08). Si cambian después de autorizar → `AUTHORIZATION_STALE` y se detiene | `delivery-lifecycle` |
| `EXECUTION_PREFLIGHT_RESULT` | Contrato, autorización, repo, rama, checkout, baseline y tooling verificados antes de escribir: `PASS` · `BLOCKED` · `DECISION_REQUIRED` · `AUTHORIZATION_STALE` | `delivery-lifecycle` |
| `EXECUTION_BASELINE` | La base congelada contra la que se mide todo. Si la rama base avanza, la integración lo resuelve; no se persigue la base a mitad de trabajo | `delivery-lifecycle` |
| Worktree de ejecución | En `FORMAL`, el producto se escribe en `<repo>/.worktrees/exec-<ID>`, aislado del checkout de control. Crearlo y borrarlo tiene gate: lo hace la Main Session, con tu aprobación | Main Session |
| `IMPLEMENTATION_RESULT` | Qué se hizo, verificación por comando, fallos separados en preexistentes, introducidos y sin atribuir | agent `implementation` |
| `AC_CONVERGENCE_RESULT` | Cada `AC-NNN` material en `PASS`, `UNVERIFIED`, `UNIMPLEMENTED` o `CONTRADICTED`, con evidencia propia, no la palabra del implementador | `implementation-review` |
| Remediation | Sólo lo inequívocamente dentro del contrato (`FIX_ALREADY_AUTHORIZED`), una vuelta; si no converge, `REMEDIATION_EXHAUSTED` y decides tú | `delivery-lifecycle` |
| `DELIVERY_EVIDENCE` | Todo lo anterior consolidado, con `integration_ready: YES/NO` y sus razones | `delivery-lifecycle` |

```
SELF-VERIFICATION != INDEPENDENT CONFORMANCE
EVERY MATERIAL AC REQUIRES EVIDENCE.
INTEGRATION_READY != COMPLETE != AUTHORIZED_TO_COMMIT / PUSH / PUBLISH_PR / MERGE
```

**El gate.** En `FORMAL`, `INTEGRATION_READY` exige todos los AC materiales en `PASS`. Uno solo en otro estado deja `integration_ready: NO`: se corrige si cabe en el contrato, o vuelve a ti como `DECISION_REQUIRED`. No se suaviza para cerrar. Después, commit, push y PR los ejecuta la Main Session sólo si lo autorizas, y el PR remoto es de `/pr`.

**Proporcional.** Un trabajo `NONE` usa la rama actual si es segura, sin fingerprint ni worktree; uno `LIGHT` usa los AC de su task contract y un worktree sólo si el checkout no es seguro. Las fronteras de autoridad son las mismas en los tres.

**Handoff con la Línea 1.** La Línea 1 termina en `EXECUTION_READY`; sólo tu autorización lo convierte en `AUTHORIZED_TO_EXECUTE`, y esa autorización — sobre la versión exacta del contrato, fijada por su fingerprint — es la frontera de la Línea 2. Si el contrato cambia después, la Línea 2 se detiene (`AUTHORIZATION_STALE`) y vuelve a ti.

**Estado.** `LINE 2 — DELIVERY FACTORY` · `STATUS: USABLE` · `MATURITY: FIELD_VALIDATION`. Sin ejecuciones reales todavía; 24 escenarios sintéticos (`tests/delivery/`) validan el método, no el campo. Detalle: `skill://delivery-lifecycle/SKILL.md` §13.

**Política de evolución.** `NO MORE LINE 2 FEATURES BY IDEA ALONE.` Igual que la Línea 1 (§8): `OBSERVED_FAILURE | OBSERVED_FRICTION | REPEATED_CAPABILITY_GAP → EVIDENCE → CLASSIFY → PATCH / MINOR` cuando se justifique; nunca `IDEA → CAMBIO INMEDIATO`. Los candidatos de observación (`WORKSPACE_PENDING`, contratos sin archivo verificable, momento de la autorización de rama frente al worktree, compatibilidad del worktree con el tooling, `WORKTREE_APPROVAL_FRICTION`, fricción de evidencia y procedencia) están en `tests/delivery/README.md`; no son backlog.

**Approvals sin cambios, por decisión de diseño.** El worktree de ejecución conserva su gate en el patrón recomendado de approvals (`git worktree*`, §23): crearlo y borrarlo lo autorizas tú en cada ejecución `FORMAL`. Decisión heredada de la baseline: no ampliar esa autonomía hasta tener evidencia de campo de su fricción.

### La ruta de fallo observado — diagnostics no está en el lifecycle

`diagnostics` **no es un paso del lifecycle**. No se ejecuta "por si acaso", ni al terminar una implementación, ni como parte de la verificación. Tiene su propia ruta, que arranca en un hecho:

```
FALLO OBSERVADO   (un síntoma real: error, salida incorrecta, incidente)
  │
  ▼
diagnostics   skill o agent, según volumen (§11)
  │
  ├─ ROOT_CAUSE_CONFIRMED          causa y atribución demostradas
  ├─ ROOT_CAUSE_HIGH_CONFIDENCE    mecanismo demostrado, atribución inferida
  └─ INSUFFICIENT_EVIDENCE         + MISSING_EVIDENCE obligatorio
  │
  ▼
█ DECISIÓN HUMANA █   qué se corrige, dónde y con qué alcance
  │
  ▼
Task / Execution Contract separado  →  implementation
```

`DIAGNOSIS != REMEDIATION`. Un diagnóstico nunca se continúa en un fix: la corrección entra por el lifecycle normal, con su propio contrato.

### Los gates humanos

1. **Gate de herramienta** (§23) — la capa de permisos de tu `config.yml`, no de Apep Core. Con `approvalMode: write`, OMP auto-aprueba lectura y escritura de archivos; el resto lo deciden `tools.approval` y `bash.patterns`. La escritura de archivos no pregunta porque su gate es el punto 3, no la tecla. Un plugin no entrega esa configuración: ver `docs/recommended-approval-patterns.md`.
2. **Gate de decisión** — toda decisión no táctica se te devuelve como `DECISION_REQUIRED` antes de proceder (`ENGINEERING_GOVERNANCE.md` §1.4, §8).
3. **Gate de contrato** — `implementation` ejecuta un contrato ya delimitado; delimitarlo y autorizarlo es tuyo. En el pipeline formal de `specification` este gate es explícito: `MANDATORY_EXECUTION_GATE` (§8 de este manual).
4. **Gate de cierre** — `COMPLETE` no se declara con los tests en verde. Ver §21.
5. **Gate de Git** — nada que cree, publique o reescriba historia se ejecuta sin autorización explícita (`RULES.md` regla 18). Ver §20.
6. **Gate de publicación remota** — publicar comentarios en un PR remoto exige autorización humana explícita e inequívoca. Ver §12.

---

## 6. Plan: cuándo sí y cuándo no

`/plan` activa el plan mode de OMP ("agent plans before executing"). `/plan-review` reabre la revisión del último plan mientras plan mode esté activo — comando **documentado previamente en este manual, no verificado contra el runtime instalado** (ver §15).

**Plan ayuda cuando hay incertidumbre de abordaje**, es decir cuando aún no sabes:

- cómo atacar el Goal;
- qué dependencias hay entre partes;
- qué hace falta investigar antes de decidir;
- qué puede paralelizarse;
- qué capabilities conviene usar y en qué orden.

**Plan no es una fase obligatoria.** Para un cambio local ya entendido, con contrato claro, plan mode sólo añade una ronda de ceremonia.

**Plan no sirve para reabrir un Execution Contract ya autorizado.** Si ya cerraste decisiones y el contrato está determinado, volver a planificar invita al agente a reconsiderar lo que tú ya decidiste — exactamente lo que `RULES.md` regla 1 y regla 2 prohíben. Un contrato autorizado se reabre sólo por **evidencia factual nueva** (y entonces el camino correcto es `DECISION_CONTRADICTION`) o por **una decisión tuya explícita** de cambiarlo.

---

## 7. Skills: metodología, no workers

Una skill es conocimiento procedimental que se carga en el contexto. **No ejecuta nada por sí sola.** Cargar `specification` no produce una especificación; hace que el trabajo de especificar siga nuestra metodología.

### Invocación

```
/skill:specification
/skill:project-management
/skill:technical-discovery
/skill:diagnostics
/skill:architecture-review
/skill:implementation-review
/skill:security-review
/skill:pr-review
/skill:git-workflow
/skill:delivery-lifecycle
```

`code-quality` **no se invoca**: es always-on por `RULES.md` regla 17 y aplica a toda escritura o modificación de código. Ningún diff se declara `COMPLETE` sin haber aplicado su revisión de diff (`skill://code-quality/SKILL.md` §6).

### Cuándo se cargan solas

Las descripciones de las skills declaran sus disparadores por contexto ("úsalo cuando se pida investigación técnica…", "cuando se pida diagnosticar un error…"). También declaran explícitamente cuándo **no** deben activarse. Invócalas a mano cuando quieras forzar la metodología o cuando el disparador por contexto sea ambiguo.

### Carga progresiva

Las skills con `references/` definen qué referencia cargar según la tarea o la escala del problema. No pidas que se carguen todas: `technical-discovery`, `diagnostics` y `architecture-review` distinguen escala `TARGETED` / `FLOW` / `SYSTEM`-`INCIDENT` precisamente para no leer el repositorio horizontalmente cuando la pregunta se responde verticalmente.

### Apep Work Modes

Un **Apep Work Mode** es una superficie de entrada orientada a intención: un slash command project-local que traduce lo que necesitas hacer a las capabilities que ya existen en el harness. No implementa la capability, no redefine su metodología, no crea autoridad y no elige el modelo.

```
COMMAND = UX ENTRYPOINT        SKILL = HOW        AGENT = WHO + TOOL BOUNDARIES
MODEL ROLE = COMPUTE CLASS     GOVERNANCE = AUTHORITY
CONTROL TOWER = ROUTING + SYNTHESIS

WORK MODE != SECOND METHODOLOGY     WORK MODE != AUTHORITY     WORK MODE != MODEL
THIN COMMAND. RICH CAPABILITY. SINGLE SOURCE OF METHODOLOGY.
```

```
USER INTENT → WORK MODE → CAPABILITY ROUTING → SKILLS + AGENTS → MODEL ROUTING → TOOLS → APPROVAL ENVELOPE
```

**Catálogo.** No necesitas saber qué skill cargar, qué agent invocar ni qué modelo usa: eliges por lo que quieres conseguir.

| Command | Cuándo | Capability | Quién ejecuta | Termina en |
|---|---|---|---|---|
| `/shape` | Tengo una necesidad, idea, ticket o bug sin forma | `project-management`, modo work item | Main Session | Assessment y `ROUTING_RECOMMENDATION`, o `DECISION_REQUIRED` |
| `/project` | Gestiono un proyecto o frente: gobernanza, alcance, requisitos, cambios, plan, riesgo, cierre | `project-management`, modo proyecto | Main Session | Salida del modo proyecto y decisiones pendientes |
| `/discover` | No sé cómo funciona algo hoy | `technical-discovery` | agent `technical-discovery` | `CURRENT_STATE` con evidencia |
| `/spec` | Hay que definir comportamiento | `specification` (Línea 1) | Main Session | `EXECUTION_READY` o lo que la bloquea. No autoriza |
| `/diagnose` | Algo falló y quiero la causa | `diagnostics` | agent `diagnostics` | Causa raíz o `INSUFFICIENT_EVIDENCE`, con `FIX_BOUNDARY` |
| `/design` | Quiero validar un diseño o cambio contra fronteras y contratos | `architecture-review` | agent `architecture-review` | Estados de architecture-review; decisiones materiales al humano |
| `/deliver` | Ya está autorizado: constrúyelo | `delivery-lifecycle` | agent `delivery-orchestrator`, con la Main Session como puente de autoridad | `INTEGRATION_READY` o el gate que lo detuvo |
| `/review` | Quiero comprobar lo implementado | `implementation-review` | Main Session | `REVIEW_OUTCOME` |
| `/pr` | Quiero procesar Pull Requests / merge requests | `pr-review` | Main Session | `PR_REVIEW_REPORT` (y `BATCH_RESULT`) |

```
/pr 127
/pr <repo> 127 131 · /pr aprueba y mergea el 127 si está listo
/shape exportar el reporte de cartera a CSV
/diagnose el endpoint /clientes devuelve 500 desde el despliegue de ayer
/review la rama feature/E1-9/x contra su contrato
```

`/review` revisa una implementación (local, rama, diff); `/pr` conduce el ciclo de vida remoto del Pull Request. `/shape` trata un work item; `/project`, el proyecto. `/spec` termina en `EXECUTION_READY`, que no es autorización. `/deliver` termina en `INTEGRATION_READY`: commit, push, PR, merge y release siguen siendo decisiones tuyas.

**Contrato común.** Cada command declara sólo intención, capability primaria, quién ejecuta, entrada (`$ARGUMENTS`), capabilities de apoyo, fronteras, condición de parada y resultado esperado, y remite a las secciones de su skill. No copia esquemas, máquinas de estados ni checklists: si command y skill discreparan, manda la skill.

**Routing entre modos.** Un modo puede recomendar otro — `/shape` → `/discover` o `/spec`; `/discover` → `/spec` o `/design`; `/diagnose` → `/design`, `/spec` o `/deliver`; `/review` → remediation vía `/deliver` —, pero no se encadena solo. `MODE RECOMMENDATION != AUTOMATIC AUTHORITY TRANSITION`: la transición la decide la Control Tower y, cuando es materia reservada, tú.

**Apep Software Delivery Model.** Los modos son la superficie del modelo de entrega de Apep Core, spec-driven en sus propios términos. El diagrama es conceptual, no un pipeline obligatorio: cada trabajo usa sólo lo que necesita (§1, proporcionalidad).

```
                 CONTROL PLANE:  /shape   /project
                                    │
       ┌────────────────────────────┼────────────────────────┐
       ▼                            ▼                        ▼
   /discover                      /spec                  /diagnose
 CURRENT_STATE                TARGET_STATE                FAILURE
       └──────────────┬─────────────┴──────────┬─────────────┘
                      ▼                        ▼
                   /design              HUMAN DECISIONS
                      └───────────┬────────────┘
                                  ▼
                          EXECUTION_READY → HUMAN AUTHORIZATION
                                  ▼
                              /deliver → IMPLEMENTATION
                                  ▼
                               /review
                                  ▼
                                 /pr → INTEGRATION
```

**Mecánica en OMP.** OMP 18.2.11 descubre los commands de proyecto en `<cwd>/.omp/commands/*.md` (`omp://slash-command-internals.md`); los de un plugin llegan por el mecanismo de activación del plugin (§2, *Activación de Apep Core*). En ambos casos sólo existen si la sesión arranca donde se carga esa configuración (§2). El cuerpo se expande como prompt de la sesión, con `$ARGUMENTS` sustituido por lo que escribes después del nombre. El frontmatter admite `description` y `argument-hint`; no permite elegir agent ni modelo. Por eso un modo con owner agent pide a la Main Session que delegue, y el agent corre con su propio rol de modelo. Ningún nombre del catálogo colisiona con un comando nativo; los nativos ganan siempre sobre los de archivo.

**OMP native modes ≠ Apep Work Modes.** `/plan`, `/goal`, `/vibe` y el resto de comandos nativos son funciones del runtime y siguen disponibles e intactos. Los Work Modes son UX del flujo de ingeniería de Apep Core, no dependen de ellos ni los redefinen. Workflow magic sigue apagado (`magicKeywords.workflow: false`): `USE OMP PRIMITIVES. KEEP APEP ORCHESTRATION.`

**Model routing.** Los modos no tienen modelo propio ni roles por capability. Un modo que corre en la Main Session usa el modelo de la sesión; uno que delega usa el rol del agent (§16).

```
MODEL SIZE FOLLOWS REASONING COMPLEXITY, NOT BUSINESS IMPORTANCE.
MODEL ROLE DOES NOT GRANT AUTHORITY.
MODEL ESCALATION DOES NOT CHANGE CAPABILITY OWNERSHIP.
```

**`smol` (política, no implementada como fan-out).** `SMOL CAN GATHER. SMOL MUST NOT OWN MATERIAL JUDGMENT.` Un modelo barato puede inventariar archivos, localizar símbolos o callers y hacer comprobaciones mecánicas acotadas; la síntesis y el juicio material quedan en la Main Session o en el agent dueño de la capability. No se crean agents nuevos sólo para usar `smol`.

### Catálogo — 11 skills project-local

Todas en `skills/<nombre>/SKILL.md` del plugin. Aquí sólo está la frontera operativa; la metodología, en cada `SKILL.md`.

| Skill | Propósito | Cuándo usarla | Qué NO autoriza | Agent |
|---|---|---|---|---|
| `code-quality` | Criterio de calidad y de tests (§9) | **Always-on** en toda escritura de código | Refactors oportunistas, scope creep | — |
| `project-management` | Work shaping + flow: clasificación, assessment, riesgo, dependencias y blockers, slicing, readiness direccional, routing recomendado, Kanban (§5); gestión de proyecto de software: gobernanza, valor, alcance, requirements management, impacto de cambios, planificación, estimación, control | Trabajo sin forma, grande, bloqueado o sin destino claro; "¿está listo, y para qué?"; requisito nuevo o que cambia; fecha, estimación o avance que evaluar; frente con incertidumbre real | Definir comportamiento de producto, aprobar alcance o cambios, decidir prioridad, fechas, baselines, aceptación de riesgo; ejecutar transiciones | — |
| `git-workflow` | Rama, base, destino; preparar commit, PR y versión (§20) | Antes de implementar en un repo; al preparar commit/PR/release | Crear rama, commit, push, PR, merge, tag; decidir versión | — |
| `specification` | Necesidad, aunque llegue ambigua → intake, clarificación, especificación → Execution Contract + quality, coherence y readiness gate C1–C4 (§8) | Hay que formalizar `TARGET_STATE` | Ejecutar: `EXECUTION_READY != AUTHORIZED_TO_EXECUTE`; declarar READY sin el gate | — |
| `technical-discovery` | Reconstruir `CURRENT_STATE` verificable (§10) | Falta saber cómo funciona algo | Diseñar, implementar o corregir | Sí |
| `diagnostics` | Causa de un fallo **observado** (§11) | Hay un síntoma real | Remediation, restarts, limpiezas que destruyan evidencia | Sí |
| `architecture-review` | ¿Preserva boundaries, dependencias, contratos? (§12.2) | El cambio toca fronteras | Diseñar la arquitectura de reemplazo | Sí |
| `implementation-review` | ¿Lo implementado es correcto? (§12.1) | Existe un cambio concreto | Corregir findings (`REVIEW_FINDING != AUTHORIZATION_TO_FIX`) | — |
| `security-review` | ¿El cambio introduce riesgo demostrable? (§12.4) | Cambio que toca superficie de seguridad | Parchear, rotar secretos, tocar IAM/config | — |
| `delivery-lifecycle` | Máquina de estados y routing del lifecycle completo de un work item (§5) | "Implementa X" de principio a fin; la ejecuta `delivery-orchestrator` o la Main Session | Materias reservadas, commit/push/PR/merge/tag, escribir código | Sí |
| `pr-review` | ¿El PR / merge request es coherente y suficiente? Y su ciclo de vida autorizado, independiente del provider (§12.5) | El cambio vive en un PR | Resolver conflictos funcionales, rebasear o tocar ramas fuera de lo que una capability de sincronización del provider autorice; publicar, aprobar, mergear, sincronizar o notificar sin autorización; autoaprobar | — |

**`governance-review` no es una skill**: existe únicamente como agent (§13). Su metodología vive en `docs/governance/ENGINEERING_GOVERNANCE.md` y en el propio `agents/governance-review.md`.

---

## 8. Specification: de necesidad a Execution Contract

`specification` es el proceso que lleva una necesidad hasta un Execution Contract. **La necesidad no tiene que llegar refinada**: una idea, un problema, un ticket breve o un requisito informal valen como entrada, porque reducir su ambigüedad es justamente el trabajo de la Línea 1. No es el punto de partida de todo trabajo, y no investiga sin pregunta: los hechos que faltan se buscan con una pregunta concreta de discovery.

```
LINE 1 DOES NOT PRODUCE DOCUMENTS.
LINE 1 REDUCES MATERIAL DEGREES OF FREEDOM.

LINE 1 REMOVES MATERIAL AMBIGUITY.
LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT.
```

```
discovery          !=    specification      !=    implementation
¿cómo funciona          ¿qué debería            ejecutar el contrato
 hoy esto?               hacer el sistema?       ya autorizado
```

El pipeline tiene diez etapas y **no es obligatorio empezar en la 01**: el entry point lo determina la evidencia realmente disponible (`skill://specification/SKILL.md` §5). La etapa **07 (Execution Contract) es el gate formal del pipeline de `specification`** (en trabajo `NONE`/`LIGHT` el gate proporcional es el task contract ligero autorizado, `delivery-lifecycle` §4); 09 y 10 son post-implementación, y 10 es opcional.

### Línea 1: de la necesidad a `EXECUTION_READY`

```
RAW / PARTIALLY DEFINED NEED
  → intake normalization          (PROBLEM ≠ PROPOSED_SOLUTION)
  → ambiguity assessment
       ├─ unknown factual    → technical-discovery → FACT / UNKNOWN → sigue
       ├─ ambigüedad material → clarificación → CLAR-NNN → respuesta aplicada
       └─ ambigüedad táctica  → assumption registrada (ASM-NNN)
  → [01 discovery] → [02 problem] → 03 hard spec (registro AC-NNN, provenance)
  → [04 use cases] → [05 behavior] → [06 tasks] · [08 acceptance tests]
  → 07 Execution Contract  =  SPEC_COMPLETE
  → spec quality (SQ1–SQ10) → spec coherence (12 pasadas) → readiness gate C1–C4
  → READINESS_RESULT → EXECUTION_READY  |  NOT_EXECUTION_READY (+ blocking_reasons, DECISION_REQUIRED)
  → █ autorización humana █  =  AUTHORIZED_TO_EXECUTE  →  Línea 2
```

Los corchetes son etapas condicionales: el entry point lo fija la evidencia disponible. Si la entrada ya está determinada, el intake ocupa pocas líneas y no hay preguntas: **no se ejecutan ceremonias vacías.** El assessment y la clarificación no son un paso único al principio, sino que se repiten en cada etapa en cuanto aparece una apertura:

```
DETECT EARLY. REMEDIATE LOCALLY. GATE FORMALLY AT THE END.
```

### Clasificar antes de preguntar

Toda apertura se clasifica antes de formular una pregunta (`skill://specification/references/ambiguity-assessment.md`):

| Clase | Ruta |
|---|---|
| `FACT` | Se cita y se usa |
| `UNKNOWN` factual (verificable en código, configuración, runtime o documentación) | `technical-discovery` con una pregunta estrecha. **No se te pregunta** |
| `ASSUMPTION` | Sólo si cumple los ocho criterios: local, reversible, arquitectónicamente neutral, invisible desde fuera, dentro del scope, sin semántica de negocio, sin cambiar contratos y verificable (la autonomía táctica de `ENGINEERING_GOVERNANCE.md` §1.3 más dos criterios propios). Se registra como `ASM-NNN` |
| `AMBIGUITY` material o `DECISION_REQUIRED` | Vuelve a ti como pregunta |
| `CONTRADICTION` | Decisión cerrada contra un hecho → `DECISION_CONTRADICTION` (§16); petición nueva contra una decisión cerrada → `DECISION_REQUIRED`; dos inputs sin decisión → ambigüedad material |

```
DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US.
DO NOT LET THE SYSTEM DECIDE WHAT ONLY THE HUMAN MAY DECIDE.
```

El assessment recorre doce dimensiones (alcance, actores y permisos, reglas de dominio, datos y estado, flujos principales, casos límite y de fallo, integraciones, no funcionales, restricciones, terminología, éxito y aceptación, decisiones abiertas), marcando cada una `CLEAR` / `PARTIAL` / `MISSING` / `NOT_APPLICABLE`, y prioriza con `IMPACT × UNCERTAINTY` como heurística, no como fórmula.

### Clarificación: qué te pregunta y cómo

Cada pregunta material llega como un `DECISION_REQUIRED` (formato §1.4 de la gobernanza), precedido de su identificador y de por qué importa:

```
CLAR-003 · CLARIFICATION_REQUIRED · AFFECTS: BR-002, AC-004
WHY_IT_MATTERS: decide si una cuenta suspendida puede seguir recibiendo pagos.
DECISION_REQUIRED
FACTS / DECISION (¿pregunta completa?) / OPTIONS / TRADEOFFS / RECOMMENDATION / CONSEQUENCES / BLOCKING_SCOPE
```

- Una sola decisión por pregunta, en lenguaje del dominio. Una pregunta a la vez cuando tu respuesta puede cambiar las siguientes; agrupadas cuando son independientes.
- `RECOMMENDED: <opción>` es sólo una recomendación: hace falta tu respuesta explícita ("acepto la recomendación" vale; el silencio no).
- **No hay máximo de preguntas**: `ASK THE MINIMUM SET OF QUESTIONS NEEDED TO REMOVE MATERIAL AMBIGUITY.` Si decides parar, lo pendiente queda abierto y la spec no llega a `EXECUTION_READY` mientras sea material.
- **Tu respuesta sólo cierra lo que dice.** El agente no completa una regla que no dijiste, ni da por decidido lo que tu respuesta sólo presupone (una métrica sobre "el flujo de cancelación" no decide que la pausa se ofrezca ahí). Si respondes "fuera de alcance" a algo de lo que depende lo que sí está en alcance, te lo vuelve a preguntar explicando la dependencia; si mantienes la exclusión, esa parte queda bloqueada o se reduce con tu decisión, nunca se rellena con una inferencia. Una inferencia del agente nunca es la fuente de un requisito material. Una regla genérica ("todo lo que sea regla de negocio, fuera") no reduce el alcance en lo que sí depende de ella, y "detenerse si hace falta definirlo" en el contrato no cuenta como haberlo definido: si el flujo en alcance llega a ese caso, la spec no está `EXECUTION_READY`.
- No te pregunta cómo implementar (tecnologías, patrones, carpetas, orden de trabajo) cuando lo que falta es comportamiento: "¿PostgreSQL o MongoDB?" se reformula como "¿qué consultas, consistencia y retención necesita el histórico?". Una tecnología que ya decidiste se registra como `CONSTRAINT`.
- En un lifecycle delegado, `delivery-orchestrator` no puede preguntarte en vivo: devuelve los `CLAR-NNN` en `decisions_required` y espera a que lo reanudes.

Cada respuesta material queda en `CLARIFICATION_LEDGER.md` (pregunta, por qué importa, clasificación, respuesta, fuente, artefactos afectados, estado `OPEN` / `APPLIED` / `SUPERSEDED`) y se aplica a los artefactos **sustituyendo** el texto que contradice: `HISTORY LIVES IN THE LEDGER. CURRENT TRUTH LIVES IN THE ARTIFACTS.` El ledger no existe hasta la primera clarificación (`skill://specification/references/clarification-loop.md`).

**Provenance.** Las reglas de negocio materiales llevan `SOURCE` (petición del stakeholder, `CLAR-NNN`, decisión, gobernanza o un `FACT` de discovery) y los AC materiales `DERIVED_FROM`. Así siempre se puede responder "¿de dónde salió esta regla?". La relación sigue siendo muchos-a-muchos, sin cadena 1:1 obligatoria.

### Calidad y coherencia antes del gate

```
QUALITY  !=  COHERENCE  !=  READINESS
```

| Revisión | Pregunta | Qué mira | Bloquea `EXECUTION_READY` |
|---|---|---|---|
| **Spec quality** (`specification-quality.md`) | ¿Está suficientemente bien especificado? | SQ1 problema separado de la solución · SQ2 alcance determinado · SQ3 requisitos verificables · SQ4 sin HOW prematuro · SQ5 sin lenguaje vago ("rápido", "seguro", "adecuado"…) · SQ6 actores · SQ7 semántica de fallo · SQ8 éxito medible · SQ9 dependencias y restricciones · SQ10 sin placeholders | Un `FAIL` material sin resolver |
| **Spec coherence** (`coherence-review.md`) | ¿Los artefactos cuentan la misma historia? | 12 pasadas read-only: duplicación, deriva terminológica, contradicción semántica, infraespecificación, alcance, BR → comportamiento, comportamiento → AC, AC → tarea, AC → test de aceptación, preservación en el contrato, gobernanza, aplicación de clarificaciones | Un finding `CRITICAL`/`HIGH` material sin resolver, o un conflicto material ambiguo |
| **Readiness** (C1–C4) | ¿Puede la Línea 2 ejecutarlo sin decisiones materiales abiertas? | Abajo | La regla de readiness |

`REFERENCE_INTEGRITY != SEMANTIC_COHERENCE`: C2 prueba que `AC-007` existe; la coherencia prueba que `AC-007` dice algo compatible con la BR de la que deriva. Una contradicción material nunca se resuelve eligiendo una de las dos versiones: vuelve a ti.

### Tres estados que no se confunden

| Estado | Significa | Lo establece |
|---|---|---|
| `SPEC_COMPLETE` | Las etapas aplicables terminaron y sus artefactos existen, incluido el contrato 07 | La etapa 07 al generar el contrato |
| `EXECUTION_READY` | La spec pasó el readiness gate (`READINESS_RESULT` con `execution_ready: YES`) | La etapa 07, sólo si se cumple la regla |
| `AUTHORIZED_TO_EXECUTE` | Hay autoridad humana / task contract para iniciar la Línea 2 | Sólo tú |

Generar el contrato ya no produce `EXECUTION_READY`. `READY` (DoR de `project-management`: el item puede **entrar** al proceso) **no** es `EXECUTION_READY`.

### Readiness gate (etapa 07)

Detalle: `skill://specification/references/07-execution-contract.md`. Se evalúan los artefactos, no la impresión de completitud: las autoevaluaciones de cobertura en prosa no cuentan como evidencia por sí mismas.

| Check | Qué mira | Bloquea `EXECUTION_READY` |
|---|---|---|
| **C1 — Open material items** | `DECISION_REQUIRED`, UNKNOWN, TBD/TODO, supuestos, hipótesis y wording equivalente ("a confirmar", "no bloqueante", "durante implementación") en todos los artefactos, incluidos `ASSUMPTIONS` e `IMPLEMENTATION_GUIDELINES`, más las `CLAR-NNN` abiertas y todos los `ASM-NNN`; cada uno clasificado `MATERIAL_FOR_EXECUTION` YES / NO / AMBIGUOUS | YES o AMBIGUOUS. Los NO se registran con su razón |
| **C2 — Reference / coverage integrity** | Todo ID referenciado (BR, UC, SC, AC, TASK, AT, CLAR, ASM, también en `SOURCE` / `DERIVED_FROM`) existe; matrices sin IDs inexistentes; todo requisito material declarado cubierto tiene evidencia aguas abajo. **No** exige cadena 1:1 | Referencia inexistente o requisito material sin evidencia |
| **C3 — Deferred promise closure** | "Se resolverá en…", "se definirá más adelante", "la implementación decidirá": ¿se resolvió donde se prometió? | `UNRESOLVED_MATERIAL` o `AMBIGUOUS` |
| **C4 — Claim / artifact consistency** | Claims como "todas las BR cubiertas", "N tareas", "sin decisiones abiertas" contrastados con los artefactos | `CONTRADICTED`; `NOT_VERIFIABLE` no cuenta como evidencia |

La calidad del oráculo de los tests, la exhaustividad de edge cases y la arquitectura **no** son condiciones duras: quedan como observaciones o como `DECISION_REQUIRED` si son materiales. El `READINESS_RESULT` registra quién y cuándo evaluó, y además los resultados de quality y coherence y las clarificaciones pendientes: `EXECUTION_READY` exige ahora también `spec_quality = PASS`, `spec_coherence = PASS` y ninguna `CLAR-NNN` material abierta. C1–C4 conservan su semántica.

### Estado de la especificación

No hay persistencia de lifecycle: el estado vive en los artefactos y en la sesión. `specification` lo reporta como `SPECIFICATION_STATE`, con uno de estos estados: `INTAKE` · `AMBIGUITY_ASSESSMENT` · `CLARIFICATION_REQUIRED` · `CLARIFYING` · `SPECIFYING` · `SPEC_COMPLETE` · `SPEC_QUALITY_REVIEW` · `SPEC_COHERENCE_REVIEW` · `NOT_EXECUTION_READY` · `EXECUTION_READY` (`skill://specification/SKILL.md` §12). En `delivery-lifecycle` todos viven dentro de `SPECIFICATION_REQUIRED`.

### Estado de la Línea 1 y política de evolución

```
LINE_1_STATUS:  USABLE
MATURITY:       FIELD_VALIDATION

GOOD ENOUGH TO USE.
NOW LET REAL WORK BREAK IT.
```

El último par es un principio operacional, no una regla de gobernanza.

| Soportado | No se afirma |
|---|---|
| Necesidades crudas o parcialmente definidas · separación problema / solución propuesta · ambiguity assessment · clasificación `FACT` / `UNKNOWN` / `ASSUMPTION` / `AMBIGUITY` / `CONTRADICTION` / `DECISION_REQUIRED` · `technical-discovery` para unknowns factuales · clarification loop y ledger · provenance de requisitos · specification quality · specification coherence · readiness C1–C4 · `EXECUTION_READY` | Que la metodología esté cerrada · detección perfecta de ambigüedad · juicio semántico determinista · estado de lifecycle persistente · modelado de dominio exhaustivo · ausencia de huecos futuros · coordinación multi-repositorio (la convergencia por AC es de la Línea 2 desde 0.8.0) · garantía de estabilidad permanente |

La frontera de la Línea 1 termina en `EXECUTION_READY`, que sigue siendo distinto de `AUTHORIZED_TO_EXECUTE`.

**Evidencia de campo.** Las observaciones de campo y los candidatos futuros se registran en `tests/specification/README.md` (*Observaciones de campo* y *Candidatos futuros*). Ninguna observación aislada justifica por sí sola un cambio de método (`ONE OBSERVATION != AUTOMATIC GOVERNANCE CHANGE`).

**Política de evolución.** `NO MORE LINE 1 FEATURES BY IDEA ALONE.` Un cambio futuro de la Línea 1 sale de evidencia de uso real:

```
OBSERVED_FAILURE | OBSERVED_FRICTION | REPEATED_CAPABILITY_GAP
  → EVIDENCE → CLASSIFICATION → PATCH / MINOR cuando se justifique
NO:  IDEA → CAMBIO INMEDIATO DEL HARNESS
```

| Origen | Significa |
|---|---|
| `OBSERVED_FAILURE` | El proceso produjo un resultado incorrecto respecto de su contrato |
| `OBSERVED_FRICTION` | El resultado fue correcto, pero el proceso introduce una fricción recurrente y material |
| `REPEATED_CAPABILITY_GAP` | Varias ejecuciones reales muestran una necesidad que la capability no puede representar o resolver razonablemente |

Una ocurrencia aislada se registra como `FIELD_OBSERVATION` sin cambiar el harness (`ONE OBSERVATION != AUTOMATIC GOVERNANCE CHANGE`). Las ideas que no responden a evidencia se registran como `FUTURE_CANDIDATE` y no se implementan. Registro vigente: `tests/specification/README.md` (*Observaciones de campo* y *Candidatos futuros*).

### Origen de los mecanismos: Spec Kit como referencia

Los mecanismos de intake, clarificación, calidad y coherencia se diseñaron contrastando el checkout local de GitHub Spec Kit (`spec-kit/`, `67e0f72`). Es una **fuente de referencia, no de autoridad**, y el harness no depende de él en ejecución: `TAKE THE MECHANISMS. KEEP THE APEP CORE MODEL.`

| Adaptado de Spec Kit | Propio del harness |
|---|---|
| Taxonomía `Clear / Partial / Missing` e `Impact × Uncertainty` (`clarify`); pregunta completa, una a la vez, "why it matters", `Recommended` / `Suggested`; registrar la respuesta e integrarla sustituyendo lo contradicho | Unknown factual → discovery en vez de pregunta; política de assumptions sobre §1.3; formato `DECISION_REQUIRED`; ledger con fuente, `AFFECTS` y `SUPERSEDED`; sin máximo de preguntas |
| "Checklists are unit tests for English" (`checklist`, `specify`) | SQ1–SQ10 con evidencia y materialidad, sin checkboxes autoevaluados |
| Análisis read-only entre artefactos con severidad (`analyze`) | Gobernanza y decisiones cerradas en vez de constitution; `REFERENCE_INTEGRITY != SEMANTIC_COHERENCE`; nunca elegir versión en una contradicción material; C1–C4 y `EXECUTION_READY != AUTHORIZED_TO_EXECUTE` |

No se adoptaron: el pipeline fijo `specify → plan → tasks → implement`, los máximos de 3 marcadores o 5 preguntas, los "informed guesses" y defaults de industria, una constitution paralela, los comandos `/speckit.*`, los presets ni la instalación, ni la autoevaluación del modelo como evidencia.

Cuando la etapa 07 reporta `STATUS: EXECUTION_READY`, el skill **se detiene** (`MANDATORY_EXECUTION_GATE`): sólo una instrucción humana posterior convierte la spec en `AUTHORIZED_TO_EXECUTE`.

### Criterios de aceptación con ID estable

- El registro `AC-001`, `AC-002`, … vive en la Hard Specification (03). Los IDs son únicos y estables en la spec: un ID referenciado no se renumera ni se reutiliza.
- Use cases, escenarios, tareas, tests de aceptación, contrato e Implementation Review los referencian por ID. La relación con BR, UC, SC, TASK y AT es muchos-a-muchos, no 1:1.
- El ID sirve a la Línea 1 (C2 y trazabilidad AC → AT/TASK) y a la Línea 2: `implementation-review` converge cada `AC-NNN` material y el gate de `INTEGRATION_READY` exige todos en `PASS` (§5, *Línea 2: Delivery Factory*).

### Specs existentes

Las specs anteriores al gate vigente (AC con ID estables y readiness C1–C4) son **evidencia histórica**: pueden tener AC sin ID y `EXECUTION_READY` declarados sin el gate, y no se migran automáticamente. Si una se refina para ejecutarse, se le aplica el contrato vigente antes de declarar `EXECUTION_READY`.

### Una vez existe un Execution Contract aprobado

| No por defecto | Por qué |
|---|---|
| **No hay rediscovery** | El CURRENT_STATE relevante ya se estableció. Reinvestigar consume contexto y reabre lo cerrado |
| **No se reabren decisiones cerradas** | Sólo con **evidencia factual nueva** — y entonces el camino es `DECISION_CONTRADICTION`, no la reinterpretación silenciosa |
| **No hay scope expansion** | `IN_SCOPE` no equivale a `CHANGE_AUTHORIZATION` (`RULES.md` regla 5) |
| **No hay refactors oportunistas** | `RULES.md` regla 10: un refactor necesita su propia autorización |

Un hallazgo fuera del contrato **se reporta clasificado**, no se corrige. Lo que pasa desde tu autorización hasta `INTEGRATION_READY` es la Línea 2 (§5, *Línea 2: Delivery Factory*).

---

## 9. Code quality y testing: transversal y siempre activa

`code-quality` es la única skill always-on (`RULES.md` regla 17). No se invoca, no se desactiva y no es opcional para una implementación.

Su filosofía, sin repetir la skill:

- **Repository-first.** Las convenciones del repositorio en curso tienen autoridad local sobre cualquier regla general. Se inspeccionan; no se inventan ni se trasladan de otro repo.
- **Legibilidad antes que métricas.** Clean Code es intención expresada, no longitud de función optimizada por sí misma.
- **Coste de comprensión, de cambio y de error.** Se minimiza carga cognitiva: conceptos simultáneos, saltos entre archivos, indirecciones sin frontera real, estado implícito, side effects ocultos. Una solución "arquitectónicamente pura" puede rechazarse si cuesta más entenderla que la alternativa simple que satisface los mismos invariantes.
- **SOLID, Clean Architecture, KISS, YAGNI, DRY son herramientas de diagnóstico, no objetivos de cumplimiento.** DIP sólo con frontera real; DRY sobre duplicación de *conocimiento*, no de texto; "podría necesitarse en el futuro" nunca basta (`RULES.md` reglas 6 y 7).
- **SEARCH BEFORE CREATE.** Se busca el equivalente existente antes de crear uno nuevo. Y el código existente es evidencia de comportamiento actual, no de arquitectura pretendida: una convención repetida puede ser deuda repetida.
- **Nada de refactor oportunista.** Encontrar algo mejorable no autoriza mejorarlo.
- **Calidad proporcional al cambio.** La vara es el cambio en curso, no una campaña de limpieza del repositorio.

- **Arquitectura y dependencias.** Se respetan las capas y la dirección de dependencias que el repositorio define; invertirlas es un hallazgo, no un atajo.
- **Documentación** sólo cuando reduce incertidumbre; describe intención y comportamiento, no sintaxis, y se actualiza en el mismo cambio que altera el comportamiento o el contrato documentado.

Antes de `COMPLETE`, la skill exige revisar **el diff completo** — no sólo el archivo que motivó el cambio (§21).

### Testing

Fuente: `skill://code-quality/SKILL.md` §8. Las convenciones técnicas del repositorio (framework, carpetas, comandos) mandan en el *cómo*.

```
TEST BEHAVIOR, NOT IMPLEMENTATION DETAILS.
```

| Tema | Política |
|---|---|
| Unidad primaria | Caso de uso / comportamiento observable |
| Casos, cuando aplique | Happy path · regla de negocio violada · excepción relevante |
| Unit tests | Deterministas · independientes · sin DB real · sin servicios externos reales · sin estado global mutable compartido |
| Se puede mockear | Repositorios · servicios externos · interfaces de infraestructura |
| No se mockea | Entidades · value objects · la regla de negocio que se prueba |
| Bugfix | Preferir test de regresión que falle primero, cuando sea práctico |
| Cobertura | Es evidencia, no objetivo. No se escriben tests para subir un porcentaje |
| Qué no exige tests | Getters triviales, wiring sin comportamiento, internals irrelevantes, cambios sólo documentales |
| TDD | Técnica útil cuando reduce incertidumbre, no mandato universal |

Un test que protege comportamiento que el contrato **no** cambia no se debilita para que pase. Cómo y cuándo ejecuta los tests el agent `implementation`: §13.

---

## 10. Technical discovery

**Pregunta:** `¿Cómo funciona actualmente esto?`

Reconstruye el `CURRENT_STATE` verificable a partir de evidencia: qué hace realmente, cómo se comporta un flujo concreto, dónde están sus entry points y fronteras, cómo se mueven datos y contratos, qué está confirmado y qué permanece desconocido.

**Qué no hace:** no diseña `TARGET_STATE`, no implementa, no corrige, y no cataloga hallazgos de estilo/deuda/seguridad salvo que sean materialmente relevantes para la pregunta. Encontrar un problema no es autorización para arreglarlo.

**Escalas:** `TARGETED_DISCOVERY` · `FLOW_DISCOVERY` · `SYSTEM_DISCOVERY`. Se elige por la pregunta, y no se escala sola.

**Skill o agent:**

| Usa… | Cuando |
|---|---|
| `/skill:technical-discovery` en la Main Session | La pregunta es estrecha, quieres iterar en conversación y el volumen de lectura es pequeño |
| Delegar al agent `technical-discovery` | La investigación es de volumen, conviene aislar el contexto de la sesión, o quieres la frontera técnica read-only (el agent no tiene `edit` ni `write`) |

El resultado separa `FACT` / `INFERENCE` / `HYPOTHESIS` / `DECLARED_INTENT` / `UNKNOWN` / `CONTRADICTION`, con confianza declarada.

---

## 11. Diagnostics

**Pregunta:** `¿Por qué falló esto que observamos fallar?`

Dos fronteras que el harness nunca fusiona:

```
DISCOVERY != DIAGNOSTICS      ¿cómo funciona?  vs.  ¿por qué falló?
DIAGNOSIS != REMEDIATION      explicar la causa  vs.  cambiarla
```

**Activación:** sólo ante un **fallo observado**. Si el encargo es en realidad "¿cómo funciona X?", el routing correcto es `technical-discovery` y así debe reportarse — no se reinterpreta como diagnóstico.

**Outcomes efectivos:** `ROOT_CAUSE_CONFIRMED` (mecanismo **y** atribución al incidente demostrados) · `ROOT_CAUSE_HIGH_CONFIDENCE` (mecanismo demostrado, atribución todavía inferida) · `INSUFFICIENT_EVIDENCE`, que **exige** `MISSING_EVIDENCE`: hipótesis vivas, la observación que las discriminaría y por qué no está disponible. Cerrar por esfuerzo invertido o por explicación plausible no es cerrar.

**Escalas:** `TARGETED_DIAGNOSIS` · `FLOW_DIAGNOSIS` · `INCIDENT_DIAGNOSIS`, sin escalado automático.

**Skill o agent:**

| Usa… | Cuando |
|---|---|
| `/skill:diagnostics` en la Main Session | El fallo es pequeño, está delimitado y quieres iterar en conversación. No necesitas levantar un worker para esto |
| Delegar al agent `diagnostics` | El diagnóstico es de volumen, cruza componentes/runtime/datos/configuración, conviene aislar el contexto, o quieres la frontera técnica read-only |

Crear el agent **no convirtió el diagnóstico delegado en obligatorio**. La metodología es la misma en ambos casos: la skill (el agent la carga con `autoloadSkills`). Lo que cambia es dónde se ejecuta y con qué fronteras de herramienta.

**Observar antes que mutar.** El agent no modifica un componente sospechoso para probar una teoría cuando existe forma observacional de discriminarla, y se detiene antes de cualquier operación que destruya evidencia todavía necesaria (restart, redeploy, retry, limpieza de cache) en vez de ejecutarla "a ver si ayuda".

Puede señalar `FAULT_OWNER`, `FIX_BOUNDARY` y una dirección correctiva de alto nivel. **Nada de eso es autorización de cambio.**

---

## 12. Las reviews: qué pregunta responde cada una

Cinco capabilities de revisión, más diagnostics. Son independientes y **ninguna sustituye a otra** — pide sólo las que aporten.

| Capability | Pregunta |
|---|---|
| `implementation-review` | ¿Está correctamente implementado? |
| `pr-review` | ¿El Pull Request tiene calidad suficiente para continuar? |
| `security-review` | ¿Introduce riesgo de seguridad demostrable? |
| `architecture-review` | ¿Preserva boundaries/ownership/contracts? |
| `governance-review` | ¿Respetó scope/autoridad/reglas? |
| `diagnostics` | ¿Por qué falló algo observado? |

Un cambio puede ser correcto y no estar autorizado, o estar autorizado y ser incorrecto. Y puede ser funcionalmente correcto y aun así introducir un riesgo de seguridad.

**Referred findings.** Cada capability puede detectar señales que pertenecen a otra. Cuando ocurre, las registra como `REFERRED_FINDINGS` con la evidencia observada y **sin veredicto especializado**. Ninguna finge haber completado la revisión de otra: un `pr-review` que ve algo sospechoso no declara vulnerabilidad, la deriva a `security-review`.

**Cuándo sí y cuándo no.** Que un cambio "suene a" algo no elige la capability; la elige la pregunta real:

| La pregunta real es… | Capability |
|---|---|
| Este **cambio concreto** ¿introduce un riesgo de seguridad material y alcanzable? | `/skill:security-review` |
| Hay un **fallo ya observado** y falta su causa raíz | `/skill:diagnostics` o agent `diagnostics` |
| ¿Lo implementado hace lo que debía hacer — **correctness funcional**? | `/skill:implementation-review` |
| ¿El PR está listo como unidad de cambio — **readiness general**? | `/skill:pr-review` |
| ¿El cambio respeta **boundaries, contratos y ownership**? | agent `architecture-review` |
| ¿El cambio estaba **autorizado y dentro de alcance**? | agent `governance-review` |

### 12.1 `implementation-review` — ¿está correctamente implementado?

**Pregunta:** `¿La implementación realizada cumple correctamente el comportamiento esperado y está técnicamente bien resuelta dentro del contrato aprobado?`

El modelo es de tres piezas:

```
EXPECTED   →   IMPLEMENTED   →   VERIFIED
expectativa     cambio real      evidencia que
autoritativa                     lo demuestra
```

La expectativa autoritativa viene del Execution Contract aprobado, la specification, los criterios de aceptación, el task contract o una decisión humana explícita. **El skill nunca inventa requisitos durante la revisión.**

Distinciones que no se conflan:

```
TEST_GREEN      != REQUIREMENT_SATISFIED
CODE_PRESENT    != BEHAVIOR_VERIFIED
NO_EXCEPTION    != CORRECT_BEHAVIOR
DIFF_SMALL      != SAFE_CHANGE
REVIEW_FINDING  != AUTHORIZATION_TO_FIX
PREFERENCE      != DEFECT
```

**Dimensiones:** cobertura de requisitos · corrección lógica · edge cases materiales · manejo de errores · riesgo de regresión · qué demuestran los tests (no si pasan) · consistencia del diff.

**Convergencia por AC.** Con una especificación formal, revisa cada `AC-NNN` material y lo deja en `PASS`, `UNVERIFIED`, `UNIMPLEMENTED` o `CONTRADICTED` (`AC_CONVERGENCE_RESULT`), desde evidencia propia: `SELF-VERIFICATION != INDEPENDENT CONFORMANCE`. Lo que no es un AC — un cambio fuera de alcance, comportamiento no pedido — es un finding transversal.

**Outcomes:** `REVIEW_PASS` · `REVIEW_PASS_WITH_FINDINGS` · `REVIEW_BLOCKED` · `INSUFFICIENT_EVIDENCE`. Severidad `BLOCKING` / `MAJOR` / `MINOR`. **La ausencia de evidencia nunca se convierte en `REVIEW_PASS`.**

**Qué NO es:** PR review · security review · architecture review · governance review · diagnostics. Y no corrige: la cadena es `finding → decisión humana → specification/task contract cuando corresponda → implementation`.

> No sustituye la **Etapa 09** de `specification`, que sigue siendo la vía cuando el trabajo va dentro de un pipeline de specification formal y necesita su deliverable `09_IMPLEMENTATION_REVIEW.md`. La propia skill documenta la equivalencia entre ambos vocabularios.

### 12.2 `architecture-review` — ¿preserva las fronteras?

**Pregunta:** `¿El cambio preserva, tensiona o contradice la arquitectura aplicable?`

Evalúa, cuando corresponda: boundaries · ownership · dirección de dependencias · contratos · coupling · ciclos · ownership de estado compartido y persistencia.

**Estándar de finding:** `OBSERVED CONDITION` + `EVIDENCE` + `ARCHITECTURAL_BASIS` + `IMPACT`. Si no hay una base arquitectónica defendible (decisión cerrada, ADR, contrato, specification, boundary observable y establecida, invariante, gobernanza), lo que hay es una **preferencia** y se reporta como tal, nunca como violación.

**Outcomes:** `ARCHITECTURE_OK` · `ARCHITECTURAL_RISK` · `ARCHITECTURAL_CONTRADICTION` · `INSUFFICIENT_EVIDENCE` · `DECISION_REQUIRED`.

**No diseña arquitectura.** Tiene una `remediation-boundary` explícita: nunca inventa capas, servicios, interfaces, ports/adapters, repositories, factories, strategies, event buses, DTOs, Anti-Corruption Layers ni infraestructura alternativa como solución. **La arquitectura nueva sigue siendo decisión humana** salvo instrucción explícita distinta; la cadena por defecto es `finding → decisión humana → specification → implementation`.

### 12.3 `governance-review` — ¿estaba autorizado?

**Pregunta:** `¿El cambio respetó scope, autoridad, task contract y reglas aplicables?`

Revisa el diff contra `ENGINEERING_GOVERNANCE.md`, la gobernanza local del repositorio (p. ej. `<repo>/IA.md`) y el task contract vigente: `SCOPE_CLASSIFICATION` / `CHANGE_AUTHORIZATION`, abstracciones especulativas, política de comentarios, refactors no autorizados, invariantes violados aunque los tests pasen, y decisiones de autoridad humana tomadas unilateralmente.

**Veredicto:** `compliant` / `non_compliant`, con findings que exigen `archivo:línea` + regla incumplida.

**Está deliberadamente separada de** correctness, arquitectura, seguridad y PR readiness. La frontera que protege:

```
"esto funciona"   !=   "esto estaba autorizado"
```

Existe **sólo como agent**, no como skill (§13).

### 12.4 `security-review` — ¿introduce riesgo demostrable?

**Pregunta:** `¿El cambio introduce un riesgo de seguridad material, demostrable y relevante que deba atenderse antes de continuar?`

Es deliberadamente escéptica:

```
POSSIBLE_ATTACK    != VULNERABILITY
THEORETICAL_PATH   != REACHABLE_PATH
MISSING_HARDENING  != SECURITY_DEFECT
SECURITY_FINDING   != AUTHORIZATION_TO_FIX

EVIDENCE BEFORE CLAIM · REACHABILITY BEFORE SEVERITY · CONTINUITY OVER SECURITY THEATER
```

**Alcance:** sólo **las superficies de seguridad materialmente relacionadas con el cambio**, y su impacto razonablemente relacionado. Leer un archivo completo o seguir una llamada para establecer reachability es legítimo; barrer subsistemas no relacionados no lo es.

**Estados de finding:** `CONFIRMED_SECURITY_FINDING` · `SUPPORTED_SECURITY_CONCERN` · `HARDENING_OPPORTUNITY` (nunca bloquea por sí sola) · `REJECTED_SECURITY_HYPOTHESIS`. Severidad `BLOCKING` / `MAJOR` / `MINOR`, sin CVSS. **La severidad nunca compensa la falta de evidencia:** si la evidencia es débil, lo que baja es el estado.

**Outcomes:** `SECURITY_PASS` · `SECURITY_PASS_WITH_FINDINGS` · `SECURITY_BLOCKED` · `INSUFFICIENT_EVIDENCE`.

**Qué NO es:** pentest · auditoría completa · threat model global del producto · remediation · arquitectura de seguridad. Un incidente de seguridad **que ya ocurrió** es `diagnostics`, no `security-review`.

**Read-only por contrato.** No parchea, no rota secretos, no toca IAM, configuración, red ni dependencias, y no ejecuta exploits ni payloads. Una revisión normal reporta `SECURITY_STATE_CHANGED: NO`.

**Coexistencia con el bundled `security-reviewer`.** OMP trae de serie el agent `security-reviewer` (read-only), que **sigue existiendo, intacto y disponible**: nuestra skill no lo reemplazó. La diferencia es la unidad de trabajo:

| Usa… | Cuando |
|---|---|
| `/skill:security-review` | La pregunta es si **un cambio concreto** introduce riesgo |
| agent bundled `security-reviewer` | Quieres un **barrido de descubrimiento sobre un repositorio** o alcance dado |

La skill no adopta el vocabulario de severidad del bundled (`critical`/`high`/`medium`/`low`/`informational`): al consumir su output lo traduce con criterio y **revalida reachability y precondiciones** antes de adoptar un finding externo.

> El escaneo nativo de OMP (`/security`, herramienta `security_scan`, URIs `security://`) depende de `security.enabled`; compruébalo con `omp config get security.enabled`. Habilitarlo es una decisión humana de configuración, no algo que esta skill active.

### 12.5 `pr-review` — ciclo de vida de Pull Requests / merge requests

**Contrato genérico, independiente del provider.** `pr-review` define qué evidencia hace falta, cómo se clasifican los findings, qué autoridad exige cada mutación remota y cómo se encadena el ciclo de vida. La mecánica concreta contra un remote —comandos o API, errores del servicio, sincronización, notificaciones— la aporta una **capability de provider configurada por separado**, p. ej. distribuida por un plugin de organización para CodeCommit, GitHub u otro remote, y se aplica **junto con** esta skill, nunca sustituyéndola. Apep Core no incluye ningún provider: sin uno configurado, `pr-review` sigue siendo válida como metodología de revisión sobre evidencia que el humano aporte, pero **no puede materializar mutaciones remotas**. Un ejemplo de adaptador de CodeCommit es `skill://pr-review-codecommit` (con sus `references/` de notificaciones, sincronización y escenarios), disponible sólo si el plugin de organización que lo distribuye está compuesto; esa mecánica no se duplica aquí.

Es el **ciclo de vida completo y autorizado** de los PRs, desde la lectura del estado remoto hasta el merge verificado y, si el provider las define, la sincronización con su destino y las notificaciones. El punto de entrada recomendado es el work mode `/pr` (§7), que carga esta skill; `/skill:pr-review` sigue disponible. No existe una capability paralela de lifecycle y lo coordina la Control Tower (§4). Fuente normativa del detalle: `skill://pr-review/SKILL.md` (§11 autoridad de mutación remota, §16 contrato de salida, §17 paradas, §18 lotes, §19 ciclo; §20 sincronización y §21 notificaciones son capabilities **opcionales del provider**).

**Pregunta de la revisión:** `¿Los cambios agregados, modificados o eliminados son coherentes con lo que el Pull Request declara hacer, y alcanzan un nivel suficiente de calidad para continuar operando y entregando?`

**Objeto primario:** el diff del PR —líneas agregadas, modificadas y eliminadas— más el contexto **estrictamente necesario** para interpretarlas. No audita el repositorio por defecto. **No es búsqueda exhaustiva de bugs**: si un defecto emerge razonablemente de revisar el cambio, se reporta, pero no se amplía el alcance para cazar defectos hipotéticos.

```
PREFERENCE  != DEFECT
SUGGESTION  != BLOCKER
GOOD_ENOUGH != BAD

CONTINUITY OVER PERFECTION
REVIEW UNTIL SAFE AND SUFFICIENT, NOT UNTIL IDEAL
```

#### Findings y outcomes

Los **findings** clasifican cada observación:

| Finding | Qué es | Bloquea |
|---|---|---|
| `MUST_FIX` | Problema material: comportamiento incorrecto, contrato roto, bug introducido, build/test esencial roto, pérdida funcional, conflicto de merge, código que contradice el objetivo del PR | **Sí** |
| `SHOULD_IMPROVE` | Mejora clara con beneficio real demostrable: duplicación introducida, manejo de errores débil, test material ausente, complejidad evitable creada por el propio cambio | No necesariamente |
| `SUGGESTION` | Mejora opcional: simplificación razonable, forma más idiomática, legibilidad menor | **Nunca** |

El **outcome** es un único valor por PR: `APPROVE` · `APPROVE_WITH_COMMENTS` · `CHANGES_REQUIRED` · `INSUFFICIENT_EVIDENCE`.

```
MUST_FIX_PRESENT → CHANGES_REQUIRED
```

`MUST_FIX` es una clase de finding y nunca un outcome. `APPROVE` como outcome no es aprobación de seguridad, arquitectura ni governance, ni autorización para aprobar o mergear en el remote. **La ausencia de evidencia nunca se convierte en aprobación.**

**Prevención de review loops.** Un reviewer no encadena mejoras: una sugerencia opcional aceptada **no** abre otra ronda de perfeccionamiento. Una zona ya revisada sólo genera una observación nueva si el cambio posterior introdujo un defecto, el finding original sigue sin resolverse o hay evidencia material nueva.

#### Entrada, control y autorización

| | |
|---|---|
| **Entrada** | Un PR · una lista explícita · un lote acotado (*"los PR abiertos de `<repo>` con destino `<rama>`"*) |
| **Control** | La Control Tower fija `AUTHORIZED_SET` (enumerado al empezar; no crece) y `AUTHORIZED_ACTIONS` |

| Acción autorizable | Qué materializa | Sin ella |
|---|---|---|
| `REVIEW` | Lectura, revisión, clasificación y reporte. Implícita en toda invocación | — |
| `PUBLISH_COMMENTS` | Publicar en el remote los comentarios de la revisión | Se presentan como `COMMENTS_TO_POST` |
| `APPROVE` | Approval sobre la revision revisada | `NOT_AUTHORIZED` |
| `MERGE` | Merge con el método determinado | `NOT_AUTHORIZED` |
| `SYNC_REMEDIATION` *(opcional, provider)* | Remediación mecánica de sincronización con el destino | `SYNC_REQUIRED (NOT_AUTHORIZED)` |
| `AUTHOR_NOTIFICATION` *(opcional, provider)* | Aviso al autor de un PR con `MUST_FIX` | `NOT_AUTHORIZED` |
| `EXECUTIVE_NOTIFICATION` *(opcional, provider)* | Un aviso consolidado al cerrar el ciclo | `NOT_AUTHORIZED` |

```
AUTHORIZE THE EFFECT, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.
AUTHORIZED != ELIGIBLE

COMMENT AUTHORIZATION  != APPROVAL AUTHORIZATION
APPROVAL AUTHORIZATION != MERGE AUTHORIZATION
MERGE AUTHORIZATION    != SYNC_REMEDIATION AUTHORIZATION
OUTCOME = APPROVE      != autorización para aprobar
MERGEABLE = YES        != autorización para mergear
```

La autorización es lenguaje natural inequívoco, sin fórmula: *"publica los comentarios y aprueba"* autoriza dos acciones y no el merge; *"ciclo completo"* autoriza las que nombres o, si no nombras ninguna, sólo `REVIEW`. Una autorización de lote cubre las acciones autorizadas **sin volver a pedir confirmación** por comentario, PR, comando ni PR auxiliar. Tú no ejecutas los comandos del provider después de autorizar. Cada PR, en cambio, conserva sus precondiciones: una acción autorizada pero no elegible se registra con su blocker (`SKIPPED_NOT_ELIGIBLE`) y no se ejecuta.

**Frontera del lote.** El conjunto debe poder enumerarse de forma determinista: IDs, una lista presentada, o los PRs de un repositorio nombrado con criterios inequívocos. *"mergea todo lo que encuentres"* no es un lote: `DECISION_REQUIRED`. `BATCH_AUTHORIZATION != BLANKET_UNBOUNDED_AUTHORIZATION`. Un lote nunca concede override de condiciones explícitas del PR (*"NO MERGE hasta …"*: `MERGE_AUTHORIZATION != BLOCKER_OVERRIDE_AUTHORIZATION`, hay que nombrarlo), ni tocar approval rules, ni resolver conflictos funcionales, ni ampliar `AUTHORIZED_SET`.

**Negativas previas del agente.** `AGENT REFUSAL != GOVERNANCE`. Si el agente se negó bajo una versión anterior de la skill y el harness cambió por decisión humana, la skill se relee y se opera bajo la policy vigente. Pero `SKILL UPDATE != MERGE AUTHORIZATION`: sigue haciendo falta tu autorización.

#### El ciclo

```
PR individual / lista / lote
  → LOAD_REMOTE_STATE → REVIEW → CLASSIFY → MATERIALIZE_RESULT
  → SYNC_IF_NEEDED (opcional, provider) → VERIFY_REMOTE → NOTIFY_IF_REQUIRED (opcional, provider) → PER_PR_RESULT
  (siguiente PR del conjunto)
→ CONSOLIDATE_REPORT → EXECUTIVE_NOTIFICATION (opcional, provider) → BATCH_RESULT
```

Orden fijo de mutaciones dentro de un PR: **comentarios → sincronización → approval → merge**. Los comentarios van primero porque el merge cierra el PR, y la sincronización va antes del approval porque cambia la revision. Cada paso se ejecuta sólo si su acción está en `AUTHORIZED_ACTIONS` **y** el PR es elegible en ese momento.

Routing por outcome (`pr-review` §19.3):

- **`APPROVE`**: [sync si hace falta] → revalidar → aprobar → verificar approval → reglas de aprobación y mergeability → merge si es elegible → verificar → registrar el merge commit.
- **`APPROVE_WITH_COMMENTS`**: publicar comentarios → verificar → [sync] → revalidar → aprobar → verificar → merge si es elegible → verificar. Si la publicación falla, ese PR no se aprueba ni se mergea: los comentarios forman parte de lo decidido.
- **`CHANGES_REQUIRED`** (hay `MUST_FIX`): publicar los comentarios (si está autorizado) → **no approve · no merge · no sync** · el PR queda abierto → aviso al autor si el provider lo soporta y está autorizado. Un fallo de notificación no cambia el outcome.
- **`INSUFFICIENT_EVIDENCE`**: se registra `MISSING_EVIDENCE` y no hay ninguna mutación. El PR queda abierto, entra en el reporte y el lote continúa, salvo un blocker transversal.

#### Autoridad de mutación remota

- **Snapshot y drift.** Una autorización corresponde a un estado concreto de cada PR (su `AUTHORIZED_SNAPSHOT`: `revisionId` o equivalente, source y destination commits, outcome, método de merge). Antes de **cada** mutación se relee el estado remoto y se compara; si la revision o el source commit cambiaron (`REMOTE_DRIFT_DETECTED`), la mutación no se ejecuta y el PR se revisa sobre la revision nueva, sólo el delta. Un approval sobre la revision vieja no cuenta para la nueva. Además, cada mutación fija la revision esperada en su propio request, para que el provider rechace del lado del servidor una carrera: un rechazo por snapshot obsoleto *es* drift, no una señal de reintento.
- **Verificación contra el remote.** Cada transición material se confirma releyendo el sistema remoto; el exit code nunca basta (ver *Reporte obligatorio*).
- **Elegibilidad previa e idempotencia.** Antes de aprobar o mergear se pregunta al provider si la operación tendría éxito ahora (`PRE_FLIGHT_ELIGIBILITY_CHECK`: reglas de aprobación, opciones y conflictos de merge, identidad efectiva distinta del autor). Toda mutación lleva una clave determinista (`IDEMPOTENT_MUTATION_KEY`) o se comprueba antes si su efecto ya existe, de modo que reintentar un ciclo, o un PR dentro de él, nunca duplica un efecto (`RETRY != DUPLICATE SIDE EFFECT`).
- **Método de merge.** No se inventa. Lo fija la gobernanza del repositorio, el task contract o el humano, o el provider cuando sólo ofrece una opción. Si no: `DECISION_REQUIRED: MERGE_METHOD`, sólo para ese PR. El merge nunca se sustituye por `git merge` + `git push` local, y nunca usa estrategias de resolución de conflictos.
- **Éxito parcial.** Si una acción falla, las siguientes de ese PR no se ejecutan a ciegas. El éxito parcial se reporta tal cual (`APPROVED` + `MERGE_FAILED`) y no se deshace: un approval verificado no se revoca.
- **Autoaprobación.** `NEVER SELF-APPROVE`: si la identidad efectiva es la autora del PR —original o auxiliar creado por el propio ciclo—, no aprueba (`SELF_APPROVAL_NOT_ALLOWED`). Nunca cambia de identidad o rol para sortearlo, ni toca ni elude approval rules. El PR queda esperando approval externo y el lote continúa; si un tercero ya satisfizo las reglas, el merge sigue siendo elegible.
- **Qué sigue prohibido, con autorización o sin ella:** revocar un approval, override o edición de approval rules, cerrar un PR sin merge, cambiar título o descripción, resolver conflictos, rebase, cherry-pick, force-push, remediation funcional, ampliar `AUTHORIZED_SET`, crear infraestructura o identidades. La lista concreta de operaciones prohibidas es del provider; la doctrina es de `pr-review` (§4.5, §11.7).

#### Sincronización y notificaciones: capabilities opcionales del provider

`pr-review` no altera arbitrariamente un PR para hacerlo mergeable. La única excepción es una **remediación mecánica de sincronización** que un provider defina, explícita, acotada y autorizada (`SYNC_REMEDIATION`): sólo cuando el PR ya es aprobable, no hay `MUST_FIX` ni decisión funcional pendiente y el único blocker es la desincronización con su destino; ante la duda sobre si un conflicto es mecánico, se trata como no mecánico. Tras sincronizar se revisa sólo el delta (`SYNC_REVALIDATION != FULL_REVIEW_RESTART`), y la destination sale siempre del PR real. Las notificaciones (`AUTHOR_NOTIFICATION`, `EXECUTIVE_NOTIFICATION`) siguen el mismo modelo: acción autorizable por separado, idempotente, y su fallo no modifica los outcomes técnicos (`NOTIFICATION_ACCEPTED != DELIVERY_CONFIRMED`). Cómo se materializan —el procedimiento de sincronización, a qué canal y con qué contenido se notifica— es del provider; Apep Core no lo define ni lo ejecuta.

#### Continuidad del lote

```
ONE BLOCKED PR != STOP WHOLE BATCH
```

`CHANGES_REQUIRED`, `INSUFFICIENT_EVIDENCE`, `SELF_APPROVAL_NOT_ALLOWED`, un bloqueo de una capability opcional, `BLOCKED_BY_APPROVAL_POLICY`, el fallo de una acción y el fallo de una notificación se registran, y el ciclo sigue con el siguiente miembro cuando es seguro. Cada merge mueve el destino común, así que cada PR se revalida en su turno. El lote completo sólo se detiene por una **condición transversal**: `AUTHORIZED_SET` ambiguo · identidad o entorno equivocados · credenciales no disponibles · estado remoto no confiable · contradicción de governance · fallo sistémico. Incluso entonces se entrega el reporte con lo hecho y lo pendiente.

#### Publicación de comentarios

```
NO EXPLICIT AUTHORIZATION == NO REMOTE COMMENT MUTATION
```

- **Sin `PUBLISH_COMMENTS`, no publica.** Te presenta `COMMENTS_TO_POST` (identificador, ubicación y texto literal) y espera. Los comentarios siguen la convención de idioma de revisión del repositorio; si no muestra ninguna, el idioma de la conversación.
- **Con `PUBLISH_COMMENTS` autorizada:** sobre comentarios que viste, publica exactamente esos; en un lote, los que la revisión de **ese** ciclo produzca para los PR del conjunto, sin confirmación individual y con cada comentario literal en el reporte.
- **No duplica** un comentario equivalente a uno existente y no cambia materialmente uno autorizado sin volver a ti (STOP-2).
- **Verifica** releyendo los comentarios del PR y reporta identificadores, fallos parciales y lo no publicado.

```
PUBLISH AUTHORIZATION != APPROVAL · MERGE · REMEDIATION · BRANCH MUTATION AUTHORIZATION
```

#### Reporte obligatorio

**Toda** ejecución de `pr-review`, también para un PR único y también si sólo se revisó, termina con una tabla de **exactamente cinco columnas**, con una fila por cada PR de `AUTHORIZED_SET` (también los omitidos o bloqueados):

| PR | Repositorio | Autor del PR | Estado del PR | Observaciones o comentarios |
|---|---|---|---|---|
| `#<id>` | `<repo>` | Identidad declarada del autor en la forma que el provider la exponga, nunca un correo | Estado remoto verificado · estado del ciclo | Outcome · findings · comentarios publicados · blockers · approval · resultados de las capabilities opcionales · merge commit · fallos parciales |

Debajo, los contadores (PR revisados · `APPROVE` · `APPROVE_WITH_COMMENTS` · `MERGED` · `CHANGES_REQUIRED` / `MUST_FIX` · `BLOCKED` por código · `INSUFFICIENT_EVIDENCE` · operaciones fuera de alcance). Cuando la autorización cubrió más de un PR, un único `BATCH_RESULT` consolida el conjunto: `COMPLETE` · `PARTIAL_SUCCESS` · `NONE_EXECUTED` · `STOPPED`, con una fila `PER_PR` por miembro y su blocker. `PARTIAL_SUCCESS` es un resultado válido y no se oculta bajo `COMPLETE`.

**Verificación remota.** `REMOTE SYSTEM STATE IS THE EVIDENCE.`

```
exit 0 != COMMENT_VERIFIED · APPROVAL_VERIFIED · MERGE_VERIFIED
```

Un merge que el comando da por bueno pero que el remote no confirma es `MERGE_UNVERIFIED`, no `MERGED`. `PR_STATE_CHANGED` es `NO` cuando sólo se observó, o la lista de mutaciones con su resultado (`COMMENTS_POSTED` · `APPROVED` · `MERGED`; en caso de fallo `COMMENTS_FAILED` · `APPROVAL_FAILED` · `MERGE_FAILED` · `APPROVAL_UNVERIFIED` · `MERGE_UNVERIFIED`).

**STOP conditions de las mutaciones** (detienen la acción afectada, no la revisión): autorización ausente o ambigua · cambio material de un comentario · ambigüedad de identidad o entorno de ejecución · drift · contradicción normativa · PR cerrado o superseded · source/destination inesperados · blocker, evidencia insuficiente o conflicto · approval requerido no satisfecho · método de merge no determinado · condición de una capability opcional del provider · autoaprobación. Sólo las transversales detienen el lote. Detalle: `skill://pr-review/SKILL.md` §17.

#### Contexto delegado y las dos capas

Dentro de `delivery-orchestrator`, `pr-review` revisa y prepara (`COMMENTS_TO_POST`, `ACTIONS_AVAILABLE`, `MERGE_READY`) pero no muta: todas las mutaciones del ciclo corren en la Main Session.

> Nota de las dos capas: `AUTHORIZED PR LIFECYCLE → NO REPETITIVE TOOL APPROVALS`. Autorizas una vez, al fijar el lote y sus `AUTHORIZED_ACTIONS`; qué operaciones del provider piden después confirmación de herramienta lo decide tu `config.yml` y el plugin del provider, no Apep Core (`pr-review` §11.5, §23). Que la herramienta no pregunte no amplía la autoridad, y que pregunte no es una pregunta semántica para ti: se reporta y se continúa cuando se apruebe, sin buscar un rodeo.

---

## 13. Agents: workers acotados

```
SKILL = metodología / capability   (cómo se trabaja; se carga en un contexto)
AGENT = worker especializado        (quién trabaja; modelo y toolset fijados)
```

Un agent se delega por nombre con la herramienta `task` (`agent: "<nombre>"`), que es autónoma (§23). OMP los descubre en `agents/*.md` del plugin (o `<cwd>/.omp/agents/` en un proyecto).

### Los 6 agents project-local

| Agent | Rol de modelo (frontmatter) | Thinking | Escribe | Cuándo | Qué NO puede |
|---|---|---|---|---|---|
| `delivery-orchestrator` | `@default` | high | No (sin `edit`/`write`); sólo agent que delega (`spawns`: implementation, technical-discovery, architecture-review, governance-review, diagnostics) | Lifecycle completo de un work item (§4) | Escribir código; decidir materias reservadas; commit/push/PR/merge/tag |
| `implementation` | `@task` | medium | **Sí** (`edit`, `write`, `bash`) | Ejecutar un Execution Contract autorizado | Redefinir scope o materias reservadas; commit/push/PR sin autorización |
| `technical-discovery` | `@default` | medium | No | Discovery de volumen o con frontera read-only | Diseñar `TARGET_STATE`, corregir |
| `diagnostics` | `@slow` | high | No | Diagnóstico de volumen o que cruza runtime/datos/config | Remediation, mutar para probar teorías |
| `architecture-review` | `@slow` | high | No | Review de fronteras con aislamiento de contexto | Diseñar arquitectura de reemplazo |
| `governance-review` | modelo explícito (ver su frontmatter) | medium | No | ¿Se respetó scope, autoridad y reglas? | Juzgar correctness, corregir |

Qué modelo concreto sirve cada rol lo decide el `modelRoles` de tu `config.yml` (§16).

**Los agents corren headless.** OMP los ejecuta con `approvalMode: yolo`, pero los `prompt` de usuario siguen mandando: dentro de un agent, un comando con gate material (`git commit`, `push`, mutación cloud, SQL destructivo…) **se rechaza** (`requires approval but no interactive UI available`), no pregunta. Consecuencia: un commit, un push o la publicación de un PR, aunque estén autorizados, **los ejecuta la Main Session**; los agents los dejan preparados. Sólo `delivery-orchestrator` declara `spawns`; los demás agents no tienen `task` y no pueden delegar. Profundidad máxima: `task.maxRecursionDepth: 2` (Main → orchestrator → worker).

Los agents read-only tienen `read`, `grep`, `glob`, `lsp`, `ast_grep`, `bash` y `yield`. Ahí `bash` es **sólo para evidencia** (Git de lectura, inspección, ejecutar tests existentes para observar). Esa restricción es contractual, no un sandbox técnico.

### Darle a cada worker trabajo compatible

| Si necesitas… | Delega a | No delegues a |
|---|---|---|
| Saber qué hace realmente X | `technical-discovery` | `implementation` |
| Saber por qué falló X | `diagnostics` | `technical-discovery` |
| Escribir el cambio | `implementation` | `technical-discovery` |
| Saber si el cambio rompe una frontera | `architecture-review` | `governance-review` |
| Saber si se respetó alcance y autoridad | `governance-review` | `architecture-review` |
| Diseñar la arquitectura de reemplazo | **A nadie — es decisión humana** | `architecture-review` |

### Autonomía de `implementation`

Con un Execution Contract aprobado, `implementation` trabaja de forma autónoma dentro del scope:

```
INSPECT → EDIT → VERIFY → FAIL?
                            ├─ inspecciona la evidencia
                            ├─ ¿lo causa mi cambio y está en scope? → FIX → RETEST
                            ├─ preexistente y no impide evaluar la aceptación → lo reporta, no lo toca
                            └─ no converge o exige salir del contrato → ESCALA (§19)
        → COMPLETE WITH EVIDENCE
```

```
IMPLEMENTATION IS NOT COMPLETE UNTIL VERIFICATION HAS RUN.
CHEAPEST RELEVANT TEST FIRST → BROADER VERIFICATION AS CONFIDENCE GROWS.
```

| Puede sin preguntar | Necesita autorización (contrato o tú) |
|---|---|
| Inspeccionar, editar, crear archivos en scope | Cualquier cosa fuera del scope |
| Formatter, linter, type-check, build | Cambiar el manifiesto de dependencias |
| Tests unitarios y de regresión relevantes; checks de integración locales | Integración que toque estado compartido o remoto |
| Scripts locales de verificación; preparación local de dependencias | Crear/cambiar de rama, commit, push, PR, merge, tag |
| Corregir y volver a probar; decisiones tácticas (`ENGINEERING_GOVERNANCE.md` §1.3) | Decisiones no tácticas: §1.2 |
| Preparar evidencia, mensaje de commit y borrador de PR | Publicar cualquiera de ellos |

- **No pregunta "¿ejecuto los tests?"** cuando existe una verificación local aplicable: la ejecuta.
- **No ejecuta suites gigantes sin criterio.** Primero los tests del comportamiento tocado; después, verificación más amplia antes de reportar.
- **No hace pasar la verificación debilitando evidencia**: no borra, salta ni relaja tests o reglas de lint que el contrato no cambia.
- **Comprueba la rama antes de escribir** (`git-workflow` §4). Si está en una rama permanente (las declara la gobernanza del repositorio) o en la rama de otro work item, no escribe. Si cambiar de rama no está autorizado, se detiene con el comando propuesto.
- **Entrega evidencia** (`ENGINEERING_GOVERNANCE.md` §13): rama, archivos modificados, cada comando de verificación con su resultado, fallos preexistentes separados de los propios, desviaciones, deuda descubierta y decisiones pendientes.

Un hallazgo `IN_SCOPE` no autoriza modificarlo. Lo `RELATED_BUT_OUT_OF_SCOPE` o `UNRELATED` se reporta y queda intacto.

### Cuando una capability es skill y agent a la vez

`technical-discovery`, `diagnostics` y `architecture-review` existen de las dos formas, y **no son excluyentes**. La metodología es la misma — la skill. Lo que cambia es dónde se ejecuta y con qué fronteras de herramienta. Elige por proporcionalidad (volumen, aislamiento de contexto, necesidad de frontera read-only), no por norma: ver §10 y §11.

Las demás son de una sola forma:

- **Sólo skill** (se ejecutan en la Main Session): `code-quality`, `specification`, `project-management`, `git-workflow`, `implementation-review`, `pr-review`, `security-review`.
- **Sólo agent**: `implementation`, `governance-review`.

### Agents que OMP trae de serie

OMP incluye cinco agents bundled: `scout` (investigación read-only en modelo rápido), `reviewer` (revisión de corrección funcional general), `security-reviewer` (especialista de seguridad read-only), `sonic` (modelo de bajo razonamiento, sólo para actualizaciones mecánicas o recolección de datos) y `task` (subagent de propósito general). Existen y son usables —la corrección funcional con metodología project-local es `implementation-review`; `reviewer` es la alternativa bundled sin esa metodología— pero **no están gobernados por nuestro harness**: su metodología es la de OMP, no la de `.omp/skills/`.

Un agent project-local con el mismo nombre que uno bundled tendría precedencia; hoy no hay colisión de nombres.

---

## 14. Orquestación proporcional: uno o varios workers

```
MULTI-AGENT WHEN THE WORK DECOMPOSES;
SINGLE OWNER FOR THE CONCLUSION.
```

Delegar la **misma capability a varios workers** ya es posible hoy: la Main Session levanta los `task` que necesite. Esta sección no añade maquinaria — dice **cuándo conviene**, con qué fronteras y quién se queda con la conclusión. La orquestación la conduce la Main Session en modo interactivo, o el `delivery-orchestrator` dentro de un lifecycle delegado (§4); en ambos casos rige un único synthesis owner (abajo).

Paralelizar tiene que aportar una ventaja real: **reducir tiempo · aislar contexto · separar componentes o repositorios · investigar hipótesis independientes · aplicar lentes especializadas distintas**. No se levantan varios agents porque estén disponibles.

### El modelo

```
                    WORK / QUESTION
                          │
                 ¿es descomponible?
                    /           \
                  NO             SÍ
                  │               │
             1 worker       fan-out acotado
                                  │
                     ┌────────────┼────────────┐
                     ▼            ▼            ▼
                  worker A     worker B     worker C
                     │            │            │
                     └────────────┼────────────┘
                                  ▼
                          SYNTHESIS OWNER
                                  │
                                  ▼
                          UN SOLO RESULTADO
```

```
PARALLEL EVIDENCE + SPECIALIZED PERSPECTIVES + SINGLE SYNTHESIS
```

Los workers reúnen **evidencia**. La conclusión es de uno solo.

### Cuándo descompone — y cuándo no

| Fan-out acotado aporta | Un solo worker |
|---|---|
| Trabajo materialmente independiente | Tarea pequeña y local |
| Varios repositorios o componentes | Un worker puede responder con evidencia suficiente |
| Gran volumen de lectura | Dividir cuesta más coordinación que trabajo |
| Fronteras naturales claras | Los workers tendrían que tocar los mismos archivos |
| Hipótesis independientes investigables en paralelo | Las subtareas dependen secuencialmente unas de otras |
| Fuentes de evidencia que no dependen entre sí | La división sólo existe para usar más agents |
| Reviews especializadas distintas | |
| El aislamiento de contexto aporta valor por sí mismo | |
| La paralelización reduce el tiempo de forma material | |

```
COORDINATION_COST < EXPECTED_PARALLELIZATION_VALUE
```

Si la desigualdad no se cumple, un solo worker. Es la misma proporcionalidad de §1 aplicada al número de workers: se usa lo que reduce incertidumbre o protege una frontera, no lo que está disponible.

### Escala: heurística, no umbral

| Escala del encargo | Forma habitual |
|---|---|
| `TARGETED` | Normalmente 1 worker |
| `FLOW` | 1 worker; **puede** abrirse a 2 si existen fronteras independientes reales |
| `SYSTEM` · `INCIDENT` · multi-repositorio | **Puede** usar fan-out especializado + synthesis owner |

Es una heurística de proporcionalidad, no una obligación ni un umbral numérico. Una escala alta no obliga a paralelizar, y una escala baja con dos fronteras genuinamente independientes puede justificar dos workers.

### El synthesis owner

Toda ejecución multi-agent tiene **exactamente un** responsable de la síntesis:

| Modo | Synthesis owner |
|---|---|
| Orquestación interactiva | Main Session |
| Lifecycle delegado | `delivery-orchestrator`, durante ese lifecycle |

Un task puede designar explícitamente a otro worker para sintetizar. Nunca hay dos synthesis owners para la misma conclusión.

El synthesis owner:

- conserva la pregunta original, el scope y los invariantes;
- asigna las fronteras y comprueba que no se solapan ni dejan huecos;
- integra la evidencia devuelta y detecta duplicación;
- reconcilia contradicciones entre workers, y entre un worker y la evidencia (§4);
- conserva los `UNKNOWN` en vez de completarlos con lo que otro worker supuso;
- mantiene separados `FACT` / `INFERENCE` / `HYPOTHESIS` (§1) — no promueve una categoría porque venga repetida;
- produce el **único** resultado final.

Sintetizar no concede autoridad adicional sobre arquitectura, contratos, alcance, seguridad, semántica de negocio ni ninguna otra materia reservada (§1; `ENGINEERING_GOVERNANCE.md` §1.2).

```
AUTONOMY != AUTHORITY
```

### No hay democracia de agents

```
AGENT_CONSENSUS != CONCLUSION
```

Un finding respaldado por evidencia **no deja de ser válido porque otros workers no lo hayan detectado**. No se decide por mayoría: tres workers que no vieron algo no refutan al que lo vio con evidencia, y tres que coinciden no convierten una inferencia en hecho. Lo que decide es la evidencia, no el recuento.

Cuando dos workers se contradicen, el synthesis owner no elige el más convincente: identifica qué observación discriminaría entre los dos y, si no está disponible, lo reporta como `CONTRADICTION` o `UNKNOWN`.

### Aplicación por capability

**`technical-discovery` — fan-out por frontera.** Cuando el `CURRENT_STATE` tiene fronteras independientes:

```
technical-discovery
  ├─ backend
  ├─ frontend
  ├─ infraestructura
  └─ contratos/datos
         ↓
   synthesis owner
         ↓
   CURRENT_STATE único
```

Cada worker recibe un scope explícito. Ninguno investiga horizontalmente sin frontera, ninguno emite su propio `TARGET_STATE` (§10), y no se producen varios `CURRENT_STATE` competidores: el synthesis owner conserva la responsabilidad de una sola reconstrucción coherente.

**`diagnostics` — fan-out por hipótesis o dominio causal.** Sólo ante un fallo observado (§11):

```
INCIDENT
  ├─ runtime/logs
  ├─ data/state
  ├─ config/deployment
  └─ code path
         ↓
   diagnosis synthesis
         ↓
   FIRST_DIVERGENCE · FAILURE_MECHANISM
   ROOT_CAUSE / INSUFFICIENT_EVIDENCE
```

Los workers producen **evidencia discriminante** sobre su dominio. La atribución causal final pertenece al synthesis owner. Lo que no se hace:

```
worker A → root cause A
worker B → root cause B     →  majority vote
worker C → root cause C
```

Tres causas raíz sin reconciliar no son un diagnóstico, y la más votada tampoco. Si la evidencia no discrimina, el resultado es `INSUFFICIENT_EVIDENCE` con su `MISSING_EVIDENCE`.

**`architecture-review` — fan-out por frontera cruzada.** Cuando el cambio cruza fronteras suficientemente independientes:

```
backend reviewer  ·  frontend reviewer  ·  infra reviewer
                          ↓
                architecture synthesis
                          ↓
              un solo architecture outcome
```

Cada worker revisa únicamente su frontera; el synthesis owner evalúa además los efectos **entre** fronteras, que es justo lo que ningún worker aislado ve. Para un cambio pequeño donde una sola revisión tiene contexto suficiente, no se abre fan-out.

**`implementation` — restricción más fuerte.**

```
MULTI-WRITER REQUIRES EXPLICIT OWNERSHIP BOUNDARIES.
```

Varios agents `implementation` **pueden** trabajar en paralelo únicamente cuando se dan **todas** estas condiciones:

- sus scopes de escritura están explícitamente delimitados;
- no poseen los mismos archivos;
- no dependen de estado mutable compartido no coordinado;
- cada modificación puede verificarse de forma independiente;
- los contratos permiten integrar los resultados sin redefinir decisiones ya cerradas.

```
implementation A → <repo-a>/          aceptable: tres contratos
implementation B → <repo-b>/          delimitados e independientes
implementation C → <repo-c>/
```

```
implementation A ─┐
implementation B ─┼→ mismos archivos / mismo working tree mutable
implementation C ─┘                  evitar por defecto
```

El harness **no tiene hoy** locking, worktrees por worker, ramas por worker ni coordinación de writers. Si una tarea los necesita, eso es diseño aparte y decisión humana (§1) — no algo que se improvise durante la ejecución. Y la disciplina Git de cada repositorio sigue íntegra: baseline por repositorio, una única intención coherente por modificación, nada que cree o publique historia sin autorización (§20, `RULES.md` 13 y 18).

**Reviews — dos cosas distintas que no se confunden:**

| | Qué es |
|---|---|
| **Multi-agent dentro de una capability** | Varios workers reúnen evidencia para **una sola** conclusión de esa capability |
| **Reviews especializadas distintas** | Capabilities distintas que responden **preguntas distintas** (§12) |

```
implementation-review · security-review · architecture-review · governance-review
                          ↓
                 humano / capa de síntesis
```

Lo segundo no es fan-out: ya era así. Ninguna review sustituye a otra, y **un finding respaldado por evidencia no queda invalidado porque otra review haya dado `PASS` en su propia dimensión** — responden a preguntas diferentes.

### La autoridad humana no se vota

```
N AGENTS RECOMMENDING X != HUMAN DECISION
```

Multi-agent no convierte varias opiniones en una decisión. Las materias reservadas siguen escalando exactamente igual, por los tres artefactos de §19 — `DECISION_REQUIRED`, `STOP_REPORT`, `DECISION_CONTRADICTION` — y el consenso entre agents nunca es el mecanismo que cierra una decisión tuya.

---

## 15. Agent Hub: supervisar sin rediseñar

| Cómo abrirlo | Qué es | Estado de la afirmación |
|---|---|---|
| `Alt+A` | Abre o cierra el Agent Hub (`app.agents.hub`); abre el roster aunque esté vacío | **Verificado** — `omp://agent-hub.md` |
| `Ctrl+S` | El mismo Hub por la acción legacy `app.session.observe` | **Verificado** — `omp://agent-hub.md` |
| Doble toque `←` con el editor de la sesión principal vacío | Abre el Hub **cuando la sesión tiene algún agent que mostrar**. No es una acción de keybinding: enfocado en un subagent, el mismo gesto vuelve a la sesión principal en vez de abrir el Hub | **Verificado** — `omp://agent-hub.md` |
| `/agents` | Control Center por agent: modelo, prewalk, advisor | **Verificado** — `omp://advisor-watchdog.md`, `omp://settings.md` (`task.agentAdvisor`, `task.agentPrewalk`) |
| `/hub` | Agent Hub en vivo, sección Activity | Documentado previamente aquí; **no verificado** |

```
DOCUMENTADO_PREVIAMENTE != VERIFICADO_EN_RUNTIME
```

`omp/18.1.22` no expone una enumeración read-only de slash commands, y `omp://slash-command-internals.md` no los enumera. Lo verificable se verificó contra la documentación oficial de OMP; el resto se conserva porque ya estaba en este manual y es operativamente útil, marcado como tal. Hoy quedan **sin verificar**: `/hub`, `/plan-review`, y la forma exacta de invocación de `/plan`, `/goal`, `/guided-goal` y `/loop` — que los *modos* plan y goal existen sí está confirmado (`omp://vibe-mode.md` los declara mutuamente excluyentes con vibe mode). Si alguno no existe en tu versión, usa el atajo equivalente y corrige esta tabla en vez de asumir que el manual manda.

`/hotkeys` muestra los chords activos, y ambas acciones se remapean en `~/.omp/agent/keybindings.yml`.

El Hub muestra el roster de agents, su estado, modelo, actividad, uso y linaje de spawns, y permite abrir el transcript de un worker.

**Para qué lo usas:** confirmar que un worker sigue vivo y trabajando en lo que creías, detectar que se está yendo de alcance, y decidir si lo dejas terminar o lo paras.

**Para qué no lo usas:** supervisar no es rediseñar la tarea a mitad de ejecución. Si al mirar el Hub concluyes que el encargo estaba mal delimitado, la respuesta correcta es parar el worker y **volver a delimitar el contrato desde la Control Tower**, no ir añadiendo correcciones sobre la marcha a un trabajo que ya partió de un encargo equivocado.

---

## 16. Model routing sin pensar en modelos

El routing de modelos tiene dos mitades, y Apep Core sólo es dueño de una:

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Rol de modelo (`@default`, `@task`, `@slow`…) | Frontmatter `model:` de cada agent (`agents/*.md`) | Declara la **clase de cómputo** que el agent necesita |
| Resolución rol → modelo | `modelRoles` en el `config.yml` **del proyecto consumidor** | Decide qué modelo concreto sirve cada rol |
| Modelo explícito | Frontmatter `model:` de un agent | Fija un modelo concreto, independiente de los roles |

Apep Core no entrega `modelRoles` (un plugin no entrega settings, §23) ni afirma qué modelo corresponde a cada rol: eso es una elección de configuración de cada proyecto. Semántica de los roles que usa Core:

| Rol | Para qué |
|---|---|
| `default` | uso general |
| `plan` | planificación |
| `task` | ejecución de un contrato ya cerrado |
| `slow` | razonamiento abierto o difícil |
| `smol` | trabajo mecánico y tareas de fondo |

Routing de los agents (frontmatter de `agents/*.md`):

| Agent | `model:` declarado | Thinking |
|---|---|---|
| `diagnostics` | `@slow` | high |
| `architecture-review` | `@slow` | high |
| `governance-review` | modelo explícito | medium |
| `technical-discovery` | `@default` | medium |
| `implementation` | `@task` | medium |
| `delivery-orchestrator` | `@default` | high |

```
@default = DAILY DRIVER
@slow    = HARD / OPEN-ENDED REASONING
smol     = MECHANICAL WORK

MODEL SIZE FOLLOWS REASONING COMPLEXITY,
NOT BUSINESS IMPORTANCE.
```

El criterio es la complejidad del razonamiento, no la importancia del trabajo. Una auditoría de gobernanza importa mucho y no pide `@slow`, porque contrastar un diff contra reglas es verificación acotada, no razonamiento abierto.

**Rol o modelo explícito.** El rol se usa cuando la intención se comparte. El modelo explícito, cuando la coincidencia es circunstancial: `governance-review` declara un modelo concreto en su frontmatter para que un cambio futuro del rol `@task` (el de `implementation`) no lo arrastre.

**No existe un rol `@review`** (§24).

Para ti: delega a una capability y no elijas modelo. Cambiar el routing de los agents (su frontmatter) es un cambio material y se registra en [CHANGELOG.md](CHANGELOG.md); cambiar tu `modelRoles` es una decisión de configuración de tu proyecto.

---

## 17. Guía de capability: situación → qué usar

| Situación | Capability | Tipo |
|---|---|---|
| Necesidad vaga, todavía no sé qué quiero | Conversación en la Control Tower; `/skill:project-management` si hay proyecto real detrás | skill |
| Incertidumbre de abordaje, dependencias, paralelización | `/plan` | modo |
| Riesgo, viabilidad, cronograma, release readiness, cierre | `/skill:project-management` | skill |
| Un requisito nuevo o que cambia, su impacto, quién decide o acepta, una fecha o una estimación, un avance reportado ("vamos al 80%") | `/skill:project-management` (modo proyecto) | skill |
| Reconstruir `CURRENT_STATE`: "¿qué hace X realmente?" | `/skill:technical-discovery` o agent `technical-discovery` | skill + agent |
| Formalizar `TARGET_STATE` → Execution Contract, también desde una idea o un ticket todavía ambiguos | `/skill:specification` | skill |
| ¿Este cambio respeta boundaries y contratos? | `/skill:architecture-review` o agent `architecture-review` | skill + agent |
| ¿Qué tipo de trabajo es? ¿Está listo, y para qué? ¿De qué depende? ¿Hay que dividirlo? ¿Cuándo está Done? | `/skill:project-management` (modo work item) | skill |
| ¿En qué rama va este trabajo, desde qué base y hacia dónde? | `/skill:git-workflow` | skill |
| Preparar mensaje de commit, cuerpo de PR o propuesta de versión | `/skill:git-workflow` | skill |
| "Implementa X" de principio a fin, sin dirigir fase por fase | agent `delivery-orchestrator` | agent |
| Lifecycle completo pero conduciéndolo tú en conversación | `/skill:delivery-lifecycle` | skill |
| Escribir el cambio | agent `implementation` | agent |
| Algo falla y no sé por qué (pequeño, interactivo) | `/skill:diagnostics` | skill |
| Algo falla y no sé por qué (volumen, cruza fronteras) | agent `diagnostics` | agent |
| ¿Se respetó alcance, autorización y política de diseño? | agent `governance-review` | agent |
| ¿Lo implementado cumple lo que debía hacer? | `/skill:implementation-review` | skill |
| Revisar un PR / merge request, listar los abiertos o ejecutar el ciclo completo de uno o varios PRs | `/pr <PRs, repositorio o lote>` (work mode; carga `pr-review`; la mecánica remota la aporta el provider configurado) | command |
| ¿Este cambio introduce riesgo de seguridad? | `/skill:security-review` | skill |
| Barrido de vulnerabilidades sobre un repositorio completo | agent bundled `security-reviewer` | OMP |
| Corrección funcional general, sin metodología project-local | agent bundled `reviewer` | OMP |
| Calidad de código | `code-quality` — **siempre activa, no se invoca** | skill |

Otros modos de OMP (`/vibe`, `/goal`, `/guided-goal`, `/loop`) existen en la herramienta pero **no están incorporados a nuestro proceso**; no hay gobernanza local que defina cómo se usan aquí. Sobre cuáles de estas invocaciones están verificadas y cuáles sólo documentadas, ver §15.

---

## 18. Recetas operativas

Distingue siempre dos cosas:

- **CONTROL PROMPT** — lo que tú escribes para dirigir. Corto, humano, delimitador.
- **EXECUTION ARTIFACT** — lo que el proceso produce (Execution Contract, reporte de discovery, findings). Estructurado y largo. **No es tu prompt.**

El error más común es intentar escribir el artefacto en el prompt. Tu trabajo es delimitar; el artefacto lo produce la capability.

### Refinement

```
CONTROL PROMPT
/skill:project-management
Quiero reducir el tiempo de generación de informes. Todavía no sé si es
un problema de proceso o de infraestructura. Ayúdame a delimitar el frente
de trabajo: valor, incertidumbre, dependencias y qué haría falta investigar.
No decidas la solución.
```

### Especificar desde una necesidad todavía ambigua

```
CONTROL PROMPT
/skill:specification
Necesidad: "los clientes deberían poder pausar su suscripción en vez de
cancelarla". Todavía no sé cuánto dura la pausa ni qué pasa con el cobro.
Llévalo hasta EXECUTION_READY: investiga lo que se pueda verificar en el
repo, pregúntame sólo lo que tenga que decidir yo y registra mis respuestas.
Los artefactos van en specs/pausa-suscripcion/.
```

Recibes primero el intake y las preguntas materiales (`CLAR-NNN`), una a la vez cuando dependen entre sí. Lo que el sistema puede responder no te lo pregunta. Al final llegan el contrato 07 y su `READINESS_RESULT`; la ejecución sigue esperando tu autorización.

### Technical discovery

```
CONTROL PROMPT
Delega a technical-discovery: reconstruye cómo se genera hoy un informe en
<servicio>, desde el entry point hasta la persistencia del resultado.
Escala FLOW_DISCOVERY. Sólo CURRENT_STATE verificable: separa FACT de INFERENCE
y declara los UNKNOWN. No propongas cambios.
```

### Diagnóstico de un fallo observado

```
CONTROL PROMPT
Delega a diagnostics: el job <X> falló ayer a las 14:05 con <error observado>.
Escala TARGETED_DIAGNOSIS. Quiero la causa con evidencia, o MISSING_EVIDENCE
explícito. No apliques ningún fix, y no reinicies ni limpies nada que pueda
destruir evidencia.
```

### Architecture review

```
CONTROL PROMPT
Delega a architecture-review: evalúa si el cambio en <ruta> preserva las
fronteras y contratos aplicables. Escala TARGETED. Cada finding necesita
ARCHITECTURAL_BASIS — si no la hay, repórtalo como preferencia, no como
violación. No diseñes la arquitectura de reemplazo.
```

### Delegar implementación

```
CONTROL PROMPT
Delega a implementation con este contrato:

SCOPE: sólo <repo>/src/reports/renderer.py
RAMA: fix/<ID>/orden-secciones-pdf desde <rama base> (autorizado crearla y trabajar en ella)
DECISIONES CERRADAS: mantenemos la interfaz pública actual; sin dependencias nuevas
INVARIANTES: el formato de salida no cambia
AC: los tests existentes siguen verdes + el caso <X> deja de fallar

Lo que encuentres fuera de scope se reporta, no se corrige.
Prepara el mensaje de commit y el borrador de PR. No hagas commit ni push.
```

No hace falta añadir "ejecuta los tests": `implementation` verifica por defecto (§13). Sí hace falta decir la rama, o que la determine y te la proponga.

### Delegar un lifecycle completo

```
CONTROL PROMPT
Delega a delivery-orchestrator: implementa <ID> — validar el contexto de
acceso, repo <repo>/. Autorizada la work branch que proponga
desde <rama base>. Lleva el lifecycle hasta INTEGRATION_READY; para en cualquier
decisión reservada.
```

Vuelve con `LIFECYCLE_STATE`: o un gate que resolver (decisión, rama, ejecución) o el paquete de integración (evidencia, findings, `COMMIT_MESSAGE`, `PR_TITLE`, `PR_BODY`). Para continuar tras un gate, responde con la decisión y la Main Session reanuda al orchestrator. Commit, push y PR los ejecuta la Main Session si los autorizas.

### Responder a un `DECISION_REQUIRED`

```
CONTROL PROMPT
DECISION: opción B.
RAZÓN: preferimos el coste de migración ahora antes que arrastrar el contrato dual.
Esto cierra la decisión. Continúa con el BLOCKING_SCOPE que quedó bloqueado.
El resto del contrato no cambia.
```

### Reviews posteriores a la implementación

```
CONTROL PROMPT
Delega a governance-review el diff actual de <repo>/: audítalo contra la
gobernanza aplicable y el contrato que autorizamos. Sólo lectura.
Interesa especialmente si se tocó algo fuera de scope o sin autorización.
No corrijas nada.
```

### Revisar un PR y publicar comentarios

```
CONTROL PROMPT
/pr Revisa el PR <id> del repositorio <repo>. Quiero saber si el diff hace lo que
el PR declara y si hay algo que bloquee. Muéstrame los comentarios propuestos
antes de publicar nada.

--- después de leerlos ---

Publica los comentarios 1 y 3 tal cual. El 2 no.
```

### Ciclo completo de un lote de PRs

```
CONTROL PROMPT
/pr Ciclo completo sobre los PR abiertos de <repo> con destino <rama>
(enumera el conjunto antes de empezar). Autorizo: publicar comentarios,
aprobar, mergear los elegibles, sincronizar los que sólo estén
desactualizados (si el provider lo soporta), avisar a los autores con
MUST_FIX y mandar el reporte ejecutivo. No toques los que tengan "NO MERGE".
```

Esperado: un `AUTHORIZED_SET` enumerado al principio, ninguna repregunta por PR y, al final, la tabla de cinco columnas más, si el provider lo soporta, un único aviso ejecutivo. Lo que el provider deje esperando (p. ej. un approval externo) se retoma en la siguiente ejecución.

Fíjate en el patrón: cada prompt **delimita** (qué, dónde, a qué escala) y **cierra puertas** (no decidas, no propongas, no corrijas, no commit). Eso es conducir.

---

## 19. STOP y decisiones

### Cuándo debe detenerse un agent

Un agent para y te devuelve evidencia + decisión — **nunca amplía alcance en silencio para resolverlo solo** — cuando encuentra:

- **contradicción entre fuentes autoritativas** (gobernanza, contrato, specification, código);
- **una decisión ya cerrada que contradice un hecho verificado** → `DECISION_CONTRADICTION`;
- **un cambio fuera de scope que parece necesario** para completar el trabajo;
- **una decisión arquitectónica nueva** que habría que tomar;
- **una dependencia no satisfecha** o no autorizada;
- **evidencia insuficiente** para afirmar éxito o causa → `INSUFFICIENT_EVIDENCE` con `MISSING_EVIDENCE`;
- **una operación destructiva o no autorizada** en el camino;
- **una mutación remota no autorizada** (Git de escritura, cloud o remota, estado de un PR).

Parar así **no es un fallo del agente: es el comportamiento correcto.** La alternativa —improvisar una salida— es lo que la gobernanza prohíbe.

### `implementation`: qué lo detiene y qué no

| No detiene el trabajo — es el ciclo normal | Detiene y escala |
|---|---|
| Un test que falla por el propio cambio, dentro del scope | Decisión reservada a autoridad humana |
| Formatter o linter con hallazgos | Contradicción con el contrato o con una decisión cerrada |
| Un build roto corregible dentro del scope | Cambio de alcance necesario |
| Un detalle táctico de implementación | Dependencia no autorizada |
| | Cambio material de arquitectura, API, schema, persistencia o contrato |
| | Fallo preexistente que impide determinar la aceptación |
| | Verificación materialmente imposible (entorno, credencial, servicio) |

### Cuatro artefactos que el harness nunca fusiona

Reconocer cuál te llegó determina qué tienes que hacer.

| Te llega | Significa | Qué haces |
|---|---|---|
| `DECISION_REQUIRED` | Hay una decisión humana pendiente | Eliges opción, o pides más evidencia. Mira `BLOCKING_SCOPE`: parte del trabajo puede seguir |
| `STOP_REPORT` | Parada por otra causa (riesgo, ambigüedad, falta de autorización) | Lee `RECOVERY_CONDITION`: dice qué tendría que ser verdad o decidirse para levantar la parada |
| `DECISION_CONTRADICTION` | Una decisión **tuya ya cerrada** contradice un hecho verificado | Tu decisión no puede vencer a un hecho externo. Redecide sobre la realidad |
| Dependencia fuera de alcance | Algo no autorizado impide hacerlo bien | Amplías alcance/autorización explícitamente, o aceptas entrega `PARTIAL` |

Reglas que te afectan directamente:

- Una `RECOMMENDATION` nunca se ejecuta sola. Requiere que tú la conviertas en `DECISION`.
- Tu silencio no cierra nada. Si no respondes, sigue bloqueado.

---

## 20. Git workflow, commits, PRs y versionado

Dos fuentes, con papeles distintos:

| Fuente | Qué fija | Estado |
|---|---|---|
| `RULES.md` reglas 13 y 18 | **Autoridad**: qué operaciones Git requieren autorización, baseline por repo, preservar trabajo ajeno | Normativa |
| `/skill:git-workflow` | **Intención**: cómo determinar la rama esperada y cómo preparar commit, PR y versión | Modelo genérico: el repositorio declara su modelo de ramas |

```
THE REPOSITORY DECLARES ITS BRANCH MODEL.
APPROVAL POLICY DEFINES AUTHORITY.
BRANCH INTENT != AUTHORIZATION TO MUTATE GIT.
```

Apep Core **no declara un GitFlow ni nombres de ramas permanentes**: branch naming, commits, PRs, releases, tags, versionado y hotfix son `REPOSITORY GOVERNANCE` (regla 18). La skill establece su aplicabilidad repositorio por repositorio, con evidencia (`POLICY_APPLICABILITY`: `REPOSITORY_DECLARED` · `HUMAN_DECIDED` · `STRUCTURAL_EVIDENCE` · `UNVERIFIED`; `git-workflow` §1). `UNVERIFIED` es un resultado válido, no un error: no se asume ninguna rama protegida, de integración ni de release, y toda determinación que lleve a una operación Git se presenta como `PROPOSAL`. Si el repo define otra cosa, manda el repo. Un plugin de organización puede componer un overlay con su modelo de ramas concreto (§1, *Composición*).

### Disciplina básica (`RULES.md` 13, 18)

- **Baseline por repositorio** antes de tocar: branch, HEAD, `git status`. Si el workspace agrupa varios repositorios, su raíz no es un repo Git.
- **Nunca mezclar repositorios**: ni baseline, ni diffs, ni políticas.
- **Trabajo preexistente intocable**: nada de `restore`, `checkout --`, `reset`, `clean` ni stash sobre lo que el agente no creó. Si estorba, `STOP_REPORT`.
- **Una intención por modificación**, en el diff y en el commit.
- **Diff antes de `COMPLETE`**, inspeccionado con Git, nunca de memoria (§21).

### Ramas

El **patrón** de las ramas de trabajo es genérico; la base y el destino salen de la gobernanza del repositorio (`git-workflow` §2):

```
feature/<ID>/<titulo> ─┐
fix/<ID>/<titulo>     ─┼─ base y PR hacia: lo que declare el repositorio
bugfix/<ID>/<titulo>  ─┘

hotfix/<ID>/<titulo>:    urgencia en producción; base, destino y back-sync: lo que declare el repositorio
```

- **Las ramas permanentes (integración, estabilización, producción) son las que la gobernanza del repositorio declara.** Apep Core no las enumera ni asume una por convención «habitual».
- **`fix/*` y `bugfix/*` son alias funcionales**: misma base, mismo destino, mismo flujo, salvo que el repositorio declare una diferencia.
- **Si el repositorio no declara un modelo de ramas**, el resultado es `BRANCH_STATUS: UNKNOWN`: el agente reporta la divergencia o la ausencia y pide confirmación para todo lo que dependa de la rama; no la normaliza en silencio.
- **Nunca se implementa "en la rama en la que esté".** Antes de escribir, `BRANCH_PREFLIGHT`: rama actual, base esperada, work branch esperada, destino del PR, `BRANCH_STATUS`.

### Autoridad Git

| Operación | Agente |
|---|---|
| Git de lectura (`status`, `diff`, `log`, `branch -r`, `ls-remote`, `fetch`…) | Autónomo |
| Preparar nombre de rama, mensaje de commit, PR, propuesta de versión | Autónomo |
| Crear / cambiar a la work branch | Requiere autorización (contrato o tú) |
| `commit`, `push`, `merge`, `rebase`, `tag`, publicar PR | Requiere autorización |

Crear rama y `switch` **no abren diálogo** en la capa de herramienta. Su gate es de política (`POLICY_PERMITS != TOOL_LAYER_AUTO_APPROVES`), y por eso se autorizan en el contrato (`AUTHORIZED_DECISIONS`). `commit`, `push`, `merge`, `rebase` y `tag` sí abren diálogo en la Main Session y **se rechazan dentro de un agent** (§13): un commit autorizado lo ejecuta la Main Session. Si quieres un commit, pídelo: por defecto no lo habrá.

### Commit

```
<tipo>(<componente-opcional>): <descripción breve en español>
```

- Tipos: `feat` · `fix` · `refactor` · `docs` · `style` · `test` · `perf` · `ci` · `chore`.
- Español, imperativo, ≤ 72 caracteres, sin punto final; una intención; commit atómico.
- Cuerpo, cuando el encabezado no basta: `Historia` · `Qué resuelve` · `Cómo probarlo` · `Notas adicionales` · `Migraciones` · `Impacto`.
- `Historia` enlaza la historia cuando existe. Sin historia formal, el campo se omite: **nunca se inventa un ticket**.

Detalle: `skill://git-workflow/references/commit-message.md`.

### Pull Request

**Título** `<tipo>(<componente-opcional>): <descripción breve en español>`:
- mismos tipos que en commits; expresa intención; sin punto final; nada de títulos genéricos;
- **sin ID de ticket**: el título identifica la intención; el cuerpo contiene la trazabilidad y la evidencia.

```
feat(auth): agregar validación del contexto de acceso
fix(informes): manejar corpus vacío antes de generar el reporte
```

**Cuerpo**: `Identificación` · `Problema / Necesidad` · `¿Qué resuelve?` · `Cómo probarlo` · `Alcance del cambio` · `Enfoque técnico` · `Migraciones / DB` · `Impacto y riesgos` · `Checklist mínimo` · `Notas / Comentarios adicionales`.

| Regla | Detalle |
|---|---|
| Tres preguntas | ¿Qué problema resuelve? · ¿Cómo se resuelve? · ¿Cómo se prueba? |
| Una intención | Nada de feature + refactor masivo, historias no relacionadas o cambios oportunistas |
| Sin ceremonia | Lo que no aplica: `N/A` + razón breve |
| Cómo probarlo | Sólo comandos realmente ejecutados, con resultado |
| Sin ticket | Nunca un ID inventado: justificación explícita **y** enlace al documento que justifica la excepción |

`PREPARAR UN PR != AUTORIDAD PARA PUBLICARLO.` Detalle: `skill://git-workflow/references/pull-request.md`. Revisar un PR ya publicado es `pr-review` (§12.5).

### Versionado

`vMAJOR.MINOR.PATCH`:
- `MAJOR`: rompe un contrato público.
- `MINOR`: funcionalidad compatible.
- `PATCH`: correcciones o cambios internos compatibles.

Dónde van los tags finales y las pre-releases (`vX.Y.Z-rc.N`) lo declara la gobernanza del repositorio: qué ramas designa como de release.

| Agente | Responsable técnico del release (Tech Lead / Head de Desarrollo / equivalente) |
|---|---|
| Analiza, **propone** y explica una versión | **Decide** `MAJOR` / `MINOR` / `PATCH` |

Crear o publicar el tag sigue el gate Git. Detalle: `skill://git-workflow/references/versioning.md`.

---

## 21. Qué significa COMPLETE aquí

`COMPLETE` **no** es "los tests están en verde". Dos usos que no se confunden: `RESULT: COMPLETE` en el reporte de un worker (`ENGINEERING_GOVERNANCE.md` §13) significa *trabajo del contrato terminado con evidencia*; el estado `COMPLETE` del lifecycle es la **declaración humana**, posterior a `INTEGRATION_READY` (§5). Un test que pasa sin verificar el comportamiento correcto sólo prueba que el test pasa (`RULES.md` regla 12).

Para declarar `COMPLETE` se verifica, según aplique: comportamiento requerido · invariantes · contratos · tests · lint y tipos · integración con patrones existentes · **el diff completo** · archivos modificados inesperadamente · cambios de configuración · regresiones previsibles en áreas relacionadas. Más la revisión de diff de `code-quality` (`RULES.md` regla 17), y la inspección del cambio efectivo con Git/filesystem — nunca de memoria (regla 18).

Y la entrega llega con evidencia estructurada: `RESULT` · `BASELINE` · `FACTS` · `DECISIONS_USED` · `IMPLEMENTED` · `FILES_MODIFIED` · `TESTS` · `VERIFICATION` · `DEVIATIONS` · `DISCOVERED_DEBT` · `RISKS` · `DECISIONS_REQUIRED` · `NEXT_ACTION`.

`FACTS` contiene sólo lo verificado directamente. Una inferencia nunca va en `FACTS`.

Y `COMPLETE` de una implementación no es aprobación de correctness, de seguridad, de arquitectura, de gobernanza ni de merge: cada una de esas es su propia capability (§12).

**`COMPLETE` es una afirmación sostenida con evidencia, y quien la acepta eres tú.**

---

## 22. Anti-patrones

| Anti-patrón | Por qué rompe el proceso |
|---|---|
| Usar `/plan` para reabrir un Execution Contract ya autorizado | Invita al agente a reconsiderar decisiones que ya cerraste (`RULES.md` 1 y 2). Se reabre por evidencia nueva o decisión tuya, no por planificar otra vez |
| Rehacer discovery sobre un contrato ya aprobado | El CURRENT_STATE relevante ya se estableció; reinvestigar reabre lo cerrado y consume contexto (§8) |
| Pedir a `implementation` que haga discovery amplio | No es su responsabilidad ni su metodología. Para eso está `technical-discovery`, que además es read-only |
| Lanzar `diagnostics` sin fallo observado | Diagnostics parte de un síntoma real. Sin él, la pregunta es "¿cómo funciona?" y la capability correcta es `technical-discovery` |
| Tratar un finding de review como autorización para corregirlo | `REVIEW_FINDING != AUTHORIZATION_TO_FIX`. La corrección entra por su propio contrato |
| Pedir a `pr-review` que resuelva cualquier conflicto que detectó | Un conflicto es un bloqueo operativo que se reporta. Sólo una capability de sincronización mecánica del provider, expresamente autorizada (`SYNC_REMEDIATION`), cuando la desincronización es el único blocker y los conflictos son mecánicos, puede tocar ramas. Un conflicto funcional es `DECISION_REQUIRED` (§12.5) |
| Esperar que el ciclo apruebe un PR propio, o un PR auxiliar que él mismo creó | `SELF_APPROVAL_NOT_ALLOWED`: queda esperando approval externo; nunca cambia de identidad (§12.5) |
| Asumir que autorizar comentarios autoriza aprobar o mergear | Cada acción se autoriza por separado: `COMMENT != APPROVAL != MERGE != SYNC_REMEDIATION AUTHORIZATION` (§12.5) |
| Asumir que `OUTCOME: APPROVE` o `mergeable: true` ya autorizan la acción | `pr-review` las ofrece en `ACTIONS_AVAILABLE`; sin tu autorización explícita no muta nada |
| Reusar una autorización de approve/merge después de un nuevo push al PR | Drift: la autorización corresponde a la revision que viste (`REAUTHORIZATION_REQUIRED`) |
| Esperar que la skill te pida confirmar cada PR de un lote ya autorizado | Una autorización cubre el conjunto; la skill revalida y ejecuta cada PR elegible y omite los bloqueados (§12.5) |
| Asumir que autorizar un lote autoriza saltarse un *"NO MERGE hasta …"* | `MERGE_AUTHORIZATION != BLOCKER_OVERRIDE_AUTHORIZATION`: el override se autoriza por separado y nombrándolo |
| Repetir la revisión integral de un PR después de sincronizarlo, sin evidencia nueva | `SYNC_REVALIDATION != FULL_REVIEW_RESTART`: se revisa el delta de sync y se revalidan los findings (§12.5) |
| Asumir una rama de destino al sincronizar | La destination sale siempre del PR real |
| Inferir el correo del autor a partir de su usuario, nombre o commits | Sólo una fuente verificada del provider; sin entrada, `AUTHOR_NOTIFICATION: NOT_CONFIGURED` |
| Reenviar la misma notificación en un reintento | `RETRY != DUPLICATE SIDE EFFECT`: misma clave `PR + revision + outcome + tipo` → `DUPLICATE_SKIPPED` |
| Detener todo el lote porque un PR está bloqueado | `ONE BLOCKED PR != STOP WHOLE BATCH`: sólo una condición transversal detiene el lote |
| Declarar una notificación como entregada porque el servicio de envío la aceptó | `NOTIFICATION_ACCEPTED != DELIVERY_CONFIRMED` |
| Reutilizar una autorización sobre una revision nueva sin revalidar | Drift: se revisa la revision nueva (el delta) antes de cualquier mutación |
| Ampliar `AUTHORIZED_SET` con PRs aparecidos durante el ciclo | El conjunto se enumera y se fija al empezar; un PR nuevo entra sólo con una autorización nueva |
| Mandar el Goal completo a cada worker | Un worker sin contrato delimitado decide por su cuenta dónde empiezan y acaban sus fronteras — justo lo que el harness evita |
| Convertir `architecture-review` en architecture-design | Tiene prohibido inventar la arquitectura de reemplazo. La cadena es `finding → decisión humana → specification → implementation` |
| Asumir tests verdes = runtime correcto | Anti-supuesto explícito de la gobernanza. Tests verdes es evidencia necesaria, no suficiente |
| Dejar que un worker expanda alcance "ya que estaba ahí" | `IN_SCOPE` no equivale a `CHANGE_AUTHORIZATION`. La calidad del código no autoriza scope creep |
| Arrancar OMP desde un subrepositorio | Una sesión iniciada dentro de un repo hijo no recibe el `.omp/` del workspace padre: pierdes config, contexto, skills y agents del proyecto sin que nada te avise (§2) |
| Crear un `.omp/` local en un repo hijo para "arreglar" lo anterior | Es un cambio de configuración durable: requiere decisión humana explícita; no es una corrección que el agente pueda tomar (`RULES.md` 1). Si tu organización lo gobierna, lo define su plugin de organización |
| Entrar en un repositorio sin leer su archivo de autoridad local designado | Es gobernanza de repositorio: se lee completo al entrar, según el protocolo de entrada de tu `AGENTS.md` (`docs/agents-md-template.md`) |
| Pedir "arregla todo lo que veas mal" | Convierte hallazgos en modificaciones sin autorización. Lo correcto: que los reporte clasificados, y tú decides |
| Implementar "en la rama en la que esté" | Mezcla intenciones o escribe sobre una rama permanente. Primero `BRANCH_PREFLIGHT` (§20) |
| Que `implementation` pregunte "¿ejecuto los tests?" | La verificación local aplicable es parte de implementar (§13), no una decisión tuya |
| Debilitar un test para que pase | Destruye evidencia. Sólo se ajusta un test cuyo comportamiento el contrato cambia explícitamente |
| Usar `eval` para hacer lo que `bash` habría preguntado | Es eludir un gate (§23), aunque la herramienta no pregunte |
| Pedir al agente que "elija la versión" del release | La propone; la decide el responsable técnico del release (§20) |

---

## 23. Autonomía operacional y approvals

### Dos capas distintas

```
POLICY_PERMITS  !=  TOOL_LAYER_AUTO_APPROVES
```

| Capa | Qué decide | Dónde vive |
|---|---|---|
| **Política** | Si el agente *debe* hacer algo o detenerse a preguntarte | `ENGINEERING_GOVERNANCE.md`, `RULES.md`, Execution Contract, skills y agents |
| **Permisos** | Si la herramienta *ejecuta* sin abrir un diálogo | `config.yml` **del proyecto consumidor** (`approvalMode`, `tools.approval`, `bash.patterns`) |

Que una herramienta no pregunte no autoriza la operación. Que la política la permita no garantiza que la herramienta no pregunte. Ante un diálogo en algo que la política permite, el agente no busca una vía menos observable: lo reporta y espera (`ENGINEERING_GOVERNANCE.md` §17.8).

```
LOCAL IMPLEMENTATION EXECUTION       → autónoma
MATERIAL / SHARED / DESTRUCTIVE      → gates explícitos, donde la herramienta los admite
```

### Lo que Apep Core entrega y lo que no

Un plugin de OMP **no puede aportar settings** (`config.yml`, `bash.patterns`, política de approvals) **ni archivos de contexto cargados siempre** (`AGENTS.md`). Apep Core no entrega ningún equivalente funcional de eso. Entrega, en su lugar:

- [`docs/recommended-approval-patterns.md`](docs/recommended-approval-patterns.md): qué poner en tu propio `config.yml`;
- [`docs/agents-md-template.md`](docs/agents-md-template.md): una plantilla para tu propio `.omp/AGENTS.md`.

Consecuencia: la capa de permisos es del proyecto consumidor, y lo que este manual diga de ella describe cómo funciona el runtime y el patrón recomendado, no una configuración vigente que Core garantice. La frontera de autoridad no depende de ella: la sostiene la capa semántica (§1, *Modelo de enforcement*).

### Claves de configuración relevantes (hechos del runtime, omp/18.2.11)

| Clave | Qué controla |
|---|---|
| `tools.approvalMode` | `write`: lectura y escritura de archivos (`edit`, `write`, `ast_edit`, `lsp`) sin prompt; el tier `exec` conserva su gate salvo política explícita. `yolo` es el default de OMP y auto-aprueba todo; `always-ask` pregunta siempre |
| `tools.approval.bash` | Política por defecto de `bash`; `bash.patterns` añade gates por patrón |
| `tools.approval.eval` | Política de `eval`, global, sin granularidad por llamada |
| `tools.approval.browser` | Llamadas a la prelude `browser` dentro de una celda de `eval`. **No** la cubre `eval: allow` |
| `tools.approval.task` | Delegar en workers: `TASK AUTONOMY != DECISION AUTONOMY`. Sólo delegan los agents que declaran `spawns`; profundidad máx. 2 |
| `bash.allowCompoundCommands` | Con `true`, las cadenas planas de `&&` se resuelven segmento a segmento |

Un proyecto que adopta la autonomía operacional descrita aquí configura `approvalMode: write`, deja `bash` autónomo por defecto y protege los efectos materiales con `bash.patterns`; si además deja `eval`, `browser` y `task` en `allow`, el harness pasa a ser la única frontera de esas superficies (ver *`eval` y `browser`*). Es una decisión de ese proyecto. **Esto no es `yolo`.** Fuera del session root rige la config global (§2).

### Observación autónoma (`RULES.md` 19, `ENGINEERING_GOVERNANCE.md` §17)

Una tarea observacional autorizada —discovery, specification, revalidación, reproducción, recopilación de evidencia— corre hasta su resultado. **Lo que autorizas es el objetivo, no cada operación.** Sincroniza por evento material: decisión pendiente, operación fuera del envelope, efecto material no autorizado, acción destructiva, credencial ausente, contradicción con una decisión cerrada, ampliación de alcance, bloqueo o resultado final. El envelope no autoriza editar código, Git de escritura, mutar datos fuera del fixture de prueba, tocar cloud/infra/identidad ni leer secretos.

### Implementación autorizada

```
█ HUMAN GATE █ → Execution Contract aprobado → writes en scope sin confirmación por archivo
                                               → operaciones materiales conservan su gate

APPROVE THE IMPLEMENTATION, NOT EVERY KEYSTROKE.
IMPLEMENTATION_AUTHORIZED != UNBOUNDED_AUTHORITY.
```

### `bash`: default allow + gates materiales (patrón recomendado)

El patrón completo y su razonamiento están en [`docs/recommended-approval-patterns.md`](docs/recommended-approval-patterns.md); aquí, el resumen operativo.

| Tier de comandos VCS | Ejemplos | Política sugerida |
|---|---|---|
| Sólo lectura | `status`, `log`, `diff`, `show`, `branch --list`, `blame` | allow |
| Destructivo local | `reset --hard`, `clean`, `checkout -- <path>`, `restore`, `stash drop`, `branch -D` | confirmar |
| Publicación / reescritura de historia | `commit`, `push`, `push --force`, `rebase`, `merge`, `tag`, `cherry-pick`, `revert`, `commit --amend` | confirmar |

**Orden: gana la primera coincidencia.** Los `bash.patterns` se evalúan en orden y el primero que coincide decide. Los patrones específicos de `confirm`/`deny` van **antes** de cualquier catch-all `allow`: un catch-all `allow` colocado primero deja muertas silenciosamente todas las reglas más estrictas que le siguen. Los catch-alls van al final.

**Típicamente sin prompt** en un proyecto que adopta autonomía local: navegación e inspección; tests, lint, type-check, build y coverage; formatters; scripts locales y targets de `make` / `npm` / `pnpm`; preparación local de dependencias (`npm ci`, `uv sync`…); Docker local; borrado de outputs regenerables; Git de lectura y Git local no publicado; `gh` de lectura; y cualquier comando sin gate.

**Gate (pregunta)**, por familia:

| Familia | Ejemplos |
|---|---|
| Git: index, historia o estado compartido | `commit`, `push`, `pull`, `merge`, `rebase`, `reset`, `clean`, `restore`, `cherry-pick`, `revert`, `tag`, `am`, `mv`, `rm`, mutación de refs; `git apply` con `--index`/`--cached`; borrar ramas o stashes; `checkout`/`switch` que descartan cambios. `WORKING TREE AUTONOMY != INDEX/HISTORY AUTONOMY` |
| Cloud / IaC | Por defecto, confirmación para cualquier CLI de proveedor cloud o plataforma remota; sólo las lecturas claramente de introspección (`get-*`, `list-*`, `describe-*`) quedan autónomas, y los verbos mutantes (`create`, `update`, `delete`, `put`, `merge`, `approve`, `send`) quedan con gate |
| Secretos, credenciales e identidad | Gate aunque la API sea de lectura: `READ-ONLY != SECRET-SAFE` (`RULES.md` 19) |
| Datos | Migraciones, seeders, SQL destructivo |
| Dependencias y publicación | Mutar el manifiesto (`add`/`remove`/`update`/`lock`, `npm install <paquete>`); instalación global o de sistema; `publish`, `docker push`/`login`; scripts `deploy`/`release`/`publish` |
| Plataforma remota (`gh` mutante) | `pr create|merge|…`, `issue create|…`, `release create|…`, `repo …`, `workflow run`, `gh api` con método/cuerpo |
| Filesystem / host | Borrado recursivo, `find -delete|-exec`, `dd`, `mkfs`, `chmod|chown -R`, `sudo`, servicios del host, fetch-then-execute |
| Docker destructivo / remoto | `rm`, `rmi`, `kill`, `prune`, `compose down -v`, `-H`/`--context` |

Si tu organización usa un proveedor cloud o de control de versiones específico, añade sus patrones concretos a tu propio `config.yml`; ni este manual ni Apep Core los definen por ti.

#### PR review: observación y lifecycle autorizado, autónomos

```
PR REVIEW OBSERVATION                → AUTONOMOUS
AUTHORIZED PR LIFECYCLE              → NO REPETITIVE TOOL APPROVALS
OPERACIONES FUERA DE ESE LIFECYCLE   → GATE
AUTHORIZE THE EFFECT, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.
```

Tu autorización ocurre **una vez**, al definir el lote: `AUTHORIZED_SET` y `AUTHORIZED_ACTIONS` (`pr-review` §11.5, §11.9, §19.2). Cómo se traduce eso a la capa de permisos —qué operaciones del provider son lecturas de observación, cuáles pertenecen al lifecycle autorizado y cuáles conservan su gate (revocar approvals, override o edición de approval rules, cerrar o editar un PR, resolver conflictos con estrategias del merge, administración del repositorio)— es **del provider configurado y de tu `config.yml`**: Apep Core fija la doctrina y el plugin del provider clasifica sus propias operaciones. Que la herramienta no pregunte no amplía la autoridad: sin la acción en `AUTHORIZED_ACTIONS` el agente no la ejecuta. Vuelves a aparecer ante `DECISION_REQUIRED`, `DECISION_CONTRADICTION`, `INSUFFICIENT_EVIDENCE`, ampliación de alcance, problema de credenciales, o una operación del provider fuera del lifecycle o en forma no canónica.

**Formas de invocación que evitan prompts falsos** (`pr-review` §4.0):

- Las lecturas remotas son llamadas de herramienta simples y discretas, una por repositorio o PR, con la iteración hecha desde el agente: no las envuelvas en bucles, pipes, sustituciones de comandos ni scripts compuestos, porque una cadena compuesta puede alcanzar un gate que la llamada simple no alcanza.
- Usa el parámetro `cwd` de la tool `bash` para operar en un repo hijo, no `cd <repo> && …`, ni opciones globales de Git como `-C`. Con `cd`, ninguna excepción `allow` aplica; con `cwd`, el gate se evalúa sobre el comando real.
- No reescribas una operación para eludir un gate (`ENGINEERING_GOVERNANCE.md` §17.8): si pregunta, se reporta y se continúa cuando se apruebe.

#### Comandos compuestos: semántica efectiva (omp/18.2.11)

Con `bash.allowCompoundCommands: true`, **un comando compuesto no implica `prompt` por sí mismo**. Una cadena plana de `&&` con argumentos literales se evalúa contra la cadena completa y contra cada segmento:

| Situación | Resultado |
|---|---|
| Algún segmento, o la cadena completa, coincide con un `deny` | `deny` gana siempre |
| Algún segmento, o la cadena completa, coincide con un `prompt` (en cualquier posición) | `prompt` gana sobre los allows |
| Todos los segmentos coinciden con un `allow` de patrón | Auto-aprobada con tier `write`, sin depender de la policy global |
| Algún segmento sin clasificación específica | Cae a la policy global (`tools.approval.bash: allow` → no pregunta; sin ella, el modo `write` preguntaría) |

No califican para la vía por segmentos `;`, `||`, `|`, redirecciones, `$()`, asignaciones, control de flujo, newlines y builtins que cambian el estado del shell como `cd`. En esas formas los allows de patrón se ignoran, pero los gates se siguen evaluando sobre la cadena completa y sobre cada segmento, y si ningún gate coincide aplica la policy global. Son limitaciones reales, no una prohibición: con `bash: allow` esas formas no preguntan si no alcanzan un gate.

**Avisos para quien escribe patrones:**
- Una cadena `&&` plana resuelve cada segmento por separado, pero un gate que coincide con la cadena completa y con ningún segmento (veto de cadena) sí pregunta; por eso conviene enumerar los gates por el primer carácter del operando en lugar de usar un `install *` amplio.
- Los gates por nombre (`make deploy`, `npm run release`) son heurísticos: un script con otro nombre puede desplegar. Que no pregunte no lo autoriza; añadir una dependencia sigue siendo decisión de `ENGINEERING_GOVERNANCE.md` §1.2 aunque la herramienta no pregunte.
- La mutación de Git y de `gh` se **enumera**, sin catch-all: un subcomando nuevo no listado queda auto-aprobado y la lista hay que mantenerla. Lo mismo vale para cualquier CLI de proveedor.
- Enumera `git merge` con sus variantes mutantes sin atrapar `merge-base`, que es lectura.
- Ningún espejo `git -* <subcomando>` puede ser `allow`: el `-*` no está anclado y un `allow` así aprueba mutaciones.

### `eval` y `browser`

`browser` no es una herramienta registrada: es una prelude de `eval` (sólo existe con `eval` y `browser.enabled` habilitados). Pero **sí tiene approval propio**: cada llamada (`browser.open`, `tab.*`) se resuelve dentro de la celda con la clave `tools.approval.browser` y tier `exec` declarado (`eval/preludes.ts`, verificado en omp/18.2.11). Hay dos gates en serie:

1. la celda de `eval` → `tools.approval.eval`;
2. cada llamada a `browser` dentro de la celda → `tools.approval.browser`.

`eval: allow` no cubre el segundo: sin `browser: allow`, bajo `write` cada llamada pregunta *"Allow tool: browser"*. Con ambos en `allow` el browser es autónomo. `eval` declara tier `exec` fijo, sin clasificación por llamada: leer el DOM y borrar archivos son, para la capa de permisos, la misma operación. Quien configura la autonomía de `eval` lo hace sabiendo eso.

```
BASH MATERIAL GATES != EVAL MATERIAL GATES
```

| Superficie | Autonomía | Qué protege los efectos materiales |
|---|---|---|
| `bash` | por defecto | `bash.patterns` (mecánico) + harness |
| `eval` / `browser` | completa, a nivel de tool | **sólo** el harness: governance, `RULES.md`, Execution Contract, contratos de skills/agents |
| `task` | autónomo | harness: contrato, `spawns` por agent, profundidad 2 |

- Los gates de `bash.patterns` **no se aplican** a lo que se ejecute vía `eval` (`omp://approval-mode.md`).
- `eval` expone `agent()` / `workpool()`, que lanzan subagentes; la delegación normal es `task`.
- Ejecutar por `eval` lo que `bash` habría preguntado **es eludir un gate** (`ENGINEERING_GOVERNANCE.md` §17.8) y no queda autorizado porque la herramienta no pregunte.

Para reproducción por browser: delimita el fixture de prueba por adelantado (`TEST_SCOPE_MUTATION`, `ENGINEERING_GOVERNANCE.md` §17.4), usa una pestaña dedicada (las sesiones son reales y con tu login) y pide el reporte al final, no confirmaciones intermedias.

### Límites de la capa de permisos

- **Git con opciones globales.** `bash.patterns` es glob textual, no parsing semántico de Git. Las formas con opciones globales (`-C`, `-c`, `--git-dir`, `--work-tree`…) deben recibir la misma clasificación que la forma normal: decide el subcomando, no la opción. Un patrón que las ignore deja pasar mutaciones, y uno que las espeje tiene falsos positivos asumidos en lecturas (`git -C x tag -l`); con el parámetro `cwd` no hace falta `-C`.
- Bajo default-allow, un intérprete evade cualquier gate anclado: `bash -c "rm -rf x"`, `python3 -c …`. `bash.patterns` protege frente al accidente, no frente a la intención; no es un sandbox.
- Un `allow` de patrón no aplica si el comando contiene, fuera de comillas, `\n \r ; & | < > \` $ ( )`. Con el allow global eso no produce prompt; sólo pierde las excepciones. Los gates sí se evalúan sobre la cadena completa y sobre cada segmento.
- El critical override interno de OMP (`rm -rf /`, fork bomb, `curl | sh`) conserva su prompt siempre.

### Regresión de approvals

`tests/approvals/run.sh` resuelve la matriz mínima y genérica de `cases.ts` (lectura de archivos, Git de lectura libre, escritura de historia o estado compartido, borrado destructivo y los gates del worktree de ejecución) con el resolutor de approvals del OMP instalado y la config efectiva del session root del proyecto que la ejecuta (`APEP_TEST_WORKSPACE`, por defecto el directorio actual). Presupone que ese proyecto declara el patrón recomendado. **No ejecuta ningún comando ni tool y no llama al modelo**: una extensión de un solo uso imprime el informe y termina en `session_start`. Exit `0` = todo PASS, `1` = algún FAIL, `2` = error del harness. Ejecútala tras actualizar OMP o tocar `config.yml`; un FAIL es drift entre runtime, config y esta documentación. Añade un caso por cada gate o excepción nueva de tu propio patrón.

---

## 24. Limitaciones conocidas y capacidades que no existen

### Limitaciones vigentes

| Limitación | Consecuencia operativa |
|---|---|
| OMP 18.2.11 lee settings sólo de `<cwd>/.omp/`, sin buscar en ancestros | La config, el contexto, las skills y los agents del proyecto dependen del lanzamiento canónico (§2). No hay enforcement técnico |
| `omp plugin link` no superficia en omp/18.2.11 las skills, agents, commands ni reglas del paquete enlazado | Se activan con `extensions:` en `config.yml` (§2, *Activación de Apep Core*). Es una limitación de runtime, no un rodeo de Apep Core |
| Apep Core no entrega ningún provider de PR | `pr-review` es el contrato genérico; la mecánica remota (CodeCommit, GitHub, GitLab…) la aporta un plugin de organización (§12.5). Sin provider, no hay mutaciones remotas |
| Apep Core no entrega settings ni `AGENTS.md` | Un plugin no puede aportarlos: la política de approvals y el contexto del workspace son del proyecto consumidor (§23, `docs/`) |
| `browser` no es separable de `eval` | Su approval propio (`tools.approval.browser`) sólo rige las llamadas dentro de una celda; la celda sigue necesitando `eval: allow`. Un browser autónomo exige `eval` autónomo (§23) |
| `tools.approval.browser` es la clave de una prelude, no de una tool registrada | `omp config` la acepta sin validar el nombre; una regresión sobre tu propia config es lo que detecta si una versión de OMP cambia esa clave |
| Gates de Git: prefijos que no empiezan por `git` y opciones globales | `GIT_DIR=x git commit`, `env git …`, `/usr/bin/git …`, aliases definidos en la config de Git (`git ci`) y las formas con `-C` no coinciden con un gate anclado en `git <subcomando>`, salvo que el patrón los enumere. Mitigación: invocación canónica con `cwd` y la regla 18 (§23) |
| Los agents no pueden ejecutar operaciones con gate | Commit, push y PR autorizados los ejecuta la Main Session (§13) |
| Sin máquina de estados persistente para el ciclo de PRs | La semántica es explícita (§4, `pr-review` §19.5), pero el estado vive en la sesión. Retomar depende del estado remoto y de lo que el provider persista |
| El orchestrator no puede preguntar en vivo | Se detiene, devuelve `LIFECYCLE_STATE` y se reanuda desde la Main Session |
| Workers en segundo plano (`async.enabled: true`) | En sesión no interactiva (`omp -p`), la Main Session debe esperar el resultado con `hub wait`; si no, termina antes de que el worker entregue (verificado) |
| `eval` sólo admite approval global (`allow` / `prompt` / `deny`) | Los gates de `bash` no lo contienen y `agent()` / `workpool()` esquivan el gate de `task`. La frontera la sostiene el harness |
| La mutación de Git y de plataformas remotas se enumera en `bash.patterns` | Un subcomando nuevo no listado se auto-aprueba hasta que se añada |
| `bash.patterns` no es un sandbox | Un intérprete (`bash -c`, `python3 -c`) evade los gates anclados |
| No verificado: descubrimiento de skills nuevas en una sesión ya abierta | Tras cambiar las skills, sesión nueva |
| El readiness gate lo ejecuta el agente aplicando `specification` | C2 y C4 son comprobables contra los artefactos; la materialidad (C1, C3) sigue siendo juicio registrado en el `READINESS_RESULT`. No hay validador automático |
| El `READINESS_RESULT` sólo persiste si se escribe el contrato 07 | Ubicación de artefactos según el task contract (`specification` §10); no hay persistencia de lifecycle (ver "No existe hoy") |
| Quality, coherence y materialidad son juicio del agente | SQ5/SQ10 y C2 tienen apoyo mecánico (léxico, IDs); la coherencia semántica, la materialidad y la clasificación de aperturas siguen siendo juicio registrado con evidencia, no un validador. La regresión `tests/specification/` (`run.py`) fija el contrato de la skill y compara veredictos de dry-runs ciegos registrados; reproducirlos exige volver a ejecutarlos |
| El aislamiento de los dry-runs es por instrucción | El agente que produce un veredicto no debe leer `expected/`; no hay barrera técnica |
| Sin persistencia del estado de la Línea 1 | `SPECIFICATION_STATE` y el ledger viven en la sesión y en los artefactos de la tarea |
| Las garantías de la Línea 2 son de método, no mecánicas | El fingerprint del contrato, la re-ejecución independiente de la verificación, la convergencia por AC y la clasificación de remediation las aplica el agente siguiendo la skill; no hay script ni runner que las imponga. Sin ejecuciones reales registradas: la suite `tests/delivery/` valida decisiones sobre escenarios descritos, no Git ni tests reales |
| `project-management` sin tracker ni historial | Las dependencias, blockers y el `WORK_GRAPH` viven en el assessment o en la sesión; no hay scheduler ni locking. Las señales de flujo (`AGING`, `BLOCKED_TIME`, `REWORK`…) son `NOT_AVAILABLE` salvo que exista una fuente real (tracker, historial de PRs, dato del humano) |
| Estado de requisitos, baselines y forecasts sin persistencia | El estado de un requisito se deriva en el momento de los estados de Kanban, `delivery-lifecycle` y `specification`; no hay registro de requisitos, cambios ni baselines. PM no los autodeclara: sin fuente, `UNKNOWN` o `NOT_AVAILABLE`. Los conceptos de PMBOK 8 se adaptaron desde fuentes secundarias concordantes porque la página oficial de PMI no fue accesible al redactarlos |
| Clasificación, tamaño, riesgo y slicing son juicio | Con evidencia y registrados, pero no deterministas: hay casos frontera (`BUG` / `INCIDENT`, `SECURITY` / `TECHNICAL_CHANGE`, `INVESTIGATION` / `DOCUMENTATION`). La suite `tests/project-management/` fija el contrato y compara veredictos ciegos registrados |
| PM no coordina entre repositorios | Identifica `CROSS_REPOSITORY_DEPENDENCY` y su orden; cada repositorio conserva su baseline, gobernanza y contrato |
| Slash commands sin verificar (`/hub`, `/plan-review`, forma exacta de `/plan`, `/goal`, `/loop`) | Ver §15 |

### No existe hoy

Se documenta para que nadie lo dé por disponible.

| No existe | Nota |
|---|---|
| Model role `@review` | OMP no lo soporta (verificado contra omp/18.1.22: roles admitidos `default`, `smol`, `slow`, `vision`, `plan`, `commit`, `tiny`, `task`, `advisor`). `modelRoles` no valida claves: un `review:` se almacena y nadie lo consume. Los workloads de review usan rol o modelo explícito (§16) |
| Agents `implementation-review`, `pr-review`, `security-review`, `project-management`, `git-workflow`, `specification`, `delivery-lifecycle` | Sólo skills; las aplica la Main Session o, dentro de un lifecycle delegado, `delivery-orchestrator` en su propio contexto |
| Skill `governance-review` | Sólo agent |
| Capability transversal de verificación / evidencia | Es norma (`RULES.md` 11, 12, 18), la ejecuta `implementation` y la revisan las reviews; no hay capability propia |
| Coordinación multi-repositorio | `RULES.md` 13 prohíbe mezclar repos; nada coordina trabajo entre varios |
| Locking, worktrees o ramas por worker para varios `implementation` en paralelo | Multi-writer exige fronteras explícitas (§14) |
| Investigación técnica externa / status reporting | `technical-discovery` es del workspace; `project-management` no es reporting periódico |
| Persistencia de Goals y Execution Contracts | El harness no los indexa |
| Reglas sticky 14, 15 y 16 | Reservadas: frontera de workspace, autoridad de repositorio designado y raíz de sesión son decisiones de organización. Apep Core no las define; si existe una versión genérica es una decisión abierta (más abajo) |
| Provider de PR, modelo de ramas permanente o settings de approvals incluidos en Core | Los aporta el plugin de organización o el proyecto consumidor (§1, *Composición*; §23) |
| Escaneo de seguridad nativo (`/security`, `security_scan`) | Depende de `security.enabled` (compruébalo con `omp config get security.enabled`). Habilitarlo es decisión humana |

### Abierto, no comprometido

- Si las reglas de organización 14–16 tendrán una versión genérica en Apep Core: decisión abierta; hoy no existe.
- Una capability reutilizable de verificación / evidencia.
- Licencia del paquete: `LICENSE_DECISION = PENDING_HUMAN` (`LICENSE.md`).

---

## 25. Referencias

| Documento | Rol |
|---|---|
| [`docs/governance/ENGINEERING_GOVERNANCE.md`](docs/governance/ENGINEERING_GOVERNANCE.md) | Autoridad normativa canónica de ingeniería, compilada por las reglas sticky |
| [`rules/engineering-discipline.md`](rules/engineering-discipline.md) (`RULES.md`) | 16 reglas always-on, numeradas 1–13 y 17–19 (normativo) |
| [`skills/`](skills/) | Las 11 metodologías del paquete |
| [`agents/`](agents/) | Los 6 agents del paquete |
| [`commands/`](commands/) | Los 9 work modes (slash commands) |
| [`docs/recommended-approval-patterns.md`](docs/recommended-approval-patterns.md) | Patrón recomendado de approvals para tu `config.yml` (consultivo) |
| [`docs/agents-md-template.md`](docs/agents-md-template.md) | Plantilla para tu `.omp/AGENTS.md` (consultivo) |
| [`tests/`](tests/) | Suites de conformidad del método y regresión de approvals |
| [`ebook/`](ebook/) | Tooling de generación y validación de EPUB |
| [`VERSION`](VERSION) · [`package.json`](package.json) | Versión del paquete |
| [`README.md`](README.md) | Entrada breve a Apep Core |
| [`USER_GUIDE.md`](USER_GUIDE.md) · [`COOKBOOK.md`](COOKBOOK.md) | Aprender a usarlo · recetas por problema |
| [`LICENSE.md`](LICENSE.md) | Decisión de licencia pendiente |
| [`CHANGELOG.md`](CHANGELOG.md) | Evolución material del paquete |
