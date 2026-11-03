# Work item flow — Kanban con disciplinas Scrum/XP complementarias

Referencia del modo *work item* de `project-management` (`SKILL.md` §6): Kanban, WIP, DoR, DoD y salud del flujo. Compila el marco ágil de Apep. Responde, para un work item concreto: ¿está Ready, y para qué? ¿qué falta? ¿cuál es la unidad mínima coherente? ¿cómo sabremos que está Done? ¿qué evidencia hace falta? ¿qué impide que fluya?

```
SUFFICIENT CLARITY, NOT CEREMONIAL COMPLETENESS.
```

Para un cambio local ya claro, la respuesta cabe en cinco líneas.

## 1. Sistema operativo: Kanban

Kanban es el marco operativo principal: flujo continuo, WIP limitado, políticas explícitas.

```
Backlog → Ready → In Progress → Review → Done
```

| Estado | Entra cuando |
|---|---|
| `Backlog` | Existe la necesidad registrada |
| `Ready` | Cumple la Definition of Ready (§3) **para su siguiente capability** (`routing-readiness.md`). No equivale a `EXECUTION_READY` de `specification` ni a autorización |
| `In Progress` | Hay autorización de ejecución y work branch correcta (`git-workflow` §4) |
| `Review` | Implementación verificada, con evidencia; PR preparado o publicado según autorización (en `delivery-lifecycle`: de `REVIEWING` a `INTEGRATION_READY`) |
| `Done` | Cumple la Definition of Done (§4) y el owner lo acepta |

`Done` lo declara la persona, no el worker (`MANUAL.md` §21). Este skill dice si el item **cumple** la DoD; no lo mueve.

## 2. WIP

**Máximo dos tareas activas simultáneas por persona.**

Cuenta como activa:

- toda tarea en `In Progress`;
- una tarea en `Review` **mientras todavía requiere acciones del autor** (responder comentarios, corregir findings). Una tarea en `Review` que sólo espera al revisor no cuenta.

Tarea bloqueada:

- permanece visible en su estado y se marca **bloqueada**, con la causa;
- puede justificar tomar otra tarea, pero el bloqueo no se oculta para liberar WIP: el tablero debe seguir mostrando que existe.

Al evaluar un item, si tomarlo llevaría a su responsable por encima de dos activas, dilo (`ISSUE`), indicando qué está activo y qué está bloqueado. No lo resuelvas moviendo tareas: priorizar es del owner.

## 3. Definition of Ready

```
SUFFICIENT CLARITY FOR THE NEXT CAPABILITY, NOT CEREMONIAL COMPLETENESS.
```

La DoR se evalúa **respecto del siguiente paso** (`routing-readiness.md` §2). Lo que exige ir a `specification` no es lo que exige ir a `implementation`:

| Criterio | Hacia `specification` / `technical-discovery` / `diagnostics` | Hacia `implementation` |
|---|---|---|
| Objetivo / resultado buscado | Entendible, aunque sea parcial | Claro y verificable |
| Criterios de aceptación | **No se exigen**: definirlos es trabajo de la Línea 1 | Existen (`AC-NNN` en `FORMAL`; AC del task contract en `NONE`/`LIGHT`) |
| Alcance | Inicial, suficiente para empezar | Delimitado (`RULES.md` 5) |
| Decisiones | Pueden estar abiertas: son lo que la Línea 1 cierra | Cerradas las materiales |
| Owner / contexto | Identificable, que pueda responder clarificaciones | Identificable |
| Dependencias | Identificadas las que bloquean el siguiente paso | Identificadas y tipadas (`dependency-model.md`) |
| Prioridad | La fija el owner, no el agente | Ídem |
| Story Points | Opcionales | Opcionales: la estima el equipo; el agente no la inventa |
| Tamaño | `SIZE_SIGNAL` conocido o `UNKNOWN` | No `TOO_LARGE_TO_EXECUTE` (§5) |

Para `specification` **no** se exige: AC completos, todos los casos límite, Execution Contract, decisiones cerradas ni ambigüedad cero. Sí se exige que ninguna contradicción impida saber qué se intenta resolver.

**La DoR es adaptativa.** No es un gate mecánico. En micro fixes, investigaciones o tareas técnicas donde un criterio no aplica, ese criterio se omite con una razón breve. Lo que no puede faltar nunca es la claridad suficiente para el siguiente paso sin improvisar.

Un item que no cumple la DoR **no se rechaza**: se responde qué le falta, para qué destino, y quién puede aportarlo. Lo que sea una decisión humana pendiente se reporta como `DECISION_REQUIRED`.

## 4. Definition of Done

La DoD es el **cierre del work item**, no una segunda review de la implementación. No vuelve a evaluar lo que ya evaluaron `implementation-review`, `pr-review` o el readiness de `specification`: comprueba que su evidencia existe y está en verde.

Cuando aplique, el item cierra con evidencia de:

- criterios de aceptación **verificados explícitamente**, uno por uno (los `AC-NNN` del contrato o los AC del task contract);
- tests requeridos escritos y tests existentes en verde (`code-quality` §8), con el comando ejecutado;
- reviews aplicables hechas, con sus findings resueltos o aceptados por el owner;
- estado de integración: PR revisado / aprobado según el repositorio;
- documentación actualizada si cambia comportamiento, arquitectura o contratos (`code-quality` §5);
- sin TODOs ni trabajo incompleto del item.

**No se aplica mecánicamente**: un criterio que no tiene sentido para el cambio (p. ej. tests en un cambio sólo documental) se marca `N/A` con razón breve. La DoD del Execution Contract (`DEFINITION_OF_DONE`) puede añadir criterios; no los quita sin decisión del owner.

"PR revisado/aprobado" es un criterio humano: el agente puede dejar todo lo demás verificado, pero no puede cumplir ese por sí mismo. **`Done` lo declara la persona** (§1): este skill dice si el item cumple la DoD, no lo mueve.

## 5. Unidad mínima coherente de trabajo

La más pequeña que: entrega una intención completa · se puede verificar por sí sola · se puede revertir sin arrastrar otra · cabe en un commit atómico o en un PR de una sola intención.

Si un item contiene varias, propón la división (`RECOMMENDATION`) con su orden y dependencias (`work-slicing.md`). La división de alcance la decide el owner.

## 6. Disciplinas complementarias — no sustitución

Kanban es el sistema operativo; Scrum y XP aportan prácticas, no la metodología.

**De Scrum:** refinamiento cuando un item no está Ready · historias con objetivo claro · criterios de aceptación · DoR/DoD como políticas explícitas · inspección y adaptación sobre evidencia · feedback temprano · trabajo pequeño y verificable.

**De XP, como refuerzo de la ingeniería:** incrementos pequeños · feedback rápido · integración continua · testing (`code-quality` §8) · diseño simple · refactoring disciplinado, dentro de `REFACTOR_AUTHORIZATION` (`RULES.md` 10) · TDD cuando reduce incertidumbre — **no es un mandato universal**.

**No se introduce:** sprint obligatorio · velocity targets · roles Scrum artificiales · ceremonias obligatorias.

## 7. Salida — READINESS_CHECK

```
READINESS_CHECK
  WORK_ITEM:                  <ID | sin ticket — justificación> — <título>
  READY:                      YES | NO | PARTIAL
  NEXT_CAPABILITY:            <routing-readiness.md §1>
  READY_FOR_NEXT_CAPABILITY:  YES | NO
  OPEN:                       <aperturas que son trabajo del siguiente paso> | NONE
  MISSING:                    <qué falta para el siguiente paso y quién puede aportarlo> | NONE
  BLOCKERS:                   NONE | <tipo · alcance>
  NOT_APPLICABLE:             <criterios DoR omitidos y por qué> | NONE
  WIP:                        <activas del responsable, si se conoce> | UNKNOWN
  UNIT_OF_WORK:               <unidad mínima coherente> | <resultado de slicing>
  DONE_WHEN:                  <criterios de aceptación + DoD aplicable> | <lo que defina specification>
  EVIDENCE_NEEDED:            <tests, comandos, comprobaciones manuales>
  DECISIONS_REQUIRED:         NONE | <lista>
  REASON:                     <por qué>
```

Es el `READINESS_CHECK` de `routing-readiness.md` §1 con los campos de flujo añadidos; no es un segundo esquema. Para un item pequeño y claro bastan cuatro o cinco líneas. No generes secciones vacías.

## 8. Salud del flujo

Señales observacionales para ver qué impide que el trabajo fluya. **Sólo se usan cuando hay evidencia**:

| Señal | Qué indica | Fuente necesaria |
|---|---|---|
| `AGING` | Un item lleva mucho en su estado | Fecha de entrada al estado |
| `BLOCKED_TIME` | Cuánto tiempo lleva bloqueado | Fecha del bloqueo |
| `WIP_PRESSURE` | El responsable supera o roza el WIP de dos (§2) | Items activos del responsable |
| `REWORK` | El item volvió atrás tras una review | Historial del item o de sus PRs |
| `RETURN_TO_SPECIFICATION` | La implementación encontró una decisión no cerrada | `DECISION_REQUIRED` o `DECISION_CONTRADICTION` desde la Línea 2 |
| `RETURN_TO_IMPLEMENTATION` | Una review devolvió el item con un finding autorizado | `REMEDIATION_REQUIRED` en `delivery-lifecycle` |

El harness **no persiste** timestamps ni historial de estados. Si la fuente no está (un tracker, el historial de PRs, lo que el humano aporte), la señal se reporta `NOT_AVAILABLE`: no se estima ni se inventa. Las señales describen el flujo; no fijan prioridad ni culpan a nadie.
