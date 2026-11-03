# Work item shaping — clasificar, dar forma, medir y recomendar formalidad

Referencia del modo *work item* de `project-management` (`SKILL.md` §6). Responde: ¿qué tipo de trabajo es? ¿qué sabemos de él y qué falta? ¿qué tamaño operativo y qué formalidad parece pedir?

```
PROJECT MANAGEMENT MANAGES THE WORK.
SPECIFICATION DEFINES THE BEHAVIOR.
DELIVERY MATERIALIZES THE CONTRACT.
```

## 1. Clasificación

`WORK_ITEM_CLASSIFICATION` se decide por **intención y evidencia**, no por el título del ticket ni por la etiqueta que trae. "Bug: agregar exportación a CSV" es una `FEATURE`; "mejora: el reporte se cae con 10.000 filas" es un `BUG`.

| Tipo | Intención | Evidencia que lo distingue | Ruta habitual |
|---|---|---|---|
| `FEATURE` | Que exista un comportamiento nuevo | Se describe algo que hoy el sistema no hace | `specification` si el comportamiento no está definido; contrato ligero si ya lo está |
| `BUG` | Que un comportamiento vuelva a ser el esperado | Hay un fallo observado: real distinto de esperado | `diagnostics` si la causa no se conoce; `implementation` con contrato si ya está diagnosticado |
| `TECHNICAL_CHANGE` | Cambio técnico sin comportamiento de producto nuevo (actualizar una dependencia, cambiar una configuración) | El efecto observable esperado es "ninguno" o es técnico | Contrato ligero; `architecture-review` si toca fronteras |
| `REFACTOR` | Cambiar estructura sin cambiar comportamiento | Se declara explícitamente comportamiento constante | Ruta técnica; `architecture-review` si cambia fronteras; exige `REFACTOR_AUTHORIZATION` (`RULES.md` 10) |
| `INVESTIGATION` | Saber algo, no cambiar nada | La salida esperada es una respuesta o un reporte | `technical-discovery` (cómo funciona) o `diagnostics` (por qué falló) |
| `INCIDENT` | Restablecer un servicio afectado ahora | Impacto activo en producción u operación | `diagnostics` y la ruta de incidente; la corrección entra después con su contrato |
| `INFRASTRUCTURE` | Crear o cambiar entornos, recursos o despliegue | Toca IaC, cloud, redes, pipelines | `architecture-review` probable; gates materiales de AWS/IaC |
| `SECURITY` | Reducir un riesgo de seguridad o cumplir un control | Vulnerabilidad, control, permiso, dato sensible | `security-review` cuando aplica; `specification` si el comportamiento cambia |
| `DOCUMENTATION` | Cambiar documentación, no comportamiento | El entregable es texto | Contrato ligero; sin pipeline formal |
| `PROCESS` | Cambiar cómo trabaja el equipo o el harness | El entregable es una política, un flujo o una herramienta de trabajo | Decisión humana; el harness evoluciona por evidencia (MANUAL §1) |
| `UNKNOWN` | No se puede determinar | — | Se explica qué evidencia falta y se pregunta sólo si bloquea el siguiente paso |

Un item puede mezclar tipos (un `BUG` que exige una `FEATURE` para corregirse bien). Se clasifica por la intención dominante y se nombra la otra; si mezclarlas cambia la ruta, es candidato a slicing (`work-slicing.md`).

Si la clasificación es materialmente ambigua, se declara `UNKNOWN` con la evidencia que falta. No se elige una por conveniencia.

La clasificación por intención **no** es el tipo de rama. `feature/`, `fix/`, `bugfix/` y `hotfix/` los decide `git-workflow` según la gobernanza del repositorio; la clasificación lo informa, no lo sustituye.

## 2. `WORK_ITEM_ASSESSMENT`

Reconstruye el work item **sólo con la evidencia disponible**:

```
WORK_ITEM_ASSESSMENT
  WORK_ITEM_ID:         <ID real | sin ticket — justificación>
  TYPE:                 <clasificación>
  TITLE:                <una línea>
  DESIRED_OUTCOME:      <qué debe llegar a ser cierto> | UNKNOWN
  VALUE_OR_REASON:      <por qué importa> | UNKNOWN
  KNOWN_SCOPE:          <lo que el item incluye explícitamente> | UNKNOWN
  OUT_OF_SCOPE:         <lo excluido explícitamente> | NONE_DECLARED
  KNOWN_ACTORS:         <quién inicia, usa, aprueba o se ve afectado> | UNKNOWN
  DEPENDENCIES:         NONE | <DEP-NNN, dependency-model.md>
  CONSTRAINTS:          NONE_DECLARED | <restricción · fuente>
  RISKS:                <WORK_RISK_PROFILE, risk-and-issue-management.md §1>
  UNCERTAINTIES:        <qué no se sabe y quién o qué puede responderlo>
  BLOCKERS:             NONE | <tipo · alcance, dependency-model.md §3>
  ACCEPTANCE_SURFACE:   <cómo se sabría, a grandes rasgos, que está hecho> | UNKNOWN
  SIZE_SIGNAL:          SMALL | MEDIUM | LARGE | TOO_LARGE_TO_EXECUTE | UNKNOWN
  CANDIDATE_SLICES:     NO_SPLIT_NEEDED | <slices, work-slicing.md>
  NEXT_CAPABILITY:      <routing-readiness.md>
  DECISIONS_REQUIRED:   NONE | <DECISION_REQUIRED>
```

- **No se completa en silencio ningún campo material.** `UNKNOWN`, `NONE_DECLARED` y `NONE` son respuestas válidas. Lo que falta se nombra, con quién o qué puede aportarlo.
- `ACCEPTANCE_SURFACE` no son criterios de aceptación: es el contorno ("el analista puede descargar el CSV filtrado"). Los `AC-NNN` los define `specification`.
- **PM no decide qué debe hacer el producto.** Si para rellenar `DESIRED_OUTCOME`, `KNOWN_SCOPE` o `ACCEPTANCE_SURFACE` hace falta fijar comportamiento que nadie decidió, el campo queda `UNKNOWN` y la ruta es `specification`, no una suposición.
- Proporcionalidad: en un micro cambio el assessment cabe en cuatro líneas (`TYPE`, `DESIRED_OUTCOME`, `SIZE_SIGNAL`, `NEXT_CAPABILITY`). No se generan campos vacíos por plantilla.

## 3. `SIZE_SIGNAL`

Una señal operacional del tamaño, no una estimación:

| Señal | Indicios |
|---|---|
| `SMALL` | Un comportamiento, un componente, sin contratos afectados, superficie de prueba acotada |
| `MEDIUM` | Varios comportamientos relacionados o varios componentes de un mismo repositorio; algún contrato interno |
| `LARGE` | Muchos comportamientos, varios contratos, dependencias, superficie de prueba amplia o radio de impacto de sistema |
| `TOO_LARGE_TO_EXECUTE` | No cabe en una unidad coherente de trabajo: no se puede verificar ni revertir como un todo, o mezcla intenciones independientes |
| `UNKNOWN` | No hay evidencia suficiente para decirlo |

Se basa en evidencia: comportamientos independientes, repositorios o componentes tocados, contratos afectados, dependencias, incertidumbre, superficie de prueba y radio de impacto. **No se convierte a horas ni a Story Points.** Los Story Points siguen siendo un dato humano opcional: si no existen, no se inventan.

`LARGE` no obliga a dividir: un item grande y coherente puede ejecutarse entero si dividirlo no aporta una unidad verificable mejor (`work-slicing.md` §2). `TOO_LARGE_TO_EXECUTE` sí exige dividir o reducir alcance antes de ejecutar.

## 4. `WORK_FORMALITY`

Recomendación de cuánta formalidad pide el trabajo. Es la misma escala que `SPECIFICATION_NEED` de `delivery-lifecycle` §4, que la consume:

| Nivel | Cuándo |
|---|---|
| `NONE` | Micro cambio local, reversible y verificable **sin comportamiento nuevo**: corrige o ajusta algo ya definido (un texto, un valor, un fallo con causa conocida). Basta un task contract ligero: objetivo, alcance, AC, rama |
| `LIGHT` | **Comportamiento nuevo acotado**, con alcance claro, riesgo limitado, varios AC y sin decisiones materiales significativas pendientes. Task contract con invariantes y AC explícitos |
| `FORMAL` | Comportamiento nuevo o material sin definir, alta incertidumbre, contratos, arquitectura, persistencia, seguridad o varias dependencias. Pipeline de `specification` |

Estas definiciones son las de `delivery-lifecycle` §4, que consume este valor como `SPECIFICATION_NEED`; no se mantienen dos escalas. `WORK_FORMALITY` recomienda **qué tipo de contrato** hace falta; no lo produce. El Execution Contract lo produce `specification`; el task contract ligero recoge el encargo y las decisiones cerradas por el humano (`SKILL.md` §1).

Se decide por el perfil de riesgo (`risk-and-issue-management.md` §1), los contratos afectados, la seguridad y la amplitud, **sin una fórmula**. Si es `FORMAL`, `NEXT_CAPABILITY` suele ser `specification`, pero la ruta real depende del caso: un `BUG` formal empieza por `diagnostics`; una necesidad formal sin `CURRENT_STATE` puede empezar por `technical-discovery`.

## 5. Origen

La separación entre forma del trabajo y comportamiento, y el contorno sin diseño ("concept, not blueprint"), se contrastaron con la extensión `assess` de GitHub Spec Kit (`shape`, `decide`, @67e0f72), como referencia y no como autoridad. Su veredicto `go | kill` lo emite el agente; aquí no: decidir qué se construye y con qué prioridad es humano (`SKILL.md` §2).
