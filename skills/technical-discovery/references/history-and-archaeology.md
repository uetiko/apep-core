# History and Archaeology

Aplica junto con `.omp/skills/technical-discovery/SKILL.md` — no lo repite. **Condicional, no un paso por defecto.**

## Cuándo consultar el historial

Sólo cuando la evidencia del estado actual, por sí sola, no explica adecuadamente:

- la procedencia de una decisión o estructura presente en el código;
- un cambio semántico relevante para la pregunta investigada;
- una migración parcial (dos patrones conviviendo, uno "viejo" y uno "nuevo");
- un concepto renombrado cuyo rastro anterior sigue afectando el comportamiento actual;
- una ruta legacy que el código actual no explica por qué sigue existiendo;
- una implementación abandonada que deja restos observables;
- una `CONTRADICTION` (`SKILL.md` §5) entre fuentes que el estado presente no resuelve.

Si el estado actual ya responde la pregunta con suficiente confianza, **no** abras historial "por si acaso" — es evidencia adicional, no un paso obligatorio.

## Principio a preservar

**El historial de git explica procedencia; no reemplaza la verdad ejecutable actual.** Un commit, un mensaje de PR o un ADR antiguo documentan una intención declarada en su momento (`DECLARED_INTENT`) — no lo que el código hace hoy. Si el historial y el comportamiento actual difieren, el comportamiento actual es el `FACT`; el historial explica el `CONTRADICTION` o la `INFERENCE` sobre cómo se llegó ahí, pero no lo sobreescribe.

## Cómo consultar — vertical, no exploratorio

No hagas `git log`/`blame` amplio sobre el repositorio completo esperando que algo relevante aparezca. Acota la consulta a lo que la pregunta necesita:

- `git log -p --follow <archivo>` o `git log -L <rango>,<archivo>` sobre el archivo/símbolo concreto en discusión, no sobre el directorio que lo contiene.
- `git blame` sobre las líneas específicas que generan la duda, para ubicar el commit/PR que las introdujo o modificó.
- Búsqueda de mensajes de commit/PR por el nombre anterior de un concepto renombrado, cuando se sospecha una migración incompleta.
- Lectura de un ADR o documento de decisión específico ya identificado como relevante — no una búsqueda abierta de "toda la documentación histórica".

Si la exploración acotada no resuelve la duda, repórtalo como `UNKNOWN` con lo que sí se intentó — no escales a una arqueología horizontal completa sin que la pregunta lo justifique.

## Salida típica

Una explicación breve de la procedencia relevante, marcada como `DECLARED_INTENT`/`INFERENCE` según corresponda, conectada explícitamente con el `FACT` del comportamiento actual que motivó la consulta — nunca presentada como sustituto de ese comportamiento actual.
