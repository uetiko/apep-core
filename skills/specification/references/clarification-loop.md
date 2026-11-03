SOURCE: harness Apep 0.5.0 — metodología propia. Adapta, sin copiar, mecanismos de GitHub Spec Kit (`templates/commands/clarify.md` @67e0f72): una pregunta a la vez cuando las respuestas dependen entre sí, pregunta interrogativa completa con "why it matters", opción recomendada o respuesta sugerida, registro de cada respuesta e integración inmediata en la spec sustituyendo el texto contradicho. No adopta su máximo de 5 preguntas ni sus defaults de industria. Spec Kit es fuente de referencia, no de autoridad.
ADAPTATION: OMP Specification Skill v0.2

# Clarification Loop y Clarification Ledger

La clarificación es parte de `specification`, no una capability aparte. Sólo trata aperturas **materiales**: los hechos verificables van a discovery y las aperturas no materiales se cierran con una assumption (`ambiguity-assessment.md` §3–§5).

```
AMBIGUITY_DETECTED → CLASSIFY → PRIORITIZE → ASK → ANSWER → RECORD → APPLY → REVALIDATE → NEXT QUESTION IF NEEDED
```

No se espera al readiness gate para preguntar:

```
AMBIGUITY SHOULD BE CLOSED AS EARLY AS THE EVIDENCE EXPOSES IT.
ASK THE MINIMUM SET OF QUESTIONS NEEDED TO REMOVE MATERIAL AMBIGUITY.
```

## 1. CLASSIFY y PRIORITIZE

- Sólo entra en el loop lo clasificado como `AMBIGUITY` material, `DECISION_REQUIRED` o `CONTRADICTION` que exige decisión.
- Se ordena por `IMPACT × UNCERTAINTY` (`ambiguity-assessment.md` §2) y por dependencia: primero la pregunta cuya respuesta puede cambiar o eliminar otras.
- **Una pregunta a la vez** cuando su respuesta puede modificar las siguientes: las dependientes se preguntan después, no en el mismo turno. Las preguntas independientes entre sí pueden agruparse en un mismo turno.
- No hay un máximo fijo de preguntas. El límite es el conjunto mínimo que elimina la ambigüedad material. Si el humano decide parar, lo pendiente queda `OPEN` y la spec no puede llegar a `EXECUTION_READY` mientras siga siendo material (C1).

## 2. ASK — forma de la pregunta

Toda pregunta material:

- es una **interrogativa completa**, que se entiende sola, terminada en `?`. Un rótulo ("Retención de datos (BR-004)") no es una pregunta;
- es **específica** y cubre **una sola decisión conceptual**;
- usa lenguaje del dominio, sin jerga técnica innecesaria;
- pregunta por **comportamiento** cuando lo que falta es comportamiento, no por implementación (§5);
- lleva `WHY_IT_MATTERS`: una frase sobre qué cambia en lo que se construye o en cómo se acepta.

Una pregunta material es una `DECISION_REQUIRED` y se emite en el formato exacto de `ENGINEERING_GOVERNANCE.md` §1.4, precedido de su identificador y su impacto:

```
CLAR-003 · CLARIFICATION_REQUIRED · AFFECTS: BR-002, AC-004
WHY_IT_MATTERS: decide si una cuenta suspendida puede seguir recibiendo pagos, lo que cambia el flujo principal y dos criterios de aceptación.

DECISION_REQUIRED

FACTS:
  <lo que dice la evidencia y lo que falta>
DECISION:
  ¿<pregunta interrogativa completa>?
OPTIONS:
  A — <opción> · B — <opción> · (C — no hacer nada, cuando sea viable)
TRADEOFFS:
  <qué implica cada opción para el comportamiento y la aceptación>
RECOMMENDATION:
  RECOMMENDED: B — <justificación breve>
CONSEQUENCES:
  <efecto a medio plazo de cada opción, cuando sea relevante>
BLOCKING_SCOPE:
  <qué queda bloqueado y qué puede seguir avanzando>
```

Las secciones pueden ser de una línea. Proporcionalidad no significa omitir campos: significa no inflarlos.

### RECOMMENDED y SUGGESTED

| Marca | Cuándo | Qué hace |
|---|---|---|
| `RECOMMENDED: <opción>` | Hay opciones discretas y una es razonablemente mejor | Es una recomendación (`SKILL.md` §3). **Nunca se aplica sola**: exige una respuesta humana explícita. "Acepto la recomendación" es explícita; el silencio no |
| `SUGGESTED: <respuesta>` | La respuesta es abierta y hay un default razonable | Antes de proponerlo se clasifica su materialidad. Si el default es no material, no hay pregunta: se registra como `ASM-NNN`. Si es material, `SUGGESTED` es una propuesta más y también exige respuesta explícita |

## 3. ANSWER, RECORD, APPLY

- **ANSWER**: si la respuesta es ambigua, se pide una aclaración breve de esa misma pregunta, sin abrir otra.
- **Una respuesta sólo cierra lo que dice.** Al aplicarla no se añade ninguna regla, umbral, momento, cálculo o permiso que la respuesta no contenga. Si para que el comportamiento sea completo hace falta algo más, es una pregunta nueva, no una consecuencia "aplicada".
- **"Fuera de alcance" no cierra lo que el alcance necesita.** Si la respuesta excluye algo de lo que depende el comportamiento que sí está en alcance (p. ej. excluir "qué pasa con el tiempo ya pagado" cuando pausar exige saber cuándo empieza la pausa), la apertura no queda cerrada: se vuelve a preguntar explicando la dependencia. Si el owner mantiene la exclusión, la parte afectada del alcance queda bloqueada (`DECISION_REQUIRED`) o se reduce con su decisión explícita; nunca se completa con una inferencia.
- **Una regla genérica no es una decisión explícita sobre una parte concreta.** Una respuesta del tipo "todo lo que sea regla de negocio, déjalo fuera" cierra las aperturas de las que no depende nada en alcance. No reduce el alcance en lo que sí depende de ellas: para eso hace falta que el owner, informado de la dependencia, decida sobre esa parte concreta ("entonces no se puede cancelar con una pausa programada", o "quita la pausa programada"). Mientras no lo haga, la parte afectada sigue bloqueada.
- **Una condición de parada no sustituye un comportamiento.** Si un estado o caso es alcanzable por el flujo en alcance (la ejecución lo encontrará necesariamente), su comportamiento tiene que estar especificado o el caso tiene que quedar fuera por una reducción de alcance que lo haga inalcanzable. Una `STOP_CONDITION` del contrato 07 del tipo "detenerse si hace falta definir X" sobre un caso así es un item abierto material para C1, no un cierre.
- **Una presuposición no es una respuesta.** Que una respuesta presuponga un comportamiento (una métrica que mide algo "dentro del flujo de cancelación" no dice que la pausa se ofrezca ahí) no lo decide: se pregunta.
- **Una pregunta respondida sólo en parte se divide.** La parte respondida queda `APPLIED` en su entrada, que lo dice en `ANSWER`; la parte sin responder pasa a una `CLAR-NNN` nueva, `OPEN`, que cita la original.
- **El comportamiento existente que el owner cita** ("la regla de cancelación de hoy") es un hecho del sistema: se verifica con discovery cuando el repositorio es accesible. Si no lo es, se registra como dependencia e invariante a preservar, con una `STOP_CONDITION` si al ejecutar resulta distinto. Eso es válido porque no especifica comportamiento nuevo, a diferencia de un caso alcanzable sin definir. Sólo cuenta como comportamiento existente lo que **el owner o la evidencia identifican como tal**. Suponer que una parte sin responder "la resuelve el proceso que ya existe" es una inferencia: esa parte se divide y queda `OPEN`. Una entrada `APPLIED` nunca registra en `ANSWER` que algo no se respondió.
- **Una delegación explícita es una respuesta.** "Decídelo tú" sobre algo **no material** permite cerrarlo como `ASM-NNN`, citando la delegación. Sobre algo material no transfiere la decisión: se aplica la política de assumptions igual, y lo que no la cumple sigue abierto.
- **RECORD**: cada respuesta se registra en el ledger (§4) en el momento, con su fuente.
- **APPLY**: la respuesta se integra en los artefactos que afecta, **sustituyendo** el texto que contradice:

| La respuesta toca… | Se actualiza |
|---|---|
| Alcance o fuera de alcance | `02` (límites del problema) y `03` (alcance funcional / fuera de alcance) |
| Actores o permisos | `03` (actores, reglas) y `04` (casos de uso) |
| Regla de negocio | `03` (`BR-NNN`, con `SOURCE: CLAR-NNN`) |
| Datos, estados o transiciones | `03` (entidades, estados, transiciones) |
| Flujo o caso límite | `03` (flujos, casos límite) y `05` (escenarios) |
| Criterio de aceptación | `03` (registro `AC-NNN`, con `DERIVED_FROM` actualizado) |
| Terminología | Se normaliza el término en todos los artefactos activos; el término antiguo se menciona una sola vez si hace falta ("antes llamado X") |
| Restricción cerrada | `03` (restricciones) y `07` (`CONSTRAINTS` / `AUTHORIZED_DECISIONS`) |

```
HISTORY LIVES IN THE LEDGER. CURRENT TRUTH LIVES IN THE ARTIFACTS.
```

En los artefactos activos no conviven versiones contradictorias: no se deja "antes decía X, ahora Y" ni la alternativa descartada. Un `AC-NNN` cuyo significado cambia se reescribe con el mismo ID cuando sigue verificando la misma intención; si la intención cambia, el AC anterior se marca retirado y se crea uno nuevo (`03-hard-specification.md`). Cuando la respuesta introduce un límite o caso nuevo que hay que verificar (p. ej. "el día 30 se acepta, el 31 se rechaza"), se añaden los AC y escenarios necesarios con el siguiente ID libre y `DERIVED_FROM: CLAR-NNN`. Un texto que sigue siendo verdadero con la respuesta no se reescribe sólo porque mencione otro valor.

- **REVALIDATE**: tras aplicar, se revisan los checks de calidad sobre los requisitos tocados (`specification-quality.md`) y las pasadas de coherencia sobre los IDs afectados (`coherence-review.md`). Una respuesta puede abrir una pregunta nueva: entra en el loop con su propia prioridad.

## 4. Clarification Ledger

Archivo `CLARIFICATION_LEDGER.md`, junto a los demás artefactos de la tarea (`SKILL.md` §10). Se crea con la primera entrada; una spec sin clarificaciones no lo necesita.

```
CLAR-001
QUESTION:        ¿<pregunta>?
WHY_IT_MATTERS:  <frase>
CLASSIFICATION:  MATERIAL_DECISION | FACTUAL_UNKNOWN | CONTRADICTION | NON_MATERIAL_ASSUMPTION
ANSWER:          <respuesta> | —
SOURCE:          HUMAN | DISCOVERY | GOVERNANCE | REPOSITORY_EVIDENCE   (+ quién / dónde / cuándo)
AFFECTS:         BR-… · UC-… · SC-… · AC-… · TASK-… · AT-…
STATUS:          OPEN | APPLIED | SUPERSEDED
SUPERSEDED_BY:   CLAR-NNN   (sólo si STATUS = SUPERSEDED)
```

| `STATUS` | Significa |
|---|---|
| `OPEN` | Sin respuesta, o con respuesta aún no integrada en los artefactos |
| `APPLIED` | Respondida e integrada; los artefactos ya no contradicen la respuesta |
| `SUPERSEDED` | Sustituida por una respuesta posterior, que vive en su propia entrada |

Reglas:

- Toda respuesta **material** queda en el ledger, sea cual sea su fuente.
- Un `FACTUAL_UNKNOWN` resuelto por discovery se registra sólo si su respuesta cambió la semántica de algún artefacto. Si sólo confirmó lo que ya estaba escrito, basta con la evidencia en el artefacto.
- Las assumptions no materiales viven como `ASM-NNN` en los artefactos, no en el ledger, salvo que una pregunta se reclasificara como `NON_MATERIAL_ASSUMPTION`; esa entrada apunta a su `ASM-NNN`.
- `SOURCE: HUMAN` exige una respuesta explícita localizable. Una recomendación aceptada se registra con la respuesta humana que la aceptó.
- Una respuesta nueva que contradice una `APPLIED` crea una entrada nueva y marca la anterior `SUPERSEDED`. Si la anterior era una decisión humana cerrada, sustituirla es decisión del owner (`ambiguity-assessment.md` §3).
- Los IDs `CLAR-NNN` son estables: no se renumeran ni se reutilizan.
- El ledger es historia. **No es fuente de requisitos**: un requisito que sólo existe en el ledger y no en los artefactos es un finding de coherencia (pass 12).

## 5. Frontera de la clarificación

La clarificación pregunta **qué** y **por qué**, no **cómo**. No pregunta por:

- tecnologías o productos ("¿PostgreSQL o DynamoDB?");
- nombres de clases, estructura de carpetas o patrones;
- comparaciones de stack;
- secuenciación de la implementación;
- detalles tácticos de código.

Cuando parece faltar una de esas cosas, normalmente falta un dato de comportamiento detrás:

| Pregunta mal planteada | Pregunta de comportamiento |
|---|---|
| ¿PostgreSQL o DynamoDB para el histórico? | ¿Qué consultas debe responder el histórico, con qué consistencia y durante cuánto tiempo se conserva? |
| ¿Usamos colas o llamadas síncronas? | ¿Puede el usuario continuar antes de que el sistema externo confirme, y qué ve si la confirmación falla? |
| ¿Lo hacemos con un patrón Strategy? | ¿Qué variantes de cálculo existen y quién decide cuál aplica a cada caso? |

**Excepción:** si una tecnología, arquitectura o contrato ya es una decisión humana cerrada o gobernanza de repositorio, no se pregunta. Se registra como `CONSTRAINT` con su fuente.

**Estado de una solución propuesta.** Preguntar si una solución mencionada (`STATUS_UNKNOWN`, `ambiguity-assessment.md` §1) es ya una decisión cerrada **no** es una pregunta de implementación: "¿Exportar a Excel es un requisito o sólo un ejemplo?" está permitida cuando su respuesta es material. Lo que no se hace es comparar alternativas técnicas. Si nada indica que la solución esté decidida y su estado no es material, se trata como `PROPOSAL` y el requisito se reescribe como comportamiento, sin preguntar.

## 6. Contexto delegado

`delivery-orchestrator` corre headless y no puede preguntar en vivo. Ante una clarificación material se detiene en esa parte, devuelve los `CLAR-NNN` en `decisions_required` de su `LIFECYCLE_STATE` y espera a que la Main Session lo reanude con las respuestas. Lo que no depende de esas respuestas puede seguir avanzando.
