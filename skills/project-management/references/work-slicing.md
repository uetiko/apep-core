# Work slicing

Referencia del modo *work item* de `project-management` (`SKILL.md` §6). Responde: ¿conviene dividir este trabajo, y cómo, sin redefinir lo que debe hacer?

```
SLICE BY OBSERVABLE VALUE, NOT BY TECHNICAL LAYER, WHEN PRACTICAL.
PM MAY RECOMMEND SPLITTING, NOT REDEFINE BEHAVIOR WHILE SPLITTING.
```

## 1. Resultado

| Resultado | Cuándo |
|---|---|
| `NO_SPLIT_NEEDED` | El item ya es una unidad coherente de trabajo (`work-item-flow.md` §5) |
| `SPLIT_RECOMMENDED` | Dividir daría unidades más verificables, más pequeñas o con menos riesgo, pero el item podría ejecutarse entero |
| `SPLIT_REQUIRED` | El item es `TOO_LARGE_TO_EXECUTE`, mezcla intenciones independientes que no se pueden verificar ni revertir juntas, o mezcla rutas distintas (p. ej. un diagnóstico y una feature) |
| `CANNOT_SPLIT_WITHOUT_DECISION` | Cualquier corte posible cambia qué se entrega primero, deja una parte del comportamiento a medias o redefine el alcance: la división es una decisión humana (`DECISION_REQUIRED`) |

Dividir es una **recomendación**. La división del alcance, y qué slice va primero, la decide el owner (`SKILL.md` §2).

## 2. Cómo cortar

Se prefiere cortar por valor observable:

| Preferir | Sobre |
|---|---|
| "el analista puede crear la regla" · "puede editarla" · "puede consultar el historial" | "base de datos" · "backend" · "frontend" |

Una slice intenta ser: **coherente** (una intención) · **verificable** (tiene su propia evidencia de aceptación) · **relativamente independiente** · **integrable** sin dejar el sistema inconsistente · con **resultado observable**.

`LARGE` no basta para dividir. Un item grande pero coherente se queda entero si cada corte posible produce slices que no se pueden verificar por sí solas o que obligan a integrar a medias. Una recomendación de dividir siempre dice qué gana cada slice.

## 3. `ENABLING_SLICE`

No se fuerza el corte vertical cuando el trabajo es genuinamente:

- infraestructura;
- un habilitador técnico (una librería, un contrato compartido, un mecanismo que varias slices necesitan);
- una migración;
- una investigación;
- seguridad;
- deuda técnica.

En esos casos vale una `ENABLING_SLICE`, **con su justificación**: qué habilita, qué slices la necesitan y cómo se verifica sin comportamiento de producto visible (tests técnicos, un entorno levantado, un contrato publicado). Una `ENABLING_SLICE` sin justificación es un corte por capa disfrazado.

```
SLICE-2  (ENABLING_SLICE)
  HABILITA:     SLICE-3, SLICE-4 (ambas necesitan el contrato de eventos)
  VERIFICACIÓN: el contrato publicado y sus tests de contrato en verde
  POR QUÉ NO VERTICAL: el contrato es compartido; cada slice vertical lo duplicaría
```

## 4. Lo que el slicing no hace

- **No divide semántica de negocio.** Separar "crear" de "aprobar" está bien si cada parte tiene sentido por sí sola; partir una regla de negocio en dos mitades que sólo tienen sentido juntas, no.
- **No decide qué entra en la primera entrega.** Si el corte obliga a elegir qué comportamiento llega antes (y eso cambia lo que reciben los usuarios), es `CANNOT_SPLIT_WITHOUT_DECISION`.
- **No crea comportamiento.** Una slice no puede añadir comportamiento que el item no tenía (un estado intermedio visible, una pantalla provisional) sin que lo decida el owner o lo especifique `specification`.
- **No es la descomposición en tareas.** Las tareas de implementación de un comportamiento ya especificado son de `specification` (Etapa 06).

## 5. Salida

```
SLICING
  RESULT:   NO_SPLIT_NEEDED | SPLIT_RECOMMENDED | SPLIT_REQUIRED | CANNOT_SPLIT_WITHOUT_DECISION
  SLICES:   <SLICE-N · resultado observable | ENABLING_SLICE + justificación · relación (SEQUENTIAL | PARALLEL | CONDITIONAL)>
  WHY:      <qué gana cada slice, o por qué no se divide>
  DECISION: NONE | <DECISION_REQUIRED>
```

## 6. Origen

Organizar el trabajo por historia de usuario independiente y verificable, con una fase de cimientos compartidos antes ("Foundational"), se contrastó con `tasks` de GitHub Spec Kit (@67e0f72), como referencia. Aquí se aplica a work items: las fases fijas de Spec Kit (Setup, Foundational, historias, Polish) no se adoptan; la `ENABLING_SLICE` justificada ocupa el lugar de su fase "Foundational".
