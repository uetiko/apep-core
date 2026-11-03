---
description: DELIVERY MODE — materializa un work item autorizado hasta INTEGRATION_READY (delivery-lifecycle)
argument-hint: <work item o Execution Contract autorizado, repositorio y rama>
---

# /deliver — DELIVERY MODE

Entrada:

$ARGUMENTS

Pregunta: *¿puedes materializar este work item hasta dejarlo listo para integración?* Cuando se delega el lifecycle completo, el owner es el agent `delivery-orchestrator`, que aplica `skill://delivery-lifecycle`: delégale el work item con su contexto, las decisiones cerradas y las autorizaciones que existan. Tú, **Main Session** y Control Tower, sigues siendo el puente de autoridad: recibes su `LIFECYCLE_STATE` en cada gate, preguntas al humano y le reenvías la decisión (`delivery-lifecycle` §0). Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

El routing es proporcional (`delivery-lifecycle` §4 y §8), no un pipeline fijo; `diagnostics` sólo entra ante un fallo observado. Antes de escribir, `EXECUTION_PREFLIGHT` fija el contrato autorizado y su fingerprint, la baseline congelada y el espacio de ejecución (worktree en `FORMAL`); al final, `DELIVERY_EVIDENCE` consolida verificación, review y, en `FORMAL`, la convergencia por AC (`delivery-lifecycle` §13).

Fronteras:

- `/deliver` no autoriza nada por existir: se implementa sólo con autorización suficiente — un contrato aprobado o un encargo explícito.
- El lifecycle termina en `INTEGRATION_READY`, y sólo si todo AC material está en `PASS` (`FORMAL`); `INTEGRATION_READY != COMPLETE`. Commit, push, publicación del PR, merge, tag y release no se ejecutan por `/deliver`: quedan preparados, y la Main Session los ejecuta sólo si el humano lo autoriza (`delivery-lifecycle` §6).
- Vuelve a la Main Session ante `DECISION_REQUIRED`, un gate material, evidencia insuficiente, `STOP_REPORT`, ampliación de alcance o una frontera de autoridad (`delivery-lifecycle` §7).

Termina con el `LIFECYCLE_STATE` (`delivery-lifecycle` §11) en `INTEGRATION_READY` o en el gate que lo detuvo. El ciclo del PR remoto es `/pr`.
