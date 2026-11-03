# Project governance — accountability, stakeholders, valor y alcance

Referencia del modo proyecto de `project-management` (`SKILL.md` §9). Responde: ¿quién decide y quién acepta? ¿quién necesita participar? ¿qué resultado se busca y para qué? ¿qué entra en el proyecto, en el producto, en una entrega y en una tarea?

```
ACCOUNTABILITY MUST BE IDENTIFIABLE.
IDENTIFIABLE ACCOUNTABILITY != ARTIFICIAL RACI.

APPLY THE MANAGEMENT CONCERN,
NOT NECESSARILY THE MANAGEMENT ARTIFACT.
```

La gobernanza del proyecto es **humana**. Esta referencia ayuda a hacerla visible; no la crea ni la ejerce. PM no es una de estas figuras y no ocupa el lugar de ninguna que falte.

## 1. `PROJECT_GOVERNANCE_MODEL`

```
PROJECT_GOVERNANCE_MODEL
  PROJECT_SPONSORSHIP:        <quién patrocina y responde por el porqué del proyecto> | NOT_IDENTIFIED
  PROJECT_OWNER:              <quién responde por el resultado del proyecto> | NOT_IDENTIFIED
  DECISION_AUTHORITY:         <quién decide alcance, prioridad, fechas, presupuesto> | NOT_IDENTIFIED
  DELIVERY_OWNERSHIP:         <quién responde por la entrega> | NOT_IDENTIFIED
  TECHNICAL_OWNERSHIP:        <quién decide arquitectura y estándares técnicos> | NOT_IDENTIFIED
  REQUIREMENT_STAKEHOLDERS:   <quién aporta o representa requisitos> | NOT_IDENTIFIED
  ACCEPTANCE_AUTHORITY:       <quién acepta los entregables> | NOT_IDENTIFIED
  RISK_ACCEPTANCE_AUTHORITY:  <quién puede aceptar un riesgo material> | NOT_IDENTIFIED
  EVIDENCE:                   <de dónde sale cada asignación>
```

- **No se inventan roles.** Si el proyecto no tiene sponsor formal, es `NOT_IDENTIFIED`, no "el cliente" ni "dirección" por deducción.
- **Una persona puede ejercer varios.** Se registra así ("`PROJECT_OWNER`, `DECISION_AUTHORITY` y `ACCEPTANCE_AUTHORITY`: la misma persona"), sin crear figuras ficticias para llenar la estructura.
- **El hueco importa sólo cuando bloquea.** Una figura `NOT_IDENTIFIED` es un `ISSUE` cuando hace falta una decisión o una aceptación que nadie puede dar; entonces la salida es `DECISION_REQUIRED` sobre *quién decide*, dirigida a quien sí tenga autoridad. Si nada la necesita todavía, basta nombrarla.
- **No hay RACI por defecto.** Una matriz RACI se produce sólo si el owner la pide o si hay varios equipos con responsabilidades que se pisan y la matriz resuelve algo que una línea no resuelve.

El modelo usa la cadena de autoridad de `SKILL.md` §1: estas figuras son la *task authority* del proyecto dentro de la gobernanza del workspace y del repositorio, no una gobernanza paralela.

## 2. Stakeholders

En software se confunden con facilidad figuras que no son la misma:

```
STAKEHOLDER != USER != OPERATOR != SYSTEM OWNER != SECURITY/COMPLIANCE != PROJECT SPONSOR
```

Quien paga no es quien usa; quien usa no es quien opera; quien opera no es quien responde por el sistema; y seguridad o cumplimiento pueden tener poder de veto sin ser usuarios ni sponsors. Tratar a uno como portavoz de otro produce requisitos que nadie validó y aceptaciones que nadie podía dar.

Cuando es relevante, por stakeholder:

| Campo | Pregunta |
|---|---|
| `STAKEHOLDER` | Quién (persona, rol o grupo identificado) |
| `INTEREST` | Qué le importa del proyecto |
| `INFLUENCE` | Qué puede bloquear, cambiar o vetar |
| `INFORMATION_NEEDED` | Qué necesita saber y cuándo |
| `DECISION_AUTHORITY` | Qué puede decidir, si algo |
| `ACCEPTANCE_ROLE` | Qué acepta, si algo |
| `ENGAGEMENT_RISK` | Qué pasa si no participa o se entera tarde |

No se genera una matriz extensa por defecto: con dos o tres stakeholders basta una línea por cada uno, y sólo los campos que aportan.

**Frontera con `specification`.** PM responde *quién necesita participar y decidir*. `specification` responde *qué necesita cada actor que el sistema haga*. Un actor de la especificación (quien interactúa con el sistema) puede ser o no un stakeholder del proyecto; PM no duplica la lista de actores ni define qué hace cada uno: cuando hace falta, referencia la especificación.

## 3. Valor

```
OUTPUT → OUTCOME → BENEFIT → VALUE
```

| Nivel | Qué es | Ejemplo |
|---|---|---|
| `OUTPUT` | Lo que el proyecto produce | Un endpoint de alta de clientes |
| `OUTCOME` | El cambio que el output hace posible | El backoffice puede crear clientes sin soporte técnico |
| `BENEFIT` | La mejora medible que se espera del outcome | Disminuye la intervención manual |
| `VALUE` | El resultado organizacional que justifica el proyecto, **si alguien lo definió** | Lo que la organización haya fijado como objetivo |

Cuando el proyecto necesita razonar sobre valor:

```
VALUE_HYPOTHESIS:  <qué se espera que ocurra y por qué> | NOT_DEFINED
VALUE_EVIDENCE:    <cómo se sabría, con qué fuente> | NOT_DEFINED
VALUE_STATUS:      NOT_DEFINED | HYPOTHESIS | EVIDENCE_PENDING | PARTIALLY_EVIDENCED | REALIZED | NOT_REALIZED | OUT_OF_HORIZON
```

- **Beneficio y valor no se infieren.** Si nadie los definió, son `NOT_DEFINED`; PM puede preguntar por ellos, no proponerlos como si fueran del owner.
- **Una hipótesis de valor no es un requisito funcional.** "Reducir el tiempo de alta un 50%" no se convierte en un comportamiento del sistema por estar en el objetivo; si alguien quiere que el sistema mida o garantice algo, eso lo define `specification`.
- **Un output entregado no es un beneficio obtenido.** Si el beneficio se mide después del horizonte del proyecto, `VALUE_STATUS: OUT_OF_HORIZON` y se dice quién lo medirá, si alguien.

## 4. Alcance

Cuatro alcances distintos, con owners distintos:

| Alcance | Qué delimita | Quién lo decide |
|---|---|---|
| `PROJECT_SCOPE` | Qué resultados y entregables pertenecen al proyecto | Humano (`DECISION_AUTHORITY`) |
| `PRODUCT_SCOPE` | Qué capacidades o comportamiento forman parte del producto | Humano; `specification` lo define |
| `DELIVERY_SCOPE` | Qué se materializa en una entrega o incremento | Humano, con el plan (`planning-and-control.md` §1) |
| `TASK_SCOPE` | Qué puede tocar una ejecución concreta | El contrato (`RULES.md` 5) |

El `SCOPE` de la clasificación de `delivery-lifecycle` (`targeted` · `flow` · `system` · `multi-repo`) mide la **extensión de un cambio** — está cerca de `BLAST_RADIUS` y de `TASK_SCOPE` —, no el alcance del proyecto.

PM puede **detectar** inconsistencias entre los cuatro (una tarea que toca lo que ninguna entrega incluye, una entrega que excede el alcance del proyecto) y nunca las resuelve redefiniendo uno en silencio.

Sólo con evidencia:

| Término | Significa | Evidencia necesaria |
|---|---|---|
| `SCOPE_BASELINE` | Alcance acordado contra el que se miden los cambios | Un acuerdo explícito del owner; PM no lo declara |
| `SCOPE_CHANGE` | Un cambio de alcance **propuesto o decidido** | Una petición o una decisión (`requirements-management.md` §4) |
| `SCOPE_DRIFT` | El trabajo real se aleja del alcance acordado sin decisión | Trabajo en curso o entregado fuera del baseline |
| `SCOPE_CREEP_SIGNAL` | Se acumulan añadidos pequeños sin análisis de impacto | Varios requisitos sin objetivo o sin decisión de entrada |

Sin baseline acordado no hay `SCOPE_DRIFT` medible: se dice que no hay baseline y se compara contra lo último decidido de forma explícita.

## 5. Proporcionalidad — el concern, no el artefacto

PMBOK es un marco para gobernar y gestionar proyectos con *tailoring*; no es una lista de artefactos que producir. En Apep no se generan por defecto: charter exhaustivo, RACI, WBS completa, risk register extenso, matriz de stakeholders, plan de comunicaciones, plan de calidad, plan de adquisiciones, red de cronograma, cost baseline ni dashboards.

Un artefacto se produce sólo cuando `INFORMATION_VALUE > PROCESS_COST`: cuando resuelve una decisión, coordina a quien de otro modo no se coordinaría o lo pide alguien con autoridad. Si no, se aplica la pregunta que el artefacto respondería, en una línea.

| Si el proyecto… | El concern se cubre con |
|---|---|
| Tiene una persona que decide todo | Una línea en `PROJECT_GOVERNANCE_MODEL` |
| Tiene dos o tres stakeholders | Una línea por stakeholder |
| No tiene presupuesto propio ni compras | Nada: finanzas y adquisiciones no aplican y se dice `NOT_APPLICABLE` |
| Depende de un proveedor externo con contrato | `EXTERNAL_DEPENDENCY` (`dependency-model.md`) y sus riesgos; el contrato lo gestiona quien tiene esa autoridad |

Finanzas y adquisiciones se tratan sólo cuando el proyecto las tiene: PM puede señalar un coste, un presupuesto o un contrato como restricción, dependencia o riesgo, y no se convierte en una capability de contabilidad ni de compras.
