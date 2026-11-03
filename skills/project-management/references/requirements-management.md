# Requirements management — el requisito como trabajo del proyecto

Referencia de `project-management` (`SKILL.md` §7). Responde: ¿qué requisitos tiene el proyecto, de dónde vienen, en qué estado están, qué cambió y qué afecta el cambio? **No** responde qué significa el requisito.

```
PM MANAGES THE REQUIREMENT AS PROJECT WORK.
SPECIFICATION DEFINES WHAT THE REQUIREMENT MEANS.

REQUIREMENT STATUS != REQUIREMENT SEMANTICS.
CHANGE ANALYSIS != CHANGE AUTHORIZATION.
```

## 1. Management frente a engineering

Sommerville separa cuatro actividades de requirements engineering — elicitación, análisis, validación y gestión — y describe la gestión como mantener identificación, proceso de cambio y trazabilidad para poder evaluar el impacto de un cambio. Apep reparte esas actividades entre dos owners:

| Concern | Owner | Qué hace |
|---|---|---|
| Que el requisito exista, quién lo pide o representa, por qué importa | `project-management` | Lo registra con su fuente; si falta la fuente, es un hueco de trazabilidad (§5) |
| Objetivo de proyecto y resultado al que contribuye | `project-management` | Lo enlaza (`project-governance.md` §3); no lo infiere |
| Estado, dependencias, incremento o hito objetivo | `project-management` | Lo deriva de evidencia y de los estados existentes (§3) |
| Prioridad | Humano | PM registra la prioridad **ya decidida** y por quién; nunca la fija |
| Cambios, volatilidad, impacto del cambio | `project-management` | Clasifica el cambio y produce el análisis de impacto (§4) |
| Aprobación de un cambio material | Humano | PM recomienda; no aprueba |
| Elicitación y refinamiento del comportamiento; requisitos funcionales y no funcionales; reglas de negocio; actores; casos de uso; escenarios; restricciones con efecto en el comportamiento | `specification` | Los define y clarifica (Línea 1) |
| Ambigüedad, clarificación (`CLAR-NNN`), provenance, `AC-NNN`, quality, coherence, Execution Contract | `specification` | Ídem |
| Validación del requisito ("¿es esto lo que se quiere?") | `specification` + humano | PM no declara un requisito válido |
| Conformidad de lo implementado con el requisito | Línea 2 (`implementation-review`) | PM compone su estado, no lo juzga |

Si para gestionar un requisito hace falta decidir qué significa, PM se detiene en ese punto y la ruta es `specification` (`SKILL.md` §2, invariante 1).

## 2. `MANAGED_REQUIREMENT`

Ficha de gestión de un requisito. **Ningún campo es obligatorio**: se usan los que aportan información; un campo sin evidencia es `UNKNOWN` o se omite, no se rellena.

```
MANAGED_REQUIREMENT
  REQUIREMENT_REF:        <ID real del tracker o de la spec> | REQ-NNN (local a este análisis)
  SOURCE:                 <de dónde viene: persona, documento, regulación, incidente> | UNKNOWN
  STAKEHOLDER:            <quién lo pide o lo representa> | UNKNOWN
  PROJECT_OBJECTIVE:      <objetivo o resultado al que contribuye> | UNKNOWN
  STATUS:                 <§3, con su fuente>
  PRIORITY_STATUS:        DECIDED (<por quién, cuándo>) | NOT_DECIDED | UNKNOWN
  DEPENDENCIES:           NONE | <DEP-NNN, dependency-model.md>
  TARGET_INCREMENT:       <incremento o release, si existe> | NONE
  TARGET_MILESTONE:       <hito, si existe> | NONE
  CHANGE_STATUS:          NONE | <CHANGE-NNN · estado de la decisión>
  VOLATILITY:             STABLE | VOLATILE | UNKNOWN — con evidencia
  ACCEPTANCE_OWNER:       <quién lo acepta> | NOT_IDENTIFIED
  SPECIFICATION_REF:      <artefacto y IDs de specification: BR, UC, AC-NNN> | NONE
  IMPLEMENTATION_STATUS:  <estado de la Línea 2 que lo evidencia> | NOT_STARTED | UNKNOWN
  VERIFICATION_STATUS:    <evidencia de verificación> | NOT_VERIFIED | UNKNOWN
```

- **Referenciar, no copiar.** Cuando existe una especificación, sus reglas de negocio, casos de uso y `AC-NNN` son la fuente autoritativa dentro de `specification`. `SPECIFICATION_REF` apunta a ellos; la ficha no los resume, no los reescribe y no los duplica. Una copia se desactualiza y se convierte en una segunda verdad.
- **`REQ-NNN` es local.** Sirve para referirse al requisito dentro del análisis cuando no hay un ID real; no es un ID externo y no se presenta como tal (`dependency-model.md`: no se inventan IDs externos).
- **`VOLATILITY` necesita evidencia**: cambios ya ocurridos, desacuerdo abierto entre stakeholders, dependencia de una regulación o de un sistema externo que está cambiando. Sommerville recuerda que el entorno de negocio y técnico cambia y los requisitos con él; un requisito volátil pide planificar con menos detalle (`planning-and-control.md` §2), no especificar más deprisa.
- **`PRIORITY_STATUS` registra, no decide.** Si hace falta ordenar y nadie lo ha decidido, la salida es `DECISION_REQUIRED` con opciones (`SKILL.md` §2).

Para un único requisito claro, la ficha cabe en tres líneas (`REQUIREMENT_REF`, `SOURCE`, `STATUS`). No se produce una matriz de requisitos por defecto.

## 3. Estado del requisito: un mapeo, no otra máquina de estados

PM **no tiene máquina de estados propia** (`SKILL.md` §8). El estado de un requisito se **deriva** de los estados que ya existen y de la evidencia, y se reporta junto con su fuente:

| `REQUIREMENT_STATUS` | Se deriva de | Owner del estado de origen |
|---|---|---|
| `IDENTIFIED` | Existe registrado (`Backlog`; `RECEIVED`) | Kanban; `delivery-lifecycle` |
| `UNDER_ANALYSIS` | En shaping o clasificación (`CLASSIFIED`; `DISCOVERY_REQUIRED`) | PM; `delivery-lifecycle` |
| `SPECIFICATION_REQUIRED` | Falta contrato proporcional (`SPECIFICATION_REQUIRED` y los estados internos de la Línea 1) | `delivery-lifecycle`; `specification` §12 |
| `SPECIFIED` | `EXECUTION_READY` en `FORMAL`, o task contract ligero existente en `NONE`/`LIGHT` | `specification`; humano |
| `APPROVED_FOR_EXECUTION` | Contrato + autorización humana de ejecución registrada | Humano |
| `IN_IMPLEMENTATION` | `IMPLEMENTING` · `VERIFYING` · `REVIEWING` · `REMEDIATION_REQUIRED` (`In Progress`/`Review`) | `delivery-lifecycle` |
| `VERIFIED` | Evidencia de verificación de sus AC en la Línea 2 | Línea 2 |
| `DELIVERED` | Integrado según la gobernanza del repositorio (`INTEGRATION_READY` + integración humana) | `delivery-lifecycle`; humano |
| `ACCEPTED` | Aceptado por su `ACCEPTANCE_OWNER` | Humano |
| `CHANGED` · `SUPERSEDED` · `CANCELLED` | Una decisión registrada (§4) | Humano |

Reglas:

- **El estado de un requisito nunca es más avanzado que la evidencia de su fuente.** Sin fuente consultable, `UNKNOWN`.
- `SPECIFIED` no es `APPROVED_FOR_EXECUTION`: `EXECUTION_READY != AUTHORIZED_TO_EXECUTE`.
- `VERIFIED` va **antes** de `DELIVERED`. Un requisito implementado sin verificar no está entregado ni `Done` (`work-item-flow.md` §4).
- `DELIVERED` no es `ACCEPTED`, y ninguno es valor realizado (`SKILL.md` §10).
- `CHANGED`, `SUPERSEDED` y `CANCELLED` sólo existen con una decisión humana registrada. PM puede recomendarlos, no aplicarlos.
- El harness no persiste estos estados (`SKILL.md` §2, invariante 9). Se reportan con lo que la fuente dice en el momento.

## 4. Change management

### 4.1 Tipo de cambio

No todo lo que llega como "cambio" es lo mismo, y tratarlos igual es una forma de cambiar el alcance en silencio:

| Tipo | Qué es | Quién responde el contenido | Ruta |
|---|---|---|---|
| `NEW_REQUIREMENT` | Una necesidad que no estaba | Humano decide si entra; `specification` la define | Análisis de impacto + `DECISION_REQUIRED` si afecta alcance comprometido |
| `REQUIREMENT_CLARIFICATION` | Precisa lo que ya estaba pedido, sin ampliarlo | `specification` (`CLAR-NNN`) | `specification`; sin cambio de alcance |
| `REQUIREMENT_CHANGE` | Modifica el comportamiento de un requisito ya acordado | Humano decide; `specification` lo redefine | Análisis de impacto + `DECISION_REQUIRED`; vuelve a `specification` sólo lo afectado |
| `SCOPE_CHANGE` | Entra o sale un entregable o resultado del proyecto | Humano | Análisis de impacto + `DECISION_REQUIRED` |
| `TECHNICAL_CHANGE` | Cambia el cómo, no el qué | Owner técnico; `architecture-review` si toca fronteras | Ruta técnica (`work-item-shaping.md` §1) |
| `DEFECT` | El sistema no hace lo ya acordado | — | `diagnostics` si la causa no se conoce |
| `CORRECTIVE_ACTION` | Acción para corregir una desviación del proyecto (plan, proceso, recursos) | Humano decide; PM propone | Control (`planning-and-control.md` §7) |

`SCOPE_CHANGE` vale para cualquiera de los cuatro alcances (`project-governance.md` §4) y `AFFECTED_SCOPE` dice cuál. Mover un item entre incrementos o releases sin tocar su semántica ni el alcance del proyecto es un cambio de `DELIVERY_SCOPE`: es **material** si mueve una fecha comprometida o un hito, o cambia lo que se acordó entregar a un stakeholder en ese incremento; si no, se registra en una línea. Quien lo decide es el owner; si ya lo decidió, PM sólo registra el impacto.

Un comportamiento **descubierto durante la implementación** es `REQUIREMENT_CLARIFICATION` si cae dentro de lo ya pedido y sólo faltaba definirlo (qué pasa en un caso del mismo flujo), y `NEW_REQUIREMENT` si añade algo que nadie pidió. En los dos casos el contenido lo define `specification` con el owner.

La distinción se hace por evidencia, no por la etiqueta. Una "clarificación" que añade un comportamiento nuevo es un `NEW_REQUIREMENT`; un "bug" que pide algo que nunca se acordó es un `NEW_REQUIREMENT` o un `REQUIREMENT_CHANGE`. Si no se puede saber si un comportamiento estaba acordado, la pregunta es para `specification` y el owner, no una suposición de PM.

### 4.2 Análisis de impacto

Un cambio es **material** cuando, si se acepta, altera comportamiento ya acordado, el alcance acordado, una fecha o hito comprometido, el coste, o un compromiso con un stakeholder. La materialidad depende del impacto, no del tipo: una `REQUIREMENT_CLARIFICATION` que mueve un hito comprometido es material.

Todo cambio **material** se analiza antes de cualquier decisión:

```
CHANGE_IMPACT_ANALYSIS
  CHANGE_REF:              CHANGE-NNN (local) | <ID real>
  CHANGE_TYPE:             <§4.1>
  CHANGE_SOURCE:           <quién o qué lo origina>
  REASON:                  <por qué se pide> | UNKNOWN
  AFFECTED_REQUIREMENTS:   <REQUIREMENT_REF / SPECIFICATION_REF> | NONE | UNKNOWN
  AFFECTED_SCOPE:          <PROJECT · PRODUCT · DELIVERY · TASK, project-governance.md §4> | NONE
  AFFECTED_DEPENDENCIES:   <DEP-NNN> | NONE
  SCHEDULE_IMPACT:         <qué hito o fecha comprometida mueve, con evidencia> | NONE | UNKNOWN
  RESOURCE_IMPACT:         <capacidad o especialista que hace falta> | NONE | UNKNOWN
  RISK_IMPACT:             <riesgos nuevos o que cambian> | NONE
  QUALITY_IMPACT:          <tests, reviews o criterios de aceptación afectados> | NONE
  ARCHITECTURE_IMPACT:     <fronteras o contratos tocados → architecture-review> | NONE | UNKNOWN
  DELIVERY_IMPACT:         <trabajo en curso que se detiene, se rehace o se invalida> | NONE
  OPTIONS:                 <alternativas con su consecuencia>
  RECOMMENDATION:          <la de PM, con su razón>
  DECISION_REQUIRED:       <qué decide quién> | NONE
```

- **PM produce el análisis; no aprueba el cambio.** Ni silencio, ni urgencia, ni que el cambio "sea pequeño" lo convierten en aprobado.
- Los impactos especializados se nombran y se derivan: `ARCHITECTURE_IMPACT` lo analiza `architecture-review`; un impacto de seguridad, `security-review`; el impacto sobre el comportamiento, `specification`. PM no los responde por ellos.
- Para analizar un cambio, Sommerville propone considerar qué pasa si **no** se hace, qué beneficio da, a cuántos usuarios afecta, cuánto cuesta y cómo encaja en el ciclo de release. Úsalo como guía de las `OPTIONS`, no como fórmula.
- Un cambio que **sólo** afecta calendario u orden, sin cambiar la semántica de ningún requisito, no vuelve a `specification`: PM analiza el impacto y, si toca una fecha comprometida o una prioridad, la decisión es humana.
- Un cambio que llega **después** de `EXECUTION_READY` o de una autorización es la evidencia nueva que permite reabrir la especificación (`routing-readiness.md` §2), sólo en lo afectado. Una **petición todavía no aceptada** abre el análisis de impacto, no la especificación: el análisis dice qué habría que reespecificar **si** se acepta (`AFFECTED_REQUIREMENTS`), y `specification` se reabre cuando el owner lo acepta. La excepción es una `REQUIREMENT_CLARIFICATION` dentro del alcance acordado, que va directamente a `specification` porque cerrarla es su trabajo. El trabajo autorizado que el cambio no toca no se detiene por defecto; el que sí toca se señala en `DELIVERY_IMPACT`.
- **Un comportamiento descubierto durante la implementación** (falta, contradice o no está decidido) vuelve como `DECISION_REQUIRED` (`RETURN_TO_SPECIFICATION`, `work-item-flow.md` §8). PM registra su impacto en alcance, dependencias e hitos; quien implementa no lo completa por su cuenta y PM tampoco.

Para un cambio no material (una redacción, un orden sin compromiso), el análisis cabe en una línea: tipo y por qué no es material.

## 5. Trazabilidad

Dos trazas complementarias. Ninguna se construye por plantilla: se registran los enlaces que existen y se nombran los huecos que importan.

**Trazabilidad de requisitos** — por qué existe cada pieza y qué la demuestra:

```
PROJECT OBJECTIVE → REQUIREMENT_REF → SPECIFICATION IDs (BR, UC) → AC-NNN → evidencia de entrega
```

**Trazabilidad de proyecto** — qué se decidió y qué pasó después:

```
DECISION → ACTION → OWNER → WORK ITEM → DELIVERY STATE
```

| Hueco | Qué indica | Salida |
|---|---|---|
| Requisito sin `SOURCE` ni `STAKEHOLDER` | Nadie puede confirmar, priorizar ni aceptar el requisito | `TRACEABILITY_GAP` + quién debería identificar la fuente; no se inventa |
| Requisito sin `PROJECT_OBJECTIVE` | Posible alcance no justificado o scope creep | `TRACEABILITY_GAP`; `SCOPE_CREEP_SIGNAL` si hay evidencia (`project-governance.md` §4) |
| Requisito sin `ACCEPTANCE_OWNER` | No se podrá cerrar | `ISSUE` antes del cierre (`project-closure.md`) |
| Decisión sin `ACTION` u `OWNER` | La decisión no se va a materializar | `ISSUE` |

**Frontera con la Línea 2.** El tramo `AC-NNN → evidencia de entrega` no lo verifica PM: la verificación por criterio pertenece a la Línea 2. PM referencia la evidencia que exista y, si falta, dice que falta. La convergencia sistemática entre `AC-NNN` y lo implementado es un candidato futuro de la Línea 2, no de este skill.

## 6. Requirements baseline

Un `REQUIREMENTS_BASELINE` existe sólo si el owner lo acordó: un conjunto de requisitos y su versión, contra el que se miden los cambios. PM no lo declara. Sin baseline acordado, los cambios se analizan contra lo último decidido de forma explícita, y se dice así (`planning-and-control.md` §5).

## 7. Qué NO hacer

No escribir criterios de aceptación ni reglas de negocio: es trabajo de `specification`, aunque se pida "ya que estás". No copiar `AC-NNN` a la ficha de gestión. No declarar un requisito válido, completo o aprobado. No convertir una petición de un stakeholder en requisito sin pasar por el tipo de cambio y la decisión. No tratar una clarificación que amplía el alcance como si fuera una clarificación. No mover un requisito a `ACCEPTED` porque está desplegado.
