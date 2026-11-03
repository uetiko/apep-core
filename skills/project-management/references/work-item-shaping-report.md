# Work item shaping report — cómo se comunica el resultado

Referencia de presentación de `project-management` (`SKILL.md` §6). No añade método: toma el resultado del modo work item — clasificación, assessment, riesgo, dependencias, tamaño, formalidad, readiness y routing — y lo presenta para que lo entiendan dirección, gerencia, producto, operaciones e ingeniería a la vez.

```
THE METHOD DETERMINES WHAT IS TRUE.
THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED.

ONE ANALYSIS. MULTIPLE READERS.
MANAGEMENT LANGUAGE FIRST. TECHNICAL EVIDENCE AVAILABLE BELOW.
```

## 1. Un resultado, tres vistas

```
RESULTADO CANÓNICO DEL MÉTODO
  ├── VISTA DE GESTIÓN      (resumen, estado, valor, alcance, riesgo, bloqueos, ruta, decisiones)
  ├── DETALLE DE INGENIERÍA (evidencia, hechos e inferencias, slices, razón del routing)
  └── REGISTRO DE PROCESO   (las estructuras canónicas que consume y audita el harness)
```

Las tres vistas son **el mismo análisis** escrito para lectores distintos, no tres análisis. Si dos vistas dicen cosas distintas, es un defecto del reporte y manda el registro de proceso.

Lo que la plantilla no puede hacer:

- crear información: hechos, requisitos, criterios de aceptación, alcance, valor, fechas, estimaciones, prioridad ni decisiones;
- cambiar la clasificación, el readiness ni el routing que produjo el método;
- convertir una recomendación en decisión, ni un `UNKNOWN` o `NOT_AVAILABLE` en un hecho.

```
EMPTY TEMPLATE SLOT != PERMISSION TO INVENT.
UNKNOWN REMAINS UNKNOWN. RECOMMENDATION REMAINS RECOMMENDATION. DECISION REMAINS HUMAN.
```

## 2. Proporcionalidad

```
SMALL INFORMATION NEED → SMALL REPORT
LARGE / RISKY / CROSS-FUNCTIONAL WORK → RICHER REPORT
```

- **Item pequeño y claro:** el resumen (dos a cuatro frases), el estado (puede ser una línea) y el registro de proceso mínimo (`TYPE · DESIRED_OUTCOME · SIZE_SIGNAL · NEXT_CAPABILITY`, `SKILL.md` §6). Nada más.
- **Item grande, con riesgo o que cruza áreas:** las secciones que aporten, en este orden.

Una sección sin información se omite; se marca `N/A` sólo cuando su ausencia es en sí un dato útil ("sin dependencias conocidas"). Las marcas *(siempre)* y *(si aplica)* de §3 dicen cuáles pueden faltar.

## 3. Estructura

```markdown
# <Título del work item>

## Resumen                                    (siempre)
## Estado                                     (siempre)
## Resultado buscado                          (si aplica)
## Alcance                                    (si aplica)
## Riesgos e incertidumbre                    (si aplica)
## Dependencias y bloqueos                    (si aplica)
## Cómo se sabrá que está hecho               (si aplica)
## Ruta recomendada                           (si aplica)
## Decisiones necesarias                      (si hay decisiones humanas pendientes)
## Detalle de ingeniería                      (si aplica)
## Registro de proceso                        (siempre)
```

Las secciones de gestión van antes que el detalle de ingeniería y que el registro. Se conserva el orden; el título de cada sección puede adaptarse al idioma del lector.

### Resumen

La única sección que muchos leerán. Hasta cinco o seis frases, en lenguaje corriente, que respondan cuando existan:

1. qué se pide;
2. por qué importa (impacto o valor, sólo si alguien lo dijo);
3. en qué estado está;
4. la principal incertidumbre, riesgo o bloqueo;
5. qué se recomienda hacer ahora y qué puede seguir mientras tanto.

Forma, no contenido obligatorio:

> El trabajo busca corregir X porque afecta a Y. Hoy sabemos A, pero todavía no B. Está listo para *definir el comportamiento*, no todavía para *construirlo*, porque falta C. Recomendamos D; mientras tanto E puede avanzar.

Reglas:

- **Sin vocabulario interno.** Ni nombres de estructuras (`WORK_ITEM_ASSESSMENT`, `READINESS_CHECK`…), ni nombres de skills o agents, ni IDs internos (`DEP-NNN`) salvo que aporten trazabilidad. El siguiente paso se dice por lo que significa (§4).
- **No redefine el alcance**: resume el que fijó el método, sin ampliarlo ni estrecharlo.
- **Lo desconocido se dice como desconocido** ("todavía no sabemos…"), nunca como hecho ni como supuesto implícito.
- **La recomendación se dice como recomendación** ("recomendamos…"); si la decisión es de alguien, se nombra quién decide.

### Estado

Los valores canónicos del método, con su traducción al lado: clasificación, readiness hacia el siguiente paso, siguiente paso, formalidad y tamaño. Es el puente entre el resumen y el registro: mismos valores, ambos lenguajes.

### Resultado buscado

El cambio observable que se busca (`DESIRED_OUTCOME`), no la solución técnica. Si nadie lo definió, `UNKNOWN`.

### Alcance

Tres listas: lo que el item incluye explícitamente (`KNOWN_SCOPE`), lo excluido (`OUT_OF_SCOPE`) y lo que todavía no se sabe. Sin completar huecos.

### Riesgos e incertidumbre

Los riesgos e incertidumbres que pueden cambiar el alcance, una decisión, el esfuerzo o la ruta, en una línea cada uno, con su perfil cualitativo si aporta (`risk-and-issue-management.md` §1). Sin puntuaciones.

### Dependencias y bloqueos

Qué depende de qué, qué está realmente bloqueado y por qué, y qué puede avanzar igualmente (`dependency-model.md`).

### Cómo se sabrá que está hecho

El contorno de aceptación del método (`ACCEPTANCE_SURFACE`, `work-item-shaping.md` §2): qué tendría que poder observarse. **No son criterios de aceptación** y no se escriben aquí: si hacen falta, los define `specification`.

### Ruta recomendada

Siguiente paso — el que puede empezar **ahora** —, por qué, qué vendrá después, qué puede ir en paralelo y qué parte espera, y qué no puede empezar todavía (`routing-readiness.md` §3), dicho en lenguaje corriente. Es una recomendación: la transición la decide quien conduce el trabajo.

**El resumen no contradice la ruta.** Si el registro dice que el siguiente paso está listo, ningún texto dice que hay que esperar antes de darlo; si hay que esperar algo, el siguiente paso es lo que resuelve esa espera. Una contradicción así no se arregla en la redacción: indica que la ruta está mal expresada.

### Decisiones necesarias

Sólo decisiones humanas genuinas: elegir entre opciones. Una autorización pendiente (ejecutar, crear la rama) no es una decisión a desplegar aquí: se dice en el resumen o en la ruta como "pendiente de autorización". Cada decisión es un `DECISION_REQUIRED` canónico (`ENGINEERING_GOVERNANCE.md` §1.4); esta sección no crea otra semántica, sólo lo presenta para gestión:

| Para gestión | Campo canónico |
|---|---|
| Qué hay que decidir | `DECISION` |
| Por qué importa ahora | `FACTS` |
| Opciones y qué implica cada una | `OPTIONS`, `TRADEOFFS`, `CONSEQUENCES` |
| Qué recomendamos | `RECOMMENDATION`, dicho como recomendación |
| Qué queda parado mientras no se decide | `BLOCKING_SCOPE` |
| Quién decide | La autoridad que corresponda; si no está identificada, "por identificar" — nunca una figura supuesta |

La versión canónica completa va en el registro de proceso.

### Detalle de ingeniería

Para quien necesita la evidencia: hechos técnicos con su fuente, separados de las inferencias (`FACT` / `INFERENCE` / `RECOMMENDATION` / `UNKNOWN` cuando la distinción es material), slices propuestas, restricciones técnicas, descubrimientos del estado actual y la razón del routing.

### Registro de proceso

Las estructuras canónicas, completas y sin reescribir: clasificación, `WORK_ITEM_ASSESSMENT`, `WORK_RISK_PROFILE`, dependencias y blockers, `SIZE_SIGNAL`, resultado del slicing, `WORK_FORMALITY`, `READINESS_CHECK`, `ROUTING_RECOMMENDATION` y `DECISION_REQUIRED`, con los nombres y valores de sus referencias. Es la representación que consumen `delivery-lifecycle`, el orchestrator y las suites; el reporte humano nunca la sustituye.

## 4. Traducción del siguiente paso

El siguiente paso se nombra por lo que significa; la capability va en el registro.

| Capability | En el resumen |
|---|---|
| `specification` | definir qué debe hacer el sistema |
| `technical-discovery` | investigar cómo funciona hoy |
| `diagnostics` | encontrar la causa del fallo |
| `architecture-review` | validar el diseño contra las fronteras del sistema |
| `security-review` | revisar el riesgo de seguridad |
| `implementation` | construirlo |
| `review` | revisar lo construido |
| `integration` | integrarlo |
| `NONE` + decisión pendiente | esperar una decisión |
