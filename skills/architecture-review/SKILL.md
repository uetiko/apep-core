---
name: architecture-review
description: Evalúa si un estado existente o un cambio propuesto/implementado preserva, viola o tensiona las decisiones arquitectónicas, boundaries, dirección de dependencias, ownership y contratos aplicables — con evidencia, no con preferencia estética. Úsalo cuando se pida revisar arquitectónicamente un cambio, un diff, un componente o una decisión de diseño, o mediante invocación explícita (`/skill:architecture-review`). No es el modo normal de trabajo del workspace — no se activa para entender cómo funciona un sistema sin pregunta arquitectónica (`technical-discovery`), para revisar cumplimiento de autoridad/scope/gobernanza (`governance-review`), para decidir qué debería ser la arquitectura (`specification`/decisión humana), ni para implementar una corrección. No diseña TARGET_STATE ni sustituye una arquitectura existente por una que el reviewer considere más elegante.
---

# Architecture Review

Este skill es un **método de evaluación arquitectónica basada en evidencia** — no diseña arquitectura, no decide qué debería cambiar, y no ejecuta remediación. Responde si un estado o cambio concreto respeta la arquitectura aplicable; no produce una arquitectura alternativa ni un catálogo de mejoras.

## 0. Cuándo NO usar este skill

No lo actives para: reconstruir cómo funciona un sistema sin una pregunta arquitectónica concreta (eso es `technical-discovery`), revisar si un cambio respetó autoridad/scope/reglas de gobernanza (`governance-review`), decidir qué debería ser la arquitectura o formalizar TARGET_STATE (`specification`, o decisión humana directa), ejecutar una corrección ya autorizada (`implementation`), ni como excusa para imponer una preferencia de diseño. Actívalo cuando la necesidad real sea: *¿este estado o cambio preserva o tensiona la arquitectura aplicable?*

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE        (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE    (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → ARCHITECTURE REVIEW    (este skill)
      → consumidor           (decisión humana / specification / governance-review / implementation)
```

No es gobernanza independiente ni tiene autoridad de decisión propia sobre arquitectura. La autoridad para cambiar arquitectura permanece humana en todos los casos (`ENGINEERING_GOVERNANCE.md` §1.2). Es executor-neutral: su resultado es evidencia consumible por una decisión humana, por `specification`, o por `implementation` una vez autorizada — nunca invoca automáticamente ninguna de ellas.

## 2. Pregunta gobernante

`¿Este estado o cambio preserva, viola o tensiona materialmente las decisiones arquitectónicas, boundaries, dirección de dependencias, ownership y contratos aplicables?`

Distinta de `technical-discovery` (¿cómo funciona realmente esto?), de `governance-review` (¿se respetó autoridad, scope y reglas?), de `specification` (¿qué debería hacer/ser el sistema?) y de `implementation` (ejecuta el cambio ya delimitado).

## 3. Relación con otras capabilities

- **`technical-discovery`** reconstruye CURRENT_STATE (cómo está construido el sistema). `architecture-review` **puede consumir** esos hechos, y puede hacer la inspección puntual necesaria para verificar evidencia — pero **no rehace discovery amplio**. Si el gap de comprensión es sustancial, repórtalo y recomienda `technical-discovery` en vez de investigar horizontalmente (ver §7).
- **`governance-review`** revisa si un cambio respetó autoridad, scope y las reglas de gobernanza vigentes. `architecture-review` revisa si preserva boundaries, dependency direction, ownership y contratos. Pueden solaparse cuando una decisión arquitectónica ya cerrada fue ignorada — en ese punto `architecture-review` puede señalar que también hay una violación de gobernanza, pero no duplica su metodología completa.
- **`specification`** decide y formaliza TARGET_STATE. `architecture-review` nunca diseña TARGET_STATE ni lo anticipa — como mucho, identifica que una decisión necesita revisarse (`DECISION_REQUIRED`).
- **`implementation`** ejecuta cambios ya autorizados. `architecture-review` nunca ejecuta ni prescribe la solución técnica — ver §9 (remediation boundary).

## 4. Distinciones que nunca se conflan

`CURRENT_STATE != TARGET_STATE` · `OBSERVED_ARCHITECTURE != DECLARED_ARCHITECTURE` · `ARCHITECTURAL_RISK != ARCHITECTURAL_VIOLATION` · `ARCHITECTURAL_PREFERENCE != ARCHITECTURAL_FINDING` · `IN_SCOPE != CHANGE_AUTHORIZATION` · `ARCHITECTURE_REVIEW != ARCHITECTURE_DESIGN` · `REVIEW != REMEDIATION`.

Una arquitectura existente puede ser imperfecta y seguir siendo el estado/decisión autoritativa aplicable. El reviewer **nunca** la sustituye por la que él consideraría más elegante.

## 5. Modelo de evidencia y estándar de finding

Reutiliza sin modificar la taxonomía epistemológica de `technical-discovery` (`skill://technical-discovery/SKILL.md` §5): `FACT` · `INFERENCE` · `HYPOTHESIS` · `DECLARED_INTENT` (arquitectura/intención declarada en documentación, ADR, contrato, decisión o specification) · `UNKNOWN` · `CONTRADICTION`.

**Architecture review es evidence-based, no taste-based.** Un finding material requiere, como mínimo:

1. **OBSERVED CONDITION** — qué relación, dependencia, ownership, contrato, estado o boundary se observó.
2. **EVIDENCE** — dónde se observa (archivo/símbolo/contrato/output de herramienta).
3. **ARCHITECTURAL BASIS** — contra qué se evalúa: decisión cerrada, ADR, contrato, specification, boundary observable y establecida, ownership conocido, dependency direction, invariante, gobernanza de repositorio/workspace, o riesgo arquitectónico demostrable.
4. **IMPACT** — qué consecuencia arquitectónica material produce o puede producir.

Si no existe una base arquitectónica defendible, el punto se clasifica como preferencia/observación — **no** como violación. Un finding **no** existe únicamente porque: el reviewer prefiere otra arquitectura, la solución no sigue un patrón conocido, no se usa Clean Architecture, no existe una interfaz, una clase es "grande", un nombre de directorio "parece" incorrecto, o la implementación es distinta de cómo el reviewer la habría diseñado.

## 6. Escalas — controlan el alcance

| Escala | Uso | Notas |
|---|---|---|
| `TARGETED_ARCHITECTURE_REVIEW` (default) | Un cambio, PR/diff, componente, dependencia, boundary concreta o decisión específica. | Modo preferente cuando la pregunta es localizada. |
| `FLOW_ARCHITECTURE_REVIEW` | Un flujo end-to-end o integración entre varios componentes: ownership/dependency direction a lo largo del flujo. | |
| `SYSTEM_ARCHITECTURE_REVIEW` | Sólo cuando se solicita explícitamente revisar ampliamente un servicio, subsistema, repositorio, pipeline o slice arquitectónico. | Un cambio estrecho **nunca** escala automáticamente a esta escala. |

## 7. Alcance de la inspección técnica

Puede realizar la inspección técnica necesaria para verificar evidencia (leer código, trazar una llamada, confirmar un import), pero no rehace discovery amplio cuando el CURRENT_STATE relevante ya está suficientemente establecido. Si la revisión descubre que no entiende una parte material del sistema necesaria para emitir juicio: identifica el gap, obtiene evidencia localizada si cae dentro de la revisión, o produce `INSUFFICIENT_EVIDENCE` recomendando `technical-discovery` cuando el gap requiera investigación sustancial — nunca convierte la revisión en archaeology por su cuenta.

## 8. Dimensiones de revisión

No todas aplican a toda revisión — la escala (§6) y la pregunta controlan cuáles son relevantes:

| Dimensión | Referencia |
|---|---|
| Dependency direction, boundaries, ownership, contracts/integration, state/persistence/side effects, runtime/deployment topology (cuando sea relevante), cross-repository boundaries | `skill://architecture-review/references/boundaries-ownership-and-contracts.md` |
| Coupling/cohesion, abstraction justification (*pattern follows pressure*), cognitive load arquitectónica | `skill://architecture-review/references/coupling-abstraction-and-cognitive-load.md` |

Una revisión localizada no obliga a cargar ambas referencias ni a evaluar todas las dimensiones que contienen.

## 9. Output semántico

La revisión concluye en uno o más de estos estados — **no es obligatorio reducir una revisión compleja a una única etiqueta** si hacerlo pierde información:

- **`ARCHITECTURE_OK`** — no se encontró finding material dentro del alcance y evidencia disponible. No está obligado a inventar hallazgos para justificar el trabajo.
- **`ARCHITECTURAL_RISK`** — tensión o riesgo material, sin contradicción demostrada contra una decisión/boundary/invariante autoritativa.
- **`ARCHITECTURAL_CONTRADICTION`** — el estado o cambio contradice de forma demostrable una decisión, boundary, ownership, dependency direction, contrato o invariante aplicable.
- **`INSUFFICIENT_EVIDENCE`** — no hay evidencia suficiente para concluir responsablemente (ver §7).
- **`DECISION_REQUIRED`** — la revisión llega a un punto donde continuar requiere una decisión arquitectónica humana (`ENGINEERING_GOVERNANCE.md` §1.4).

## 10. Formato de finding

Cuando exista un finding material:

`ID` · `SEVERITY` · `OBSERVED` (condición observada) · `EVIDENCE` (archivos/símbolos/contratos/tool output) · `ARCHITECTURAL_BASIS` (decisión/boundary/invariante/contrato contra el que se evalúa) · `IMPACT` · `CLASSIFICATION` (`RISK` | `CONTRADICTION` | `DECISION_REQUIRED`) · `CONFIDENCE` (`CONFIRMED`/`HIGH`/`MEDIUM`/`LOW`, cuando aporte) · `RECOMMENDATION` (sólo acción de gobernanza/proceso: revisar decisión, obtener evidencia, formalizar decisión, devolver a `specification`, escalar — nunca diseño técnico de remediación).

## 11. Remediation boundary

Architecture review puede decir qué propiedad se viola, qué boundary se cruza, qué coupling se introduce, qué ownership queda ambiguo, qué decisión debe revisarse, o qué resultado arquitectónico ya definido debería preservarse. **Nunca** inventa como solución: nuevas capas, servicios, microservicios, interfaces, ports/adapters, repositories, factories, strategies, event buses, DTOs, Anti-Corruption Layers, schemas, ni infraestructura alternativa.

Puede mencionar una remediación concreta sólo cuando (1) ya existe una decisión arquitectónica autoritativa que la establece, o (2) el usuario pidió explícitamente evaluar opciones de diseño en una tarea separada. En cualquier otro caso, la cadena es: `finding → decisión humana → specification → implementation` — este skill nunca la salta.
