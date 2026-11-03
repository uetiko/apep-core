# Project Closure

Carga esta referencia cuando se prepare el cierre de un proyecto o frente — no cuando simplemente se complete una tarea o se despliegue un cambio (ver `SKILL.md` §10: deployment no equivale a cierre).

## PROJECT_SUCCESS vs. PROJECT_CLOSURE (ver `SKILL.md` §10)

`PROJECT_SUCCESS` es un juicio sobre resultados: ¿se alcanzaron los criterios de éxito definidos? `PROJECT_CLOSURE` es un estado administrativo/operativo: ¿se cumplieron las condiciones para cerrar formalmente el proyecto? Un proyecto puede cerrarse sin haber alcanzado éxito completo (cierre con deuda aceptada y documentada), y puede haber tenido éxito técnico sin estar aún en condiciones de cerrarse (falta transferencia, documentación o aceptación formal). No los trates como sinónimos ni asumas que uno implica el otro.

## Checklist de cierre

Evalúa explícitamente cada punto; si no aplica al proyecto concreto, decláralo `NOT_APPLICABLE`. Si falta evidencia, decláralo — no asumas cumplimiento por defecto.

| Criterio | Qué verificar |
|---|---|
| `DELIVERABLES_ACCEPTED` | Los entregables finales fueron aceptados explícitamente por quien tiene autoridad para aceptarlos — no sólo entregados. |
| `KNOWLEDGE_TRANSFERRED` | Quien va a operar, mantener o continuar el trabajo tiene el conocimiento necesario, no sólo acceso a documentación. |
| `DOCUMENTATION_UPDATED` | La documentación relevante (técnica, operativa, de usuario) refleja el estado final, no un estado intermedio. |
| `DEBT_DOCUMENTED` | Toda deuda técnica u organizacional aceptada conscientemente está registrada, con su condición de resolución si la tiene. |
| `PENDING_ITEMS_TRACKED` | Todo pendiente que no bloquea el cierre está registrado en algún lugar de seguimiento real, no perdido en la conversación. |
| `OPERATIONAL_HANDOVER_CONFIRMED` | Operación confirma explícitamente que puede sostener el sistema — no se asume por haber compartido un runbook. |
| `STAKEHOLDER_SIGN_OFF` | Los stakeholders con autoridad relevante confirmaron el cierre — silencio no es sign-off. |
| `LESSONS_CAPTURED` | Se registraron aprendizajes concretos (qué funcionó, qué no, qué haría distinto) — no una frase genérica de cierre. |
| `FOLLOW_UP_DEFINED` | Si el proyecto requiere seguimiento posterior (métricas de adopción, revisión a N semanas), está definido quién lo hace y cuándo. |
| `ADMINISTRATIVE_CLOSURE` | Cuando aplique: contratos, presupuestos o compromisos externos asociados quedaron formalmente cerrados. |

## Veredicto de cierre

```
CLOSURE_READINESS:  READY_FOR_CLOSURE | NOT_READY_FOR_CLOSURE | INSUFFICIENT_EVIDENCE
BLOCKING:           <criterios del checklist sin cumplir que impiden cerrar>
```

`READY_FOR_CLOSURE` dice que las condiciones se cumplen; **cerrar lo decide quien tiene autoridad** (`project-governance.md` §1), no este skill. Sin owner operativo acordado para lo entregado (`OPERATIONAL_HANDOVER_CONFIRMED`), sin `ACCEPTANCE_AUTHORITY` que haya aceptado, o con requisitos sin `ACCEPTANCE_OWNER` (`requirements-management.md` §5), el veredicto es `NOT_READY_FOR_CLOSURE`, aunque todo esté desplegado. Cerrar el proyecto no cierra el producto: su evolución y mantenimiento continúan con su owner (`software-project-management.md` §6).

Quien tiene autoridad puede decidir **cerrar igualmente**, con lo que falta como deuda o pendiente aceptado (`DEBT_DOCUMENTED`, `PENDING_ITEMS_TRACKED`). Eso es una `DECISION` suya con su riesgo aceptado por la `RISK_ACCEPTANCE_AUTHORITY`, no un cambio del veredicto: PM lo presenta como opción con su consecuencia, el veredicto sigue siendo `NOT_READY_FOR_CLOSURE` y lo que falta queda registrado con owner.

## Criterios de cierre vs. criterios de éxito

Los criterios de cierre son condiciones de proceso (¿está todo entregado, aceptado, documentado y transferido?). Los criterios de éxito son condiciones de resultado (¿se logró el valor perseguido?). Un proyecto puede cumplir todos los criterios de cierre y aun así no haber alcanzado sus criterios de éxito — en ese caso, ambos hechos se reportan por separado, sin que uno oscurezca al otro.

## Qué NO hacer

No declarar cierre porque el código está desplegado. No asumir transferencia de conocimiento por la existencia de documentación. No convertir "nadie se quejó" en `STAKEHOLDER_SIGN_OFF`. No omitir deuda o pendientes para que el cierre parezca más limpio de lo que es — el objetivo es conocer el estado real, no producir un cierre que se vea bien (`SKILL.md` §17).
