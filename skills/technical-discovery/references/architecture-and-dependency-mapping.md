# Architecture and Dependency Mapping

Aplica junto con `.omp/skills/technical-discovery/SKILL.md` — no lo repite. Úsalo para `SYSTEM_DISCOVERY`, y para la parte de un `FLOW_DISCOVERY` que necesite entender qué componentes participan y cómo se relacionan.

## Principio central

La arquitectura se **deriva** de relaciones de dependencia y responsabilidad observadas — no se **asume** a partir de nombres de carpetas, diagramas, documentación o convenciones declaradas. Aplica una etiqueta arquitectónica (capas, hexagonal, microservicios, event-driven, monolito modular, etc.) sólo después de confirmar con evidencia que el código realmente se comporta así.

## Evidencia a reunir, en orden de prioridad

1. **Quién llama a quién** — el grafo de invocación real entre módulos/servicios/componentes, no el que el diagrama declara.
2. **Quién importa/depende de quién** — dependencias de compilación/build, no sólo de ejecución.
3. **Quién es dueño del estado** — qué componente posee la fuente de verdad de un dato (no quién simplemente lo lee o lo cachea).
4. **Dónde ocurren los side effects** — persistencia, I/O, llamadas externas, eventos emitidos.
5. **Dónde ocurren las fronteras reales** — un límite de proceso, de despliegue, de esquema de datos, o de contrato de red observable — no una carpeta con nombre de capa.
6. **Dónde las responsabilidades cruzan esas fronteras** — casos donde un componente hace trabajo que "debería" pertenecer a otro según la arquitectura declarada; esto es evidencia de arquitectura observada, no un juicio de calidad que corregir aquí.

## Arquitectura declarada vs. arquitectura observada

Regístralas por separado y compáralas explícitamente:

- **`DECLARED_ARCHITECTURE`** — lo que documentación, ADRs, diagramas, nombres de carpetas o comentarios afirman que es la arquitectura.
- **`OBSERVED_ARCHITECTURE`** — lo que el grafo real de llamadas/dependencias/estado demuestra.

Una discrepancia entre ambas es un hallazgo válido de discovery (repórtalo como `FACT` sobre la brecha, no como un defecto a corregir) — no autoriza a "arreglar" la arquitectura ni a decidir cuál debería prevalecer; eso pertenece a `specification` o a una decisión humana.

## Preguntas de apoyo

- ¿Existe más de una implementación real de la misma interfaz, o la abstracción sólo tiene un consumidor?
- ¿Un cambio en un componente obliga a cambiar otro que "no debería" conocerlo, según la arquitectura declarada?
- ¿Qué tan estable es la frontera observada frente a cambios recientes (ver `history-and-archaeology.md` si el estado actual no lo explica)?
- ¿Qué dependencias externas (servicios, colas, terceros) participan, y son duras (bloquean el flujo) o blandas (degradan sin bloquear)?

## Salida típica

Un mapa de componentes con sus relaciones observadas, marcado con nivel de confianza (`CONFIRMED`/`HIGH`/`MEDIUM`/`LOW`, ver `SKILL.md` §5) y, cuando aplique, la comparación `DECLARED_ARCHITECTURE` vs `OBSERVED_ARCHITECTURE`. No es un veredicto de si la arquitectura es buena o mala.
