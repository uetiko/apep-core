# Dependencias, blockers y grafo de trabajo

Referencia del modo *work item* de `project-management` (`SKILL.md` §6). Sustituye "dependencias: sí/no" por una clasificación que sirva para ordenar y desbloquear.

```
CONTINUITY OVER PERFECTION.
A PARTIAL BLOCKER DOES NOT FREEZE INDEPENDENT WORK.
```

## 1. Dependencias

```
DEP-001
  TYPE:            <tipo>
  TARGET:          <de qué depende: work item, decisión, sistema, persona, recurso — con su ID real si existe>
  STATUS:          OPEN | SATISFIED | BLOCKED | UNKNOWN
  EVIDENCE:        <de dónde sale la dependencia>
  BLOCKING_SCOPE:  <qué parte del trabajo no puede avanzar mientras siga abierta> | NONE
```

| Tipo | Significa | Ejemplo |
|---|---|---|
| `BLOCKING_DEPENDENCY` | No se puede empezar o terminar sin el otro | WI-102 necesita el endpoint que crea WI-101 |
| `SEQUENCING_DEPENDENCY` | Se puede hacer en paralelo, pero debe integrarse en orden | La migración va antes que el código que la usa |
| `INFORMATION_DEPENDENCY` | Falta un hecho | Hace falta saber el formato actual del archivo |
| `EXTERNAL_DEPENDENCY` | Depende de un tercero fuera del equipo | El proveedor tiene que habilitar la API |
| `SHARED_RESOURCE` | Compite por un recurso (entorno, ventana, persona, cuota) | El entorno de QA es único |
| `CROSS_REPOSITORY_DEPENDENCY` | Toca o espera otro repositorio del workspace | `frontend` espera un contrato nuevo de `backend` |
| `DECISION_DEPENDENCY` | Espera una decisión humana | Falta elegir la política de retención |
| `AUTHORIZATION_DEPENDENCY` | Espera una autorización (ejecución, rama, acceso, despliegue) | Falta autorizar la creación de la rama |

Reglas:

- **No se inventan IDs externos.** `TARGET` usa el ID real (ticket, PR, `DEC-NNN`, `CLAR-NNN`) si existe; si no, una descripción. `DEP-NNN` son IDs locales del assessment, no de un tracker.
- `UNKNOWN` cuando no se sabe si la dependencia existe o en qué estado está. No se resuelve suponiendo `SATISFIED`.
- Una `DECISION_DEPENDENCY` se reporta además como `DECISION_REQUIRED` (`ENGINEERING_GOVERNANCE.md` §1.4): PM no la cierra.
- Una `DECISION_DEPENDENCY` existe cuando la evidencia establece que una persona tiene que elegir. Una referencia cuyo significado no se conoce — aunque su nombre parezca el de una decisión — es una `INFORMATION_DEPENDENCY` con `STATUS: UNKNOWN` hasta que se sepa qué es (`routing-readiness.md` §3).
- Una `CROSS_REPOSITORY_DEPENDENCY` se identifica y se ordena, pero PM no coordina la ejecución entre repositorios: cada repositorio tiene su baseline, su gobernanza y su contrato (`RULES.md` 13). El harness no tiene coordinación multi-repositorio automática.

## 2. Grafo de trabajo

Para que la Control Tower razone sobre orden y paralelismo, sin scheduler ni persistencia:

```
WORK_GRAPH
  WI-001
    ├─ DISC-001   technical-discovery (PREREQUISITE)
    ├─ SPEC-001   specification       (SEQUENTIAL tras DISC-001)
    └─ EXEC-001   implementation      (SEQUENTIAL tras SPEC-001 EXECUTION_READY + autorización)

  WI-101 ─┐
  WI-102 ─┴→ WI-103      (WI-103 SEQUENTIAL tras ambos; WI-101 y WI-102 PARALLEL)
```

| Relación | Significa |
|---|---|
| `SEQUENTIAL` | B empieza cuando A termina o alcanza un estado dado |
| `PARALLEL` | Pueden avanzar a la vez sin fronteras compartidas |
| `CONDITIONAL` | B sólo existe o sólo sigue si A da un resultado dado (p. ej. EXEC sólo si DIAG demuestra la causa) |

- Los nodos `DISC-`, `SPEC-`, `EXEC-`, `DIAG-` son etiquetas locales del grafo, no artefactos ni tickets.
- Dos nodos son `PARALLEL` sólo si no comparten archivos, contratos ni recursos; si los comparten, es `SEQUENTIAL` o `SHARED_RESOURCE`.
- No hay locking, no hay scheduler y **no hay persistencia**: el grafo vive en el assessment o en la sesión. No se afirma lo contrario.

## 3. Blockers

`BLOCKED` sólo no dice qué hacer. Cada blocker se tipa y lleva su alcance:

| Tipo | Se desbloquea con |
|---|---|
| `BLOCKED_BY_DECISION` | Una decisión humana (`DECISION_REQUIRED`) |
| `BLOCKED_BY_DEPENDENCY` | Que otra dependencia pase a `SATISFIED` |
| `BLOCKED_BY_EVIDENCE` | Discovery, diagnóstico o datos |
| `BLOCKED_BY_EXTERNAL_SYSTEM` | Que un tercero o sistema externo responda |
| `BLOCKED_BY_AUTHORIZATION` | Una autorización explícita |
| `BLOCKED_BY_CONFLICT` | Resolver una contradicción entre fuentes o entre trabajos concurrentes |
| `BLOCKED_BY_CAPACITY` | Capacidad o WIP disponible (la prioridad la decide el owner) |

```
BLOCKER
  TYPE:            <tipo>
  CAUSE:           <qué lo bloquea, con evidencia>
  BLOCKING_SCOPE:  <qué parte del trabajo>
  CAN_CONTINUE:    <qué parte sigue avanzando> | NOTHING
  UNBLOCKED_BY:    <qué o quién lo desbloquea>
```

Siempre se indica `BLOCKING_SCOPE`. Un blocker parcial no congela el trabajo independiente: se sigue con lo que no depende de él y se reporta el bloqueo. En Kanban el item bloqueado sigue visible y marcado (`work-item-flow.md` §2).

## 4. Origen

La identificación de trabajo paralelizable ("archivos distintos, sin dependencias pendientes") y el orden por dependencias se contrastaron con `tasks` e `implement` de GitHub Spec Kit (@67e0f72), como referencia. Aquí se aplica a work items y capabilities, no a tareas por archivo: la descomposición en tareas de implementación es de `specification` (Etapa 06) y su ejecución, de `implementation`.
