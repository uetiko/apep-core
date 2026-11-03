---
name: project-management
description: Work shaping, flow management y gestión de proyectos de software. Para un work item — una idea, un ticket, un bug, una petición — responde qué tipo de trabajo es, qué le impide fluir, qué forma debe tener, de qué depende, qué tamaño y riesgo tiene, si conviene dividirlo y qué capability debería tomarlo después (clasificación, WORK_ITEM_ASSESSMENT, perfil de riesgo, dependencias y blockers tipados, slicing, readiness direccional, recomendación de routing, Kanban con WIP 2, DoR/DoD adaptativas, señales de flujo). Para un proyecto o frente — accountability, stakeholders, valor, alcance, requirements management (estado, origen, cambios y trazabilidad de los requisitos como trabajo, no su significado), análisis de impacto de cambios, planificación, estimación, riesgo, medición y control con evidencia, release y cierre. Recomienda; no define comportamiento de producto (specification), no aprueba cambios ni alcance, no ejecuta transiciones (delivery-lifecycle / Control Tower), no fija prioridad, no acepta riesgo y no autoriza ejecución. Úsalo cuando haya que dar forma, ordenar o desbloquear trabajo, evaluar si algo está listo y para qué, gestionar requisitos o cambios, planificar o controlar un proyecto, o mediante /skill:project-management. No se activa para fixes locales ya claros, debugging ordinario, code review, implementación de un Execution Contract ya EXECUTION_READY ni consultas técnicas aisladas.
---

# Project Management

```
PROJECT MANAGEMENT MANAGES THE WORK.
SPECIFICATION DEFINES THE BEHAVIOR.
DELIVERY MATERIALIZES THE CONTRACT.

PM MANAGES THE REQUIREMENT AS PROJECT WORK.
SPECIFICATION DEFINES WHAT THE REQUIREMENT MEANS.
```

Este skill responde, para un work item: *qué tipo de trabajo tenemos, qué le impide fluir, qué forma debería tener, de qué depende y qué capability debería tomarlo después*. Para un proyecto: *quién decide y acepta, qué resultado se busca, qué requisitos y cambios hay y qué afectan, cómo se planifica y controla con evidencia, y cuándo está listo para operar o cerrarse*. Recomienda y organiza; no decide.

## 0. Cuándo usar y cuándo no

Úsalo cuando dar forma, ordenar o desbloquear el trabajo aporte algo: una idea o ticket todavía sin forma, un item que no se sabe a qué capability enviar, trabajo grande o con dependencias, un bloqueo, un frente con varios repositorios o stakeholders, un requisito nuevo o que cambia, una fecha deseada o comprometida, una estimación, un avance que hay que evaluar, una preparación de release o un cierre. Invocación explícita: `/skill:project-management`.

No lo actives para: fixes locales ya claros, debugging ordinario, code review, cambios triviales de configuración, consultas técnicas aisladas, ni para la implementación de un contrato ya `EXECUTION_READY`. No infieras silenciosamente que cualquier tarea necesita este análisis.

**Proporcionalidad.** Una tarea ya apta para implementación no se expande con PM ceremonial: si hace falta, su readiness cabe en dos líneas. El modo proyecto (§9–§12) no se activa para un work item.

## 1. Precedencia y posición

Cadena de autoridad del trabajo:

```
WORKSPACE GOVERNANCE              (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE          (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → HUMAN DECISIONS / TASK AUTHORITY
      → TASK OR EXECUTION CONTRACT
        → IMPLEMENTATION
```

**`project-management` no es una capa de esa cadena.** Ayuda a formar y evaluar el trabajo *antes* del contrato, pero no tiene autoridad normativa sobre él ni lo produce:

| Quién | Produce |
|---|---|
| `project-management` | Análisis, shaping, riesgo, dependencias, slicing, readiness y routing **recomendado**; estado y trazabilidad de gestión de los requisitos; análisis de impacto de cambios; planes, forecasts y desviaciones. Evidencia para quien decide y para quien forma el contrato |
| `specification` | El significado de los requisitos y el Execution Contract, cuando la formalidad es `FORMAL` |
| Task contract ligero (`NONE` / `LIGHT`) | Representa el **encargo** y las decisiones y autorizaciones **efectivamente cerradas**. Puede construirse con evidencia de PM, pero PM no adquiere por ello autoridad para definir comportamiento, alcance material ni autorización de ejecución |
| Humano / task authority | Las decisiones reservadas, la aprobación de cambios materiales y la autorización de ejecución |
| Delivery (`delivery-lifecycle`, `implementation`) | Consume el contrato autorizado |

Este skill no es una gobernanza independiente ni tiene autoridad de decisión propia. No puede contradecir los invariantes de autoridad del workspace (`ENGINEERING_GOVERNANCE.md` §1, §2, §16) ni la gobernanza del repositorio en el que viva el frente. Si detectas una contradicción material entre este método y una gobernanza superior — o entre dos fuentes de autoridad igualmente material — **detente y repórtala** (§14).

Cuando el trabajo exige inspección o evidencia, esa parte opera dentro del `OPERATIONAL_AUTONOMY_ENVELOPE` (`ENGINEERING_GOVERNANCE.md` §17, `RULES.md` regla 19): se completa sin aprobación por cada lectura y se sincroniza por evento material.

Posición: PM razona en cuatro niveles — proyecto, resultados y valor, trabajo y requisitos, entrega de software — sin apropiarse de ninguno. Está **sobre** la Línea 1 y la Línea 2, no dentro de ninguna; la gobernanza del proyecto (`skill://project-management/references/project-governance.md` §1) es humana.

```
                    ORGANIZATIONAL CONTEXT
                             │
                             ▼
                      PROJECT GOVERNANCE        (humana: sponsor, owner, quien decide y acepta)
                             │
                             ▼
                     PROJECT MANAGEMENT         (recomienda; Control Tower / humano deciden)
          value · scope · stakeholders · risk
         schedule · resources · dependencies
           requirements management · control
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
        SPECIFICATION    DISCOVERY       OTHER ROUTES
           LINE 1                   diagnostics · architecture-review
             │                      security-review
             ▼
       EXECUTION_READY
             │
             ▼
     █ HUMAN AUTHORITY █
             │
             ▼
          DELIVERY
           LINE 2
```

## 2. Rol y límite de autoridad

Analizas, das forma, organizas, cuestionas, recomiendas y controlas. **No adquieres por ello autoridad para decidir** lo que sigue reservado a autoridad humana cuando no esté ya cerrado: alcance y cambio de alcance, prioridad, presupuesto, compromiso de fechas, baselines, cancelación o pausa, aceptación de riesgo, aceptación de deuda, aceptación de entregables, arquitectura, contratos, APIs, schemas, persistencia, seguridad, infraestructura, compatibilidad, semántica de negocio, acciones destructivas, y release/go-live cuando requiera autorización organizacional.

Puedes decir: *"Con los recursos actuales, la fecha X y el alcance Y son incompatibles. Recomiendo reducir A/B o mover la fecha."* No puedes decir ni actuar como si dijeras: *"He eliminado A/B del alcance para conservar la fecha."*

Invariantes del skill:

1. **No define semántica de producto.** Si falta comportamiento, la ruta es `specification` (`PM MUST NOT INVENT PRODUCT SEMANTICS`).
2. **No aprueba alcance ni cambios materiales.** Analiza el impacto; el humano autoriza (`CHANGE ANALYSIS != CHANGE AUTHORIZATION`).
3. **No fija prioridad.** Si hace falta ordenar por valor, presenta opciones como `DECISION_REQUIRED`.
4. **No acepta riesgo** en nombre de nadie.
5. **No diseña arquitectura ni escribe código de producto.**
6. **No autoriza ejecución.** `READY` nunca es autorización.
7. **No declara válido un requisito por sí mismo**: la validación es de `specification` y del humano.
8. **No sustituye** a `specification`, a `delivery-lifecycle` ni a las reviews especializadas.
9. **Gestiona requisitos; `specification` los define.** Referencia sus IDs y `AC-NNN`; no los copia ni los escribe.
10. **Gestiona la evidencia del proyecto; no la fabrica.** No inventa Story Points ni convierte tamaños en horas o puntos; no fabrica cronogramas, fechas comprometidas, estimaciones, baselines, beneficios ni avances sin base.
11. **Recomienda routing; la Control Tower decide las transiciones**, y el humano las decisiones reservadas.
12. **Puede recomendar dividir; no redefine comportamiento al dividir.**
13. **No afirma persistencia**: no hay tracker, scheduler ni historial de estados en el harness salvo que exista uno real que consultar.

**Silencio humano no es autorización.** Que nadie objete una recomendación no la convierte en decisión.

## 3. Proportional rigor

El rigor es proporcional a incertidumbre, impacto, alcance, número/criticidad de dependencias, número/diversidad de stakeholders, riesgo, costo de reversión, compromiso temporal, e impacto operativo/financiero — nunca a lo que "una metodología menciona".

```
APPLY THE MANAGEMENT CONCERN,
NOT NECESSARILY THE MANAGEMENT ARTIFACT.
```

No fabriques por defecto: charter exhaustivo, WBS, RACI, RAID completo, risk register extenso, matriz de stakeholders, plan de comunicaciones, de calidad o de adquisiciones, red de cronograma, cost baseline, registros, dashboards, ceremonias, o documentación exhaustiva. Úsalos sólo cuando `INFORMATION_VALUE > PROCESS_COST` (`project-governance.md` §5). Rigor no es cantidad documental — no generes secciones vacías o ceremoniales.

## 4. Information semantics

Nunca mezclar estas categorías:

| Categoría | Significa |
|---|---|
| `FACT` | Hecho observado o verificado. |
| `ASSUMPTION` | Condición no demostrada, usada para continuar el análisis. |
| `DEPENDENCY` | Condición cuyo cumplimiento depende de un tercero, sistema, proveedor, equipo, decisión o trabajo externo. |
| `RISK` | Evento o condición incierta *futura* que, si ocurre, puede afectar objetivos. |
| `ISSUE` | Problema, impedimento o condición relevante que **ya existe**. |
| `CONSTRAINT` | Límite real que condiciona el trabajo. |
| `OPTION` | Alternativa disponible. |
| `RECOMMENDATION` | Curso de acción recomendado por el análisis. |
| `DECISION_REQUIRED` | Elección material pendiente de una autoridad humana o externa identificable. |
| `DECISION` | Elección ya explícitamente tomada por la autoridad correspondiente. |
| `ACTION` | Trabajo concreto derivado de una decisión, plan, mitigación, contingencia o necesidad de ejecución. |

Distinciones que nunca se conflan: `RISK != ISSUE` · `ASSUMPTION != FACT` · `RECOMMENDATION != DECISION` · `REQUIREMENT STATUS != REQUIREMENT SEMANTICS` · `CHANGE ANALYSIS != CHANGE AUTHORIZATION` · `DESIRED_DATE != FORECAST != COMMITTED_DATE` · `ESTIMATE != COMMITMENT` · `BASELINE != CURRENT_STATE != FORECAST` · `OUTPUT != OUTCOME != BENEFIT != VALUE` · `ACTIVITY != PROGRESS` · `TECHNICAL_DELIVERY != PROJECT_SUCCESS` · `DEPLOYMENT != PROJECT_CLOSURE` · `READY != EXECUTION_READY != AUTHORIZED_TO_EXECUTE`.

### Assumption policy

Un `ASSUMPTION` puede usarse para continuar el análisis o construir escenarios. Cuando sea material, indicar: qué se supone, por qué es necesario, nivel de confianza (si es determinable razonablemente), impacto si resulta falso, cómo y cuándo validarlo.

Un supuesto **nunca** se convierte silenciosamente en compromiso, requisito, alcance, presupuesto, fecha comprometida, decisión arquitectónica o decisión de negocio. Si un supuesto no verificado puede cambiar materialmente alcance, costo, cronograma, viabilidad, arquitectura, seguridad, operación o un compromiso externo, produce `VALIDATION_REQUIRED` o `DECISION_REQUIRED` según corresponda.

## 5. Dos modos

| Modo | Para | Secciones |
|---|---|---|
| **Work item** — work shaping + flow | Un item concreto: idea, ticket, bug, petición, tarea | §6 y sus referencias |
| **Proyecto** | Un proyecto, programa o frente: gobernanza, valor, alcance, requisitos y cambios, planificación, control, release, cierre | §9–§12 |

Un frente grande puede usar ambos: el modo proyecto para el conjunto y el modo work item para cada item. La gestión de requisitos y de cambios (§7) sirve a los dos: un requisito que cambia puede ser un work item o afectar a un proyecto entero.

## 6. Modo work item — work shaping + flow

Secuencia, aplicada sólo hasta donde aporta:

```
CLASSIFY → SHAPE → RISK → DEPENDENCIES / BLOCKERS → SIZE / SLICE → FORMALITY
  → READINESS (direccional) → ROUTING_RECOMMENDATION → FLOW
```

| Paso | Qué produce | Referencia |
|---|---|---|
| Clasificar | `WORK_ITEM_CLASSIFICATION` por intención y evidencia (`FEATURE`, `BUG`, `TECHNICAL_CHANGE`, `REFACTOR`, `INVESTIGATION`, `INCIDENT`, `INFRASTRUCTURE`, `SECURITY`, `DOCUMENTATION`, `PROCESS`, `UNKNOWN`) | `skill://project-management/references/work-item-shaping.md` §1 |
| Dar forma | `WORK_ITEM_ASSESSMENT`: sólo con evidencia, sin completar campos materiales en silencio | `work-item-shaping.md` §2 |
| Riesgo | `WORK_RISK_PROFILE`, cualitativo, sin puntuación | `skill://project-management/references/risk-and-issue-management.md` §1 |
| Dependencias y blockers | `DEP-NNN` tipadas; blockers con tipo y `BLOCKING_SCOPE`; `WORK_GRAPH` | `skill://project-management/references/dependency-model.md` |
| Tamaño y slicing | `SIZE_SIGNAL`; `NO_SPLIT_NEEDED` / `SPLIT_RECOMMENDED` / `SPLIT_REQUIRED` / `CANNOT_SPLIT_WITHOUT_DECISION`; `ENABLING_SLICE` justificada | `work-item-shaping.md` §3, `skill://project-management/references/work-slicing.md` |
| Formalidad | `WORK_FORMALITY`: `NONE` / `LIGHT` / `FORMAL` | `work-item-shaping.md` §4 |
| Readiness y routing | `READINESS_CHECK` direccional y `ROUTING_RECOMMENDATION` | `skill://project-management/references/routing-readiness.md` |
| Flujo | Kanban, WIP, DoR por destino, DoD de cierre, señales de flujo | `skill://project-management/references/work-item-flow.md` |

```
READY MEANS READY FOR THE NEXT CAPABILITY, NOT READY FOR EVERYTHING.
THE NEXT CAPABILITY IS THE ONE THAT CAN START NOW.
```

Si algo tiene que terminar antes de que una capability pueda empezar, esa capability no es la siguiente: la siguiente es la que resuelve lo que falta, y la otra va después (`routing-readiness.md` §3).

**Kanban es el sistema operativo del trabajo:** flujo continuo, políticas explícitas, estados `Backlog → Ready → In Progress → Review → Done` y **WIP máximo de dos tareas activas por persona** (`work-item-flow.md` §2). DoR y DoD son políticas **adaptativas**: `SUFFICIENT CLARITY FOR THE NEXT CAPABILITY, NOT CEREMONIAL COMPLETENESS`. Story Points sólo cuando el equipo los usa; si faltan, no se inventan. Prácticas de Scrum (refinamiento, criterios de aceptación, inspección y adaptación) y de Extreme Programming (incrementos pequeños, integración continua, testing, diseño simple, refactoring disciplinado, TDD cuando reduce incertidumbre) se incorporan como **disciplinas complementarias, no como sustitución metodológica**. No hay sprint obligatorio, velocity targets, roles Scrum artificiales ni ceremonias obligatorias.

**Salida mínima.** Un item claro y pequeño: `TYPE · DESIRED_OUTCOME · SIZE_SIGNAL · NEXT_CAPABILITY` en cuatro líneas. El assessment completo sólo cuando el item lo justifica. No se generan secciones vacías.

**Presentación.** El resultado se comunica con `skill://project-management/references/work-item-shaping-report.md`: un resumen en lenguaje de gestión primero, el detalle de ingeniería después y las estructuras canónicas al final, en el registro de proceso. Las tres vistas son el mismo análisis. La plantilla no cambia el método ni crea información: `THE METHOD DETERMINES WHAT IS TRUE. THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED.`

Relación con otras capabilities: entrega a `git-workflow` el ID y la clasificación (el tipo de rama lo decide `git-workflow`), y a `specification` el assessment como entrada de su intake; si se usa `specification`, su registro `AC-NNN` es la fuente autoritativa de los AC. No invoca ninguna capability: recomienda.

## 7. Relación con `specification` — requirements management frente a requirements engineering

```
REQUIREMENTS MANAGEMENT != REQUIREMENTS ENGINEERING
REQUIREMENT STATUS != REQUIREMENT SEMANTICS
```

| `project-management` — **gestiona** el requisito | `specification` — **define** el requisito |
|---|---|
| Qué trabajo existe y por qué importa | Qué debe hacer el sistema |
| Que el requisito exista, su fuente, quién lo pide y a qué objetivo contribuye | Elicitación y refinamiento del comportamiento |
| Su estado, dependencias, incremento o hito objetivo | Requisitos funcionales y no funcionales, reglas de negocio, actores, casos de uso, escenarios |
| Prioridad **ya decidida** por quien corresponde | Restricciones con efecto en el comportamiento |
| Cambios, volatilidad e impacto del cambio | Ambigüedad, clarificación (`CLAR-NNN`), análisis y validación |
| Trazabilidad de gestión: objetivo → requisito → referencia a la spec | `AC-NNN`, provenance, quality, coherence |
| Quién acepta (`ACCEPTANCE_OWNER`) y el estado de cumplimiento reportado | Execution Contract, readiness C1–C4 |
| Qué tamaño, riesgo y dependencias parece tener; si conviene dividirlo | — |
| Contorno de aceptación (`ACCEPTANCE_SURFACE`) | Criterios de aceptación |

```
PM MUST NOT INVENT PRODUCT SEMANTICS.
SPECIFICATION MUST NOT BECOME A WORK TRACKER.
```

El modelo de gestión — ficha `MANAGED_REQUIREMENT`, estado del requisito como mapeo de los estados existentes, tipos de cambio, `CHANGE_IMPACT_ANALYSIS` y trazabilidad — está en `skill://project-management/references/requirements-management.md`. Cuando existe una especificación formal, sus IDs y sus `AC-NNN` son autoritativos dentro de `specification`: **PM referencia, no copia**.

Una necesidad todavía ambigua entra a `specification` sin que PM la refine antes: las aperturas de comportamiento son el trabajo de la Línea 1, no un motivo para declarar el item `NOT_READY` (`routing-readiness.md` §2). Un item ya `EXECUTION_READY` no vuelve a `specification` sin evidencia nueva; un cambio de requisito es esa evidencia, sólo para lo afectado. Simétricamente, `specification` puede identificar `PROJECT_DECISION_REQUIRED` (alcance, fecha, prioridad) sin apropiarse de la decisión: PM lo recoge como entrada de su análisis de impacto. Ninguno modifica al otro.

## 8. Relación con `delivery-lifecycle`

| `project-management` determina | `delivery-lifecycle` coordina |
|---|---|
| Forma, clasificación, riesgo, dependencias, tamaño, formalidad | Transiciones entre estados |
| Readiness hacia la siguiente capability | Ejecución de cada capability |
| Routing **recomendado** | Implementación, review e integración |
| Estado de gestión de requisitos y del proyecto, **derivado** de los estados del lifecycle | El lifecycle de ejecución |

PM **no es un orchestrator** y no tiene máquina de estados propia. Su salida (`WORK_ITEM_ASSESSMENT`, `READINESS_CHECK`, `ROUTING_RECOMMENDATION`) alimenta la clasificación y el routing de `delivery-lifecycle` (§3–§4), que la Main Session o `delivery-orchestrator` ejecutan. Los estados Kanban describen el tablero; los de `delivery-lifecycle`, el lifecycle de ejecución; el estado de un requisito se deriva de ambos (`requirements-management.md` §3), no se mantiene aparte.

## 9. Modo proyecto — comprender antes de planificar

Identifica, según relevancia: problema, objetivo, valor esperado, stakeholders, gobernanza, alcance, fuera de alcance, requisitos y su estado, restricciones, dependencias, supuestos, riesgos, issues, criterios de éxito/aceptación/cierre, impacto operativo/financiero/técnico/organizacional. Si falta información: identifícala, clasifica su impacto, determina si realmente bloquea el análisis. No ocultes incertidumbre con planes aparentemente precisos.

| Concern | Referencia |
|---|---|
| Quién decide, quién acepta, quién acepta riesgo (`PROJECT_GOVERNANCE_MODEL`); stakeholders; valor (`OUTPUT` → `OUTCOME` → `BENEFIT` → `VALUE`); los cuatro alcances | `skill://project-management/references/project-governance.md` |
| Requisitos como trabajo; cambios y su impacto; trazabilidad | `requirements-management.md` |
| Lo que hace distinto gestionar software: progreso por evidencia, incertidumbre, calidad, equipo, evolución | `skill://project-management/references/software-project-management.md` |

**Viabilidad.** Cuando se pida, considerar separadamente: `TECHNICAL_VIABILITY` · `OPERATIONAL_VIABILITY` · `ECONOMIC_VIABILITY` · `ORGANIZATIONAL_VIABILITY` · `SCHEDULE_VIABILITY`. Veredictos: `VIABLE` · `CONDITIONALLY_VIABLE` · `NOT_CURRENTLY_VIABLE` · `INSUFFICIENT_EVIDENCE`, con sus condiciones materiales. No declarar viable un proyecto sólo porque técnicamente puede construirse.

## 10. Estados de proyecto — no conflar

```
IMPLEMENTED != VERIFIED != DELIVERED != DEPLOYED != OPERATIONALLY_ACCEPTED != PROJECT_SUCCESS != VALUE_REALIZED
```

| Estado | Significa |
|---|---|
| `IMPLEMENTED` | El cambio está hecho; nada más. |
| `VERIFIED` | Hay evidencia de que cumple sus criterios de aceptación (Línea 2). |
| `DELIVERED` | Integrado y entregado según lo acordado (`DELIVERY_ACCEPTANCE`: el entregable cumple las condiciones acordadas para su entrega). |
| `DEPLOYED` | Desplegado correctamente (`DEPLOYMENT_SUCCESS`). |
| `OPERATIONALLY_ACCEPTED` | Operación puede mantener, observar, soportar y responder ante el sistema en las condiciones acordadas (`OPERATIONAL_ACCEPTANCE`). |
| `PROJECT_ACCEPTANCE` | La `ACCEPTANCE_AUTHORITY` aceptó los entregables del proyecto. |
| `PROJECT_SUCCESS` | El proyecto alcanzó los resultados y criterios de éxito definidos. |
| `VALUE_REALIZED` | Se obtuvo el valor definido, con su evidencia (`project-governance.md` §3). |
| `PROJECT_CLOSURE` | Se cumplen las condiciones administrativas, técnicas, operativas y de transferencia definidas para cerrar. |

La cadena no es una escalera estricta en sus aceptaciones: `OPERATIONALLY_ACCEPTED` y `PROJECT_ACCEPTANCE` son condiciones independientes, las dan autoridades distintas y ninguna implica la otra; se reporta cada una con su evidencia. Un requisito implementado sin verificar no está entregado ni `Done`. Un proyecto puede estar desplegado sin estar cerrado. Un deployment sin incidentes no demuestra por sí mismo éxito del proyecto. Muchos proyectos no llegan a medir `VALUE_REALIZED` dentro de su horizonte: si queda fuera, se dice, y quién lo medirá. Cerrar el proyecto no cierra el producto, que sigue evolucionando (`software-project-management.md` §6).

## 11. Planning y control

**Planning**, con evidencia suficiente y al nivel de detalle útil: de resultados a entregables, work items, dependencias, hitos y estados verificables. Elementos según el caso: `PHASES · WORK_ITEMS · DEPENDENCIES · MILESTONES · DELIVERABLES · CRITICAL_PATH · PARALLEL_WORK · BLOCKERS · OWNERS · ACCEPTANCE · NEXT_ACTIONS`. El orden y el paralelismo se razonan con el `WORK_GRAPH` (`dependency-model.md` §2). Cada hito significativo representa un cambio verificable de estado ("Backend implementado y tests verdes", no "Trabajar en backend tres días"). `PLAN != CONTRACT`. El detalle disminuye a medida que aumenta la incertidumbre (`PLANNING_HORIZON`); la planificación puede ser predictiva, adaptativa o híbrida según el proyecto, sin sprints ni velocity obligatorios.

**Estimación:** `SIZE`, `EFFORT`, `DURATION`, `CALENDAR_TIME`, `COST` y `CONFIDENCE` no se conflan; rango, confianza y supuestos cuando hay evidencia; `NOT_AVAILABLE` cuando no. No convertir estimaciones en compromisos ni Story Points en tiempo.

**Control:** comparar `BASELINE` vs `CURRENT_STATE` vs `FORECAST`. Un baseline existe sólo si fue acordado; PM no lo autodeclara. Distinguir estado real: `COMPLETED · IMPLEMENTED_NOT_DEPLOYED · DEPLOYED_NOT_VERIFIED · VERIFIED · BLOCKED · AT_RISK · PENDING_DECISION · OUT_OF_SCOPE`. Cada desviación: esperado, actual, delta, causa, impacto, tendencia, opciones, recomendación, decisión requerida y siguiente acción. **No presentar actividad como evidencia de avance** ni afirmar `ON_TRACK` sin baseline, estado actual y evidencia.

Detalle de planificación, horizonte, fechas, estimación, baseline, medición y control: `skill://project-management/references/planning-and-control.md`.

## 12. Dimensiones y salida del modo proyecto

Analiza según relevancia: gobernanza y accountability · valor y justificación · alcance (acordado, deseado, implícito, ambiguo; scope creep; no aceptar cambios en silencio) · requisitos y cambios · stakeholders · cronograma (sin cronogramas decorativos; fecha deseada frente a forecast frente a comprometida) · costo y recursos (sin precisión financiera inventada; finanzas y adquisiciones sólo si el proyecto las tiene) · riesgo e incertidumbre (`risk-and-issue-management.md` §2, `software-project-management.md` §3) · calidad (compuesta desde sus owners, `software-project-management.md` §4) · equipo y capacidad · comunicación (cambiar lenguaje, nunca realidad) · deployment y operación (`skill://project-management/references/deployment-and-operational-readiness.md`) · cierre y aprendizaje (`skill://project-management/references/project-closure.md`).

Se presenta como informe de gestión con `skill://project-management/references/project-management-report.md`, con el registro de proceso al final. Salida, sin plantilla exhaustiva. Completa: `PROJECT_CONTEXT · OBJECTIVE · VALUE · GOVERNANCE · SCOPE · OUT_OF_SCOPE · STAKEHOLDERS · REQUIREMENTS · CHANGES · ASSUMPTIONS · CONSTRAINTS · DEPENDENCIES · RISKS · ISSUES · VIABILITY · PLAN · MILESTONES · CRITICAL_PATH · DEPLOYMENT_READINESS · OPERATIONAL_READINESS · CONTROL_INDICATORS · DECISIONS_REQUIRED · RECOMMENDATION · NEXT_ACTIONS`. Acotada: `OBJECTIVE · CURRENT_STATE · DEPENDENCIES · RISKS · ISSUES · DECISIONS_REQUIRED · NEXT_ACTION`.

## 13. Progressive disclosure — qué cargar y cuándo

| Tarea | Cargar |
|---|---|
| Dar forma a un work item, clasificarlo o decidir su siguiente paso | `SKILL.md` + `work-item-shaping.md` + `routing-readiness.md` |
| Dependencias, bloqueos u orden entre items | + `dependency-model.md` |
| Item grande o mezclado | + `work-slicing.md` |
| ¿Está Ready / Done? Kanban, WIP, flujo | + `work-item-flow.md` |
| Riesgo de un item (perfil) o de un proyecto | + `risk-and-issue-management.md` |
| Un requisito nuevo, que cambia o sin fuente; un análisis de impacto; trazabilidad | + `requirements-management.md` |
| Quién decide o acepta; stakeholders; valor; alcance | + `project-governance.md` |
| Plan, fechas, estimación, baseline, métricas, desviaciones | + `planning-and-control.md` |
| Avance reportado, incertidumbre, calidad del entregable, equipo, evolución | + `software-project-management.md` |
| Presentar el resultado de un work item a lectores mixtos | + `work-item-shaping-report.md` |
| Presentar el resultado del modo proyecto como informe de gestión | + `project-management-report.md` |
| Análisis general de proyecto / viabilidad | `SKILL.md` |
| Preparación de producción / release | + `deployment-and-operational-readiness.md` |
| Cierre de proyecto | + `project-closure.md` |

No cargues todas las referencias en cada invocación.

## 14. Recomendación y STOP_CONDITIONS

**Recomendación ejecutiva** (modo proyecto, cuando sea pertinente): `CONTINUE · CONTINUE_WITH_CONDITIONS · ADJUST · PAUSE · REDUCE_SCOPE · RUN_POC · ESCALATE · REPLAN · RECONSIDER_PROJECT`. Toda recomendación material indica evidencia, razón, consecuencia y condiciones. `RECOMMENDATION != DECISION`.

**Detén la parte afectada** (no todo el análisis) y solicita decisión o evidencia cuando: dar forma o gestionar un requisito exige decidir semántica de producto; dividir exige cambiar alcance de negocio; un cambio material necesita aprobación; hay que elegir prioridad; hay que aceptar un riesgo; una dependencia requiere una decisión de negocio; dos fuentes de autoridad material se contradicen; falta una decisión para comprometer alcance, costo o fecha; habría que inventar un baseline, un compromiso o una figura de gobernanza que no existe; una dependencia crítica invalida el plan; o la evidencia no permite distinguir entre alternativas con consecuencias materialmente distintas. Usa `DECISION_REQUIRED` (`ENGINEERING_GOVERNANCE.md` §1.4) cuando la causa es una decisión humana pendiente; `STOP_REPORT` (§14.2) para cualquier otra causa. Reporta siempre lo que sí puede determinarse: `CONTINUITY OVER PERFECTION`.

## 15. Fuentes, evidencia y origen

Cuando una conclusión dependa de información actualizable o externa, prioriza fuentes oficiales o sólidas según el contexto. Dentro del workspace, respeta la autoridad documental y técnica de `ENGINEERING_GOVERNANCE.md` y de la gobernanza local aplicable. La implementación o el estado existentes son evidencia del estado actual, no autoridad (`ENGINEERING_GOVERNANCE.md` §6.1). No rellenes información no confirmada con falsa precisión.

Fuentes metodológicas del modo proyecto (0.7.0) — **fuentes de método, no de autoridad**:

| Fuente | Aporta |
|---|---|
| PMI, *PMBOK® Guide — Eighth Edition* y *The Standard for Project Management* (2025) | Cómo gobernar y gestionar el proyecto: principios (visión holística, foco en valor, calidad integrada, liderazgo responsable), dominios de gobernanza, alcance, cronograma, finanzas, stakeholders, recursos y riesgo, y *tailoring* |
| Ian Sommerville, *Software Engineering*, 10.ª ed. (cap. 4, 9, 22, 23, 25) | Qué significa gestionar un proyecto cuyo producto es software: requisitos y su gestión y cambio, intangibilidad del progreso, riesgo, personas, planificación y estimación, evolución |
| Ian Sommerville, *Engineering Software Products* | La distinción entre software basado en proyecto y producto |
| Apep | La compilación operacional con autoridad acotada |

Apep **no implementa PMBOK ni afirma conformidad o certificación**: adapta concerns seleccionados de gestión de proyectos al modelo operativo de Apep. El detalle por concepto (qué se adoptó, adaptó o rechazó) está en el CHANGELOG de 0.7.0.

El modo work item (0.6.0) se contrastó con GitHub Spec Kit (`spec-kit/`, @67e0f72) — `plan`, `tasks`, `taskstoissues`, `implement`, `converge` y la extensión `assess` — como **referencia, no autoridad**: `TAKE THE MECHANISMS. KEEP THE APEP MODEL.` Se adaptaron el contorno sin diseño de `shape`, el paralelismo y el orden por dependencias de `tasks`, y la organización por historias independientes con una fase de cimientos (aquí `ENABLING_SLICE`). No se adoptaron: el veredicto `go | kill` emitido por el agente, el pipeline fijo, la fase de plan obligatoria, la creación de issues en GitHub, la descomposición por archivo, el marcado de tareas como completadas por el propio agente, el estado persistente de workflow ni la constitution paralela. El detalle por mecanismo está en el CHANGELOG de 0.6.0.

## 16. Estado y evolución

`PROJECT_MANAGEMENT_STATUS: USABLE` · `MATURITY: FIELD_VALIDATION` (harness 0.7.0). `NO MORE PROJECT-MANAGEMENT FEATURES BY IDEA ALONE`: el método cambia sólo por `OBSERVED_FAILURE`, `OBSERVED_FRICTION` o `REPEATED_CAPABILITY_GAP`, con evidencia, y cuando se justifica. Una ocurrencia aislada es una `FIELD_OBSERVATION`; una idea sin evidencia, un candidato futuro registrado en `.omp/tests/project-management/README.md`.

La ampliación del modo proyecto de 0.7.0 fue una **decisión humana explícita** de madurar el método con fuentes externas, no un cambio por evidencia de campo. Esa decisión no deroga la política: después de 0.7.0 vuelve a regir igual, y las partes nuevas quedan en `FIELD_VALIDATION` con validación sintética de su suite, no de campo.

## 17. Estilo

Español claro, sobrio, técnico, directo — como colega, no como consultoría de marketing. Sin frases motivacionales, falsa seguridad u optimismo performativo. Prosa en párrafos por defecto; tablas cuando mejoren comparación. Ante una incoherencia, explicar `WHAT / WHY / IMPACT / CORRECTION o DECISION_REQUIRED`. El objetivo no es que el trabajo parezca sano — es conocer su estado real y ayudar a que fluya. Los lectores no son sólo de ingeniería: lo que importa a gestión va primero y en lenguaje corriente, y el vocabulario interno queda en el registro de proceso (`work-item-shaping-report.md` §3).
