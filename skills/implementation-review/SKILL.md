---
name: implementation-review
description: Revisa si una implementación ya realizada cumple correctamente el comportamiento esperado y está técnicamente bien resuelta dentro del contrato aprobado — cobertura de requisitos, corrección lógica, edge cases materiales, manejo de errores, riesgo de regresión, calidad probatoria de los tests y consistencia del diff. Úsalo cuando exista un cambio concreto que revisar (diff, archivos modificados, resultado de implementación, commit/rango) o mediante invocación explícita (`/skill:implementation-review`). No es el modo normal de trabajo del workspace — no se activa para entender cómo funciona un sistema (`technical-discovery`), para explicar por qué falló algo (`diagnostics`), para decidir qué debería hacer el sistema (`specification`), para revisar autoridad/alcance/gobernanza (`governance-review`), para evaluar boundaries y contratos arquitectónicos (`architecture-review`), ni como revisión de seguridad o de Pull Request. No implementa correcciones ni convierte preferencias del reviewer en defectos.
---

# Implementation Review

Este skill es un **método de revisión de correctness basada en evidencia**. Evalúa una implementación ya realizada; no la rediseña, no la corrige y no la vuelve a implementar. Su producto es una **evaluación**, no una segunda implementación.

## 0. Cuándo NO usar este skill

No lo actives para: reconstruir cómo funciona un sistema (`technical-discovery`), explicar la causa de un fallo observado (`diagnostics`), decidir o formalizar qué debería hacer el sistema (`specification` o decisión humana), revisar si un cambio respetó autoridad, alcance y reglas (`governance-review`), evaluar boundaries/ownership/dependencias/contratos arquitectónicos (`architecture-review`), hacer evaluación de seguridad, o gestionar mergeability/PR/CI.

Actívalo cuando exista **una implementación concreta susceptible de revisión** y la pregunta real sea si lo implementado es correcto.

Debe existir al menos uno de: un diff · archivos modificados conocidos · un resultado de implementación · un commit o rango, cuando esté disponible · un working tree modificado · un artefacto equivalente verificable. Sin objeto de revisión no hay revisión: pedirla sin cambio concreto es `INSUFFICIENT_EVIDENCE` (§12), no una revisión genérica del repositorio.

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE          (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE     (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → IMPLEMENTATION REVIEW   (este skill)
      → consumidor            (decisión humana / specification / implementation)
```

No es gobernanza independiente ni tiene autoridad de decisión propia. Es executor-neutral: su resultado es evidencia consumible por una decisión humana, por `specification` o por `implementation` una vez autorizada — nunca invoca automáticamente ninguna de ellas.

## 2. Pregunta gobernante

`¿La implementación realizada cumple correctamente el comportamiento esperado y está técnicamente bien resuelta dentro del contrato aprobado?`

Distinta de `technical-discovery` (¿cómo funciona realmente esto?), de `diagnostics` (¿por qué ocurrió este fallo observado?), de `specification` (¿qué debería hacer el sistema?), de `governance-review` (¿se respetó autoridad, alcance y reglas?) y de `architecture-review` (¿preserva boundaries y contratos arquitectónicos?).

## 3. Relación con otras capabilities

- **`governance-review`** — revisa autorización, alcance y cumplimiento de gobernanza. Este skill revisa **corrección funcional**. Un cambio puede ser correcto y no estar autorizado, o estar autorizado y ser incorrecto. Cuando detectes un posible cambio fuera de autorización, clasifícalo como `OUT_OF_SCOPE_CHANGE` y **derívalo** (§13): `governance-review` sigue siendo la autoridad especializada.
- **`architecture-review`** — revisa boundaries, dirección de dependencias, ownership y contratos arquitectónicos. Este skill no evalúa si la arquitectura elegida es la adecuada, y **nunca diseña la arquitectura de reemplazo**.
- **Revisión de seguridad** — no forma parte de este skill. Una señal de posible vulnerabilidad se deriva; no se confirma ni se descarta aquí (§13).
- **PR review** — mergeability, historia de commits, descripción del PR, integración de ramas y gates de CI **no** pertenecen a este skill. Cuando el cambio vive en un Pull Request remoto, esa dimensión es `skill://pr-review/SKILL.md`, que a su vez se apoya en este skill para la correctness.
- **`diagnostics`** — `DIAGNOSIS != REVIEW`. Diagnostics parte de un **fallo ya observado** y determina su causa. Este skill parte de un **cambio implementado** y determina si es correcto, exista o no un fallo observado. Si la revisión detecta un fallo cuya causa no es determinable dentro del alcance, se reporta como finding con la evidencia disponible; investigar la causa a fondo es `diagnostics`.
- **`code-quality`** — es always-on y gobierna calidad del código, convenciones y revisión transversal del diff (`skill://code-quality/SKILL.md`). Este skill **no la duplica**: aplica siempre en paralelo, y este skill se ocupa de si el comportamiento es correcto, no de si el código está bien escrito. Un problema puramente de calidad/estilo no es un finding de correctness.
- **`specification`** — decide y formaliza TARGET_STATE. Este skill nunca inventa requisitos nuevos durante la revisión (§5). Ver §15 para la relación con su Etapa 09.

## 4. Distinciones que nunca se conflan

`TEST_GREEN != REQUIREMENT_SATISFIED` · `CODE_PRESENT != BEHAVIOR_VERIFIED` · `NO_EXCEPTION != CORRECT_BEHAVIOR` · `DIFF_SMALL != SAFE_CHANGE` · `REVIEW_FINDING != AUTHORIZATION_TO_FIX` · `PREFERENCE != DEFECT` · `REVIEW != REMEDIATION` · `CURRENT_STATE != TARGET_STATE`.

Consecuencias operativas:

- Un test en verde demuestra lo que ese test ejercita, no que el requisito esté satisfecho (§7.6).
- Que el código exista no demuestra que el comportamiento ocurra: `UNVERIFIED_BEHAVIOR` es un estado real y frecuente.
- Que no se lance una excepción no demuestra que el resultado sea correcto — un fallo silencioso es peor que uno ruidoso.
- Un diff pequeño puede producir una regresión grande. El tamaño no es un argumento de seguridad.
- **Un test existente puede estar protegiendo comportamiento legacy que el cambio debía precisamente modificar.** Un test que falla no siempre indica una implementación incorrecta: puede indicar un test obsoleto. Determina cuál es el caso con la expectativa autoritativa, no con el resultado del test.
- El código existente describe CURRENT_STATE; no constituye automáticamente TARGET_STATE.

## 5. Expectativa autoritativa — `EXPECTED` / `IMPLEMENTED` / `VERIFIED`

Antes de revisar, determina cuál es la fuente autoritativa del comportamiento esperado. Preferencia **contextual**, no precedencia universal: Execution Contract aprobado · specification · criterios de aceptación · especificación de comportamiento/casos de uso · task contract · issue o requisito autoritativo · decisión humana explícita.

Si no existe ninguna, dilo: revisar contra una expectativa que el reviewer construye por su cuenta no es revisión, es diseño encubierto. **No se inventan requisitos durante la revisión.** Si el comportamiento esperado es ambiguo, eso es en sí mismo un hallazgo (`CONTRACT_MISMATCH` o `INSUFFICIENT_EVIDENCE`, según el caso).

Mantén siempre separadas tres cosas distintas:

| Dimensión | Qué es | Cómo se establece |
|---|---|---|
| `EXPECTED` | Lo que debía ocurrir | Fuente autoritativa aplicable |
| `IMPLEMENTED` | Lo que el cambio realmente hace | Diff efectivo, obtenido con tooling cuando sea posible |
| `VERIFIED` | Lo que la evidencia demuestra que ocurre | Tests, ejecución observada, evidencia de runtime |

Las tres pueden divergir independientemente. La revisión consiste en gran medida en localizar dónde divergen.

Determina el cambio efectivo con herramientas, no de memoria ni por el relato del implementador.

```
SELF-VERIFICATION != INDEPENDENT CONFORMANCE
```

En la Línea 2 la revisión parte de evidencia propia: el contrato autorizado y su fingerprint, el inventario de AC, la `EXECUTION_BASELINE`, el diff efectivo contra el commit de esa baseline, el `IMPLEMENTATION_RESULT` y la evidencia de verificación (`skill://delivery-lifecycle/references/delivery-evidence.md` §2). El `IMPLEMENTATION_RESULT` es la declaración de quien implementó: orienta la revisión, no la sustituye. Una verificación afirmada sin comando ni resultado no es evidencia; una registrada es evidencia de su procedencia; la que observa o re-ejecuta quien revisa es independiente. Cuando exista un repositorio Git aplicable, establece su baseline de forma independiente por repositorio y no mezcles evidencia entre repositorios (`.omp/RULES.md` reglas 13 y 18). Si no puede determinarse la base del diff, es `MISSING_EVIDENCE` (§12).

## 6. Modelo de revisión

```
AUTHORITATIVE_EXPECTATION → IMPLEMENTED_CHANGE → OBSERVABLE_BEHAVIOR → VERIFICATION_EVIDENCE → FINDINGS → REVIEW_OUTCOME
```

No es una receta rígida. Un cambio pequeño con contrato claro y evidencia directa puede recorrerse en pocos pasos; no infles la revisión para recorrer el diagrama completo.

## 7. Dimensiones de revisión

No todas aplican a todo cambio. La naturaleza del cambio decide cuáles son materiales.

### 7.1 Cobertura de requisitos
Qué requisitos aplicables existen · qué parte del diff implementa cada uno · qué evidencia lo demuestra · qué requisito quedó sin implementación o sin evidencia. Un requisito implementado pero no demostrado es `UNVERIFIED_BEHAVIOR`, no un requisito cumplido.

Con una especificación formal, la cobertura se hace **por cada `AC-NNN` material** y termina en `AC_CONVERGENCE_RESULT`, con cuatro estados por AC — `PASS`, `UNVERIFIED`, `UNIMPLEMENTED`, `CONTRADICTED` — y su evidencia: `skill://implementation-review/references/ac-convergence.md`. Este skill es el owner de la convergencia; `implementation` no la declara.

### 7.2 Corrección lógica
Condiciones incorrectas o invertidas · ramas inalcanzables o alcanzables por error · valores mal propagados · estados inconsistentes · errores de orden u operación · assumptions inválidos · manejo incorrecto de `null`/vacío/error/resultado · side effects incorrectos u omitidos.

### 7.3 Edge cases
Casos límite **materialmente relacionados** con el comportamiento solicitado. No se exige cobertura exhaustiva del dominio: un edge case es un finding cuando es razonablemente alcanzable y su tratamiento contradice la expectativa aplicable.

### 7.4 Manejo de errores
Failure paths · propagación de errores/excepciones · comportamiento de fallback · manejo de estado inválido, evaluado **contra el contrato aplicable**. Una preferencia sobre el estilo de manejo de errores no es un finding (§8).

### 7.5 Riesgo de regresión
Comportamiento existente razonablemente relacionado que el cambio pueda haber alterado de forma no intencionada. **Debe existir evidencia de la relación** — una llamada, un contrato compartido, un estado común, un consumidor conocido. No hagas caza especulativa de regresiones por todo el repositorio.

### 7.6 Tests — qué demuestran, no si pasan
La pregunta no es *¿pasan?* sino *¿qué comportamiento demuestran?*. Busca: requisito sin test · test que no alcanza realmente el path que se afirma cubierto · assertions insuficientes para demostrar el requisito · falso positivo · fixture incapaz de representar el caso real · comportamiento verificado sólo de forma indirecta · ausencia de caso negativo o de edge case material.

El criterio de qué debe estar probado es `skill://code-quality/SKILL.md` §8 (comportamiento, no detalles de implementación). Consecuencias para la revisión: una corrección de bug sin test que reproduzca la regresión, cuando era practicable, es `MISSING_TEST` · un test que mockea la regla o entidad que dice probar no demuestra esa regla · un test debilitado o eliminado sin que el contrato cambie el comportamiento que protegía es `CONTRACT_MISMATCH` o `DEFECT` · una verificación afirmada sin comando ni resultado registrado es `MISSING_EVIDENCE` (§12), no evidencia. La ausencia de tests para getters triviales, wiring sin comportamiento, internals irrelevantes o cambios sólo documentales **no** es finding, y una cobertura de líneas baja no lo es por sí misma: el criterio es comportamiento sin evidencia, no porcentaje.

### 7.7 Consistencia del diff
Código accidental · comportamiento no relacionado con el contrato · paths inconsistentes entre sí · implementación parcial · restos de una implementación anterior o de depuración · cambios que contradicen el propio contrato que dicen cumplir. Un posible incumplimiento de alcance se reporta como `OUT_OF_SCOPE_CHANGE` y se deriva (§3, §13).

## 8. Estándar de finding — evidencia, no preferencia

**`PREFERENCE != DEFECT`.** Todo finding debe apoyarse en al menos una base verificable: un requisito · un contrato aprobado · comportamiento observablemente incorrecto · semántica del lenguaje o del runtime · una convención aplicable del repositorio · un invariante · un test que lo revela · un requisito de compatibilidad · una regresión verificable.

Un finding cuya única base es *"yo lo habría implementado de otra forma"* es **inválido**. No fabriques observaciones para justificar la revisión: **no encontrar findings es un resultado válido** (§11).

Todo finding identifica, como mínimo:

`OBSERVED` (qué se observó) · `EXPECTED` (qué debía ocurrir) · `EVIDENCE` (qué lo demuestra) · `IMPACT` (qué consecuencia material tiene).

Formato completo:

`ID` · `SEVERITY` · `TYPE` · `OBSERVED` · `EXPECTED` · `EVIDENCE` · `IMPACT` · `LOCATION` · y cuando aplique: `REQUIREMENT` · `REPRODUCTION` · `RECOMMENDATION`.

`RECOMMENDATION` es **opcional**. No es autorización, no debe convertirse en diseño extensivo, y no debe prescribir una solución única cuando varias resolverían correctamente el defecto.

## 9. Taxonomía de findings

| Tipo | Cuándo |
|---|---|
| `DEFECT` | Comportamiento incorrecto demostrable. |
| `REGRESSION_RISK` | Comportamiento existente relacionado que el cambio puede haber alterado, con evidencia de la relación. |
| `MISSING_TEST` | Requisito o path material sin cobertura probatoria. |
| `CONTRACT_MISMATCH` | Divergencia entre lo implementado y el contrato/specification aplicable. |
| `ERROR_HANDLING_GAP` | Failure path ausente o incorrecto frente al contrato. |
| `EDGE_CASE_GAP` | Caso límite material alcanzable y no tratado conforme a la expectativa. |
| `UNVERIFIED_BEHAVIOR` | Comportamiento afirmado pero no demostrado por la evidencia disponible. |
| `OUT_OF_SCOPE_CHANGE` | Cambio ajeno al contrato revisado. Se deriva a `governance-review` (§13). |
| `UNREQUESTED_BEHAVIOR` | Comportamiento añadido dentro del cambio que ningún requisito pidió. No es el estado de un AC: puede coexistir con todos en `PASS`. |

`NO_FINDING` es un estado descriptivo válido cuando no se detectan defectos dentro del alcance revisado.

La taxonomía **clasifica**; no sustituye la explicación. `TYPE: DEFECT` sin `OBSERVED`/`EXPECTED`/`EVIDENCE`/`IMPACT` es una etiqueta, no un finding.

## 10. Severidad

Sólo tres niveles. No se usan `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` en este skill.

- **`BLOCKING`** — el cambio no debería considerarse correctamente terminado dentro del alcance revisado: requisito obligatorio incumplido · comportamiento incorrecto material · regresión demostrable · pérdida de consistencia o aislamiento funcional · evidencia que contradice una afirmación esencial de completion.
- **`MAJOR`** — problema funcional relevante que debe resolverse, pero que no invalida necesariamente todo el cambio.
- **`MINOR`** — defecto real de impacto limitado.

**La severidad no se usa para elevar preferencias.** Si algo no supera el estándar de finding (§8), no tiene severidad: no es un finding.

## 11. Outcomes

La revisión termina en exactamente uno:

- **`REVIEW_PASS`** — no se identificaron defectos materiales dentro del alcance revisado **y** existe evidencia suficiente para evaluar el comportamiento requerido. No significa perfección, ausencia absoluta de bugs, aprobación arquitectónica, aprobación de seguridad, cumplimiento de gobernanza ni merge readiness.
- **`REVIEW_PASS_WITH_FINDINGS`** — la implementación satisface materialmente el comportamiento revisado, pero existen findings no bloqueantes.
- **`REVIEW_BLOCKED`** — existe al menos un finding `BLOCKING` que impide considerar correcta la implementación dentro del alcance revisado.
- **`INSUFFICIENT_EVIDENCE`** — no hay evidencia suficiente para revisar responsablemente uno o más aspectos materiales.

**La ausencia de evidencia nunca se convierte en `REVIEW_PASS`.** Si un aspecto material no pudo evaluarse, el resultado no es PASS aunque nada visible parezca roto.

## 12. Missing evidence

Cuando falte evidencia necesaria, identifícala explícitamente como `MISSING_EVIDENCE`: no existe Execution Contract ni expectativa autoritativa · no se conoce la base del diff · se afirman tests que no son ejecutables o cuya ejecución no consta · el comportamiento observable no es verificable con el acceso disponible · las fuentes de verdad se contradicen · el artefacto de implementación está incompleto.

No todo missing evidence bloquea la revisión completa. Declara **qué conclusión concreta queda limitada** y revisa el resto si puede hacerse responsablemente. Una revisión parcial honesta y delimitada vale más que una completa fabricada.

## 13. Derivación a otras revisiones

Este skill **puede detectar** señales que pertenecen a otra competencia; debe clasificarlas y derivarlas, nunca resolverlas fingiendo haber completado esa revisión especializada:

| Señal detectada | Se deriva a |
|---|---|
| Posible modificación fuera de autorización o de alcance | `governance-review` |
| Posible violación de boundary, ownership o contrato arquitectónico | `architecture-review` |
| Posible vulnerabilidad | `security-review` |
| Mergeability, base, CI, historia o metadatos de PR | `pr-review` |
| Fallo observado cuya causa requiere investigación | `diagnostics` |

Regístralas como `REFERRED_FINDING`, con la evidencia observada y sin veredicto especializado. Si determinar si un finding de seguridad es real exigiera un análisis de vulnerabilidad profundo, **no lo declares defecto de seguridad confirmado**: derívalo y continúa el resto de la revisión de correctness.

## 14. Remediation boundary

**`REVIEW_FINDING != AUTHORIZATION_TO_FIX`.** Durante la revisión no se modifica código, ni tests, ni configuración; no se aplican patches; no se corrigen los findings; no se ejecutan refactors; no se rediseña la solución.

La cadena es: `finding → decisión humana → specification/task contract cuando corresponda → implementation`. Este skill nunca la salta, y encontrar un defecto — por evidente que sea su corrección — no autoriza aplicarla. Cuando la corrección cae inequívocamente dentro de un contrato ya autorizado, sin cambio de semántica ni de alcance, la decisión humana que la cubre es ese contrato: quien ejecuta el lifecycle la clasifica `FIX_ALREADY_AUTHORIZED` y la devuelve a `implementation` (`skill://delivery-lifecycle/references/delivery-evidence.md` §3). Esa clasificación no la hace este skill, y lo que la exceda vuelve a ser decisión humana.

## 15. Relación con `specification` Etapa 09

`skill://specification/references/09-implementation-review.md` es la **Etapa 09** del pipeline de `specification`: produce el deliverable `09_IMPLEMENTATION_REVIEW.md` con su propio vocabulario de veredicto y severidad. Sigue vigente y este skill **no la sustituye ni la modifica**.

| Situación | Usa |
|---|---|
| Revisión dentro de un pipeline `specification` formal, con Execution Contract y necesidad del deliverable `09_IMPLEMENTATION_REVIEW.md` | Etapa 09 (puede apoyarse en la metodología de este skill para el análisis de correctness) |
| Revisión de correctness independiente, sin producir un deliverable de specification | Este skill |

Equivalencia cuando el análisis de este skill alimente el deliverable de la Etapa 09:

| `implementation-review` | Etapa 09 |
|---|---|
| `REVIEW_PASS` | `APPROVED` |
| `REVIEW_PASS_WITH_FINDINGS` | `APPROVED_WITH_OBSERVATIONS` |
| `REVIEW_BLOCKED` | `CORRECTION_REQUIRED`, o `BLOCKED` cuando impida determinar cumplimiento |
| `INSUFFICIENT_EVIDENCE` | Revisión limitada declarando la evidencia faltante; `BLOCKED` si impide determinar cumplimiento |
| `REFERRED_FINDING` → `architecture-review` | `ARCHITECTURAL_REVIEW_REQUIRED` |
| `BLOCKING` / `MAJOR` / `MINOR` | `Bloqueante` / `Alta` / `Media` o `Baja` |

La última fila es deliberadamente asimétrica: `MINOR` cubre `Media` y `Baja`. Cuando el deliverable de la Etapa 09 exija esa distinción, la aporta la Etapa 09 — este skill no crea un cuarto nivel. Cuando una fuente de autoridad aplicable ya imponga un quality gate obligatorio (p. ej. Repository Governance o el Execution Contract), verifica evidencia real de su cumplimiento; no inventes un umbral propio ni eleves una recomendación personal a gate.

## 16. Output contract

`REVIEW_OUTCOME` · `SCOPE_REVIEWED` · `AUTHORITATIVE_EXPECTATION` · `IMPLEMENTED_CHANGE` · `EVIDENCE_USED` · `REQUIREMENT_COVERAGE` · `AC_CONVERGENCE_RESULT` · `FINDINGS` · `REFERRED_FINDINGS` · `MISSING_EVIDENCE` · `LIMITATIONS`.

`AC_CONVERGENCE_RESULT` es obligatorio cuando el cambio implementa una especificación formal con `AC-NNN`.

Sólo `REVIEW_OUTCOME` es obligatorio cuando la revisión llega a un cierre; `MISSING_EVIDENCE` lo es cuando el outcome es `INSUFFICIENT_EVIDENCE` o cuando alguna conclusión quedó limitada. Omite lo que no aplique — no fabriques secciones vacías. El resultado debe ser compacto, verificable y proporcional al cambio revisado.
