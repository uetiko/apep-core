# Data, Contract and Persistence Tracing

Aplica junto con `.omp/skills/technical-discovery/SKILL.md` — no lo repite. Úsalo para `FLOW_DISCOVERY`/`SYSTEM_DISCOVERY` cuando la pregunta involucra qué forma tiene un dato, cómo cambia, o qué lo persiste/consume.

## Cadena a trazar

```
input
  → validación/schema
    → transformaciones
      → representación interna/de dominio
        → persistencia
          → representación de serialización/mensaje/archivo
            → consumidor/output downstream
```

No asumas que la forma del dato es la misma en cada etapa — el objetivo es confirmar, con evidencia, dónde y cómo cambia.

## Contratos a identificar, explícitos e implícitos

DTOs · schemas (JSON Schema, protobuf, GraphQL SDL) · OpenAPI/especificación de API · payloads de mensajes · contratos de cola/tópico · archivos (formato, layout) · tablas (columnas, constraints, índices relevantes) · colecciones (shape de documento) · claves de object storage · contratos de entorno (variables, configuración esperada) · identificadores · claves naturales/idempotencia.

## Clasificación de contratos

Cuando la evidencia lo permita, distingue:

- **`EXPLICIT_CONTRACT`** — declarado formalmente (schema, tipo, spec de API, DDL) y verificable directamente.
- **`IMPLICIT_CONTRACT`** — no declarado formalmente, pero exigido de facto por cómo el consumidor usa el dato (p. ej. un campo que ningún schema exige pero cuya ausencia rompe al consumidor).
- **`DERIVED_CONTRACT`** — inferido a partir del comportamiento observado de múltiples puntos (p. ej. "todos los consumidores asumen que este campo nunca es null aunque el schema lo permita").
- **`FRAGILE_CONTRACT`** — un contrato implícito o derivado que depende de un detalle de implementación no garantizado (orden de campos, comportamiento no documentado de una librería, timing) y que podría romperse sin aviso.

No fuerces esta clasificación cuando la evidencia no la sostenga — repórtalo como `UNKNOWN` antes que adivinar la categoría.

## Preguntas de apoyo

- ¿Qué pasa si el dato de entrada no cumple el contrato esperado? ¿Falla explícitamente, se degrada silenciosamente, o corrompe estado?
- ¿La representación persistida coincide con la representación de dominio, o hay una traducción con pérdida/adición de información?
- ¿Qué identifica de forma única un registro/mensaje (clave natural, idempotency key), y qué pasa si se procesa duplicado?
- ¿Hay más de una fuente de verdad para el mismo dato (cache vs. base de datos, réplica vs. primario)? ¿Cómo se resuelve la divergencia si existe?

## Salida típica

La cadena reconstruida con la forma del dato en cada etapa, los contratos identificados y su clasificación, y los puntos donde la evidencia es insuficiente (`UNKNOWN`) o contradictoria (`CONTRADICTION`) — no un juicio sobre si el diseño de datos es correcto.
