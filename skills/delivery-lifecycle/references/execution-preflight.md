# Execution preflight — snapshot, baseline y espacio de ejecución

Referencia de `delivery-lifecycle` (`SKILL.md` §4, estado `EXECUTION_PREFLIGHT`). Responde, antes de la primera escritura productiva: ¿qué contrato exacto se autorizó? ¿sobre qué base se ejecuta? ¿dónde se escribe sin pisar nada?

```
LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT.
AUTHORIZED SNAPSHOT IS THE EXECUTION BOUNDARY.
THE EXECUTION BASELINE IS FROZEN. INTEGRATION HANDLES LATER DIVERGENCE.
```

Proporcional a `SPECIFICATION_NEED` (`SKILL.md` §3):

| | `NONE` | `LIGHT` | `FORMAL` |
|---|---|---|---|
| Snapshot | Referencia al encargo | Referencia al task contract y sus AC | Completo, con fingerprint (§1) |
| Baseline | Rama y HEAD del `BRANCH_PREFLIGHT` | Ídem + fallos preexistentes relevantes | Completo (§3) |
| Espacio de ejecución | Work branch actual si es segura | Worktree recomendado; obligatorio si el checkout no es seguro | Worktree obligatorio (§4) |

No se fabrican artefactos `FORMAL` para un trabajo `NONE` o `LIGHT`; las fronteras de autoridad son las mismas en los tres.

## 1. `AUTHORIZED_EXECUTION_SNAPSHOT`

Liga la autorización humana con la versión concreta del contrato que se ejecuta. Es un artefacto de la ejecución: vive en el contrato al worker, en `IMPLEMENTATION_RESULT` y en `DELIVERY_EVIDENCE`; no hay registro global.

```
AUTHORIZED_EXECUTION_SNAPSHOT
  execution:        <work item ID | sin ticket — justificación> — <título>
  contract:         <ruta del Execution Contract (07) | task contract en sesión>
  fingerprint:      <sha256 por archivo del contrato> | NOT_AVAILABLE (<por qué>)
  repository:       <repo>
  scope:            <SCOPE / OUT_OF_SCOPE del contrato, en referencia>
  ac_inventory:     <AC-NNN materiales del contrato> | <AC del task contract> | NONE
  authorization:    <cita literal o referencia de la autorización humana, con fecha>
  base_ref:         <rama base y commit, si se conoce>
```

**Fingerprint.** `sha256sum` de cada archivo que define el contrato, calculado al autorizar y verificado antes de escribir y antes de declarar `INTEGRATION_READY`. En `FORMAL`: `07_EXECUTION_CONTRACT.md`, el archivo de la Etapa 03 que contiene el registro `AC-NNN` (los AC se citan por ID en el 07) y el de la Etapa 08 si existe. Funciona dentro o fuera de Git; si los archivos están versionados y commiteados, se puede añadir el commit, pero el hash del contenido es lo que se compara. Un task contract que sólo existe en la conversación no tiene fingerprint: se declara `NOT_AVAILABLE (contrato en sesión)` y no se presenta una garantía que no existe.

```
AUTHORIZED CONTRACT MUTATED → AUTHORIZATION_STALE → EXECUTION MUST NOT CONTINUE
```

Si un hash no coincide, la autorización no cubre el contrato actual: la ejecución se detiene (`AWAITING_AUTHORIZATION`) hasta que el humano autorice la versión nueva. Lo ya implementado se conserva como evidencia; no se adapta en silencio al contrato nuevo.

## 2. `EXECUTION_PREFLIGHT_RESULT`

Antes de la primera escritura productiva:

| Comprobación | `BLOCKED` / `DECISION_REQUIRED` / `AUTHORIZATION_STALE` cuando |
|---|---|
| Contrato | No existe, o en `FORMAL` no es `EXECUTION_READY` → `BLOCKED` |
| Autorización | No consta autorización humana de ejecución (`EXECUTION_READY != AUTHORIZED_TO_EXECUTE`) → `BLOCKED` |
| Fingerprint | No coincide con el autorizado → `AUTHORIZATION_STALE` |
| Repositorio y su gobernanza | No identificado, o su gobernanza local no se leyó (`.omp/AGENTS.md` §4) → `BLOCKED` |
| Rama y base | `BRANCH_PREFLIGHT` sin `MATCH` y sin autorización para crear o cambiar la work branch (`git-workflow` §4) → `BLOCKED` |
| Estado del checkout | Cambios ajenos en el checkout donde se escribiría y no hay espacio aislado posible (§4) → `BLOCKED` |
| Trabajo en conflicto | Otra ejecución escribe sobre la misma rama o los mismos archivos → `BLOCKED` |
| Baseline | No puede establecerse la base (§3) → `BLOCKED` |
| Tooling | La verificación que el contrato exige no puede ejecutarse localmente → `DECISION_REQUIRED` (continuar sin ella, o proveerla) |
| Decisión | Cualquiera de lo anterior exige elegir entre opciones materiales → `DECISION_REQUIRED` |

```
EXECUTION_PREFLIGHT_RESULT
  result:            PASS | BLOCKED | DECISION_REQUIRED | AUTHORIZATION_STALE
  snapshot:          <§1>
  baseline:          <§3>
  workspace:         <§4>
  blocking_reasons:  NONE | <comprobación · evidencia>
```

Sólo con `PASS` hay escritura productiva. Si el espacio de ejecución es obligatorio (§4) y todavía no existe, el preflight no da `PASS` hasta que existe: cuando quien ejecuta es la Main Session, lo crea como parte del preflight (con su gate) y emite el resultado después; cuando es el orchestrator, el resultado es `BLOCKED` con `WORKSPACE_PENDING: <comando propuesto>` y el lifecycle queda en `AWAITING_AUTHORIZATION` hasta que la Main Session lo crea. El preflight lo hace quien ejecuta el lifecycle con Git de sólo lectura; `implementation` lo **verifica** al empezar y no escribe si su espacio, su rama o su fingerprint no coinciden con lo que el contrato le entrega.

## 3. `EXECUTION_BASELINE`

```
EXECUTION_BASELINE
  repository:          <repo>
  remote:              <remote y URL, si aplica>
  base:                <rama base> @ <commit>
  work_branch:         <rama de trabajo>
  workspace:           <ruta del checkout o worktree>
  working_state:       clean | <cambios preexistentes y de quién>
  contract_fingerprint: <§1>
  preexisting_failures: NONE | <comando · fallo> | NOT_MEASURED (<por qué>)
  captured_at:         <fecha y hora>
```

**La baseline se congela.** Durante la implementación no se persigue una base que se mueve: si la rama base avanza, la evidencia sigue atada al commit de la baseline, y la divergencia la resuelve la integración (el PR y, si hace falta, la sincronización de `pr-review` §20). Re-basar a mitad de ejecución es una decisión, no una corrección.

Los fallos preexistentes se miden cuando es barato, ejecutando antes de editar la verificación relevante (agent `implementation`, *verification-loop*). Son la base para separar un fallo introducido de uno que ya estaba (`references/delivery-evidence.md` §1).

## 4. Espacio de ejecución

```
CONTROL CHECKOUT    → refs, fetch, observación
EXECUTION WORKTREE  → implementación del producto
```

| `SPECIFICATION_NEED` | Espacio |
|---|---|
| `NONE` | La work branch actual, si el `BRANCH_PREFLIGHT` da `MATCH` y el checkout no tiene cambios ajenos |
| `LIGHT` | Worktree recomendado; obligatorio si el checkout no es seguro (cambios ajenos, otra rama de trabajo en uso, checkout compartido) |
| `FORMAL` | Worktree obligatorio |

**Forma.** Sigue la convención ya decidida para la sincronización de `pr-review` (`<repo>/.worktrees/reconcile-pr-<id>`, `git-workflow` §2):

```
git worktree add .worktrees/exec-<ID> -b <work-branch> <base>     # rama nueva, autorizada
git worktree add .worktrees/exec-<ID> <work-branch>               # rama existente
```

- Crear el worktree **es** crear o tomar la work branch: exige la misma autorización que `git-workflow` §3 exige para crearla. Además, `git worktree add` y `git worktree remove` son una operación material con gate en `.omp/config.yml` (`git worktree*`; regresión en `.omp/tests/approvals/`, grupo `exec-worktree`): en un subagent se rechazan. Los ejecuta **la Main Session**, con la rama autorizada; en un lifecycle delegado, el orchestrator se detiene en `EXECUTION_PREFLIGHT` con el comando propuesto (`AWAITING_AUTHORIZATION`) y continúa cuando el worktree existe. Ni el orchestrator ni `implementation` lo crean ni lo borran.
- Dentro del worktree se trabaja con el parámetro `cwd` de `bash` (`.omp/AGENTS.md` §10), no con `git -C`: el gate de commit, push y merge se resuelve igual sobre el comando real.
- El directorio `.worktrees/` del checkout de control es del harness: el preflight no lo cuenta como cambio ajeno.
- Si el worktree no es practicable — el tooling del repositorio no funciona fuera del checkout principal, por ejemplo —, en `FORMAL` es `DECISION_REQUIRED`: el humano decide trabajar en el checkout principal y queda registrado como `WORKSPACE_ISOLATION_WAIVED`.

**Limpieza.** `git worktree remove .worktrees/exec-<ID>` sólo cuando se cumple todo:

- la evidencia está capturada en `DELIVERY_EVIDENCE`;
- `git status --porcelain` del worktree está vacío: no hay trabajo sin commitear;
- el handoff de integración terminó (commit hecho por quien estaba autorizado, o el humano decidió abandonar ese trabajo);
- borrar el worktree no borra la única copia de una evidencia.

La rama sobrevive al worktree. Nunca `--force`; nunca por suponer que un comando que terminó bien implica merge. Ante un estado ambiguo, el worktree se conserva y se reporta.
