# Risk and Issue Management

Carga esta referencia cuando el frente justifique una revisión de riesgo real (ver `SKILL.md` §3, proportional rigor) — no para registrar una preocupación aislada, que puede vivir como una línea suelta en `RISKS`/`ISSUES` del output del análisis general. Para un work item concreto basta el perfil de §1.

## 1. Perfil de riesgo de un work item — `WORK_RISK_PROFILE`

Caracteriza el riesgo del trabajo para decidir su ruta y su formalidad. **No produce un número**: cada dimensión es una escala cualitativa con su evidencia.

```
WORK_RISK_PROFILE
  CHANGE_IMPACT:              LOW | MEDIUM | HIGH
  UNCERTAINTY:                LOW | MEDIUM | HIGH
  REVERSIBILITY:              EASY | MODERATE | HARD
  BLAST_RADIUS:               LOCAL | COMPONENT | SYSTEM | EXTERNAL
  DEPENDENCY_RISK:            LOW | MEDIUM | HIGH
  SECURITY_DATA_SENSITIVITY:  NONE | RELEVANT | MATERIAL
  OPERATIONAL_RISK:           LOW | MEDIUM | HIGH
  EVIDENCE:                   <de dónde sale cada valor>
```

| Dimensión | Pregunta |
|---|---|
| `CHANGE_IMPACT` | ¿Cuánto cambia lo que usuarios, otros sistemas u otros equipos observan? |
| `UNCERTAINTY` | ¿Cuánto no sabemos del comportamiento deseado o del estado actual? |
| `REVERSIBILITY` | ¿Se puede deshacer sin dejar datos o estado inconsistentes? |
| `BLAST_RADIUS` | Si sale mal, ¿hasta dónde llega? |
| `DEPENDENCY_RISK` | ¿Cuánto depende de otros trabajos, equipos, sistemas o decisiones abiertas? |
| `SECURITY_DATA_SENSITIVITY` | ¿Toca autenticación, permisos, secretos o datos sensibles? |
| `OPERATIONAL_RISK` | ¿Puede afectar disponibilidad, rendimiento u operación? |

Un valor sin evidencia se declara `UNKNOWN`, no se elige el más cómodo.

Uso: el perfil orienta la ruta y la formalidad (`work-item-shaping.md` §4), sin fórmula:

| Patrón | Orientación |
|---|---|
| `CHANGE_IMPACT: HIGH` + `UNCERTAINTY: HIGH` + `REVERSIBILITY: HARD` | `FORMAL` esperado; `specification`; `architecture-review` probable |
| `BLAST_RADIUS: SYSTEM`/`EXTERNAL` o contratos afectados | `architecture-review` probable |
| `SECURITY_DATA_SENSITIVITY: MATERIAL` | `security-review` cuando aplica |
| Todo `LOW` / `EASY` / `LOCAL` | Ruta `LIGHT` o `NONE` proporcional |

**El perfil no decide prioridad ni acepta riesgo.** Ordenar trabajo y aceptar un riesgo material son decisiones humanas (`SKILL.md` §2): el perfil es su evidencia, no su sustituto.

## 2. Riesgo de proyecto

El perfil de §1 caracteriza un work item. Un proyecto necesita además ver los riesgos que no pertenecen a ningún item concreto. Sommerville distingue riesgos de **proyecto** (afectan calendario o recursos), de **producto** (afectan calidad o rendimiento de lo construido) y de **negocio** (afectan a la organización), y un proceso de identificación, análisis, planificación y monitorización. Apep usa esa idea con categorías más finas, sólo las que aplican:

| Categoría | Ejemplo | Análisis profundo |
|---|---|---|
| `PROJECT_RISK` | El proyecto pierde su justificación o su sponsor | PM |
| `TECHNICAL_RISK` | Una tecnología no rinde como se espera | `technical-discovery`, `architecture-review` |
| `DELIVERY_RISK` | La integración o el despliegue falla | `delivery-lifecycle`; operación |
| `REQUIREMENTS_RISK` | Requisitos volátiles o sin fuente (`requirements-management.md` §2) | `specification` para la semántica |
| `DEPENDENCY_RISK` | Un tercero no entrega a tiempo | El dueño de la dependencia |
| `OPERATIONAL_RISK` | Nadie puede operar lo entregado | Operación; `deployment-and-operational-readiness.md` |
| `SECURITY_RISK` | Exposición de datos o permisos | `security-review` |
| `ORGANIZATIONAL_RISK` | Cambio de prioridades o de estructura | Autoridad humana |
| `SCHEDULE_RISK` | Un compromiso de fecha no es alcanzable | PM (`planning-and-control.md` §7) |
| `RESOURCE_RISK` | Falta capacidad o un especialista | PM (`software-project-management.md` §5) |

Reparto de responsabilidades:

```
PM IDENTIFIES AND MANAGES THE RISK.
THE SPECIALIST CAPABILITY ANALYZES THE DEEP TECHNICAL RISK.
HUMAN AUTHORITY ACCEPTS THE RISK.
```

PM no repite el análisis de `security-review` ni de `architecture-review`: registra el riesgo, lo deriva y sigue su estado.

**Estado de un riesgo**, reportado con lo que se sabe en el momento (el harness no persiste registros):

| Estado | Significa |
|---|---|
| `IDENTIFIED` | Existe y está descrito |
| `ASSESSED` | Se estimaron, con evidencia, su probabilidad y su impacto, o se declaró `INSUFFICIENT_EVIDENCE` |
| `RESPONSE_PROPOSED` | Hay una mitigación o contingencia propuesta, **no aceptada todavía** |
| `MONITORED` | Hay una señal temprana y alguien que la observa |
| `MATERIALIZED` | Ocurrió: pasa a ser un `ISSUE` (abajo) |
| `CLOSED` | Ya no puede ocurrir, o el owner lo cerró |

Aceptar un riesgo (seguir adelante con una mitigación insuficiente) no es un estado que PM asigne: es una `DECISION` de la `RISK_ACCEPTANCE_AUTHORITY` (`project-governance.md` §1).

## RISK != ISSUE

`RISK` es un evento o condición incierta **futura** que, si ocurre, puede afectar objetivos. `ISSUE` es un problema, impedimento o condición relevante que **ya existe**. Si la condición ya ocurrió, clasifícala como `ISSUE`, nunca como `RISK` retroactivo — un riesgo materializado deja de ser riesgo.

## Estructura de un riesgo

Cuando sea proporcional al proyecto, registra cada riesgo con:

| Campo | Contenido |
|---|---|
| `CAUSE` | Qué condición o factor origina el riesgo. |
| `EVENT` | Qué podría ocurrir concretamente. |
| `IMPACT` | Qué objetivo se vería afectado y cómo. |
| `PROBABILITY` | Qué tan probable es, cuando pueda estimarse razonablemente — no inventar precisión. |
| `SEVERITY` | Magnitud del impacto si ocurre. |
| `EARLY_SIGNALS` | Qué señal observable indicaría que el riesgo se está materializando. |
| `MITIGATION` | Acción para reducir probabilidad o impacto antes de que ocurra. |
| `CONTINGENCY` | Qué hacer si ocurre a pesar de la mitigación. |
| `OWNER` | Quién es responsable de monitorear y actuar. |

No completar un campo con precisión falsa cuando la evidencia no la sustenta — es preferible declarar `INSUFFICIENT_EVIDENCE` en `PROBABILITY` o `SEVERITY` que inventar un número o una escala sin base.

## Categorías de riesgo

Distinguir, según aplique: técnico · operativo · financiero · humano · legal · proveedor · alcance · seguridad · infraestructura · deployment · adopción. Un mismo evento puede tener más de una categoría — regístralas todas las relevantes, no fuerces una única etiqueta.

## Estructura de un issue

Un issue no necesita `PROBABILITY` (ya ocurrió) pero sí: descripción concreta, desde cuándo existe, impacto actual (no hipotético), qué lo está bloqueando, y `OWNER`. Si un issue bloquea una decisión de alcance, costo, fecha o arquitectura no cerrada, decláralo como `DECISION_REQUIRED` además de como `ISSUE` — son categorías compatibles, no excluyentes.

## Orden de atención

Para presentar los riesgos, ordénalos por severidad × probabilidad, y los issues por impacto actual × urgencia — no por orden de descubrimiento ni por facilidad de resolución. Ese orden es **evidencia para quien decide**, no una prioridad de trabajo: qué se atiende primero lo decide el owner (`SKILL.md` §2). No generes una matriz de riesgo/impacto decorativa si el número de riesgos es pequeño (menos de 4-5); en ese caso una tabla simple o incluso prosa es más útil y menos ceremonial.

## Relación con control (ver `SKILL.md` §11)

Un riesgo que se materializa se reclasifica como `ISSUE` y, si además invalida el plan vigente, dispara `STOP_CONDITIONS` de `SKILL.md` §14 para la parte afectada del análisis — no para el frente completo salvo que la severidad lo justifique. Un riesgo aceptado (mitigación insuficiente pero se decide continuar) requiere `DECISION` explícita de la autoridad correspondiente — nunca se asume aceptado por defecto ni por silencio.

## Qué NO hacer

No generar un registro de riesgos exhaustivo por hábito metodológico. No inventar probabilidades o severidades sin evidencia. No mezclar `RISK` e `ISSUE` en la misma fila de una tabla sin distinguir la columna. No aceptar un riesgo en nombre del stakeholder — reportar `DECISION_REQUIRED` cuando la aceptación de riesgo sea material.
