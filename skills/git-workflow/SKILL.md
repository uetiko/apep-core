---
name: git-workflow
description: Determina el flujo Git que corresponde a un work item antes y después de implementarlo — rama actual vs. rama esperada (base, tipo y nombre de la work branch, destino del PR) — y prepara mensaje de commit, cuerpo de Pull Request y propuesta de versión SemVer, verificando primero qué estándar de flujo declara el repositorio en curso (y aceptando que puede no declarar ninguno). Úsalo antes de implementar en un repositorio (branch preflight), al preparar un commit o un PR, al proponer una versión/tag, o mediante /skill:git-workflow. PREPARA y PROPONE; no ejecuta por sí mismo commit, push, merge, rebase, tag, creación de rama ni publicación de PR — esas operaciones conservan el gate de la política de autoridad Git y de la configuración de aprobación del proyecto. No revisa PRs (pr-review) ni correctness (implementation-review).
---

# Git Workflow

Este skill es el **modelo genérico de flujo Git**: cómo decidir si existe un estándar de ramas aplicable a un repositorio, cómo determinar la rama esperada a partir de él, y cómo preparar commits, Pull Requests y propuestas de versión. Su producto son **determinaciones y artefactos preparados**: qué rama corresponde, qué mensaje de commit, qué cuerpo de PR, qué versión se propone. Nunca la ejecución de una operación Git gateada.

No contiene nombres de ramas permanentes ni un GitFlow propio: esos datos pertenecen a la gobernanza de cada repositorio, o a una capa de organización que componga este skill.

```
THE REPOSITORY DECLARES ITS BRANCH MODEL.
APPROVAL POLICY DEFINES AUTHORITY.
```

## 0. Cuándo usarlo y cuándo no

**Usarlo:** antes de modificar un repositorio (§4, branch preflight) · al terminar una implementación, para preparar commit y PR (§6, §7) · al preparar una integración o release, para proponer versión (§8).

**No usarlo para:** revisar un PR existente (`pr-review`) · evaluar correctness (`implementation-review`) · decidir alcance, prioridad o readiness del work item (`project-management`) · ejecutar operaciones Git gateadas por iniciativa propia.

Un repositorio puede tener su propio procedimiento de reconciliación mecánica de ramas como parte de su capability de ciclo de vida de PRs; este skill no define ni exige ninguno.

Proporcionalidad: un preflight es un bloque de pocas líneas, no un documento. Si el work item, la rama y el destino son evidentes y coinciden, el resultado es `BRANCH_STATUS: MATCH` y se sigue.

## 1. Precedencia y aplicabilidad — leer antes que nada

```
WORKSPACE GOVERNANCE        (gobernanza de ingeniería, AGENTS.md, reglas del proyecto)
  → REPOSITORY GOVERNANCE    (p. ej. <repo>/AGENTS.md o <repo>/IA.md, cuando define flujo Git propio)
    → GIT WORKFLOW           (este skill: mecanismo genérico)
      → TASK CONTRACT
        → IMPLEMENTATION
```

Branch naming, formato de commit, Pull Requests, releases, tags, versionado y hotfix son `REPOSITORY GOVERNANCE`: este skill **no declara un estándar vigente en todo repositorio**. Su aplicabilidad se establece repositorio por repositorio, con evidencia:

| `POLICY_APPLICABILITY` | Cuándo | Consecuencia |
|---|---|---|
| `REPOSITORY_DECLARED` | La gobernanza del repositorio declara un modelo de ramas y flujo | Se aplica. Si el repositorio define algo distinto de lo que este skill sugiere, **manda el repositorio** y la diferencia se reporta |
| `HUMAN_DECIDED` | El task contract o el owner declaran explícitamente qué modelo sigue el repositorio | Se aplica |
| `STRUCTURAL_EVIDENCE` | Git de sólo lectura del propio repositorio (`git branch -r`, `git ls-remote --heads`) muestra ramas permanentes y convenciones de nombre consistentes con un modelo identificable | Se aplica como `INFERENCE` declarada; las discrepancias puntuales se reportan |
| `UNVERIFIED` | Ninguna de las anteriores | Se puede **preparar** (mensajes, cuerpo de PR) marcando la aplicabilidad como no verificada; toda determinación que lleve a una operación Git (base, destino, nombre de rama) se presenta como `PROPOSAL` y se pide confirmación |

### 1.1 `UNVERIFIED` es un resultado válido, no un error

Cuando no existe un modelo de ramas declarado por el repositorio, el resultado por defecto y enteramente válido es:

```
POLICY_APPLICABILITY: UNVERIFIED
BRANCH_STATUS:        UNKNOWN
```

No es un estado de fallo: es el default honesto para un repositorio sobre el que este harness genérico no tiene conocimiento previo. En ese estado:

- no se asume ningún nombre de rama protegida, de integración ni de release;
- no se sustituye en silencio la ausencia de un dato por una convención «habitual»;
- se puede continuar con trabajo que no dependa de la rama (preparar texto de commit, PR draft) y se pide confirmación para todo lo que sí dependa de ella.

La evidencia se reúne dentro del protocolo de entrada al repositorio que la gobernanza del workspace defina (si existe), del repositorio involucrado, nunca a nivel workspace (un workspace multi-repo no es un repositorio Git) y nunca trasladando lo observado en un repositorio a otro.

## 2. Modelo de ramas — patrón, no valores

Las ramas **permanentes** (integración, estabilización, producción) son las que la gobernanza del repositorio declara. Este skill no las enumera.

**De trabajo** — el patrón es genérico; base y destino salen de la gobernanza del repositorio (consulta su `BRANCH_PREFLIGHT`, §4):

| Tipo | Patrón | Base | PR hacia |
|---|---|---|---|
| Funcionalidad | `feature/<ID>/<titulo-kebab>` | lo que la gobernanza del repositorio declare | lo que la gobernanza del repositorio declare |
| Corrección de defecto (no hotfix) | `fix/<ID>/<titulo-kebab>` o `bugfix/<ID>/<titulo-kebab>` | lo que la gobernanza del repositorio declare | lo que la gobernanza del repositorio declare |
| Urgencia en producción | `hotfix/<ID>/<titulo-kebab>` | lo que la gobernanza del repositorio declare | lo que la gobernanza del repositorio declare |

- `<ID>` es el identificador real del work item. **Nunca se inventa** (§5).
- `<titulo-kebab>`: título del work item en minúsculas, palabras separadas por guiones, sin espacios. Si el repositorio ya muestra una convención observable (p. ej. normalización de acentos), se sigue; si no, se propone ASCII.
- **`fix/` y `bugfix/` son alias funcionales** salvo que el repositorio declare una diferencia: ambos corrigen defectos no-hotfix y siguen el mismo flujo. No se les atribuye semántica distinta. Si el work item, el repositorio o el equipo ya usan uno de los dos, se sigue ese; si no, cualquiera es válido.
- Si el repositorio usa otra taxonomía de prefijos, manda el repositorio.

**Worktree de ejecución.** En trabajo `FORMAL` (y en `LIGHT` cuando el checkout no es seguro), la work branch se trabaja en un worktree dedicado, siguiendo `skill://delivery-lifecycle/references/execution-preflight.md`. No es otro tipo de rama: es dónde vive la work branch normal. Crear el worktree con `-b` es crear la rama y exige la autorización de §3; además `git worktree add`/`remove` pueden tener gate en la capa de herramientas y los ejecuta la Main Session, no un subagent headless. Borrarlo no borra la rama.

Cada integración entre ramas permanentes (merge, promoción, sincronización) es una **operación gateada** (§3). Este skill sabe cuál corresponde según el modelo declarado; no la ejecuta.

## 3. Autoridad Git

| Operación | Política | Capa de herramienta |
|---|---|---|
| `status`, `diff`, `log`, `show`, `branch -r`, `ls-remote`, `describe`, `tag -l`, `fetch` (sin refspec destino ni `--force`) | **Autónoma** — evidencia | Depende de la configuración del proyecto |
| Crear la work branch, `switch`/`checkout` a ella | Requiere autorización del task contract o del usuario | Puede no preguntar |
| `add` (staging) | Sólo como parte de un commit autorizado | Puede no preguntar |
| `commit`, `amend` | Requiere autorización | Depende de la configuración |
| `push`, `pull`, `merge`, `rebase`, `cherry-pick`, `revert`, `reset`, `tag` | Requiere autorización | Depende de la configuración |
| Crear/publicar el PR en el remote | Requiere autorización | Depende de la configuración y del provider |

```
POLICY_PERMITS != TOOL_LAYER_AUTO_APPROVES
```

La capa de herramientas puede no detenerte; la política sí. Que `git switch -c` no abra un diálogo no lo autoriza. Una autorización vale cuando está escrita en el task contract (`AUTHORIZED_DECISIONS`, p. ej. *"crear `feature/<ID>/<titulo>` desde `<base>` y trabajar en ella"*) o la da el usuario explícitamente para esa operación. Autorizar la implementación no autoriza commit, push ni PR; autorizar un commit no autoriza push; autorizar un push no autoriza merge.

**PREPARAR != EJECUTAR.** El agente puede preparar de forma autónoma mensajes de commit, cuerpos de PR, propuestas de versión y el comando exacto que haría falta. Ejecutar cualquier operación de escritura, publicación o reescritura de historia es un gate separado, con su propia autorización. La conveniencia técnica nunca es autorización.

## 4. Branch preflight — antes de implementar

Anti-patrón que este paso existe para impedir:

> *"Estoy en una rama cualquiera, así que implemento aquí."*

Antes de la primera escritura en un repositorio, determina con Git de sólo lectura y con el work item:

```
BRANCH_PREFLIGHT
  REPOSITORY:            <repo>
  POLICY_APPLICABILITY:  REPOSITORY_DECLARED | HUMAN_DECIDED | STRUCTURAL_EVIDENCE | UNVERIFIED
  WORK_ITEM_ID:          <ID> | MISSING
  WORK_TYPE:             feature | fix | bugfix | hotfix | UNDETERMINED   (tipo de rama; distinto de WORK_ITEM_CLASSIFICATION de project-management)
  CURRENT_BRANCH:        <git branch --show-current>
  WORKING_TREE:          clean | dirty (PREEXISTING_CHANGE: …)
  EXPECTED_BASE:         <rama> | MISSING_DATA
  EXPECTED_WORK_BRANCH:  <patrón resuelto> | MISSING_DATA
  PR_TARGET:             <rama> | MISSING_DATA
  BRANCH_STATUS:         MATCH | ON_PERMANENT_BRANCH | OTHER_WORK_BRANCH | UNKNOWN
  GIT_ACTIONS_AUTHORIZED: <lo que el contrato o el usuario autorizan, literal> | NONE
  NEXT_GIT_ACTION:       NONE | AUTHORIZATION_REQUIRED: <comando exacto propuesto>
```

| `BRANCH_STATUS` | Qué haces |
|---|---|
| `MATCH` — ya estás en la work branch esperada | Continúa. |
| `ON_PERMANENT_BRANCH` — una rama permanente que la gobernanza del repositorio declara | **No implementes ahí.** Si crear/cambiar a la work branch está autorizado, hazlo y continúa; si no, propón el comando exacto y pide autorización. |
| `OTHER_WORK_BRANCH` — rama de otro work item | No mezcles intenciones. Igual que el caso anterior. |
| `UNKNOWN` — falta el ID o el tipo, o el repositorio no declara un modelo de ramas (`POLICY_APPLICABILITY: UNVERIFIED`), o falta la base/destino esperados | Pide el dato o reporta la divergencia. No inventes. Es el resultado honesto por defecto (§1.1), no un error. |

Un working tree sucio con cambios ajenos **no se mueve** para poder cambiar de rama: ni stash, ni checkout forzado, ni restore. Si estorba, `STOP_REPORT`.

**Quién ejecuta el preflight.** La Main Session lo hace al preparar o aprobar el contrato, y su resultado entra en `BASELINE` (y, ya autorizada la ejecución, en el `EXECUTION_PREFLIGHT` de `delivery-lifecycle`). El agent `implementation` lo **verifica** al empezar: si `CURRENT_BRANCH` no es la rama que el contrato fija, no continúa en silencio.

## 5. Trazabilidad: el ID del work item

El ID se toma del work item, del task contract o del usuario — **nunca se inventa**, ni se usa un placeholder que parezca real. Cuando no existe ticket o historia formal, no se fabrica trazabilidad inexistente: el campo se omite o se justifica según la convención del repositorio.

| Artefacto | Con ticket | Sin ticket formal |
|---|---|---|
| **Commit** | Referencia al ID en el cuerpo, si la convención del repositorio la pide | Se omite la referencia. No se fabrica trazabilidad inexistente |
| **Pull Request** | Referencia al ID, si la convención lo pide | Justificación explícita de por qué no hay ticket, según lo que la convención del repositorio exija |
| **Rama** | `<tipo>/<ID>/<titulo-kebab>` | El patrón sin ID no está definido: preguntar, no inventar un segmento |

Si falta un ID que debería existir (el work item lo tiene pero no se conoce), pide el dato.

## 6. Commit

Detalle, tipos, cuerpo y ejemplos: `skill://git-workflow/references/commit-message.md`.

Resumen: `<tipo>(<componente-opcional>): <descripción, imperativo, ≤ 72 caracteres, sin punto final>` · una intención por commit · commit atómico · comunica intención, no lista de archivos.

**El agente puede preparar el mensaje de forma autónoma. Ejecutar `git commit` requiere autorización** (§3).

## 7. Pull Request

Plantilla, reglas y ejemplo: `skill://git-workflow/references/pull-request.md`.

Resumen: título `<tipo>(<componente-opcional>): <descripción breve>` sin ID de ticket; todo PR responde *qué problema resuelve · cómo lo resuelve · cómo se prueba*; una sola intención coherente; secciones que no aplican → `N/A` + razón breve; nada de texto ceremonial.

**El agente puede preparar título, cuerpo, checklist y evidencia (incluidos los comandos de verificación realmente ejecutados). Publicar el PR requiere autorización** (§3). La revisión de un PR ya publicado es `pr-review`.

## 8. Versionado

Reglas SemVer y autoridad: `skill://git-workflow/references/versioning.md`.

Resumen: `vMAJOR.MINOR.PATCH`; la ubicación de tags y pre-releases la fija la gobernanza del repositorio (qué ramas designa como de release). **El número de versión no se decide automáticamente: lo evalúa el responsable técnico del release.** El agente analiza impacto, propone y explica; crear o publicar un tag requiere autorización (§3).

## 9. Progressive disclosure

| Tarea | Cargar |
|---|---|
| Branch preflight | `SKILL.md` |
| Preparar commit | `SKILL.md` + `references/commit-message.md` |
| Preparar PR | `SKILL.md` + `references/pull-request.md` (+ `commit-message.md` si se prepara también el commit) |
| Proponer versión / release / hotfix | `SKILL.md` + `references/versioning.md` |

## 10. Salida y paradas

Reporta sólo lo que la tarea pidió: el bloque `BRANCH_PREFLIGHT`, un `COMMIT_MESSAGE` preparado, un `PR_DRAFT`, una `VERSION_PROPOSAL`. Cada uno indica qué operación Git haría falta y si está autorizada (`NEXT_GIT_ACTION`).

Detente con `DECISION_REQUIRED` cuando: la tarea exige una base o destino de integración que el repositorio no declara · el tipo de rama no es determinable · la gobernanza del repositorio contradice lo que se pide en algo que afecta a una operación. La versión de un release nunca es una decisión del agente (§8): se entrega como `VERSION_PROPOSAL` al responsable técnico. Falta de ID: §5. Usa `STOP_REPORT` cuando el estado del repositorio impide continuar sin destruir trabajo ajeno.
