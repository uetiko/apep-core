# Delivery evidence — verificación, convergencia, remediation e integración

Referencia de `delivery-lifecycle` (`SKILL.md` §4–§6). Responde: ¿qué demuestra la evidencia? ¿cumple cada criterio del contrato? ¿qué se puede corregir sin una decisión nueva? ¿cuándo está listo para integrar, y qué no significa eso?

```
IMPLEMENTED != VERIFIED != CONFORMANT
SELF-VERIFICATION != INDEPENDENT CONFORMANCE
EVERY MATERIAL AC REQUIRES EVIDENCE.
INTEGRATION_READY != COMPLETE
```

## 1. Verificación

La hace `implementation`, dentro de su contrato y sin preguntar por cada comando:

```
CHEAPEST RELEVANT CHECK → TARGETED VERIFICATION → BROADER REGRESSION WHEN JUSTIFIED
```

Una suite masiva se ejecuta cuando el radio del cambio la justifica, no por costumbre. La evidencia no se debilita para pasar: no se borra, salta ni relaja un test o una regla para obtener verde (`code-quality` §8).

Cada verificación se registra:

```
command:   <comando exacto>
purpose:   <qué demuestra>
scope:     <qué cubre: archivos, módulo, AC>
result:    PASS | FAIL | ERROR | NOT_RUN (<por qué>)
evidence:  <extracto de salida, conteos, ruta del log>
```

**Atribución de fallos**, contra la baseline (`references/execution-preflight.md` §3):

| Clase | Cuándo |
|---|---|
| `PREEXISTING_FAILURE` | Fallaba igual en la baseline, sin relación con el cambio |
| `INTRODUCED_FAILURE` | Pasa en la baseline y falla con el cambio, o la evidencia lo liga al cambio |
| `UNKNOWN_ATTRIBUTION` | No se midió en la baseline o la evidencia no permite decidir |

Un `INTRODUCED_FAILURE` se corrige dentro del contrato. Un `PREEXISTING_FAILURE` se reporta y no se corrige, salvo que el contrato lo incluya; si impide evaluar un AC, es un evento de escalado del worker. `UNKNOWN_ATTRIBUTION` nunca se presenta como preexistente para cerrar.

El worker entrega `IMPLEMENTATION_RESULT` (agent `implementation`, *report*). Es la declaración de quien implementó: entrada de la revisión, no su prueba.

## 2. Revisión independiente y convergencia

`implementation-review` revisa partiendo de evidencia propia — contrato autorizado, inventario de AC, baseline, diff efectivo obtenido con Git desde el commit de la baseline, `IMPLEMENTATION_RESULT` y evidencia de verificación — y, cuando existe una especificación formal, produce `AC_CONVERGENCE_RESULT` (`skill://implementation-review/references/ac-convergence.md`). Es el owner de la convergencia; `implementation` no la declara.

## 3. Remediation

`REVIEW_FINDING != AUTHORIZATION_TO_FIX`. Quien ejecuta el lifecycle clasifica cada finding — y cada AC que no esté en `PASS` —; ni la review ni el worker lo hacen:

| Clase | Cuándo | Acción |
|---|---|---|
| `FIX_ALREADY_AUTHORIZED` | La corrección está inequívocamente dentro del contrato, no cambia semántica, no amplía alcance y no introduce una decisión material | Vuelve a `implementation` con el finding concreto. La decisión humana que la cubre es el contrato autorizado; no hace falta otra |
| `DECISION_REQUIRED` | Corregir exige una decisión reservada o elegir entre comportamientos | `DECISION_REQUIRED` al humano; nada se corrige mientras tanto |
| `OUT_OF_SCOPE` | El finding señala algo fuera del contrato y fuera del cambio (deuda, un defecto ajeno) | Se reporta; no se toca |
| `CONTRACT_CONTRADICTION` | El finding muestra que el contrato es contradictorio o imposible de cumplir tal como está | `DECISION_CONTRADICTION` hacia `specification` y el humano; el contrato no se reescribe en Línea 2 |

```
REMEDIATION MAY REPAIR IMPLEMENTATION.
REMEDIATION MAY NOT REWRITE THE CONTRACT.
OUT-OF-SCOPE DISCOVERY IS REPORTED, NOT ABSORBED.
```

Precisiones:

- **Cambio fuera de alcance introducido por esta ejecución** (`OUT_OF_SCOPE_CHANGE`, `UNREQUESTED_BEHAVIOR`): no es `OUT_OF_SCOPE` — está en el diff. Retirarlo o incorporarlo al contrato lo decide el humano (`DECISION_REQUIRED`, con derivación a `governance-review`), y mientras tanto `integration_ready: NO`.
- **AC `UNVERIFIED`**: aportar la evidencia que falta es `FIX_ALREADY_AUTHORIZED` cuando el contrato la exige — su `VALIDATION`, el método de verificación del AC o su `DEFINITION_OF_DONE` —; no es comportamiento nuevo. Si el contrato no permite saber cómo debe verificarse, `DECISION_REQUIRED`.
- **Test que protege lo contrario del AC**: corregirlo hacia el contrato no es debilitar evidencia (`code-quality` §8 lo permite cuando el contrato define ese comportamiento); es parte de la remediation del AC.
- **Fallos dentro del bucle del worker**: lo que `implementation` corrige en su propio ciclo `edit → test → fix → test` es parte de implementar, no remediation; la clasificación de esta sección se aplica a lo que encuentra la review.

**Vuelta acotada:** `fix → retest → re-review independiente → convergencia`, **una vez**. Si después persiste un finding bloqueante o un AC material fuera de `PASS`, el resultado es `REMEDIATION_EXHAUSTED` con su evidencia (estado `BLOCKED`): decide el humano. Sin bucles: `CONTINUITY OVER PERFECTION`.

## 4. `DELIVERY_EVIDENCE`

Consolida la ejecución para que `git-workflow` prepare commit y PR, y para que el humano decida el siguiente paso. Lo produce quien ejecuta el lifecycle; en un micro cambio cabe en pocas líneas.

```
DELIVERY_EVIDENCE
  execution:            <work item>
  snapshot:             <AUTHORIZED_EXECUTION_SNAPSHOT · fingerprint re-verificado: MATCH | STALE | NOT_AVAILABLE>
  baseline:             <EXECUTION_BASELINE>
  workspace:            <checkout o worktree · estado>
  files_changed:        <lista, desde el diff contra la baseline>
  verification:         <registros de §1 · fallos por atribución>
  implementation_review: <REVIEW_OUTCOME · findings>
  ac_convergence:       <AC_CONVERGENCE_RESULT> | NOT_APPLICABLE (sin AC-NNN formales)
  specialized_reviews:  <architecture · security · governance, con su resultado> | NONE
  remediation:          NONE | REMEDIATED | REMEDIATION_EXHAUSTED
  unresolved_findings:  NONE | <lista>
  deviations:           NONE | <lista>
  discovered_debt:      NONE | <lista clasificada>
  decisions_required:   NONE | <lista>
  integration_ready:    YES | NO
  blocking_reasons:     NONE | <lista>
```

## 5. Gate de `INTEGRATION_READY`

`integration_ready: YES` exige:

- fingerprint del contrato re-verificado sin cambios, o `NOT_AVAILABLE` declarado para un contrato en sesión;
- verificación aplicable ejecutada y registrada, sin `INTRODUCED_FAILURE` ni `UNKNOWN_ATTRIBUTION` material abiertos;
- `implementation-review` sin finding `BLOCKING` abierto;
- ningún cambio fuera de alcance ni comportamiento no pedido introducido por esta ejecución sin decisión humana (§3);
- en `FORMAL`, **todo AC material aplicable en `PASS`** (`AC_CONVERGENCE_RESULT: CONVERGED`). Un solo AC material en `UNVERIFIED`, `UNIMPLEMENTED` o `CONTRADICTED` deja `integration_ready: NO` con sus `blocking_reasons`, y la salida es remediation autorizable, `DECISION_REQUIRED` o `REMEDIATION_EXHAUSTED`. El requisito no se suaviza para cerrar;
- reviews especializadas aplicables hechas, sin bloqueo abierto;
- `COMMIT_MESSAGE` y, si corresponde, `PR_TITLE`/`PR_BODY` preparados (`git-workflow`).

En `NONE` y `LIGHT` el gate es el mismo con los AC del task contract y su evidencia proporcional; no se exige un inventario `AC-NNN` que no existe.

```
INTEGRATION_READY != COMPLETE
INTEGRATION_READY != AUTHORIZED_TO_COMMIT
INTEGRATION_READY != AUTHORIZED_TO_PUSH
INTEGRATION_READY != AUTHORIZED_TO_PUBLISH_PR
INTEGRATION_READY != AUTHORIZED_TO_MERGE
REMOTE INTEGRATION BELONGS TO THE PR LIFECYCLE.
```

`/deliver` termina aquí. Commit, push y publicación del PR los ejecuta la Main Session sólo con autorización (`SKILL.md` §6); el ciclo del PR remoto es `pr-review` (`/pr`); `COMPLETE` lo declara el humano.
