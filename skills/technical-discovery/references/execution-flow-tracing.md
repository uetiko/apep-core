# Execution Flow Tracing

Aplica junto con `.omp/skills/technical-discovery/SKILL.md` — no lo repite. Úsalo para `FLOW_DISCOVERY` y para la parte `TRACE EXECUTION` de un `SYSTEM_DISCOVERY` o de un `TARGETED_DISCOVERY` que involucre un camino de ejecución.

## Objetivo

Reconstruir cómo se comporta realmente un flujo ejecutable — no cómo parece que debería comportarse por su nombre, su documentación o su ubicación en el código.

## Preguntas a resolver, en orden

1. **Trigger** — ¿qué dispara este flujo? (request HTTP, evento, mensaje de cola, cron, CLI, webhook, señal interna).
2. **Frontera de entrada ejecutable** — ¿cuál es el primer punto de código que realmente se ejecuta? No asumas que el archivo "obvio" es el entry point real — verifica el routing/registro/wiring efectivo.
3. **Validación** — ¿qué se valida antes de continuar? ¿Qué pasa si la validación falla?
4. **Transformación** — ¿qué transforma el dato de entrada antes de usarlo (mapeo, normalización, enriquecimiento)?
5. **Llamadas a servicios** — ¿qué otros componentes, servicios o sistemas externos invoca, y en qué orden?
6. **Lecturas de estado** — ¿qué lee (cache, base de datos, configuración, estado en memoria) y de dónde?
7. **Escrituras de estado** — ¿qué escribe y dónde?
8. **Persistencia** — ¿qué se persiste, en qué forma, y bajo qué condición?
9. **Side effects** — ¿qué efectos observables produce además del retorno (emails, eventos, métricas, archivos, llamadas externas)?
10. **Errores** — ¿qué errores puede producir el flujo y cómo se propagan?
11. **Errores silenciados** — ¿hay `catch`/`except`/manejo que absorbe un error sin propagarlo ni registrarlo? Esto es evidencia crítica: cambia el comportamiento observable frente a lo que el código "parece" hacer.
12. **Reintentos** — ¿el flujo reintenta? ¿bajo qué condición, con qué backoff, con qué límite?
13. **Condiciones de terminación** — ¿cuándo termina el flujo exitosamente, y cuándo termina por corte/timeout/cancelación?
14. **Outputs observables** — ¿qué retorna, emite o produce como resultado final verificable?

No todas las preguntas requieren la misma profundidad — usa las que la pregunta de investigación (`TARGETED_DISCOVERY`) o el flujo completo (`FLOW_DISCOVERY`/`SYSTEM_DISCOVERY`) realmente necesiten.

## Forma de la explicación

Expresa el flujo reconstruido de forma trazable, no narrativa difusa:

```
WHEN <trigger> -> A valida -> B resuelve -> C persiste -> D invoca -> E retorna
```

Cada paso (`A`, `B`, `C`...) debe poder anclarse a evidencia concreta: símbolo, archivo, rango de líneas, o salida de una herramienta (test ejecutado, log, query). Un paso sin evidencia identificable se marca `INFERENCE` o `UNKNOWN` (ver `SKILL.md` §5), nunca se presenta como parte confirmada del flujo.

## Errores comunes a evitar

- Asumir que el código "debería" comportarse de cierta forma porque el nombre de la función lo sugiere — verifica el cuerpo real.
- Tratar un branch de manejo de errores no ejercitado por ningún test como equivalente a uno verificado.
- Detenerse en la primera llamada a función sin confirmar si hay wrapping, middleware, decoradores o interceptores que alteran el comportamiento observable.
- Ignorar código muerto o feature flags que desactivan la ruta que el código fuente sugiere como activa.
