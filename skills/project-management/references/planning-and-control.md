# Planning and control — planificar, estimar, medir y controlar con evidencia

Referencia del modo proyecto de `project-management` (`SKILL.md` §11). Responde: ¿cómo se llega de los resultados buscados a estados verificables? ¿cuánto se sabe de cuánto costará? ¿contra qué se compara el avance y qué se hace con una desviación?

```
PLAN != CONTRACT.
ESTIMATE != COMMITMENT.
BASELINE != CURRENT_STATE != FORECAST.
DETAIL DECREASES AS UNCERTAINTY INCREASES.
```

## 1. Del resultado al estado verificable

```
OUTCOMES → DELIVERABLES → WORK ITEMS → DEPENDENCIES → MILESTONES → VERIFIABLE STATES
```

- Cada **hito** es un cambio verificable de estado ("alta de clientes verificada en staging"), no una actividad con duración ("trabajar en backend tres días"). Sommerville define los hitos como puntos del calendario contra los que se puede evaluar el progreso, y los entregables como productos de trabajo que se entregan al cliente.
- El orden y el paralelismo se razonan con el `WORK_GRAPH` (`dependency-model.md` §2).
- **Un plan no es un contrato.** El plan organiza; lo que se ejecuta lo fija el contrato (`SKILL.md` §1). Un hito en el plan no autoriza nada.

## 2. Horizonte y modo de planificación

| `PLANNING_HORIZON` | Precisión razonable |
|---|---|
| `NEAR_TERM` | Work items concretos, dependencias tipadas, hitos con evidencia esperada |
| `MID_TERM` | Entregables e incrementos; orden aproximado; dependencias conocidas |
| `LONG_TERM` | Resultados y grandes bloques; sin fechas salvo las comprometidas |

**El detalle disminuye a medida que aumenta la incertidumbre.** Un plan detallado a seis meses en un proyecto de requisitos volátiles es falsa precisión.

El modo se elige por el proyecto, no por preferencia:

| Situación | Planificación |
|---|---|
| Requisitos estables, coste de cambio alto, compromisos externos fijos | Más predictiva: más detalle por adelantado y control contra baseline |
| Requisitos que evolucionan, feedback necesario para saber qué construir | Adaptativa: `ITERATIVE_PLANNING`, `INCREMENTAL_DELIVERY`, `FEEDBACK`, `REFINEMENT`, `ADAPTATION` |
| Mezcla (fecha externa fija con contenido que evoluciona) | Híbrida: el compromiso fijo se protege y el contenido se replanifica |

Sommerville distingue la planificación dirigida por plan, en la que el trabajo se planifica en detalle, de la planificación ágil en dos niveles: la de release, a meses vista, y la de iteración, a corto plazo. Apep toma la idea de dos niveles de precisión y deja fuera su forma obligatoria: **no exige sprints, velocity, ceremonias ni roles Scrum**. Kanban sigue siendo el sistema operativo (`work-item-flow.md`).

## 3. Fechas

| Término | Significa |
|---|---|
| `DESIRED_DATE` | Cuándo le gustaría a alguien. No obliga a nada |
| `FORECAST` | Cuándo es probable, según la evidencia actual. Se revisa cuando la evidencia cambia |
| `COMMITTED_DATE` | Una fecha con **decisión o compromiso real** de quien tiene autoridad. Sólo existe si esa decisión existe |
| `EXTERNAL_DEADLINE` | Una restricción externa (regulación, contrato, evento) con su fuente |

`DESIRED_DATE != COMMITTED_DATE`. PM no convierte un deseo en compromiso, ni un forecast optimista en fecha comprometida. Si una fecha deseada choca con el alcance o la capacidad, la salida son opciones y `DECISION_REQUIRED` (§7).

## 4. Estimación

Seis cosas distintas que no se conflan:

| Dimensión | Pregunta |
|---|---|
| `SIZE` | Cuánto trabajo hay (por ejemplo `SIZE_SIGNAL`, `work-item-shaping.md` §3) |
| `EFFORT` | Cuánto trabajo de personas requiere |
| `DURATION` | Cuánto tiempo de trabajo transcurre |
| `CALENDAR_TIME` | Cuándo termina, con disponibilidad, esperas y dependencias |
| `COST` | Cuánto cuesta |
| `CONFIDENCE` | Cuánto fiarse de las anteriores |

Conversiones prohibidas: `SIZE_SIGNAL` → horas, Story Points → días, estimación → compromiso. Los Story Points son un dato del equipo: si se aportan, se registran como tales; nunca se convierten en tiempo, y si faltan, no se inventan.

Cuando hay evidencia para estimar:

```
ESTIMATE
  DIMENSION:     <EFFORT | DURATION | CALENDAR_TIME | COST>
  RANGE:         <mínimo – máximo>
  CONFIDENCE:    LOW | MEDIUM | HIGH
  ASSUMPTIONS:   <de qué depende el rango>
  DEPENDENCIES:  <DEP-NNN que pueden moverlo>
  BASIS:         <de dónde sale: historial comparable, descomposición, juicio de quién>
```

- **Rango, no punto**, cuando la incertidumbre es material. Un único número con incertidumbre alta es falsa precisión.
- Sommerville recuerda que el tamaño real sólo se conoce al final y que las estimaciones mejoran a medida que el proyecto avanza: se reestiman con evidencia nueva, no se defienden. Añadir personas a un proyecto retrasado puede retrasarlo más; el margen de contingencia es una decisión de quien comprometa, no algo que PM añada por su cuenta.
- **Alta incertidumbre** → una pregunta acotada a `technical-discovery`, un spike o una prueba de concepto antes de estimar, cuando la diferencia importa para decidir.
- **No se fabrica una estimación para llenar una plantilla.** Sin base: `ESTIMATE: NOT_AVAILABLE`, qué haría falta para tenerla y quién puede aportarlo.

## 5. Baseline

```
BASELINE != CURRENT_STATE != FORECAST
```

Según el proyecto, puede haber `SCOPE_BASELINE`, `SCHEDULE_BASELINE`, `COST_BASELINE`, `REQUIREMENTS_BASELINE` o `RISK_BASELINE`. **Un baseline existe sólo cuando fue acordado o aprobado** por quien tiene autoridad. PM no lo autodeclara ni lo deduce del plan. No se crean baselines por simetría: un proyecto sin presupuesto propio no tiene `COST_BASELINE`.

Sin baseline, el control compara contra lo último decidido de forma explícita y lo dice (`NO_BASELINE`).

## 6. Medición

| Categoría | Mide | Ejemplos |
|---|---|---|
| `ACTIVITY_METRIC` | Esfuerzo gastado | Commits, horas, tickets movidos |
| `FLOW_METRIC` | Cómo fluye el trabajo | `AGING`, `BLOCKED_TIME`, `WIP_PRESSURE`, lead time, cycle time, throughput |
| `DELIVERY_METRIC` | Qué se entrega verificado | Requisitos `VERIFIED` / `DELIVERED` |
| `QUALITY_METRIC` | Cómo se comporta lo entregado | Defectos escapados, `REWORK`, findings bloqueantes |
| `OUTCOME_METRIC` | Si el cambio buscado ocurre | Uso real de la capacidad entregada |
| `VALUE_METRIC` | Si se obtiene el valor definido | Lo que defina `VALUE_EVIDENCE` (`project-governance.md` §3) |

- **La actividad no es outcome**, y ninguna de las dos es valor.
- Las señales de flujo de `work-item-flow.md` §8 se mantienen. `LEAD_TIME`, `CYCLE_TIME` y `THROUGHPUT` sólo se calculan con **datos reales** de una fuente (tracker, historial de PRs, o un dato concreto que aporta el humano, citado como tal). El harness no persiste estados: sin fuente, `NOT_AVAILABLE`.
- Un **forecast** calculado desde un ritmo observado es una extrapolación: se da como rango, con el supuesto (mismo equipo, mismo ritmo) explícito, y no se convierte en fecha comprometida (§3).
- No se inventan dashboards ni se rellenan métricas para que el reporte parezca completo.

## 7. Control

Cada desviación relevante:

```
DEVIATION
  EXPECTED:           <lo acordado o planificado, con su fuente (baseline o decisión)>
  CURRENT:            <estado verificado, con su evidencia>
  DELTA:              <la diferencia>
  CAUSE:              <causa conocida> | UNKNOWN
  IMPACT:             <qué objetivo, hito o compromiso afecta>
  TREND:              IMPROVING | STABLE | WORSENING | UNKNOWN
  OPTIONS:            <alternativas, con su consecuencia>
  RECOMMENDATION:     <la de PM>
  DECISION_REQUIRED:  <qué decide quién> | NONE
  NEXT_ACTION:        <acción concreta y owner>
```

- **Sin semáforos sin evidencia.** No se afirma `ON_TRACK` sin baseline (o decisión explícita), estado actual verificado y evidencia suficiente. Si falta alguno: `INSUFFICIENT_EVIDENCE` o `NO_BASELINE`, y qué falta.
- El estado actual es el de `software-project-management.md` §2: estados verificables, no porcentajes ni actividad.
- **Un conflicto entre alcance, fecha y capacidad se presenta como opciones** (reducir alcance, mover fecha, añadir capacidad, aceptar riesgo) y `DECISION_REQUIRED`. PM no reduce el alcance en silencio para conservar una fecha, ni mueve una fecha comprometida para conservar el alcance (`SKILL.md` §2).
- Una `CORRECTIVE_ACTION` la propone PM y la decide el humano (`requirements-management.md` §4.1).
