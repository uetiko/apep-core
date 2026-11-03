# Hypothesis-Driven Diagnosis

Aplica junto con `.omp/skills/diagnostics/SKILL.md` — no lo repite. Úsalo cuando exista más de una explicación plausible para el fallo y haga falta discriminar entre ellas.

## Cuándo NO se necesita este proceso

Si el fallo es directamente verificable de forma determinista (un log muestra exactamente la excepción y su origen, una query reproduce el error de forma inequívoca), no fuerces múltiples hipótesis ni un ledger — verifica directamente y pasa a `ROOT_CAUSE` (`SKILL.md` §8).

## Formular hipótesis mínimas

Genera sólo las hipótesis necesarias para cubrir las explicaciones plausibles distintas — no una lista exhaustiva de posibilidades teóricas. Cada hipótesis debe ser una afirmación causal concreta y falsable, no una vaga sospecha ("algo en la config" no es una hipótesis; "la variable de entorno X no se está inyectando en el contenedor de producción" sí lo es).

## Hipótesis vs. hecho

Una hipótesis nunca se presenta como hecho mientras no tenga evidencia confirmatoria suficiente (`SKILL.md` §3.10, evidence before inference). El `RECENT_CHANGE` que la originó, o la `PROXIMITY` que la sugirió, son motivos válidos para *plantear* la hipótesis — nunca para darla por cierta (`SKILL.md` §3.3–3.4).

## Buscar evidencia discriminante

Para cada par de hipótesis en competencia, identifica una observación cuyo resultado sería **diferente** según cuál sea cierta. Prioriza esa observación sobre evidencia que sólo confirmaría una de ellas sin descartar la otra. Pregunta rectora: *"¿qué vería si H1 fuera cierta y H2 no, frente a lo que vería si fuera al revés?"*

## Falsificar, no sólo confirmar

Intenta activamente encontrar evidencia que refute cada hipótesis viable, no sólo evidencia que la sostenga. Una hipótesis que sobrevive un intento serio de falsificación gana confianza; una que nunca fue puesta a prueba de esa forma no debería marcarse `CONFIRMED`.

## Sesgos a manejar explícitamente

- **Confirmation bias** — dejar de buscar en cuanto aparece evidencia que apoya la primera hipótesis. Contramedida: busca deliberadamente evidencia que la contradiga antes de cerrarla.
- **Recent-change bias** — asumir que el cambio más reciente es la causa sólo por proximidad temporal (`SKILL.md` §3.4). Contramedida: exige evidencia de mecanismo, no sólo de cronología.
- **Causalidad por proximidad** — asumir causa por cercanía de archivo, stack trace o línea (`SKILL.md` §3.2–3.3). Contramedida: traza el mecanismo real que conecta la causa propuesta con el síntoma.

## Observar antes que mutar

Si una hipótesis puede discriminarse observacionalmente, **no se modifica el componente sospechoso para probarla** (`SKILL.md` §3.17). Cambiar el sujeto del diagnóstico destruye la condición que estabas investigando y convierte el resultado en no reproducible. Orden de preferencia:

1. observación directa del estado, config efectiva, datos, logs o artefacto desplegado;
2. reproducción controlada en un entorno aislado, no destructiva;
3. experimento acotado y reversible, con autorización cuando toque estado real;
4. mutación del componente sospechoso — último recurso, sólo con autorización explícita.

## Selección de experimentos seguros

Antes de ejecutar un experimento para discriminar hipótesis, confirma que: es reversible o de impacto acotado, no destruye evidencia todavía necesaria (ver `runtime-and-logs.md`), y no requiere mutar producción sin autorización explícita. Si ningún experimento seguro discrimina las hipótesis restantes, márcalas `UNTESTABLE` y repórtalo como `INSUFFICIENT_EVIDENCE` (`SKILL.md` §8) en vez de forzar un experimento riesgoso.

## Reproducción: mecanismo, no historia

Reproducir el fallo demuestra que el mecanismo **existe y es capaz** de producir el síntoma. No demuestra por sí solo que ése fue el mecanismo que actuó en la ocurrencia diagnosticada (`SKILL.md` §3.14, `REPRODUCED_MECHANISM != HISTORICAL_PROOF`). Para atribuir hace falta evidencia del incidente real — ver `distributed-and-ci-incidents.md`.

## Hypothesis Ledger (proporcional)

Úsalo cuando haya varias hipótesis activas y perderles pista sea un riesgo real — no por ceremonia cuando una única explicación es directamente verificable. Cuando exista incertidumbre material, las hipótesis relevantes sí deben quedar explícitas (`SKILL.md` §7).

```
ID: H1
CLAIM: <afirmación causal concreta y falsable>
EXPLAINS: <qué parte del síntoma observado explicaría si fuera cierta>
EVIDENCE_FOR: <...>
EVIDENCE_AGAINST: <...>
DISCRIMINATING_TEST: <observación cuyo resultado difiere según esta hipótesis o sus competidoras>
STATUS: OPEN | SUPPORTED | REJECTED | CONFIRMED | UNTESTABLE
```

`EXPLAINS` importa: una hipótesis que sólo explica parte del síntoma no puede cerrarse como causa completa sin declarar qué queda sin explicar.

### Estados

| Estado | Significa |
|---|---|
| `OPEN` | Planteada, sin evidencia decisiva todavía. También el estado de una hipótesis con `EVIDENCE_AGAINST` parcial que aún no ha sido descartada — la evidencia en contra se registra en su campo, no se refleja promoviendo el estado. |
| `SUPPORTED` | Evidencia a favor, pero sin haber discriminado a sus competidoras. |
| `REJECTED` | Evidencia discriminante la descarta. |
| `CONFIRMED` | Evidencia causal directa o convergente, suficientemente determinista, la sostiene frente a sus competidoras. |
| `UNTESTABLE` | No existe observación accesible y segura que pueda discriminarla con los medios disponibles. Declararla `UNTESTABLE` es lo que permite cerrar honestamente en `INSUFFICIENT_EVIDENCE` (`SKILL.md` §8) en vez de dejarla colgando como `OPEN` indefinida. |

**`SUPPORTED` no se promueve a `CONFIRMED` sin evidencia discriminante suficiente** (`SKILL.md` §3.15). No asignes porcentajes ni scores probabilísticos a las hipótesis: el estado y la evidencia registrada son la representación de confianza.

Una hipótesis `CONFIRMED` sostiene el **mecanismo**. Atribuirlo al incidente concreto es una afirmación separada (`SKILL.md` §8.1) y requiere su propia evidencia.
