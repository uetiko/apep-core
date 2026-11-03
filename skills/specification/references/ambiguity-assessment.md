SOURCE: harness Apep 0.5.0 — metodología propia. Adapta, sin copiar, la taxonomía de cobertura `Clear / Partial / Missing` y la heurística `Impact × Uncertainty` de GitHub Spec Kit (`templates/commands/clarify.md` @67e0f72). Spec Kit es fuente de referencia, no de autoridad.
ADAPTATION: OMP Specification Skill v0.2

# Intake, Ambiguity Assessment y clasificación de la incertidumbre

```
LINE 1 DOES NOT PRODUCE DOCUMENTS.
LINE 1 REDUCES MATERIAL DEGREES OF FREEDOM.
```

Esta referencia cubre la entrada a la Línea 1 y el análisis de ambigüedad que se repite durante todo el pipeline (`SKILL.md` §13). Se aplica en cualquier etapa en la que la evidencia exponga una apertura. No es una etapa nueva ni un documento obligatorio.

## 1. Intake normalization

`specification` acepta una entrada todavía poco refinada: una idea, una necesidad, un problema, un ticket breve, una descripción parcial, un requisito informal o una solicitud que mezcla problema y solución.

```
RAW_NEED → INTAKE_NORMALIZATION → AMBIGUITY_ASSESSMENT
```

`INTAKE_NORMALIZATION` reconstruye, **sólo con la evidencia disponible**, estos campos:

| Campo | Qué contiene | Si no hay evidencia |
|---|---|---|
| `stated_need` | La necesidad tal como se expresó (cita literal cuando exista) | — siempre existe |
| `desired_outcome` | El resultado que se espera observar cuando la necesidad esté resuelta | `UNKNOWN` |
| `known_scope` | Lo que la entrada incluye explícitamente | `UNKNOWN` |
| `known_actors` | Quién inicia, usa, aprueba o se ve afectado | `UNKNOWN` |
| `declared_constraints` | Restricciones dichas por el stakeholder o fijadas por gobernanza | `NONE_DECLARED` |
| `explicit_non_goals` | Lo que la entrada excluye explícitamente | `NONE_DECLARED` |
| `proposed_solution_if_any` | Una solución mencionada, con su estado (abajo) | `NONE` |
| `factual_unknowns` | Huecos verificables en código, configuración, runtime o documentación accesibles | `NONE` |
| `possible_material_decisions` | Aperturas que parecen exigir decisión humana | `NONE` |

No se inventa ningún campo. `UNKNOWN` y `NONE_DECLARED` son respuestas válidas y alimentan el Ambiguity Assessment.

Si la necesidad llega con un `WORK_ITEM_ASSESSMENT` de `project-management`, sus campos son evidencia de entrada del intake (forma, alcance conocido, dependencias, aperturas), no decisiones: lo que el assessment dejó `UNKNOWN` sigue siendo trabajo de este intake.

### PROBLEM ≠ PROPOSED_SOLUTION

Toda entrada se separa siempre en:

```
PROBLEM            qué ocurre, a quién, por qué importa, qué resultado se busca
PROPOSED_SOLUTION  un cómo mencionado por alguien
```

Una solución mencionada por el stakeholder tiene uno de estos estados:

| Estado | Evidencia exigida | Tratamiento |
|---|---|---|
| `CLOSED_DECISION` | Una decisión humana explícita y localizable (quién, dónde, cuándo), o gobernanza de repositorio | Se registra como `CONSTRAINT` con su fuente |
| `PROPOSAL` | Se menciona como idea, preferencia o ejemplo | Se conserva como propuesta; el problema se especifica sin depender de ella |
| `STATUS_UNKNOWN` | No se sabe si está decidida | Se trata como `PROPOSAL`. Si su estado es material, se convierte en una pregunta (`clarification-loop.md`) |

No se asume cuál de los tres aplica. "Quiero un botón que exporte a Excel" contiene un problema (necesito sacar estos datos a otra herramienta) y una propuesta (botón, formato Excel). Que el formato sea Excel es una decisión cerrada sólo si hay evidencia de que lo es.

### Dónde queda registrado

- Si la entrada es material de stakeholder sin estructurar, la normalización se registra como sección `Normalización de intake` de `01_STAKEHOLDER_DISCOVERY.md`. La Etapa 01 sigue preservando la petición original literal.
- Si el entry point es posterior (la entrada ya llega estructurada), la normalización es un bloque breve al inicio del primer artefacto que se produzca.
- Si la entrada ya está suficientemente determinada, la normalización ocupa pocas líneas y no genera preguntas. **No se ejecutan ceremonias vacías.**

## 2. Ambiguity Assessment

Evalúa doce dimensiones. Cada una se marca con un estado:

| Estado | Significa |
|---|---|
| `CLEAR` | La evidencia determina la dimensión lo suficiente para especificar sin inventar |
| `PARTIAL` | Hay evidencia, pero deja interpretaciones con consecuencias distintas |
| `MISSING` | No hay evidencia y la dimensión aplica |
| `NOT_APPLICABLE` | La dimensión no aplica a esta necesidad (se dice por qué en una línea) |

| # | Dimensión | Qué se pregunta | Señales típicas de apertura |
|---|---|---|---|
| 1 | `FUNCTIONAL_SCOPE` | ¿Qué capacidades entran y cuáles no? | "y cosas similares", alcance sin frontera, mezcla de varias necesidades |
| 2 | `ACTORS_AND_PERMISSIONS` | ¿Quién inicia, quién puede hacer qué, quién aprueba? | "el usuario" sin rol, permisos implícitos |
| 3 | `DOMAIN_RULES` | ¿Qué reglas de negocio gobiernan el comportamiento? | umbrales, plazos, cálculos o prioridades no fijados |
| 4 | `DATA_AND_STATE` | ¿Qué entidades, identidad, estados, transiciones y retención? | "guardar el histórico" sin qué, cuánto ni hasta cuándo |
| 5 | `PRIMARY_FLOWS` | ¿Cuál es el camino principal de principio a fin? | pasos sin orden o sin disparador |
| 6 | `EDGE_AND_FAILURE_CASES` | ¿Qué pasa en límites, vacíos, duplicados, fallos y concurrencia? | "manejar errores", "validar los datos" |
| 7 | `EXTERNAL_INTEGRATIONS` | ¿Con qué sistemas externos, en qué dirección y con qué fallo? | "se integra con X" sin contrato ni modo de fallo |
| 8 | `NON_FUNCTIONAL_REQUIREMENTS` | ¿Rendimiento, disponibilidad, seguridad, privacidad, observabilidad? | "rápido", "seguro", "escalable" sin significado operacional |
| 9 | `CONSTRAINTS` | ¿Qué restricciones están cerradas (tecnología, plazo, contrato, normativa)? | soluciones mencionadas con estado desconocido |
| 10 | `TERMINOLOGY` | ¿Cada término tiene un significado único y estable? | dos nombres para lo mismo, un nombre para dos cosas |
| 11 | `SUCCESS_AND_ACCEPTANCE` | ¿Cómo se sabe objetivamente que la necesidad quedó resuelta? | éxito descrito como sensación |
| 12 | `OPEN_DECISIONS` | ¿Qué decisiones humanas siguen abiertas? | materias reservadas (`ENGINEERING_GOVERNANCE.md` §1.2) sin cierre |

Una dimensión que no es `CLEAR` se clasifica además en:

| Eje | `LOW` | `MEDIUM` | `HIGH` |
|---|---|---|---|
| `IMPACT` | Cambiarla no altera qué se construye ni cómo se acepta | Altera una parte acotada del comportamiento o de su verificación | Altera alcance, reglas de negocio, contratos, datos persistidos, seguridad o aceptación |
| `UNCERTAINTY` | Una interpretación es claramente dominante según la evidencia | Hay dos interpretaciones plausibles | No hay base para preferir ninguna, o las fuentes se contradicen |

`IMPACT × UNCERTAINTY` es una **heurística de priorización, no una fórmula**: no se calculan puntuaciones. Primero `HIGH × HIGH`, después los que tienen un eje `HIGH`, después el resto. Ante empate, va antes lo que condiciona otras respuestas.

### Resultado

```
AMBIGUITY_ASSESSMENT
| DIMENSION | STATUS | EVIDENCE | IMPACT | UNCERTAINTY | MATERIAL_FOR_EXECUTION | NEXT_ACTION |
```

- `EVIDENCE`: dónde está (cita, artefacto, archivo) o por qué no hay.
- `MATERIAL_FOR_EXECUTION`: `YES` | `NO` | `AMBIGUOUS`, con el mismo criterio que C1 (`07-execution-contract.md`): es material todo lo que cambiaría qué se construye, cómo se verifica o qué contrato se preserva, y toda materia reservada.
- `NEXT_ACTION`: `NONE` · `DISCOVERY: <pregunta>` · `CLARIFY: CLAR-NNN` · `ASSUMPTION: ASM-NNN` · `DECISION_CONTRADICTION` · `DECISION_REQUIRED`.

Se omiten las filas `CLEAR` cuando no aportan; basta con listarlas en una línea. Una apertura de baja incertidumbre que se deja para una etapa posterior (p. ej. el formato de un monto, que se fijará en la Hard Specification) **no se descarta en silencio**: queda como `PARTIAL` con `NEXT_ACTION: resolver en <etapa>`, y esa etapa la cierra con evidencia, con una assumption o con una pregunta. "Ante la duda, material" (§3) se aplica cuando la etapa la resuelve; dejarla para después sólo es proporcionalidad si queda registrada. El assessment no es un documento propio: vive en el artefacto de la etapa en curso o en la conversación, y lo que queda de él son los `CLAR-NNN`, los `ASM-NNN` y las preguntas de discovery.

## 3. Clasificación de la incertidumbre

Toda apertura se clasifica **antes** de formular una pregunta:

| Clase | Significa | Ruta |
|---|---|---|
| `FACT` | Lo establece una fuente autoritativa (`ENGINEERING_GOVERNANCE.md` §16.1) | Se cita y se usa |
| `UNKNOWN` (factual) | Falta un hecho verificable en código, configuración, runtime o documentación accesibles | `technical-discovery` (§5) |
| `ASSUMPTION` | Apertura no material que cumple **todos** los criterios de §4 | Se registra `ASM-NNN` y se continúa |
| `AMBIGUITY` | La evidencia admite varias interpretaciones con consecuencias distintas | Material → `clarification-loop.md`; no material → `ASSUMPTION` |
| `CONTRADICTION` | Dos fuentes dicen cosas incompatibles | Según el subtipo (abajo) |
| `DECISION_REQUIRED` | Materia reservada sin cierre humano | `clarification-loop.md`, en formato §1.4 |

Este vocabulario es compatible con el de `technical-discovery` (`FACT` / `INFERENCE` / `HYPOTHESIS` / `UNKNOWN` / `CONTRADICTION`) y con el modelo FACT/DECISION de `SKILL.md` §3. Una `INFERENCE` o `HYPOTHESIS` nunca se promueve a `FACT` ni a decisión sin evidencia o cierre humano.

### Procedimiento de clasificación (en orden)

1. ¿Lo establece una fuente autoritativa accesible? → `FACT`.
2. ¿Es un hecho que se puede verificar en el sistema o su documentación? → `UNKNOWN` factual → discovery. **No se pregunta al humano.**
3. ¿Dos fuentes chocan? → `CONTRADICTION`.
4. ¿Cambia qué se construye, cómo se verifica o qué contrato se preserva, o es materia reservada? → material → `DECISION_REQUIRED` / clarificación.
5. ¿Cumple los ocho criterios de §4? → `ASSUMPTION`.
6. Si queda duda en cualquier paso → se trata como material.

```
DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US.
DO NOT LET THE SYSTEM DECIDE WHAT ONLY THE HUMAN MAY DECIDE.
```

### Subtipos de CONTRADICTION

| Choque | Ruta | Base |
|---|---|---|
| Una decisión humana cerrada contradice un hecho autoritativo | `DECISION_CONTRADICTION` | `ENGINEERING_GOVERNANCE.md` §16 |
| Una petición o respuesta nueva contradice una decisión humana cerrada | `DECISION_REQUIRED`: el owner decide si la sustituye. Nunca se elige una de las dos en silencio | §1.4 |
| Dos inputs de stakeholder se contradicen y ninguno es una decisión cerrada | `AMBIGUITY` material → clarificación | — |
| Dos artefactos de la spec se contradicen | Finding de coherencia (`coherence-review.md`) | — |

## 4. Política de assumptions

Una apertura sólo puede cerrarse con una assumption si cumple **todos** estos criterios. Son los de autonomía táctica de `ENGINEERING_GOVERNANCE.md` §1.3, aplicados a una especificación, más dos propios de la Línea 1:

| # | Criterio | Pregunta |
|---|---|---|
| A1 | local | ¿Afecta sólo a una parte acotada de la spec? |
| A2 | reversible | ¿Puede cambiarse después sin dejar estado ni datos inconsistentes? |
| A3 | architecturally neutral | ¿No introduce ni cambia una decisión de arquitectura? |
| A4 | externally invisible | ¿No cambia comportamiento observable por usuarios, otros sistemas u otros equipos? |
| A5 | dentro del scope | ¿Cae dentro de lo que la necesidad ya incluye? |
| A6 | sin semántica de negocio | ¿No fija una regla, umbral, plazo, cálculo, prioridad o permiso de negocio? |
| A7 | contract-preserving | ¿No crea ni cambia un contrato, API, schema, evento o formato compartido? |
| A8 | verificable | ¿Hay forma objetiva de comprobar que se respetó? |

Si un solo criterio falla o es dudoso, no es una assumption: es material y va a clarificación. **Una decisión de negocio disfrazada de assumption bloquea.**

Registro (en `Supuestos documentados` de la Etapa 03 o en `ASSUMPTIONS` del contrato 07):

```
ASM-001
ASSUMPTION:      <qué se asume>
REASON:          <por qué es razonable con la evidencia disponible>
NON_MATERIAL:    A1–A8 cumplidos · <la justificación de los que no son obvios>
VERIFICATION:    <cómo se comprueba>
REVERSAL:        <qué cambia si resulta falsa>
```

C1 vuelve a clasificar cada `ASM-NNN` en el readiness gate. Una assumption que resulte material allí bloquea `EXECUTION_READY` igual que cualquier otro item abierto.

| Ejemplo | ¿Assumption? |
|---|---|
| El identificador de correlación interno de los logs del nuevo proceso sigue el formato que ya usan los demás procesos del repositorio | Sí: local, invisible, sin negocio, verificable |
| "Se conservan los registros 90 días" | **No**: fija retención, es semántica de negocio (A6) y posiblemente normativa |
| "Si la integración externa falla, se reintenta tres veces" | **No**: comportamiento observable y semántica de fallo (A4, A6) |
| "El listado interno de administración ordena por fecha descendente" sin AC ni actor que dependa del orden | Depende: si un actor depende del orden es visible (A4) y va a clarificación; ante la duda, material |

## 5. Unknown factual → technical-discovery

```
specification → technical-discovery → FACT / UNKNOWN → specification resumes
```

- Se formula una pregunta de discovery estrecha (`TARGETED_DISCOVERY` por defecto, `skill://technical-discovery/SKILL.md` §4): "¿qué endpoint expone hoy el estado de la cuenta y qué campos devuelve?", no "explora el repositorio".
- Una pregunta estrecha se resuelve aplicando la skill en el propio contexto; un volumen grande o una frontera read-only van al agent `technical-discovery`.
- El resultado vuelve como `FACT` (con evidencia) o como `UNKNOWN` confirmado. Un `UNKNOWN` que sigue siendo material después de investigar pasa a clarificación con la evidencia de que no se pudo establecer.
- Discovery describe el `CURRENT_STATE`; no decide el `TARGET_STATE`. Que hoy el sistema haga algo no lo convierte en el comportamiento deseado (`ENGINEERING_GOVERNANCE.md` §6.1).
- Un discovery ya cerrado no se reabre sin evidencia nueva.

## 6. Cuándo se aplica

En cualquier etapa: intake, problem, hard spec, use cases, behavior, AC, tasks, acceptance tests y execution contract. Cada etapa que encuentra una apertura la clasifica en el momento, no al final.

```
AMBIGUITY SHOULD BE CLOSED AS EARLY AS THE EVIDENCE EXPOSES IT.
```
