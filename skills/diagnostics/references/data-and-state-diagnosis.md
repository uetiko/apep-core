# Data and State Diagnosis

Aplica junto con `.omp/skills/diagnostics/SKILL.md` — no lo repite. Úsalo cuando el fallo involucra datos o estado persistido/derivado: bases de datos relacionales, document/state stores, transacciones, caches.

## Qué inspeccionar

- **Bases de datos relacionales** — filas, constraints, foreign keys, índices y su relación con el fallo observado.
- **Document/state stores** — forma real del documento/estado frente a la esperada por el consumidor que falla.
- **Transacciones** — si el fallo ocurrió dentro, fuera, o a caballo de una transacción; si hubo commit parcial o rollback.
- **FK/constraints** — si una violación de integridad es la causa o un síntoma de un problema anterior (un dato inválido que llegó desde otro punto).
- **Transiciones de estado** — si el estado observado es alcanzable legítimamente desde el estado anterior según las reglas del sistema, o si representa una transición inválida.
- **Estado duplicado o obsoleto (stale)** — múltiples copias del mismo dato (cache, réplica, vista materializada) que divergieron.
- **Idempotencia** — si una operación se ejecutó más de una vez y el sistema no lo maneja correctamente.
- **Caches** — sólo cuando forman parte causal del fallo (dato servido desde cache desactualizado, invalidación que no ocurrió).
- **Estado persistido vs. derivado** — si el problema está en la fuente de verdad o en una proyección/derivación que quedó desincronizada.
- **Escrituras parciales** — si una operación que debía ser atómica dejó estado a medio escribir.
- **Rollback** — si ocurrió, si fue completo, y qué quedó en el estado resultante.
- **Violaciones de integridad** — constraint violado, referencia rota, invariante de negocio no verificado en la capa de datos.
- **Inconsistencia entre representaciones** — el mismo concepto representado de forma distinta en dos capas (dominio vs. persistencia vs. serialización) que dejó de coincidir.

## Schema drift

**`SCHEMA_LOCAL != SCHEMA_EXPECTED_BY_CODE`** (`SKILL.md` §3.16, §4.2). El schema de tu entorno local o el resultado de aplicar las migraciones del repositorio no es necesariamente:

- el schema que el código en ejecución asume; ni
- el schema que tenía el entorno donde ocurrió el fallo, en el momento en que ocurrió.

Cuando el fallo pueda explicarse por una diferencia de schema, verifica el schema **efectivo** del entorno del incidente, no el derivado del código fuente. Una migración pendiente, aplicada parcialmente o aplicada en distinto orden es `SCHEMA_DRIFT` (`SKILL.md` §4.5), y su `FAULT_DOMAIN` no está en el código que falla sino en el estado del schema.

## Distinciones a preservar

No trates como equivalentes:

- **`invalid data`** — el dato en sí viola una regla de forma (tipo, formato, rango).
- **`invalid transition`** — el dato es válido en forma pero llegó a ese estado por un camino que las reglas del sistema no permiten.
- **`invalid persistence model`** — el modelo de datos no puede representar correctamente un caso real del dominio (la estructura, no una instancia particular, es la causa).
- **`incorrect interpretation of valid state`** — el dato persistido es correcto, pero el código que lo lee/interpreta asume algo distinto de lo que realmente significa.

Confundir estas categorías produce diagnósticos que corrigen el síntoma equivocado (p. ej. "sanear" un dato cuando el problema real es una transición inválida que seguirá produciendo datos igual de "inválidos").

## Read-only por defecto

Las consultas diagnósticas son de sólo lectura por defecto (`SELECT`, lecturas de estado, inspección de documentos). Cualquier mutación de datos con fines diagnósticos (insertar un registro de prueba, forzar una transición, limpiar un estado) requiere autorización explícita — sin ella, se reporta como bloqueado (`SKILL.md` §13, condiciones 2–3), no se ejecuta "para confirmar".
