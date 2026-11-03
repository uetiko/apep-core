---
name: pr-review
description: Modelo canónico de autoridad y ciclo de vida de Pull Requests / merge requests, independiente del provider — de un PR, una lista o un lote acotado — conducido por la Control Tower (Main Session). Revisa cada PR como propuesta de cambio (¿el diff es coherente con lo que el PR declara y alcanza calidad suficiente para seguir entregando?), clasifica findings (MUST_FIX / SHOULD_IMPROVE / SUGGESTION) y outcome, y materializa sólo las acciones que un humano autorizó explícitamente (publicar comentarios, aprobar, mergear), verificando cada efecto contra el estado remoto, detectando drift de revisions y sin duplicar efectos. Define el contrato genérico; la mecánica concreta contra un remote la aporta una capability de provider configurada por separado. Úsalo para revisar uno o varios PRs o conducir su ciclo completo (`/pr`, o `/skill:pr-review`). Observacional por defecto. `AUTHORIZED != ELIGIBLE`. Nunca autoaprueba, revoca approvals, toca approval rules, cierra sin merge ni resuelve conflictos funcionales. No es correctness review exhaustiva (`implementation-review`), ni revisión de autoridad (`governance-review`), de arquitectura, de seguridad ni de causa de fallos (`diagnostics`). No persigue el código ideal.
---

# PR Review

Este skill evalúa un **Pull Request (o merge request) como unidad de cambio e integración**. Su objetivo es que el cambio pueda continuar con seguridad razonable, no que alcance la perfección.

**Este skill define el contrato genérico, independiente del provider.** Describe qué evidencia hace falta, cómo se clasifican los findings, qué autoridad exige cada mutación remota y cómo se encadena el ciclo de vida. La mecánica concreta contra un remote (comandos, API, errores del servicio, sincronización, notificaciones) la aporta una capability de provider configurada por separado —p. ej. distribuida por un plugin de organización—; se aplica junto con este skill, nunca sustituyéndolo. Sin un provider configurado, este skill sigue siendo válido como metodología de revisión sobre evidencia que el humano aporte, pero no puede materializar mutaciones remotas.

## 0. Cuándo NO usar este skill

No lo actives para: revisar correctness a fondo de una implementación sin PR (`implementation-review`), revisar autoridad/alcance/gobernanza (`governance-review`), evaluar boundaries y contratos arquitectónicos (`architecture-review`), hacer revisión de seguridad, o determinar la causa de un fallo observado (`diagnostics`).

Actívalo cuando exista uno o más Pull Requests que revisar o cuyo ciclo de vida haya que conducir. Es el **único** procedimiento de ciclo de vida de PRs del harness: no existe un skill paralelo.

**Mapa del skill.** §1–§10: la revisión (evidencia, diff, findings). §11–§14: autoridad y mutaciones remotas (comentarios, approval, merge). §15–§16: outcomes y contrato de salida, incluido el reporte obligatorio de cinco columnas (§16.3). §17–§18: paradas y lotes. **§19: el ciclo de vida canónico** que encadena todo lo anterior. §20–§21: capabilities opcionales del provider (sincronización, notificaciones).

## 1. Pregunta gobernante

`¿Los cambios agregados, modificados o eliminados son coherentes con lo que el Pull Request declara hacer, y alcanzan un nivel suficiente de calidad para continuar operando y entregando?`

## 2. Invariantes

`PR_REVIEW != PR_REMEDIATION` · `MERGE_CONFLICT_DETECTED != AUTHORIZATION_TO_RESOLVE` · `REVIEW_FINDING != AUTHORIZATION_TO_PUBLISH` · `COMMENT_GENERATION != COMMENT_PUBLICATION` · `PREFERENCE != DEFECT` · `SUGGESTION != BLOCKER` · `GOOD_ENOUGH != BAD`.

Una excepción estrecha a `PR_REVIEW != PR_REMEDIATION`: una remediación autorizada, mecánica y de alcance limitado a sincronización/mergeabilidad (nunca a código funcional) puede existir como capability del provider configurado, bajo autorización humana explícita; esta skill no la define ni la ejecuta.

Sobre las mutaciones remotas (§11), dos invariantes simétricas:

> **`NO EXPLICIT AUTHORIZATION == NO REMOTE MUTATION`**
>
> **`EXPLICIT_HUMAN_AUTHORIZATION == AUTHORIZATION TO MATERIALIZE EXACTLY THAT ACTION`**

Autoridades independientes —publicar comentarios, aprobar, mergear y, si el provider las soporta, sincronizar, notificar al autor, reporte ejecutivo (§19.2)— que no se implican entre sí: `COMMENT AUTHORIZATION != APPROVAL AUTHORIZATION` · `APPROVAL AUTHORIZATION != MERGE AUTHORIZATION` · `MERGE AUTHORIZATION != REMEDIATION AUTHORIZATION` · `MERGE AUTHORIZATION != SYNC_REMEDIATION AUTHORIZATION`. `OUTCOME = APPROVE` no autoriza aprobar; `MERGEABLE = YES` no autoriza mergear; `AUTHORIZED != ELIGIBLE`.

Dos reglas rectoras:

> **`CONTINUITY OVER PERFECTION`**
>
> **`REVIEW UNTIL SAFE AND SUFFICIENT, NOT UNTIL IDEAL`**

La revisión existe para **reducir riesgo y mejorar el cambio**, no para maximizar refinamiento. Un cambio correcto, comprensible, suficientemente probado y consistente con el repositorio es un cambio aprobable aunque exista una alternativa más elegante.

Fronteras adicionales que no se conflan: `APPROVAL_RULES_SATISFIED != TECHNICALLY_CORRECT` y `TECHNICALLY_CORRECT != APPROVAL_RULES_SATISFIED`. Calidad técnica suficiente tampoco implica seguridad aprobada, arquitectura aprobada, governance aprobada, ni autorización para mergear.

## 3. Alcance de la revisión

El objeto primario es **el diff del PR**: líneas agregadas, modificadas y eliminadas, más el contexto **estrictamente necesario** para interpretarlas.

Este skill **no audita el repositorio por defecto**. Leer un archivo completo, un caller o un test es legítimo cuando hace falta para entender el diff; recorrer subsistemas no relacionados no lo es (disciplina de alcance de la gobernanza de ingeniería).

## 4. Modelo de evidencia

**El remote del provider es la fuente autoritativa del estado del PR.** Una capability de provider configurada debe poder, **en sólo lectura**:

| Capacidad de lectura | Qué devuelve |
|---|---|
| Identificar un PR por id | Su `revisionId` o identidad de revision equivalente, estado (abierto/cerrado/mergeado), título y descripción, identidad declarada del autor, referencias source/destination |
| Commits del PR | El equivalente de `sourceCommit` y `destinationCommit` (y el merge base cuando exista) |
| Diff efectivo | El contenido del diff entre destino/merge-base y source, **paginado hasta agotarse** |
| Comentarios existentes | Todos los comentarios y hilos del PR, paginados hasta agotarse |
| Estado de approval | Quién aprobó qué revision; si las reglas de aprobación del provider están satisfechas |
| Estado de override | Si alguien hizo override de las reglas de aprobación (este skill nunca lo ejecuta) |
| Estado de merge | Opciones/estrategias de merge disponibles y si existen conflictos para cada una |

Estas lecturas son los únicos insumos remotos del modelo de evidencia. Las únicas operaciones de escritura que este skill puede llegar a ejecutar —publicar comentarios, aprobar y mergear, cada una ya autorizada— viven aparte, en §11–§14.

### 4.0 Cómo recolectarla — eficiencia

`EVIDENCE_QUALITY != NUMBER_OF_ROUND_TRIPS`. Una revisión sólida no es una revisión lenta, y casi toda la evidencia de un PR es **independiente entre sí**: pedirla de una en una multiplica el tiempo sin añadir un solo finding.

La dependencia real es de tres rondas, no de diez:

```
RONDA 1   identificar el PR              -> id · revisionId · source/destination commits · repo
             |
RONDA 2   (todo esto en UNA sola tanda — nada depende de nada)
          diff efectivo · comentarios · approval state · approval rules ·
          override state · eventos del PR · opciones y conflictos de merge
             |
RONDA 3   contenido de los archivos que el diff señaló
```

Reglas:

1. **Agrupa las lecturas independientes en una sola tanda.** Encadena en serie sólo cuando el resultado de una *determina cuál es* la siguiente — en la práctica, sólo el `revisionId` (ronda 1) y la lista de archivos del diff (ronda 2).

2. **Pagina hasta el final antes de concluir.** El diff y los comentarios están paginados. Un diff parcial produce findings falsos y omite los reales: si no se agotó la paginación, el alcance está incompleto y eso se declara (§9), no se disimula.

3. **Usa el parámetro `cwd` de la tool de shell, nunca `cd <repo> && <cmd>`.** Un comando compuesto con `cd` cambia el estado del shell y puede sacar la cadena de la clasificación por segmentos de la política de aprobación: los allows por patrón dejan de aplicar y una excepción puede preguntar donde la llamada simple no lo haría. Con `cwd`, el gate se evalúa sobre el comando real.

4. **Prefiere la tool dedicada para leer código local.** Las tools de lectura/búsqueda estructuradas devuelven resultados limpios y no pasan por el gate del shell.

5. **Las lecturas remotas deben seguir siendo llamadas de herramienta simples y discretas**, no composiciones de shell. No las envuelvas en bucles, sustituciones de comandos, pipes, `&&`, `;`, redirecciones ni scripts compuestos: una cadena compuesta puede alcanzar un gate que la llamada simple no alcanza. Procesa el resultado después, y si hay varios repositorios o PRs, itera desde la lógica del agente: una llamada simple por repositorio o PR, en la misma tanda si son independientes (regla 1).

6. **Si un comando pide aprobación, no busques un rodeo.** Repórtalo y continúa cuando se apruebe. La capa de herramientas del runtime puede o no exigir confirmación para estas operaciones según la configuración del proyecto; nunca busques un rodeo si la pide — repórtalo y continúa cuando se apruebe. Reescribir la operación para eludir el gate está prohibido.

Nada de esto relaja la lista de operaciones prohibidas (§11.7), la frontera de mutación remota (§11) ni la obligación de declarar evidencia faltante (§9). Es sobre *cómo* se recoge la evidencia de lectura, nunca sobre qué se permite ejecutar.

### 4.1 Descubrimiento y baseline

Listar los PRs abiertos de un repositorio devuelve identificadores; el detalle requiere leer cada PR. La operación puede estar paginada: una página limitada no es el conjunto completo.

El baseline de un PR es: id · título · descripción · estado · identidad del autor · `revisionId` · referencias y commits de source y destination · merge base · metadata de merge. El `revisionId` es necesario para approvals; los commits gobiernan el diff.

### 4.2 Diff efectivo

El diff efectivo se calcula entre la base correcta (destination commit o merge base) y el source commit del PR. Es el objeto de la revisión (§3). **MUST NOT asumir** que la rama local equivale al PR remoto, que el `HEAD` local equivale al source commit, ni que la rama de destino local equivale al destination commit.

### 4.3 Identidad del contexto local

El repositorio local puede aportar contexto de código sólo cuando **su identidad respecto de las revisions del PR pueda establecerse con evidencia** — es decir, cuando los commits requeridos estén presentes localmente y coincidan con el source y el destination commit del PR, y la operación sea de sólo lectura. Contenido de código local no verificado contra esa identidad no es contexto confiable.

Un fetch de sólo lectura (que sólo actualiza refs remote-tracking) puede ser razonable cuando se necesita contexto local que la evidencia remota no da, **no como paso reflejo**; en cuanto se hace, sigue obligado el requisito de identidad: commits locales que coinciden, verificado, no supuesto. Las formas que escriben refs locales, fuerzan, o fusionan en el working tree (p. ej. `pull`) no son operaciones de revisión.

Si el contexto local no está disponible, continúa con la evidencia remota y **declara el límite** (§9).

Establece el baseline Git de forma independiente por repositorio y no mezcles evidencia entre repositorios.

### 4.4 Comentarios, approvals y conflictos

Comentarios existentes, estado de approval (por revision), evaluación de reglas de aprobación, estado de override, eventos del PR y estado de merge/conflictos se leen según la tabla de §4 y se anclan a la revision identificada en la ronda 1. Lo observado sobre una revision anterior no vale para la actual.

### 4.5 Operaciones prohibidas y limitación de lectura

Cada provider define su **lista de operaciones prohibidas** (nunca ejecutadas, aunque el remote las exponga): como mínimo, merge de ramas fuera del PR, cambio de estado/título/descripción del PR, override o modificación de approval rules, edición o borrado de comentarios ajenos, escritura sobre ramas y archivos fuera de lo que una capability autorizada permita. Esta skill fija la doctrina —esa lista existe, es del provider, y **ninguna autorización de esta capability habilita ninguna de esas operaciones** (§11.7)—, no la lista concreta.

Mutaciones permitidas, **cada tipo exclusivamente bajo la autorización humana explícita que lo cubre** —para un PR, una lista o un lote acotado (§11.9)— y con revalidación previa de cada PR (§11.3):

| Operación | Autoridad | Restricción |
|---|---|---|
| Publicar comentario / responder en un hilo | `COMMENT_PUBLISH_AUTHORIZATION` | §12 |
| Registrar un approval | `APPROVAL_AUTHORIZATION` | Sólo `APPROVE`; revocar nunca (§13) |
| Mergear el PR | `MERGE_AUTHORIZATION` | Siempre fijando la revision esperada; nunca con estrategia de resolución de conflictos (§14) |
| Sincronización / notificaciones | Capabilities opcionales del provider | §20, §21 |

Sin la autorización correspondiente siguen prohibidas — `NO EXPLICIT AUTHORIZATION == NO REMOTE MUTATION`.

Si una operación necesaria del provider no puede verificarse, **no inventes el comando ni asumas su respuesta**: declara la limitación y detén sólo esa dimensión (§9).

### 4.6 Evidencia de CI

Cuando un sistema de CI forma parte real del flujo, su estado puede consultarse **de sólo lectura**. **No asumas que existe CI**, no inventes la relación entre un pipeline y el PR si no puede verificarse, y **nunca dispares builds ni deploys**.

## 5. Intención declarada vs. cambio efectivo

`DECLARED_INTENT` — qué dice hacer el PR: título, descripción, tarea/specification vinculada si existe, contexto aportado por la persona, Execution Contract si se proporciona.

`EFFECTIVE_CHANGE` — qué hace realmente, según §4.2.

Mantenerlos separados es el eje de esta revisión. Si la intención declarada es demasiado vaga para evaluar coherencia, eso es en sí mismo un hallazgo, no una licencia para inventar la intención.

## 6. Qué evaluar

Proporcionalmente al cambio — no todo aplica a todo PR:

- **Coherencia con la intención:** ¿el diff implementa lo declarado? ¿falta una parte evidente? ¿hay cambio no relacionado? ¿algo eliminado contradice el objetivo?
- **Comportamiento no pretendido:** alteraciones fuera de lo declarado, código accidental, restos de depuración.
- **Calidad proporcional:** legibilidad, nombres, coherencia con el código circundante, duplicación introducida, complejidad innecesaria **creada por el propio cambio**, estructura local.
- **Manejo de errores:** razonable para el cambio, evaluado contra los contratos existentes.
- **Tests relacionados:** cuando existen, si aportan evidencia suficiente de lo que el PR afirma.
- **Convenciones:** las del repositorio primero (`skill://code-quality/SKILL.md` §1). El estilo personal del reviewer no es una convención.

**No bloquees** por una alternativa más elegante cuando el código es correcto, comprensible, suficientemente probado, consistente con el repositorio y razonable para continuar.

## 7. Relación con otras capabilities

- **`implementation-review`** (`skill://implementation-review/SKILL.md`) es la autoridad sobre **correctness**: cobertura de requisitos, corrección lógica, edge cases, riesgo de regresión, calidad probatoria de los tests, estándar de finding y `PREFERENCE != DEFECT`. Este skill **no la duplica**: cuando el PR exija evaluar correctness a fondo, aplica o consume esa metodología e incorpora sus findings. `pr-review` añade encima lo específico del Pull Request: intención declarada, metadata, source/destination, revisions, diff efectivo, comentarios existentes, approvals, conflictos, evidencia de CI y readiness a nivel de PR.
- **`code-quality`** es always-on y gobierna la calidad del código. Este skill la aplica proporcionalmente al diff; no la reescribe.
- **`git-workflow`** (`skill://git-workflow/SKILL.md`) define cómo se **preparan** rama, commits y descripción de PR. Cuando el estándar aplica al repositorio (su §1), úsalo como convención para evaluar la intención declarada, el destino del PR y la mezcla de intenciones; una desviación de plantilla es `SHOULD_IMPROVE`, salvo que impida entender qué resuelve el PR o cómo se prueba, o que la gobernanza del repositorio la haga obligatoria. Este skill no prepara PRs y `git-workflow` no los revisa.
- **`governance-review`** — si determinar si un cambio estaba autorizado exige interpretar alcance o autoridad, **deriva**; no lo resuelvas aquí.
- **`architecture-review`** — si evaluar el cambio exigiera decidir una arquitectura nueva, **no la diseñes**: deriva.
- **`security-review`** — si una observación requiere análisis de vulnerabilidad, **no la confirmes como vulnerabilidad** aquí: deriva a `skill://security-review/SKILL.md` y continúa el resto.
- **`diagnostics`** — si aparece un fallo observado cuya causa requiere análisis causal, deriva.

Registra estas señales como `REFERRED_FINDINGS`, con la evidencia observada y **sin veredicto especializado**. Nunca finjas haber completado la revisión de otra capability.

## 8. Findings y comentarios

### 8.1 Clases

| Clase | Qué es | Bloquea |
|---|---|---|
| `MUST_FIX` | Problema material: comportamiento incorrecto, contrato roto, bug evidente introducido por el cambio, test o build esencial roto, cambio accidental material, pérdida funcional, conflicto de merge, código que contradice el objetivo del PR. | **Sí** |
| `SHOULD_IMPROVE` | Mejora clara, concreta y con beneficio real: duplicación introducida, manejo de errores débil, test material ausente, nombre confuso que dificulta entender el nuevo comportamiento, complejidad evitable creada por el propio cambio. | No necesariamente |
| `SUGGESTION` | Mejora opcional: simplificación razonable, forma ligeramente más idiomática, mejora menor de legibilidad. | **Nunca** |

> **`SUGGESTION MUST NOT BLOCK APPROVAL.`**

`SHOULD_IMPROVE` exige beneficio real demostrable, no gusto personal. Si un punto no supera esa vara, es `SUGGESTION` o no es finding.

### 8.2 Detección de bugs

Los bugs son un **resultado posible** de revisar el cambio, no la misión de esta capability.

> **Si un defecto emerge razonablemente de revisar el cambio, repórtalo. No amplíes el alcance sólo para cazar defectos hipotéticos.**

Quedan excluidos: fuzzing exhaustivo, auditoría general, debugging sin síntoma, búsqueda ilimitada de defectos hipotéticos y exploración de subsistemas no relacionados.

### 8.3 Prevención de bucles de perfeccionamiento

> **Un reviewer MUST NOT crear una cadena de mejoras donde cada sugerencia opcional aceptada se convierte en la base de otra sugerencia opcional.**

Una zona ya revisada sólo genera una observación nueva si: el cambio posterior introdujo un defecto nuevo · el finding original sigue sin resolverse · existe evidencia material nueva.

No comentes de nuevo únicamente porque ahora existe una variante más elegante.

### 8.4 Comentarios

Los comentarios propuestos para el PR siguen la convención de idioma de revisión que ya establezca este repositorio (si el repositorio no muestra ninguna, usa el idioma de la conversación con el humano).

Concretos, profesionales, breves, accionables cuando corresponda y proporcionales al impacto. Estructura recomendada cuando las tres partes aporten:

```
OBSERVACIÓN: qué se ve y dónde
IMPACTO:     por qué importa
PROPUESTA:   qué haría falta, o la pregunta concreta que resuelve la duda
```

Evita `Esto está mal.` y evita convertir cada finding en un ensayo. Un `SUGGESTION` suele caber en una frase.

Redactar un comentario no es publicarlo: `COMMENT_GENERATION != COMMENT_PUBLICATION`. Cómo se propone y, si el humano lo autoriza, cómo se publica, está en §12.

### 8.5 Comentarios existentes

Los comentarios ya presentes en el PR son `EXISTING_REVIEW_CONTEXT`, **no hechos autoritativos**. Puedes señalar que un finding previo sigue vigente, que fue resuelto, que un punto ya está cubierto, o que existe discusión relevante.

**No dupliques un comentario materialmente equivalente a uno que ya existe.**

## 9. Evidencia faltante

Cuando falte evidencia material, decláralo: no se pudo determinar el diff efectivo · el contexto local no es identificable respecto de las revisions · no hay evidencia de CI verificable · una operación necesaria no está disponible o autorizada · la intención declarada es insuficiente para evaluar coherencia.

Declara **qué conclusión concreta queda limitada** y revisa el resto si puede hacerse responsablemente. **La ausencia de evidencia nunca se convierte en aprobación.**

## 10. Conflictos de merge

Detéctalos y repórtalos con la evidencia de merge de §4. Un conflicto es un **bloqueo operativo**: identifica los archivos afectados y la acción que corresponde al desarrollador, y detén cualquier pretensión de readiness.

> **El reviewer puede determinar que un Pull Request no es mergeable. No lo altera arbitrariamente para hacerlo mergeable ni resuelve decisiones funcionales.** La única excepción es la remediación mecánica de sincronización que un provider pueda definir (§20): explícita, acotada y autorizada.

Prohibido para el reviewer: resolver conflictos (tampoco recurriendo a ninguna bandera de estrategia de resolución de conflictos que el provider pudiera exponer), editar archivos, rebase, cherry-pick, modificar la rama origen o destino, crear commits, push, y mergear un PR con conflictos. Mergear un PR **ya** mergeable, tras autorización humana explícita, es otra cosa y vive en §14.

Un conflicto funcional sigue siendo un bloqueo que se reporta.

## 11. Frontera de mutación remota — modelo de autoridad

Este skill es **observacional por defecto**. Puede materializar en el remote tres mutaciones sobre el PR revisado —publicar comentarios, aprobar y mergear—, más las capabilities opcionales que el provider defina (§20, §21). Cada una exige **antes** la autorización humana explícita que le corresponde (§19.2). Todo lo demás permanece prohibido (§4.5, §10, §11.7).

```
HUMANO       → decide PUBLICAR / APROBAR / MERGEAR
PR-REVIEW    → ejecuta la acción autorizada → verifica el estado remoto → reporta evidencia
```

> **`AUTHORIZE THE DECISION, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.`**

### 11.1 Autoridades independientes

| Autoridad | La da | Cubre | Detalle |
|---|---|---|---|
| `COMMENT_PUBLISH_AUTHORIZATION` | *"publica los comentarios"* | Publicar los comentarios identificados | §12 |
| `APPROVAL_AUTHORIZATION` | *"aprueba el PR"* | Registrar `APPROVE` sobre la revision revisada | §13 |
| `MERGE_AUTHORIZATION` | *"mergea el PR"* | Mergear el PR con el método mostrado, si las precondiciones se cumplen | §14 |
| `SYNC_REMEDIATION` *(opcional, provider)* | *"sincroniza los que sólo estén desactualizados"* | Remediación mecánica de sincronización, si el provider la soporta | §20 |
| `AUTHOR_NOTIFICATION` · `EXECUTIVE_NOTIFICATION` *(opcionales, provider)* | *"avisa a los autores con MUST_FIX"* · *"manda el reporte ejecutivo"* | Notificaciones, si el provider las soporta | §21 |

```
COMMENT AUTHORIZATION  != APPROVAL AUTHORIZATION
APPROVAL AUTHORIZATION != MERGE AUTHORIZATION
MERGE AUTHORIZATION    != REMEDIATION AUTHORIZATION
```

Una autorización cubre **sólo lo que el humano expresó inequívocamente**: qué acciones, sobre qué PRs. Las acciones se combinan cuando el humano las combina: *"publica los comentarios y aprueba"* autoriza dos acciones y no el merge; *"aprueba y mergea"* autoriza approval + merge; *"publica, aprueba y mergea"*, las tres. El alcance de PRs puede ser uno, una lista o un lote acotado (§11.9).

**No se exige una fórmula ceremonial**: se interpreta lenguaje natural inequívoco. Y **no se repregunta lo ya autorizado** — ni por acción, ni por comando, **ni por PR** cuando el conjunto ya fue autorizado. Si la intención es ambigua (qué PRs, qué acciones, qué comentarios), STOP-1 (§17).

```
EXPLICIT · BOUNDED · UNAMBIGUOUS   — no necesariamente INDIVIDUAL POR COMANDO NI POR PR
MERGE_AUTHORIZATION != BLOCKER_OVERRIDE_AUTHORIZATION
```

```
OUTCOME = APPROVE   != AUTORIZACIÓN PARA APROBAR
MERGEABLE = YES     != AUTORIZACIÓN PARA MERGEAR
```

Que la revisión recomiende aprobar, o que el provider considere el PR mergeable, **nunca** dispara la acción. Tampoco una autorización dada para otro PR (fuera del conjunto autorizado) o para una revision anterior.

### 11.2 Qué es autónomo y qué no

| Paso | Autoridad |
|---|---|
| Revisar, clasificar findings, determinar outcome | Autónomo |
| Preparar `COMMENTS_TO_POST` | Autónomo |
| Determinar elegibilidad de approval y merge, preparar `MERGE_READY` | Autónomo |
| **Publicar comentarios** | **Autorización humana** |
| **Aprobar** | **Autorización humana** |
| **Mergear** | **Autorización humana** |
| Sincronizar / notificar (si el provider lo soporta) | **Autorización humana** |
| Revalidar antes de mutar y verificar el estado remoto después | Autónomo, como parte de la acción autorizada |
| Producir el reporte de cinco columnas (§16.3) | Autónomo, siempre |

### 11.3 Snapshot autorizado, revalidación y drift

La autorización se aplica a **un estado concreto de cada PR**: su `AUTHORIZED_SNAPSHOT` — el conjunto de campos con que el provider detecta que el PR cambió: identificador del PR · `revisionId` (o equivalente) · source commit · destination commit · outcome · método de merge si aplica. Es el estado que el humano tenía delante al autorizar o, cuando autorizó un conjunto o lote cuyos miembros no había visto uno a uno, el estado que esta capability revisó en la misma ejecución, justo antes de mutar (§18).

> **`REMOTE STATE MUST BE REVALIDATED BEFORE MUTATION.`**

Inmediatamente antes de **cada** mutación (publicar, aprobar, mergear) se vuelve a leer el estado del PR (§4.1) y se compara con el snapshot:

| Cambio observado | Consecuencia |
|---|---|
| El PR ya no está abierto, o ya está mergeado | STOP-7: no hay nada que mutar; se reporta el estado real |
| `revisionId` o source commit distintos | **`REMOTE_DRIFT_DETECTED`** — el código que se aprobaría o mergearía no es el revisado. STOP-4 |
| Referencias source / destination distintas de las esperadas | STOP-8 |
| Sólo avanzó el destination commit | No invalida la review del diff por sí solo, pero **re-ejecuta la evaluación de merge** (§14.2). Si cambia el resultado — aparecen conflictos, deja de estar disponible el método autorizado, cambia el diff efectivo — es drift material: STOP-4 |

```
REMOTE_DRIFT_DETECTED
  pull_request_id:    <id>
  previous_revision:  <revisionId · source commit autorizados>
  current_revision:   <revisionId · source commit actuales>
  requested_action:   PUBLISH_COMMENTS | APPROVE | MERGE
  status:             REAUTHORIZATION_REQUIRED
```

**Una autorización vieja no se aplica a código nuevo.** Tras un drift, la acción no se ejecuta **sobre ese PR**: se reporta y el humano decide sobre la revision nueva. En un lote, el PR con drift se omite (`SKIPPED_NOT_ELIGIBLE: REVISION_DRIFT`) y el resto continúa (§18).

**`DRIFT DETECTION` es un concepto con nombre propio.** Además de la revalidación previa, toda mutación debe fijar la revision esperada en el propio request —una mutación condicional—, de modo que el provider rechace del lado del servidor una carrera entre la revalidación y la mutación. **Un rechazo por snapshot obsoleto *es* drift, no una señal de reintento**: STOP-4, no un reintento automático.

### 11.4 Identidad de ejecución

Antes de la primera mutación de una tanda, la capability del provider establece **con qué identidad** se mutará (y, cuando aplique, contra qué entorno o destino). La identidad que publica, aprueba o mergea es la que el humano autorizó usar. Si la identidad o el entorno de ejecución son ambiguos y existe riesgo material de mutar el destino equivocado: STOP-3.

### 11.5 Gates de herramienta

```
AUTHORIZED PR LIFECYCLE → NO REPETITIVE TOOL APPROVALS
AUTHORIZE THE EFFECT, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.
```

La autorización humana ocurre **una vez**, al fijar `AUTHORIZED_SET` y `AUTHORIZED_ACTIONS` (§11.9, §19.2). La capa de herramientas del runtime puede o no exigir confirmación para estas operaciones según la configuración del proyecto; nunca busques un rodeo si la pide — repórtalo y continúa cuando se apruebe.

Que no haya prompt **no amplía la autoridad** (`POLICY_PERMITS != TOOL_LAYER_AUTO_APPROVES`, y su inverso): cada mutación sigue exigiendo que su clase de acción esté en `AUTHORIZED_ACTIONS` y que el PR sea elegible (`AUTHORIZED != ELIGIBLE`). Sin autorización, una operación del lifecycle no se ejecuta aunque la herramienta la dejara pasar. La frontera de autoridad es el lote, no el prompt.

Si aparece un prompt durante una mutación autorizada, **no lo eludas** —ni con otro CLI, wrapper, SDK o API menos observable— y no lo conviertas en una pregunta semántica al humano (*"¿seguro que quieres aprobar?"*). Repórtalo como hecho y continúa cuando se apruebe; si se rechaza, la acción no se ejecutó y se reporta así.

### 11.6 Atribución

La mutación se registra con la identidad disponible, que es la que el humano autorizó usar. El approval materializa **la decisión del humano**: no lo presentes como una review humana independiente realizada por otra persona, y no levantes una segunda barrera artificial después de una autorización ya concedida.

### 11.7 Qué sigue prohibido

Con autorización o sin ella, este skill **no** ejecuta: ninguna operación de la lista de prohibidas del provider (§4.5) · revocar un approval · override, creación o modificación de approval rules · aprobar un PR propio o cambiar de identidad o rol para poder aprobar (§19.4) · cerrar un PR sin merge · cambiar título o descripción de un PR existente · resolver conflictos mediante cualquier estrategia o bandera de resolución · resolver un conflicto funcional · rebase · cherry-pick · force-push · modificar source o destination fuera de lo que una capability autorizada de sincronización permita · remediation funcional · llamar a `implementation` para arreglar findings · ampliar `AUTHORIZED_SET` · crear infraestructura o identidades.

La lista concreta de operaciones prohibidas **existe y es del provider**; esta skill fija la doctrina, no los nombres.

### 11.8 Contexto delegado

Las mutaciones de §12–§14 (y las capabilities de §20–§21) se ejecutan en la **Main Session**, que es la Control Tower del ciclo (§19), donde el humano autoriza en vivo. En un subagent, que corre headless, todo comando con gate se **rechaza**. Aplicado dentro de un lifecycle delegado (`delivery-orchestrator`), este skill revisa y **prepara** (`COMMENTS_TO_POST`, `ACTIONS_AVAILABLE`, `MERGE_READY`), pero no muta: el orchestrator no ejecuta merge y el lifecycle automático termina en `INTEGRATION_READY` (`delivery-lifecycle`).

### 11.9 Alcance de la autorización: un PR, varios, un lote

Formas válidas cuando el alcance es inequívoco:

| Forma | Ejemplo | Cubre |
|---|---|---|
| **Acción única** | *"aprueba el PR 531"* | Approval de 531 |
| **Acción combinada** | *"aprueba y mergea el PR 531"* | Approval + merge de 531 |
| **Conjunto explícito** | *"aprueba y mergea los PR 501, 502, 503 y 504"* | Esas acciones sobre esos cuatro |
| **Lote acotado** | *"aprueba y mergea los PR abiertos de esta lista que estén realmente listos; omite los bloqueados"* | Esas acciones sobre los miembros del lote que resulten elegibles |

```
BATCH_AUTHORIZATION != BLANKET_UNBOUNDED_AUTHORIZATION
```

Un lote es válido cuando su conjunto **puede enumerarse de forma determinista** desde una frontera acotada: una lista de IDs · los PRs de un artefacto o lista presentada al humano · los PRs de un repositorio nombrado que cumplan criterios inequívocos acordados · un subconjunto explícitamente nombrado. El conjunto se **enumera y fija al empezar** (`AUTHORIZED_SET`) y se reporta; un PR abierto después de la enumeración no entra. *"mergea todo lo que encuentres"* no tiene frontera: STOP-1, `DECISION_REQUIRED`.

```
AUTHORIZED  → el humano permite la acción si las precondiciones se cumplen
ELIGIBLE    → el estado remoto y las reglas la permiten ahora
EJECUTAR    ⇔ AUTHORIZED && ELIGIBLE
```

Un PR autorizado pero no elegible es **`SKIPPED_NOT_ELIGIBLE`** con su blocker exacto, no `DECISION_REQUIRED` — salvo que resolver el bloqueo exija realmente una decisión humana nueva (método de merge no determinable, override de una condición explícita), y entonces `DECISION_REQUIRED` es **para ese miembro**, no para el lote. Un miembro bloqueado no invalida la autorización del resto (§18).

### 11.10 Fuentes de verdad y negativas previas del agente

```
AGENT CONCLUSION              != HUMAN DECISION
AGENT REFUSAL                 != GOVERNANCE
AGENT PREVIOUS INTERPRETATION != CLOSED DECISION
```

Una negativa anterior del propio agente —p. ej. "no puedo mergear", "dime PR por PR cuál fusiono"— basada en una versión anterior de este skill **no es una decisión persistente** (una recomendación anterior del agente no equivale a decisión). Sólo se preserva como decisión lo que realmente lo es: una decisión humana explícita, governance vigente, un contrato cerrado, o evidencia factual todavía válida.

Cuando una fuente de verdad cambia legítimamente durante la sesión —este skill, el task contract, la governance, una decisión humana— se **relee y se re-evalúa** el estado actual antes de seguir. Se distingue:

| Cambio | Tratamiento |
|---|---|
| **A.** El agente que opera modifica el skill o la policy para ganarse autoridad | Prohibido — contradicción (`DECISION_CONTRADICTION`) |
| **B.** Cambio del harness dirigido por decisión humana explícita | Nueva fuente de verdad: releer → verificar la policy vigente → operar bajo ella |

En el caso B no se arrastra la restricción antigua sólo porque existía al empezar la sesión. Pero tampoco se inventa autorización retroactivamente:

```
SKILL UPDATE   != MERGE AUTHORIZATION
PRIOR REFUSAL  != PERMANENT DENIAL
```

Ejecutar exige **ambas**: una policy vigente que soporte la acción y una autorización humana que cubra la acción y el alcance. Una petición humana explícita que el agente rechazó bajo la policy anterior sigue siendo la intención vigente si el humano la mantiene en la conversación (la repite, la referencia o pide re-evaluarla): no se le exige reformularla. Lo que no se hace es ejecutar en silencio una petición antigua que el humano ya no sostiene.

### 11.11 Mutaciones idempotentes y elegibilidad previa

Dos conceptos con nombre propio que toda mutación de este modelo cumple:

**`IDEMPOTENT_MUTATION_KEY`.** Toda solicitud de mutación debe llevar —o tener derivada— una clave determinista (p. ej. a partir del repositorio, id del PR, source commit y un ordinal local) de modo que reintentar una mutación ya aplicada **nunca duplique su efecto**. Si el provider no ofrece un token de idempotencia nativo, la idempotencia se logra comprobando antes (§19.8) si el efecto ya existe. Un source commit nuevo o un outcome materialmente distinto generan una clave nueva.

**`PRE_FLIGHT_ELIGIBILITY_CHECK`.** Antes de intentar aprobar o mergear, se pregunta al provider si la operación **tendría éxito ahora** (reglas de aprobación evaluadas, opciones y conflictos de merge, estado del PR, identidad efectiva distinta del autor) en vez de intentarla a ciegas y reaccionar al error. El resultado de esa comprobación decide `AVAILABLE` / `CONDITIONAL` / `NOT_AVAILABLE` (§15) y alimenta `MERGE_READY` (§14.4). Un rechazo posterior pese a una comprobación favorable es drift (§11.3) o un blocker nuevo, y se reporta.

## 12. Publicación de comentarios

### 12.1 Flujo

```
PR REVIEW → FINDINGS → COMMENTS_TO_POST → REVISIÓN HUMANA
  → AUTORIZACIÓN EXPLÍCITA DE PUBLICACIÓN
    → PUBLICACIÓN DE LOS COMENTARIOS AUTORIZADOS
      → VERIFICACIÓN DEL RESULTADO REMOTO
```

`COMMENTS_TO_POST` son **comentarios propuestos para revisión humana**, no una cola de ejecución: generarlos nunca dispara su publicación. Pero tampoco son *manual-only* — una vez autorizados, publicarlos es trabajo de esta capability, no tarea que se devuelve al humano para que copie comandos.

### 12.2 Por defecto: proponer, no publicar

Sin `PUBLISH_COMMENTS` autorizada, al cerrar una revisión el skill presenta `COMMENTS_TO_POST` y **no publica**. Con ella autorizada sobre un lote, rige §12.4. La propuesta debe ser lo bastante precisa para que el humano sepa exactamente qué se publicaría: un identificador corto por comentario, su ubicación (archivo y línea, o *general* si es un comentario de PR sin ubicación) y el texto literal.

No publiques por iniciativa propia, por conveniencia, porque el finding sea evidente, ni porque el humano autorizara una publicación en una revisión anterior.

### 12.3 Autorización explícita

La publicación queda autorizada cuando el humano expresa **inequívocamente** esa intención — *"publicálos"*, *"pon esos comentarios"*, *"puedes publicar estos comentarios"*, *"sí, publica ambos"*, o cualquier equivalente semántico inequívoco (§11.1).

### 12.4 Alcance de la autorización

La autorización cubre **exactamente** los comentarios que el humano vio, o cuya identidad y contenido están determinados sin ambigüedad en el contexto inmediato.

**En un ciclo de lote (§19)**, `PUBLISH_COMMENTS` autorizada sobre `AUTHORIZED_SET` cubre los comentarios que la revisión de **ese** ciclo produzca para los PR del conjunto, aunque el humano no los haya visto uno a uno. Es la misma forma que `BATCH_AUTHORIZATION` de §11.9 aplicada a comentarios. Siguen rigiendo §8.4, §8.5 y §12.6, y cada comentario publicado aparece literal en el reporte. No cubre comentarios de ciclos anteriores ni de PR fuera del conjunto. Si el humano pidió ver los comentarios antes de publicar, se presentan y se espera, como en §12.2.

`publica estos comentarios` **MUST NOT** interpretarse como autorización para: generar findings nuevos y publicarlos · publicar comentarios adicionales · cambiar el contenido sustancial de lo autorizado · aprobar el PR · mergearlo · cerrarlo · modificar título o descripción · tocar ramas · resolver conflictos · ejecutar remediation.

### 12.5 Un conjunto autorizado, una sola operación

Si el humano autoriza un conjunto claramente identificado — `publica los dos comentarios` autoriza los dos comentarios mostrados —, publícalos **en una misma operación de trabajo**.

No pidas confirmación para el comentario 1, ni para el comentario 2, ni para cada invocación mecánica necesaria para materializarlos. La autorización opera al nivel de la **intención humana** (`PUBLICAR ESTOS COMENTARIOS`), no al nivel de cada comando. Prompts de herramienta: §11.5.

### 12.6 Preservación del contenido autorizado

Publica el contenido autorizado. Las únicas transformaciones admisibles son las **mecánicas** que exige el transporte: escaping, quoting, serialización y parámetros técnicos.

**MUST NOT** cambiar en silencio la severidad, el significado, la recomendación, el tono material ni la ubicación del comentario.

Si antes de publicar descubres que el comentario necesita una modificación **sustancial** — la línea ya no existe, el finding cambió, la propuesta dejó de aplicar —, **detén esa publicación**, muestra la diferencia y pide autorización sobre la versión nueva: STOP-2 (§17).

### 12.7 Parámetros y mecánica

Los parámetros de cada publicación (repositorio, commits de referencia, ruta y posición del archivo, hilo al que se responde) se **derivan de la evidencia, no de supuestos**: el repositorio y los commits salen del estado del PR revalidado (§11.3); ruta y posición, del diff efectivo (§4.2); el hilo al que se responde, de los comentarios existentes (§4.4). Cada comentario lleva su `IDEMPOTENT_MUTATION_KEY` (§11.11) para que un reintento tras un fallo parcial no duplique uno ya publicado (§12.9). La sintaxis concreta de la operación la aporta el provider configurado; si la operación necesaria no existe o sus parámetros no pueden determinarse con evidencia, **no inventes el comando**: reporta la limitación (§9).

### 12.8 Verificación del resultado remoto

Una publicación no está completa porque la operación haya terminado sin error. Inspecciona la respuesta y, cuando aporte, confirma releyendo los comentarios del PR (§4.4).

Reporta: el PR · qué comentarios se intentaron · cuáles se publicaron · los identificadores y referencias devueltos · errores parciales · qué quedó sin publicar y por qué.

> **No declares éxito sólo porque el comando terminó.**

### 12.9 Fallo parcial

Si se autorizaron varios comentarios y uno falla: no inventes éxito · reporta cuáles se publicaron · reporta cuál falló y por qué · **no dupliques los ya publicados** al reintentar (§11.11). Pide una decisión nueva sólo si el siguiente paso cambia materialmente la acción autorizada.

## 13. Approval

### 13.1 Elegibilidad — `ACTION_AVAILABLE: APPROVE`

`APPROVE` se ofrece en `ACTIONS_AVAILABLE` (§15) **sólo** cuando se cumplen todas (verificadas con el `PRE_FLIGHT_ELIGIBILITY_CHECK`, §11.11):

- outcome `APPROVE` o `APPROVE_WITH_COMMENTS` (§15), con `MUST_FIX` = 0;
- PR abierto;
- la identidad efectiva **no** es el autor del PR — la identidad que actúa no debe aprobar su propio cambio; la capability del provider determina cómo se establece esa identidad (§19.4);
- la identidad efectiva no tiene ya un `APPROVE` sobre la revision actual (si lo tiene, no hay acción: se reporta `APPROVAL_ALREADY_PRESENT`).

`CHANGES_REQUIRED` → **no** approval. `INSUFFICIENT_EVIDENCE` → **no** approval. La clasificación de findings y outcomes (§8, §15) no se relaja para hacer un PR aprobable.

`APPROVE` como outcome de esta revisión sigue significando lo que dice §15 —no aprobación de seguridad, arquitectura ni governance—. Registrar el approval en el remote es una decisión humana que esta capability materializa; no es una certificación adicional.

### 13.2 Operación

El approval se registra **sobre la revision autorizada** (mutación condicional a esa revision, §11.3), con valor `APPROVE` únicamente: este skill **nunca** revoca (§11.7). La identidad que aprueba es la establecida en §11.4. Muchos providers no devuelven cuerpo en esta operación: su éxito no se infiere de la respuesta. Un rechazo por revision obsoleta es drift (STOP-4); por PR ya cerrado, STOP-7; por autoría, STOP-14.

### 13.3 Flujo autorizado

```
APPROVAL_AUTHORIZATION
  → revalidar (§11.3, §11.4)
  → PRE_FLIGHT_ELIGIBILITY_CHECK
  → registrar APPROVE sobre la revision autorizada
  → releer approval state sobre la misma revision
  → releer approval rules
  → reportar
```

### 13.4 Verificación

```
EXIT 0 != APPROVAL VERIFIED
```

`APPROVAL_VERIFIED` exige que la lectura del approval state sobre la **misma** revision liste la identidad efectiva con `APPROVE`. Reporta además la evaluación de reglas de aprobación (satisfechas / no satisfechas): un approval registrado no implica que las reglas del PR estén satisfechas (`APPROVAL_RULES_SATISFIED != TECHNICALLY_CORRECT`, y a la inversa).

Si el approval no aparece en la lectura posterior: `APPROVAL_UNVERIFIED`, nunca éxito.

## 14. Merge

> **El reviewer puede determinar la mergeability.**
> **El reviewer puede materializar un merge autorizado.**
> **El reviewer no altera arbitrariamente el PR para hacerlo mergeable.**

```
MODIFY A PR ARBITRARILY TO MAKE IT MERGEABLE                    → NO
SYNC-ONLY BLOCKER + SYNC AUTHORIZED (capability del provider)   → SÍ, vía lo que el provider defina (§20)
MERGE AN ALREADY MERGEABLE PR AFTER HUMAN AUTHORIZATION         → SÍ
```

### 14.1 Operaciones y estrategias

El provider ofrece una o más **estrategias de merge** (fast-forward, squash, three-way u otras). Cada una, si tiene éxito, **cierra el PR**. Reglas independientes del provider:

- La mutación de merge **fija el source commit esperado** (mutación condicional): es el guard de drift del lado servidor (§11.3).
- **Nunca** se pasa una estrategia o bandera de resolución de conflictos: el default exige que no haya conflictos. Usarla es resolver conflictos (§10, §11.7).
- El nivel de detalle de conflictos es el mismo con que se evaluó la mergeability en §14.2. **No se cambia de nivel para convertir un resultado no-mergeable en mergeable** — eso es hacer mergeable el PR.
- Mensaje de merge, nombre y correo del autor del merge: no se inventan. Se omiten (el provider usa sus defaults y la identidad de la sesión) salvo que la gobernanza del repositorio o el humano los fijen; lo que se vaya a usar se muestra en `MERGE_READY`.

Los rechazos del provider se clasifican por significado: revision/source obsoleto → drift (STOP-4) · merge manual requerido → conflicto (STOP-9) · reglas de aprobación no satisfechas → STOP-10 · PR ya cerrado → STOP-7 · el destino cambió durante el merge → revalidar, no reintentar a ciegas.

### 14.2 Elegibilidad — `ACTION_AVAILABLE: MERGE`

La mergeability **no se hereda de una review anterior**: se evalúa con las lecturas de §4 sobre el estado actual (`PRE_FLIGHT_ELIGIBILITY_CHECK`, §11.11), y se **re-evalúa inmediatamente antes del merge** (§14.5). `MERGE` se ofrece sólo con evidencia de todo esto:

| Precondición | Evidencia |
|---|---|
| PR existe y está abierto, no mergeado | Estado del PR y metadata de merge |
| Source y destination son los esperados | Referencias del PR (y el destino que designe `git-workflow` cuando aplica) |
| Revision identificada y sin drift | `revisionId` y source commit = snapshot (§11.3) |
| Review permite continuar | outcome `APPROVE` / `APPROVE_WITH_COMMENTS`, `MUST_FIX` = 0 |
| Reglas de aprobación satisfechas | Evaluación de reglas del provider: satisfechas, u overridden por otro (este skill nunca lo ejecuta) |
| Requisitos de approval de la gobernanza del repositorio | Los approvals son `REPOSITORY GOVERNANCE`; si el repositorio exige algo que el provider no modela, se verifica aparte |
| Método determinado y ofrecido por el provider | §14.3 y las opciones de merge del provider |
| Sin conflictos para ese método | Estado de conflictos para ese método: mergeable |
| Condiciones explícitas del PR cumplidas | Descripción, comentarios y eventos del PR: *"NO MERGE hasta D1–D6"*, predecesor requerido, PR de integración pendiente. Se **verifica** si se cumplen; si no, `BLOCKED_BY_PR_CONDITION` |
| Dependencias y orden | Un PR que depende de otro va después; si el predecesor no se mergeó (omitido, fallido o fuera del conjunto y abierto), el dependiente es `BLOCKED_BY_DEPENDENCY` |
| Ninguna STOP condition activa | §17 |

Si sólo falta el approval y el humano puede autorizarlo en la misma decisión, `MERGE` se muestra como `CONDITIONAL: requiere APPROVE` — no como disponible.

**Blockers explícitos y override.** Una autorización de merge —individual o de lote— **no** implica override de una condición explícita del PR: `MERGE_AUTHORIZATION != BLOCKER_OVERRIDE_AUTHORIZATION`. Ignorar una condición así exige una autorización inequívoca que la nombre (*"mergea 531 aunque D4 siga pendiente"*). Las approval rules del provider **no** tienen override en esta capability: se tratan como precondición remota (`BLOCKED_BY_APPROVAL_POLICY`) y nunca se modifican, borran ni eluden (§11.7).

### 14.3 Método de merge — no se inventa

Se determina en este orden:

1. **Gobernanza del repositorio** declara la estrategia (protocolo de entrada al repositorio) → ésa.
2. **Task contract o el humano** la declaran (*"mergea con squash"*) → ésa.
3. **El provider restringe**: sólo ofrece una opción → ésa, declarada como restricción del provider.
4. Si no → **`DECISION_REQUIRED: MERGE_METHOD`** con las opciones que el provider ofreció para este PR.

`git-workflow` **no** define estrategia de merge; el método usado en PRs anteriores es contexto, nunca decide. Si el método determinado no está entre los que el provider ofrece, no se sustituye por otro: STOP-11.

### 14.4 `MERGE_READY` — payload de autorización

Cuando el humano todavía no autorizó el merge, se le muestra este resumen compacto antes de pedírselo, para que la decisión sea informada. Cuando la autorización ya llegó —para ese PR, un conjunto o un lote— **no se vuelve a pedir**: el mismo bloque se registra por PR como evidencia en el reporte (§16.2).

```
MERGE_READY
  repository:         <repo>
  pull_request_id:    <id>
  source:             <source ref> @ <source commit>
  destination:        <destination ref> @ <destination commit>
  revision:           <revisionId>
  review_outcome:     APPROVE | APPROVE_WITH_COMMENTS
  approval_state:     <evaluación de reglas: satisfechas / no satisfechas>
  merge_method:       <método> (fuente: repositorio | humano | restricción del provider)
  commit_message:     default del provider | <texto y su fuente>
  blocking_findings:  0
  checks/evidence:    <CI verificable | no verificable (§4.6)>
  remote_state:       abierto · mergeable: true (<nivel de detalle de conflictos>) · evaluado <cuándo>
  proposed_action:    MERGE
```

La autorización de merge cubre este payload, o —si llegó antes de verlo— el payload que satisface las precondiciones de §14.2 y el método de §14.3. No se pide confirmación por cada comando posterior ni por cada PR del conjunto autorizado.

### 14.5 Flujo autorizado

```
MERGE_AUTHORIZATION
  → revalidar el estado del PR (§11.3, §11.4)
  → re-evaluar reglas de aprobación · opciones de merge · conflictos (PRE_FLIGHT_ELIGIBILITY_CHECK)
  → merge con la estrategia determinada, fijando el source commit autorizado
  → verificar (§14.6)
  → reportar
```

Si la re-evaluación ya no coincide con `MERGE_READY` —método no disponible, conflictos, reglas no satisfechas, destino distinto— no se mergea: STOP correspondiente y, si cambió lo que el humano autorizó, `REAUTHORIZATION_REQUIRED`.

**Git local nunca sustituye al merge del provider.** No se implementa un merge con `checkout` + `merge` + `push` local: la operación respeta el modelo del provider (reglas de aprobación, cierre del PR, metadata de merge). Sólo una política explícita del repositorio podría establecer otra cosa, y no se asume.

### 14.6 Verificación

```
EXIT 0 != MERGE VERIFIED
```

Después del merge, contra el remote:

- el PR figura **cerrado y mergeado**, con identificador de merge commit, estrategia igual a la autorizada y autor del merge;
- la rama destino apunta al merge commit (en fast-forward, al source commit autorizado) — si el destino ya avanzó por otro push, se reporta como tal;
- los eventos del PR, cuando aporten.

Con todo eso: `MERGE_VERIFIED`. Si la operación terminó bien pero el estado remoto no confirma el merge: **`MERGE_UNVERIFIED`**, nunca éxito.

### 14.7 Autorización combinada y éxito parcial

*"aprueba y mergea"* es **una** decisión humana que cubre dos acciones. Orden fijo, una revalidación antes de cada mutación:

```
[publicar comentarios] → revalidar → aprobar → verificar approval
                       → revalidar → mergear → verificar merge
```

Los comentarios, si están autorizados, van primero: el merge cierra el PR.

Si una acción falla o queda sin verificar, **las siguientes de ese PR no se ejecutan a ciegas**: se detiene la secuencia de ese PR y se reporta. En un lote, los demás miembros continúan (§18). **No se oculta el éxito parcial ni se deshace**: un approval verificado no se revoca porque el merge falle.

```
PR_STATE_CHANGED:
  - APPROVED
  - MERGE_FAILED
MERGE_FAILURE:       <rechazo del provider> — <regla no satisfecha>
REMOTE_FINAL_STATE:  abierto · approved por <identidad> sobre <revisionId> · no mergeado
```

Continuar después de un fallo es una decisión nueva sólo si el siguiente paso cambia materialmente lo autorizado (otro método, otra revision, resolver algo).

### 14.8 Lo que el merge no hace

No resuelve conflictos, no rebasea, no hace cherry-pick, no modifica source ni destination fuera de la propia operación de merge autorizada, no cambia el método para sortear un conflicto, no hace override de approval rules, no borra la rama origen. Si el PR necesita cambios para ser mergeable, se reporta; corregido externamente, se revisa la revision nueva (`REVIEW_FINDING != AUTHORIZATION_TO_FIX`). La excepción es un PR cuyo **único** blocker es la desincronización, con la sincronización autorizada y soportada por el provider (§20).

## 15. Outcomes y acciones disponibles

- **`APPROVE`** — no hay problemas materiales conocidos dentro del alcance revisado; el cambio es suficientemente claro, coherente y seguro para continuar **desde la perspectiva de esta revisión**. No significa perfección, ni ausencia de bugs, ni aprobación de seguridad, arquitectura o governance, ni autorización para aprobar en el remote ni para mergear.
- **`APPROVE_WITH_COMMENTS`** — el PR puede continuar, pero existen `SHOULD_IMPROVE`, `SUGGESTION` u observaciones no bloqueantes.
- **`CHANGES_REQUIRED`** — existe al menos un `MUST_FIX`.
- **`INSUFFICIENT_EVIDENCE`** — no hay evidencia suficiente para evaluar responsablemente una dimensión material.

```
MUST_FIX_PRESENT → CHANGES_REQUIRED
```

`MUST_FIX` es una **clase de finding**, nunca un outcome. El vocabulario de outcomes es exactamente el de arriba: hay consumidores (§16, §19) que dependen de él. `INSUFFICIENT_EVIDENCE` prevalece sobre `APPROVE*` cuando falta evidencia material, aunque no haya `MUST_FIX`. Si hay `MUST_FIX` **y** falta evidencia, el outcome es `CHANGES_REQUIRED` y la evidencia faltante se declara en `MISSING_EVIDENCE`.

Al cerrar una revisión, `ACTIONS_AVAILABLE` declara qué mutaciones podría materializar esta capability **si el humano las autoriza**, y por qué no las demás:

```
OUTCOME: APPROVE_WITH_COMMENTS

COMMENTS_TO_POST:
  - C1 …
  - C2 …

ACTIONS_AVAILABLE:
  - PUBLISH_COMMENTS: AVAILABLE (C1, C2)
  - APPROVE:          AVAILABLE
  - MERGE:            CONDITIONAL: requiere APPROVE (regla "<nombre>" no satisfecha) · método: DECISION_REQUIRED
  - SYNC_REMEDIATION: NOT_AVAILABLE: no hay desincronización
  - AUTHOR_NOTIFICATION: NOT_AVAILABLE: sin MUST_FIX
```

Cada entrada es `AVAILABLE` · `CONDITIONAL: <qué falta>` · `NOT_AVAILABLE: <razón>`. Listar una acción no la ejecuta (§11.1). Si el humano no responde con una autorización, `PR_STATE_CHANGED: NO`. Con varios PRs revisados, `ACTIONS_AVAILABLE` va por PR (una tabla), y el humano puede autorizar el conjunto o un subconjunto en una sola decisión (§11.9). Las acciones opcionales del provider (sincronización, notificaciones) sólo aparecen si el provider configurado las soporta.

## 16. Contrato de salida

`RESULT` · `PR` · `SUMMARY` · `MUST_FIX` · `SHOULD_IMPROVE` · `SUGGESTIONS` · `MERGE_CONFLICTS` · `APPROVALS` · `CI` · `COMMENTS_TO_POST` · `ACTIONS_AVAILABLE` · `MERGE_READY` · `POSTED_COMMENTS` · `APPROVAL_RESULT` · `MERGE_RESULT` · `REFERRED_FINDINGS` · `MISSING_EVIDENCE` · `REVIEW_SCOPE` · `PR_STATE_CHANGED` · `REMOTE_FINAL_STATE` · `PR_REVIEW_REPORT` · `CYCLE_STATE` · `BATCH_RESULT` — más los campos de las capabilities opcionales del provider (`SYNC`, `AUTHOR_NOTIFICATION`, `EXECUTIVE_NOTIFICATION`) cuando estén configuradas.

Obligatorios al cerrar: `RESULT`, `PR`, `ACTIONS_AVAILABLE`, `PR_STATE_CHANGED` y **`PR_REVIEW_REPORT` (§16.3), siempre, incluso con un solo PR**. `MISSING_EVIDENCE` es obligatorio cuando el resultado es `INSUFFICIENT_EVIDENCE` o cuando alguna conclusión quedó limitada. `POSTED_COMMENTS` (§12.8), `APPROVAL_RESULT` (§13.4), `MERGE_RESULT` (§14.6) y `REMOTE_FINAL_STATE` son obligatorios cuando se intentó la mutación correspondiente. `BATCH_RESULT` (§16.2) es obligatorio cuando la autorización cubrió más de un PR; en ese caso `PR_REVIEW_REPORT` conserva una fila por cada PR del conjunto.

### 16.1 `PR_STATE_CHANGED`

Un único campo: `NO`, o la **lista** de mutaciones intentadas con su resultado. Sin combinatoria de valores compuestos:

| Valor | Significa |
|---|---|
| `NO` | Sólo se revisó; no hubo mutación remota |
| `COMMENTS_POSTED` | Se publicaron y verificaron comentarios autorizados |
| `APPROVED` | Approval registrado y verificado (§13.4) |
| `MERGED` | Merge realizado y verificado (§14.6) |
| `COMMENTS_FAILED` · `APPROVAL_FAILED` · `MERGE_FAILED` | Se intentó y el provider lo rechazó |
| `APPROVAL_UNVERIFIED` · `MERGE_UNVERIFIED` | Se ejecutó pero el estado remoto no lo confirma |

```
PR_STATE_CHANGED:
  - COMMENTS_POSTED
  - APPROVED
  - MERGED
REMOTE_FINAL_STATE:
  status: cerrado · mergeado: true · estrategia: <método> · merge commit: <id>
  destination <rama> @ <commit>
```

`NO` y `COMMENTS_POSTED` conservan exactamente su significado. Ningún valor representa cierre sin merge ni update de metadata: esas mutaciones no existen en esta capability.

### 16.2 `BATCH_RESULT` — ejecución sobre varios PRs

Una autorización sobre varios PRs produce **un** reporte consolidado:

```
BATCH_RESULT:     COMPLETE | PARTIAL_SUCCESS | NONE_EXECUTED | STOPPED (<STOP global>)
  authorization:  <cita literal de la autorización> · acciones: APPROVE + MERGE
  authorized:     22   (AUTHORIZED_SET: <IDs enumerados y fuente>)
  attempted:      15
  approved:       15
  merged:         14
  skipped:        7
  failed:         1

PER_PR:
  - PR: 501
    revision:           <revisionId> · <source commit>
    authorization:      AUTHORIZED (lote)
    eligibility:        ELIGIBLE | SKIPPED_NOT_ELIGIBLE: <BLOCKER> | DECISION_REQUIRED: <qué>
    approval:           APPROVED | APPROVAL_ALREADY_PRESENT | APPROVAL_FAILED | NOT_ATTEMPTED
    merge:              MERGED | MERGE_FAILED | MERGE_UNVERIFIED | NOT_ATTEMPTED
    final_remote_state: <status · mergeado · merge commit>
    blocker:            <código y detalle> | —
    evidence:           <MERGE_READY / lecturas que lo sostienen>
```

Categorías genéricas de blocker por miembro: `REVISION_DRIFT` · `BLOCKED_BY_APPROVAL_POLICY` · `BLOCKED_BY_PR_CONDITION` · `BLOCKED_BY_DEPENDENCY` · `BLOCKED_BY_MERGE_CONFLICT` · `BLOCKED_BY_PENDING_REVISION` · `CHANGES_REQUIRED` · `INSUFFICIENT_EVIDENCE` · `SOURCE_TARGET_MISMATCH` · `PR_NOT_OPEN` · `SELF_APPROVAL_NOT_ALLOWED` · `MERGE_METHOD_UNDETERMINED` · `ACTION_FAILED: <COMMENTS|APPROVAL|MERGE>`. Un provider puede añadir códigos propios para sus capabilities opcionales (p. ej. sincronización), mapeándolos explícitamente a estas categorías.

`PARTIAL_SUCCESS` es un resultado válido y se declara como tal: no se oculta bajo `COMPLETE` ni bajo `FAILED` global.

`BATCH_RESULT` añade `cycle_id` y, si el provider los soporta, los resultados de sus capabilities opcionales.

### 16.3 `PR_REVIEW_REPORT` — reporte obligatorio

**Toda** ejecución de este skill termina con esta tabla, también con un solo PR y también si sólo se revisó. Tiene **exactamente cinco columnas**, en este orden, y una fila por **cada** PR de `AUTHORIZED_SET`, incluidos los omitidos, bloqueados o no revisables:

| PR | Repositorio | Autor del PR | Estado del PR | Observaciones o comentarios |
|---|---|---|---|---|
| #531 | <repo-a> | dev-a | MERGED | APPROVE · 0 findings · approval verificado · SQUASH · merge commit `a1b2c3d` |
| #532 | <repo-a> | dev-b | OPEN · CHANGES_REQUIRED | 2 MUST_FIX (validación de input en `X.php:41`; test roto) · comentarios publicados C1, C2 |
| #533 | <repo-b> | dev-c | OPEN · BLOCKED | APPROVE_WITH_COMMENTS · SELF_APPROVAL_NOT_ALLOWED: espera approval externo |
| #534 | <repo-a> | dev-d | OPEN · BLOCKED | APPROVE · BLOCKED_BY_MERGE_CONFLICT: sólo desincronización, sync no autorizada |

- **PR**: `#<id del PR>`. Un PR auxiliar, si el provider los usa, no tiene fila propia: se cita en la fila del original.
- **Autor del PR**: la identidad declarada del autor, en la forma que el provider la exponga (nombre corto o identificador legible). **Nunca** un correo.
- **Estado del PR**: estado remoto **verificado** (`MERGED`, `OPEN`, `CLOSED`) más el estado terminal del ciclo cuando el PR sigue abierto. `MERGED` sólo con `MERGE_VERIFIED`.
- **Observaciones o comentarios**: outcome · findings (`MUST_FIX` resumidos) · comentarios publicados · blockers · estado de approval · `merge commit` · fallos parciales (y resultados de capabilities opcionales del provider). Sin saltos de línea y sin el carácter `|`.

Debajo de la tabla, los contadores. Cada PR cuenta en las filas que le correspondan y la suma de categorías no se fuerza a coincidir:

```
PR revisados:                <n> de <total en AUTHORIZED_SET>
APPROVE:                     <n>
APPROVE_WITH_COMMENTS:       <n>
MERGED:                      <n>
CHANGES_REQUIRED / MUST_FIX: <n> PRs · <n> findings
BLOCKED:                     <n> (por código)
INSUFFICIENT_EVIDENCE:       <n>
Operaciones fuera de alcance: <lista | ninguna>
```

## 17. Condiciones de parada de las mutaciones

Estas condiciones detienen **la mutación afectada**, no la revisión: el resto del reporte se entrega igual. Aplican a publicar, aprobar y mergear salvo que se indique.

**Alcance de la parada en un lote.** Detienen **todo el lote** sólo: STOP-1 sobre el conjunto (autorización del conjunto ambigua o sin frontera) · STOP-3 global (identidad o entorno de ejecución) · STOP-6 global (fuentes de verdad en contradicción) · STOP-12. Todas las demás son **del miembro**: `SKIP MEMBER → CONTINUE BATCH`, con el blocker registrado (§16.2).

- **STOP-1 — Autorización ausente o ambigua.** No está claro qué PRs (conjunto no enumerable de forma determinista), qué acciones o qué comentarios autoriza el humano: no mutes, muestra lo pendiente y pide la precisión mínima necesaria.
- **STOP-2 — Cambio material del comentario.** Publicar exigiría modificar sustancialmente lo autorizado: no lo cambies en silencio, muestra la versión nueva y pide autorización sobre ella (§12.6).
- **STOP-3 — Ambigüedad sobre identidad, target o entorno de ejecución.** No puede verificarse razonablemente qué identidad o destino se usaría, y existe riesgo material de mutar el equivocado (§11.4).
- **STOP-4 — Drift de revisions.** `REMOTE_DRIFT_DETECTED`, `REAUTHORIZATION_REQUIRED` (§11.3). Incluye el rechazo del servidor a una mutación condicional por snapshot obsoleto.
- **STOP-5 — Reservada.** El modelo genérico no define esta condición; un provider configurado puede definir condiciones de parada adicionales propias de su remote y documentarlas.
- **STOP-6 — Contradicción normativa.** La gobernanza del workspace o del repositorio prohíbe materialmente la acción incluso con autorización humana explícita: no la reinterpretes ni la modifiques — `DECISION_CONTRADICTION` / `DECISION_REQUIRED`.
- **STOP-7 — PR cerrado, mergeado o superseded.** El PR ya no está abierto, ya está mergeado, o otro PR lo reemplaza: no hay nada que aprobar ni mergear; reporta el estado real.
- **STOP-8 — Source o destination inesperados.** No coinciden con el snapshot autorizado o con el destino que corresponde (el `PR_TARGET` de `git-workflow`, cuando aplica).
- **STOP-9 — Blocker, evidencia insuficiente o conflicto** *(approve, merge)*. `MUST_FIX` pendiente, outcome `CHANGES_REQUIRED` o `INSUFFICIENT_EVIDENCE`, no mergeable, merge manual requerido. Se reporta; no se resuelve.
- **STOP-10 — Requisito de approval no satisfecho** *(merge)*. Reglas de aprobación del provider o de la gobernanza del repositorio no satisfechas, sin `APPROVAL_AUTHORIZATION` que las cubra. No se aprueba implícitamente ni se hace override.
- **STOP-11 — Método de merge no determinado o no disponible** *(merge)*. `DECISION_REQUIRED: MERGE_METHOD` (§14.3) — para ese miembro; en un lote, los demás continúan. Si el humano fija el método para todo el lote, cubre a todos los miembros donde el provider lo ofrezca.
- **STOP-12 — Condición transversal** *(lote)*. Aparece algo que invalida la ejecución segura del conjunto, no de un miembro: errores de acceso o cifrado generalizados, pérdida de credenciales, el destino común cambia de forma inesperada entre merges, fallos encadenados que indican que la operación remota no es confiable. Se detiene el lote, se reporta lo ejecutado hasta ese punto y lo pendiente, y se entrega igual `PR_REVIEW_REPORT`.
- **STOP-13 — Capability opcional del provider no permitida** *(del miembro)*. Una condición que el provider defina para su sincronización o notificación (p. ej. sincronización no mecánica) → blocker con código y, si la resolución es materia reservada, `DECISION_REQUIRED`. El lote continúa.
- **STOP-14 — Autoaprobación** *(approve, del miembro)*. La identidad efectiva es la autora del PR (original o auxiliar): `SELF_APPROVAL_NOT_ALLOWED` (§19.4). Nunca se resuelve cambiando de identidad.

El fallo de una notificación (capability opcional) **no** es una STOP condition: se registra y el ciclo sigue.

## 18. Ejecución por lote

Autorizado un conjunto o lote (§11.9), **una sola autorización** gobierna toda la ejecución. No se pregunta *"¿cuál es el primer PR?"*, ni *"confirma el PR 1"*, ni *"confirma ahora el merge del mismo PR"*.

```
ENUMERAR AUTHORIZED_SET (frontera determinista, fijada al empezar)
VERIFICAR identidad/entorno de ejecución una vez (§11.4)
ORDENAR por dependencias declaradas (predecesores primero)

FOR EACH PR del conjunto:            ← el ciclo por PR de §19.1
  1. re-leer estado remoto del PR
  2. verificar revision vs snapshot (§11.3)
  3. verificar source / destination
  4. verificar review outcome (revisar la revision actual si no se revisó en esta ejecución)
  5. verificar approval requirements (reglas de aprobación, governance del repositorio)
  6. verificar dependencias / orden y condiciones explícitas del PR (§14.2)
  7. verificar que no queda ninguna STOP condition del miembro
  8. si ELIGIBLE:  ejecutar las acciones autorizadas según el routing de §19.3 → verificar resultado remoto
     si sólo falta sincronizar: §20 (si el provider lo soporta)
     si no:        SKIPPED_NOT_ELIGIBLE → registrar el blocker exacto → siguiente PR
  9. notificación al autor si aplica y el provider lo soporta (§21) → PER_PR_RESULT

CONSOLIDAR → PR_REVIEW_REPORT (§16.3) → reporte ejecutivo si está autorizado y soportado (§21) → BATCH_RESULT (§16.2)
```

```
PARTIAL ELIGIBILITY → PARTIAL EXECUTION + HONEST REPORTING
```

Ejemplo: 22 PRs autorizados — 15 elegibles, 4 bloqueados por reglas de aprobación, 2 por dependencia, 1 con drift → se ejecutan los 15, se omiten los 7 con su evidencia individual. No se detienen los 22 salvo condición transversal (STOP-12).

Reglas:

- **El blocker afecta a la elegibilidad, no a la autorización del lote.** Si se evalúa objetivamente: skip. Si resolverlo exige cambiar una decisión: `DECISION_REQUIRED` para ese miembro o subconjunto, al final, en el reporte.
- **Mergear un miembro puede cambiar a los siguientes.** Cada merge mueve el destino común: la revalidación de cada PR se hace en su turno, no con lecturas tomadas al empezar (§11.3, fila del destination commit).
- **Sin approvals de herramienta repetitivos** (§11.5): un prompt durante el lote señala una operación fuera del lifecycle o una forma no canónica, no una pregunta por PR al humano.
- **Lo que un lote nunca concede:** override de condiciones explícitas del PR, override o modificación de approval rules, resolver conflictos, ni ampliar el conjunto más allá de `AUTHORIZED_SET`.

## 19. Ciclo de vida canónico

Este skill no se limita a una revisión puntual: es el **ciclo de vida completo autorizado** de los PRs. El punto de entrada recomendado es el work mode `/pr`, que carga este skill sin añadir método ni autoridad; `/skill:pr-review` sigue disponible. Lo conduce la **Control Tower** (Main Session), que reutiliza las capabilities especializadas sin absorberlas.

```
ENTRADA:  PR individual | lista explícita | lote acotado (§11.9)
CONTROL TOWER fija:  CYCLE_ID · AUTHORIZED_SET · AUTHORIZED_ACTIONS

POR PR:
  LOAD_REMOTE_STATE → REVIEW → CLASSIFY → MATERIALIZE_RESULT
    → SYNC_IF_NEEDED (opcional, provider) → VERIFY_REMOTE → NOTIFY_IF_REQUIRED (opcional, provider) → PER_PR_RESULT

AL CERRAR EL CONJUNTO:
  CONSOLIDATE_REPORT → EXECUTIVE_NOTIFICATION (opcional, provider) → BATCH_RESULT
```

### 19.1 Fases y responsables

| Fase | Qué hace | Quién | Detalle |
|---|---|---|---|
| `LOAD_REMOTE_STATE` | Identificar el PR y las lecturas de la ronda 2; snapshot | pr-review | §4 |
| `REVIEW` | Intención declarada vs. diff efectivo; contexto mínimo | pr-review (+ `implementation-review` si hace falta correctness profunda) | §5–§7 |
| `CLASSIFY` | Findings, outcome, `MUST_FIX_PRESENT → CHANGES_REQUIRED`, elegibilidad (approve, merge, sync) | pr-review | §8, §13.1, §14.2, §15 |
| `MATERIALIZE_RESULT` | Las acciones autorizadas y elegibles según el routing de §19.3 | pr-review | §12–§14 |
| `SYNC_IF_NEEDED` | Remediación mecánica de sincronización, si el provider la soporta y está autorizada | capability del provider | §20 |
| `VERIFY_REMOTE` | Releer el remote tras cada transición material | pr-review | §19.7 |
| `NOTIFY_IF_REQUIRED` | Aviso al autor si hay `MUST_FIX`, si el provider lo soporta y está autorizado | capability del provider | §21 |
| `PER_PR_RESULT` | Fila del reporte y `PER_PR` | pr-review | §16 |
| `CONSOLIDATE_REPORT` | `PR_REVIEW_REPORT` y contadores | Control Tower | §16.3 |
| `EXECUTIVE_NOTIFICATION` | Un aviso consolidado, si el provider lo soporta y está autorizado | Control Tower | §21 |
| `BATCH_RESULT` | Resultado del conjunto | Control Tower | §16.2 |

**Control Tower**: fija y enumera `AUTHORIZED_SET` (§11.9), coordina las capabilities, mantiene el estado del ciclo (§19.5), no amplía el alcance, continúa el lote frente a blockers locales (§19.6), consolida el reporte. Sólo devuelve `DECISION_REQUIRED` ante materia reservada o una decisión que el ciclo no puede tomar (método de merge indeterminado, conflicto funcional, condición explícita del PR).

### 19.2 Acciones autorizables

| Acción | Cubre | Sin ella |
|---|---|---|
| `REVIEW` | Fases de lectura, clasificación y reporte. **Implícita** en toda invocación | — |
| `PUBLISH_COMMENTS` | Publicar los comentarios que la revisión genere (§12) | `COMMENTS_TO_POST` se presentan y no se publican |
| `APPROVE` | Approval sobre la revision revisada, si es elegible (§13) | `APPROVAL: NOT_AUTHORIZED` |
| `MERGE` | Merge con el método determinado, si es elegible (§14) | `MERGE: NOT_AUTHORIZED` |
| `SYNC_REMEDIATION` *(opcional, provider)* | Remediación mecánica de sincronización (§20) | `SYNC_REQUIRED (NOT_AUTHORIZED)` |
| `AUTHOR_NOTIFICATION` *(opcional, provider)* | Aviso al autor por PR en `CHANGES_REQUIRED` (§21) | `NOT_AUTHORIZED` |
| `EXECUTIVE_NOTIFICATION` *(opcional, provider)* | Un aviso consolidado al cerrar el ciclo (§21) | `NOT_AUTHORIZED` |

Una autorización de lote fija `AUTHORIZED_ACTIONS` una vez. Una vez autorizada una clase de acción, **no se vuelve a pedir confirmación** por comentario, PR, llamada remota, approval ni merge, y la capa de herramientas, según la configuración del proyecto, tampoco debería pedirla para los comandos del lifecycle (§11.5). Sólo conservan su gate las operaciones fuera del lifecycle.

```
AUTHORIZE THE EFFECT, NOT EVERY COMMAND REQUIRED TO MATERIALIZE IT.
AUTHORIZED != ELIGIBLE
```

Cada PR conserva sus precondiciones. Una acción autorizada pero no elegible se registra con su blocker y no se ejecuta. Si las acciones son ambiguas (p. ej. *"encárgate de los PRs"*): STOP-1 sobre lo ambiguo, y sólo `REVIEW` sobre el resto.

### 19.3 Routing por outcome

Cada paso se ejecuta sólo si su acción está en `AUTHORIZED_ACTIONS` **y** el PR es elegible en ese momento. Si un paso no aplica, se registra (`NOT_AUTHORIZED`, `NOT_ELIGIBLE: <blocker>`) y se sigue con el siguiente, salvo que dependa del anterior. Antes de cada mutación se revalida (§11.3).

| Outcome | Secuencia |
|---|---|
| **`APPROVE`** | [sync si `SYNC_REQUIRED`, §20] → revalidar → aprobar → `APPROVAL_VERIFIED` → reglas de aprobación → opciones y conflictos de merge → si es mergeable, merge → `MERGE_VERIFIED` → registrar el merge commit |
| **`APPROVE_WITH_COMMENTS`** | publicar comentarios → `COMMENT_VERIFIED` (identificadores) → [sync si `SYNC_REQUIRED`] → revalidar → aprobar → `APPROVAL_VERIFIED` → reglas de aprobación → mergeability → merge si es elegible → `MERGE_VERIFIED` |
| **`CHANGES_REQUIRED`** (hay `MUST_FIX`) | publicar los comentarios (incluidos los bloqueantes) → `COMMENT_VERIFIED` → **no aprobar · no mergear · no sincronizar** · el PR queda abierto → notificación al autor si el provider la soporta y está autorizada |
| **`INSUFFICIENT_EVIDENCE`** | Registrar `MISSING_EVIDENCE` → **ninguna mutación** (ni comentarios, approval, merge, sync ni aviso al autor) → el PR queda abierto → entra en el reporte final |

Reglas del routing:

- **Orden fijo.** Comentarios → sync → approval → merge. Los comentarios van primero porque el merge cierra el PR. La sincronización va antes del approval porque cambia la revision e invalidaría un approval previo.
- **Fallo de una mutación.** Las siguientes de **ese** PR no se ejecutan a ciegas (§14.7). Si fallan los comentarios en `APPROVE_WITH_COMMENTS`, no se aprueba ni se mergea: los comentarios forman parte de lo decidido y mergear cerraría el PR sin ellos. Se reporta `ACTION_FAILED: COMMENTS`. Un fallo parcial se rige por §12.9.
- **PR propio.** No se aprueba (§19.4). Si las reglas de aprobación ya están satisfechas por un tercero, el merge sigue siendo elegible.
- **`MERGED`** sólo con `MERGE_VERIFIED` (§14.6). Nunca por el exit code.

### 19.4 Autoaprobación

```
NEVER SELF-APPROVE.
```

La identidad que actúa debe establecerse (la capability del provider determina cómo, §11.4) y compararse con la identidad del autor del PR. Si coinciden, sea el PR original o uno auxiliar creado por el propio ciclo: **`SELF_APPROVAL_NOT_ALLOWED`**. No se cambia de identidad ni de rol, no se asume otro rol, no se tocan ni eluden las reglas de aprobación y no se usa otra vía. El PR queda `BLOCKED` esperando approval externo. El merge sólo procede si la evaluación de reglas de aprobación ya da satisfecho gracias a otro aprobador.

### 19.5 Estado del ciclo

No hay persistencia de lifecycle en el harness: el estado vive en la sesión de la Control Tower y se muestra en el reporte. Lo que no es opcional es la **semántica de transición**:

```
CYCLE_STATE
  cycle_id:           prr-<YYYYMMDD-HHMM>-<repo|multi>
  authorized_set:     <IDs enumerados · fuente>          (fijado al empezar, no crece)
  authorized_actions: <lista §19.2 · cita literal de la autorización>
  identity:           <identidad efectiva · entorno>      (§11.4, una vez)
  current_pr:         <id | —>
  per_pr_state:       <id: estado> …
  auxiliary_prs:      <aux_id → original_id · estado> …   (sólo si el provider los usa)
  notifications:      <clave → STATUS · id> …             (sólo si el provider las soporta)
  batch_result:       <pendiente | §16.2>
```

| Estado por PR | Entra cuando | Sale a |
|---|---|---|
| `RECEIVED` | PR en `AUTHORIZED_SET` | `INVENTORIED` |
| `INVENTORIED` | Estado del PR leído y snapshot fijado | `REVIEWING` · `BLOCKED` (`PR_NOT_OPEN`, refs ambiguas) |
| `REVIEWING` | Revisión en curso | `REVIEWED` |
| `REVIEWED` | Outcome fijado | `COMMENTS_PENDING` · `SYNC_REQUIRED` · `APPROVAL_PENDING` · `CHANGES_REQUIRED` · `INSUFFICIENT_EVIDENCE` · `BLOCKED` |
| `COMMENTS_PENDING` | Hay comentarios y `PUBLISH_COMMENTS` está autorizada | `COMMENTS_POSTED` · `BLOCKED` (`ACTION_FAILED: COMMENTS`) |
| `COMMENTS_POSTED` | `COMMENT_VERIFIED` | `SYNC_REQUIRED` · `APPROVAL_PENDING` · `CHANGES_REQUIRED` |
| `SYNC_REQUIRED` | Único blocker = desincronización | `SYNCING` (autorizada y soportada) · `BLOCKED` (`SYNC_REQUIRED (NOT_AUTHORIZED)`) |
| `SYNCING` | Remediación de sincronización en curso | `SYNC_VERIFIED` · `BLOCKED` (el código que defina el provider) |
| `SYNC_VERIFIED` | Sincronización verificada y original recargado | `REVIEWING` (sólo el delta, §20) |
| `APPROVAL_PENDING` | Elegible para aprobar y `APPROVE` está autorizada | `APPROVED` · `BLOCKED` |
| `APPROVED` | `APPROVAL_VERIFIED`, o approval de un tercero ya presente | `MERGE_READY` · `BLOCKED` |
| `MERGE_READY` | §14.2 completo | `MERGING` (autorizado) · terminal si `MERGE` no está autorizado |
| `MERGING` | Merge lanzado | `MERGED` · `BLOCKED` (`ACTION_FAILED: MERGE`) · `REVIEWING` (drift) |
| `MERGED` | `MERGE_VERIFIED` | `REPORTED` |
| `CHANGES_REQUIRED` | `MUST_FIX` presente; comentarios y notificación resueltos | `REPORTED` |
| `INSUFFICIENT_EVIDENCE` | Falta evidencia material | `REPORTED` |
| `BLOCKED` | Blocker con código (§16.2) | `REPORTED` |
| `REPORTED` | Fila escrita en `PR_REVIEW_REPORT` | — |

**Drift** (source commit o `revisionId` distintos del snapshot) en cualquier estado anterior a `MERGED`: la mutación en curso no se ejecuta (§11.3) y el PR vuelve a `REVIEWING` sobre la revision nueva, revisando sólo el delta (§8.3). Lo ya publicado o aprobado no se repite ni se deshace. Un approval sobre la revision vieja no cuenta para la nueva.

### 19.6 Continuidad del lote

```
A BLOCKED MEMBER NEVER CANCELS THE BATCH.
```

`CHANGES_REQUIRED`, `INSUFFICIENT_EVIDENCE`, `SELF_APPROVAL_NOT_ALLOWED`, un bloqueo de capability opcional, `BLOCKED_BY_APPROVAL_POLICY`, el fallo de una acción y el fallo de una notificación se registran y el ciclo pasa al siguiente PR. El lote completo sólo se detiene por una condición transversal (§17): `AUTHORIZED_SET` ambiguo · identidad o entorno equivocados · pérdida de credenciales · estado remoto no confiable · contradicción de gobernanza · fallo sistémico que invalide los resultados. Incluso entonces se entrega `PR_REVIEW_REPORT` con lo ejecutado y lo pendiente.

### 19.7 Verificación remota

Cada transición material se confirma **releyendo el sistema remoto**. El exit code nunca basta:

| Efecto | Verificado cuando | Sección |
|---|---|---|
| Comentario | La lectura de comentarios del PR lo contiene (identificador, contenido, ubicación) | §12.8 |
| Approval | El approval state de la misma revision lista la identidad con `APPROVE` | §13.4 |
| Merge | El PR figura cerrado y mergeado, con merge commit; la rama destino lo refleja | §14.6 |
| Efectos de capabilities opcionales | Según lo que defina el provider | §20, §21 |

```
exit 0 != COMMENT_VERIFIED · APPROVAL_VERIFIED · MERGE_VERIFIED
```

### 19.8 Idempotencia

Reintentar un ciclo, o un PR dentro de él, **no duplica efectos**. Antes de cada mutación se comprueba si ya existe (`IDEMPOTENT_MUTATION_KEY`, §11.11):

| Efecto | Comprobación previa | Si ya existe |
|---|---|---|
| Comentario | Comentarios del PR: comentario de la identidad efectiva, mismo commit de referencia y ubicación, contenido materialmente equivalente (§8.5). La clave determinista incluye repo, id del PR, prefijo del source commit y ordinal del comentario | No se publica; se reporta su identificador |
| Approval | Approval state de la revision actual | `APPROVAL_ALREADY_PRESENT` |
| Merge | Estado del PR: ya mergeado | `MERGED` con su merge commit, sin mutar |
| Efectos de capabilities opcionales | Según lo que defina el provider | Reutilizar o `DUPLICATE_SKIPPED` |

Un source commit nuevo o un outcome materialmente distinto generan una clave nueva, y el efecto puede volver a producirse.

### 19.9 Lo que el ciclo no concede

No amplía `AUTHORIZED_SET` ni `AUTHORIZED_ACTIONS`; no modifica approval rules ni permisos de identidad; no crea infraestructura ni identidades; no asume roles; no autoaprueba; no cambia reglas de negocio de la organización; no usa ningún rodeo para eludir gates; no hace commit ni push fuera de lo que una capability autorizada de sincronización permita; no cierra PRs sin merge. Todo lo de §11.7 sigue prohibido.

## 20. Sincronización con la rama destino

La sincronización mecánica de un PR desincronizado, si el provider la soporta, es una capability separada bajo autorización explícita — ver la documentación del provider configurado.

## 21. Notificaciones

El envío de notificaciones al autor o a un destinatario ejecutivo, si el provider lo soporta, es una capability separada — ver la documentación del provider configurado.
