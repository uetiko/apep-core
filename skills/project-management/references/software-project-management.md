# Software project management — lo que cambia cuando el producto es software

Referencia del modo proyecto de `project-management` (`SKILL.md` §12). Responde: ¿qué hace distinto gestionar un proyecto de software? ¿cómo se sabe que avanza? ¿quién responde cada incertidumbre? ¿qué significa calidad, capacidad del equipo y fin cuando el producto sigue vivo?

```
SOFTWARE PROGRESS MUST BE EVIDENCE-BASED.
```

## 1. Por qué el software es distinto

Sommerville señala tres diferencias de base: el producto es **intangible** (no se ve el avance mirándolo), muchos proyectos son **únicos** (la experiencia previa predice mal los problemas nuevos) y los **procesos varían** entre organizaciones. A eso se suman características que cambian cómo se gestiona:

| Característica | Consecuencia para la gestión |
|---|---|
| Intangibilidad del progreso | El avance se mide en estados verificables (§2), no en impresiones |
| Volatilidad de requisitos | Requisitos con `VOLATILITY` (`requirements-management.md` §2); menos detalle en el plan lejano |
| Descubrimiento durante la implementación | La implementación puede devolver decisiones (`RETURN_TO_SPECIFICATION`); se planifica para que ocurra, no se oculta |
| Coste de cambio no uniforme | Cambiar un contrato, un schema o una frontera cuesta mucho más que un texto; el análisis de impacto lo distingue |
| Dependencias técnicas | Tipadas y con alcance (`dependency-model.md`) |
| Integración continua y riesgo de integración | "Funciona en mi rama" no es entregado; la integración es un estado aparte |
| Evolución y deuda técnica | El proyecto puede terminar; el producto no (§6) |
| Incertidumbre y dificultad de estimación | Rangos y confianza (`planning-and-control.md` §4) |
| Actividad ≠ progreso | Commits, horas y archivos miden esfuerzo, no avance |
| Implementado ≠ usable · desplegado ≠ aceptado | Cadena de estados de `SKILL.md` §10 |
| Calidad invisible en el porcentaje completado | Un 90% sin tests ni review puede estar más lejos que un 50% verificado |

## 2. Progreso basado en evidencia

No es evidencia suficiente de progreso: "se está trabajando", "80% terminado", número de archivos, líneas de código, número de commits ni Story Points consumidos.

Sí lo es un **estado verificable** con su evidencia, en la cadena de `SKILL.md` §10:

```
IMPLEMENTED → VERIFIED → DELIVERED → DEPLOYED → OPERATIONALLY_ACCEPTED → PROJECT_SUCCESS → VALUE_REALIZED
```

Ante un porcentaje o una impresión, la respuesta es `PROGRESS_EVIDENCE: INSUFFICIENT` y la pregunta concreta: qué requisitos o work items están en qué estado verificable, con qué evidencia (tests, review, integración, despliegue, aceptación). No se traduce el porcentaje a un estado ni se lo da por bueno.

## 3. Incertidumbre como objeto de gestión

| Tipo | Ejemplo | Quién la responde |
|---|---|---|
| `REQUIREMENT_UNCERTAINTY` | No se sabe qué comportamiento se quiere | `specification` |
| `DOMAIN_UNCERTAINTY` | No se conocen las reglas del negocio o del dominio | `specification` con el owner o experto de dominio |
| `TECHNICAL_UNCERTAINTY` | No se sabe cómo funciona hoy el sistema o si algo es factible | `technical-discovery`; spike o prueba de concepto |
| `ESTIMATION_UNCERTAINTY` | No se sabe cuánto costará | Rango y confianza; reducir las anteriores |
| `DEPENDENCY_UNCERTAINTY` | No se sabe si o cuándo llega algo de un tercero | El dueño de la dependencia; `UNKNOWN` tipado |
| `OPERATIONAL_UNCERTAINTY` | No se sabe cómo se comportará en producción | Operación; `deployment-and-operational-readiness.md` |

Ruta por naturaleza de la incógnita: un hecho técnico → `technical-discovery`; la semántica del producto → `specification`; una cuestión de arquitectura → `architecture-review` o decisión humana; un fallo observado → `diagnostics`; una decisión de proyecto → autoridad humana. **PM gestiona el impacto de la incertidumbre** (qué bloquea, qué plan depende de ella, qué riesgo genera); no responde la incertidumbre especializada.

## 4. Calidad de proyecto

PM pregunta, para el entregable: qué significa calidad aquí, qué evidencia demuestra la aceptación, qué quality gates aplican, qué riesgos de calidad hay y quién acepta.

No responde por las capabilities que juzgan cada calidad:

| Calidad | Owner |
|---|---|
| Del código | `code-quality` |
| De los requisitos | `specification` (quality, coherence) |
| De la arquitectura | `architecture-review` |
| De seguridad | `security-review` |
| Conformidad de la implementación con el contrato | `implementation-review` |
| Aceptación del entregable | `ACCEPTANCE_AUTHORITY` (`project-governance.md` §1) |

PM sólo **compone su estado** en el proyecto: qué evidencia existe, qué falta y qué riesgo implica lo que falta. No sustituye ninguna review ni emite veredictos de calidad propios.

## 5. Recursos y equipo

Concerns de gestión, sólo con evidencia:

| Concern | Qué se observa |
|---|---|
| `SKILL_NEEDS` | Qué conocimiento pide el trabajo (dominio, tecnología, operación) |
| `CAPACITY` | Disponibilidad real frente al trabajo comprometido |
| `OWNERSHIP` | Quién responde por cada pieza |
| `BUS_FACTOR` | Conocimiento crítico concentrado en una persona, **cuando hay evidencia** |
| `DEPENDENCY_ON_SPECIALIST` | Trabajo que espera a una persona o equipo concreto (`SHARED_RESOURCE`, `dependency-model.md`) |
| `CONTEXT_SWITCHING` | Varias líneas de trabajo simultáneas para la misma persona |
| `WIP` | Máximo de dos activas por persona (`work-item-flow.md` §2) |
| `TEAM_CONSTRAINTS` | Zonas horarias, dedicación parcial, dependencias organizativas |

Sommerville destaca que el desarrollo de software es una actividad de grupo y que la capacidad de un equipo depende de experiencia en el dominio, resolución de problemas, comunicación y adaptabilidad. Apep usa esos factores como **capacidad del proyecto** (¿falta experiencia de dominio en este frente?), nunca como ranking de personas. De su gestión de personas se adopta la honestidad sobre lo que va bien y lo que va mal.

Prohibido: evaluar psicológicamente a personas, inferir competencia sin evidencia, y medir productividad individual por líneas de código, commits, tickets o Story Points. Una falta de capacidad se presenta como opciones (mover fecha, reducir alcance, añadir capacidad, secuenciar) y `DECISION_REQUIRED`; PM no reduce el alcance para que la capacidad alcance.

## 6. Ciclo de vida: el software no termina en el deploy

```
DELIVERY → DEPLOYMENT → OPERATIONAL_ACCEPTANCE → PROJECT_ACCEPTANCE → PROJECT_CLOSURE → PRODUCT_EVOLUTION
```

Un proyecto tiene fin; el producto, en general, no. Sommerville distingue la **evolución** (se añaden requisitos con el sistema en uso), el **servicing** (sólo cambios para mantenerlo funcionando) y el **phase-out**, y tres tipos de mantenimiento: reparar fallos, adaptar al entorno y añadir o modificar funcionalidad. Para el proyecto, eso significa que cerrar exige decidir quién sostiene lo entregado.

Cuando aplica, se consideran: `MAINTENANCE` · `EVOLUTION` · `HANDOVER` · `OBSERVABILITY` · `SUPPORT` · `ROLLBACK` · `OPERABILITY`. Se evalúan en `deployment-and-operational-readiness.md` (antes de liberar) y `project-closure.md` (antes de cerrar). Sin owner operativo acordado, el proyecto no está listo para cerrarse.

PM no absorbe DevOps: no diseña pipelines, observabilidad ni procedimientos de operación; comprueba que existen, que tienen owner y que su ausencia es un riesgo visible.

## 7. Proyecto frente a producto

*Engineering Software Products* distingue el software **basado en proyecto** — parte de requisitos que posee un cliente externo — del software **de producto** — parte de una oportunidad de negocio y de una visión de producto, con un product manager que responde por el producto. La distinción cambia **quién decide** los requisitos, no quién los define técnicamente:

| | Basado en proyecto | Producto |
|---|---|---|
| Origen de los requisitos | Un cliente externo | La organización, a partir de una visión |
| Quién decide qué entra | El cliente, según lo contratado | El responsable de producto |
| Fin | Entrega y aceptación | Evolución continua |

En Apep, quien decide el producto es una figura humana del `PROJECT_GOVERNANCE_MODEL` (`project-governance.md` §1). **`project-management` no es Product Owner ni product manager**: no fija visión, prioridad ni contenido del producto. Registra quién lo hace y gestiona el trabajo que resulta.
