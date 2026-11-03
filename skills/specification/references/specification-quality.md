SOURCE: harness Apep 0.5.0 — metodología propia. Adapta, sin copiar, la idea de GitHub Spec Kit de que una checklist de requisitos es "unit tests for English" (`templates/commands/checklist.md` y la checklist de calidad de `templates/commands/specify.md` @67e0f72): se evalúa el texto de los requisitos, no la implementación. No adopta sus checkboxes autoevaluados como evidencia ni su límite de iteraciones. Spec Kit es fuente de referencia, no de autoridad.
ADAPTATION: OMP Specification Skill v0.2

# Specification Quality Review

**Pregunta:** ¿está la necesidad suficientemente bien especificada?

Evalúa el **texto** de los artefactos como un conjunto de tests sobre el inglés (o el español) de los requisitos: si cada requisito material dice algo determinado, observable y verificable. No evalúa si la implementación funciona ni si los artefactos son coherentes entre sí (`coherence-review.md`).

```
QUALITY   ¿está suficientemente bien especificado?
```

## 1. Reglas de evaluación

- Se evalúan los artefactos, no la impresión de completitud. Un "sí, está claro" sin cita no es evidencia: **SELF-CLAIM NEVER SUBSTITUTES EVIDENCE.**
- Cada `FAIL` cita el fragmento y su ubicación (artefacto, sección, ID).
- Un hallazgo léxico (una palabra vaga, un `TODO`) es una **señal**, no un veredicto: falla sólo si el texto no tiene significado operacional en su contexto.
- Cada check se marca `MATERIAL: YES | NO`. Es material si el defecto cambia qué se construye, cómo se verifica o qué contrato se preserva.
- Se aplica a los artefactos de **WHAT/WHY** (01–05 y 08). El contrato 07 y el Task Breakdown 06 contienen **HOW** legítimo; ahí sólo aplican SQ3, SQ5, SQ9 y SQ10, y la introducción de comportamiento la detecta la coherencia.

## 2. Checks

| Check | PASS cuando | FAIL típico | `NOT_APPLICABLE` cuando | Remediación habitual |
|---|---|---|---|---|
| **SQ1 PROBLEM_CLARITY** | El problema expresa necesidad, dolor o resultado esperado, separado de cualquier solución propuesta | Una solución mencionada se presenta como la necesidad sin evidencia de que sea una decisión cerrada ("el problema es que no hay botón de exportar") | Entry point posterior con problema ya aprobado y sin cambios | `02` o normalización de intake |
| **SQ2 SCOPE_DETERMINACY** | Dentro y fuera de alcance se distinguen sin interpretación | "incluye lo relacionado con pagos", alcance sin exclusiones cuando hay vecinos obvios | — | `02`, `03` (alcance / fuera de alcance) |
| **SQ3 REQUIREMENT_TESTABILITY** | Cada requisito material (BR, AC) es observable y tiene un resultado verificable | "el sistema gestiona correctamente las devoluciones" | — | `03` (BR, AC), `05` |
| **SQ4 TECHNOLOGY_LEAKAGE** | WHAT/WHY no prescriben HOW, salvo `CONSTRAINT` cerrada con fuente | "guardar en una tabla de Postgres", "exponer un endpoint REST" en la Hard Specification sin decisión cerrada | Artefacto 06/07, o la tecnología es `CONSTRAINT` registrada | `03`; o registrar la constraint con su fuente; o clarificación |
| **SQ5 VAGUE_LANGUAGE** | Los adjetivos y adverbios materiales tienen significado operacional | "rápido", "seguro", "adecuado" sin métrica ni criterio (léxico en §3) | — | `03` (AC medibles), clarificación |
| **SQ6 ACTOR_COMPLETENESS** | Se identifican los actores que inician, usan, aprueban o se ven afectados, con su rol | "el usuario" con dos roles posibles; flujos sin iniciador | Sin interacción con actores (proceso puramente automático con disparador definido) | `03` (actores), `04` |
| **SQ7 FAILURE_SEMANTICS** | El comportamiento material ante error, límite o fallo externo está especificado | "manejar errores", "validar los datos", "notificar si falla" sin qué ni a quién | Sin modos de fallo materiales | `03` (casos límite, excepciones), `05` |
| **SQ8 SUCCESS_MEASURABILITY** | Existe una forma objetiva de decidir que la necesidad quedó resuelta | Éxito como sensación ("los usuarios estarán más contentos") sin criterio | — | `02` (objetivo), `03` (AC) |
| **SQ9 DEPENDENCIES_AND_CONSTRAINTS** | Las dependencias y restricciones materiales son explícitas, con su fuente | Una integración o plazo mencionado sin estado; una restricción implícita | Sin dependencias ni restricciones materiales | `02`, `03`, `07` (`DEPENDENCIES`, `CONSTRAINTS`) |
| **SQ10 PLACEHOLDER_CLOSURE** | No quedan marcadores sin clasificar | `TBD`, `TODO`, `???`, `<…>`, "a definir", "etc." en un requisito material, `[NEEDS CLARIFICATION]` | — | Cerrar o clasificar (C1) |

SQ10 no sustituye a C1: C1 clasifica la materialidad de todo item abierto en el gate; SQ10 detecta que un requisito quedó escrito a medias.

## 3. Léxico de señales para SQ5 y SQ10

Las palabras siguientes disparan revisión, no un `FAIL` automático. Pasan si el mismo requisito o un AC que lo cite les da significado operacional.

- **Vaguedad (SQ5):** rápido · lento · eficiente · inmediato · en tiempo real · escalable · robusto · seguro · confiable · fácil · intuitivo · amigable · simple · correcto · correctamente · adecuado · apropiado · razonable · normal · suficiente · óptimo · flexible · moderno · mínimo · máximo (sin cifra) · la mayoría · varios · algunos · frecuentemente · cuando sea necesario · si aplica · según corresponda · en lo posible · etc. — y sus equivalentes en inglés (fast, secure, robust, intuitive, user-friendly, appropriate, as needed, if applicable, etc.).
- **Placeholders (SQ10):** `TBD` · `TODO` · `TKTK` · `???` · `<…>` · `[NEEDS CLARIFICATION…]` · "a definir" · "pendiente" · "por confirmar" · "XXX".

La búsqueda mecánica (`grep`) de este léxico sobre los artefactos es un apoyo legítimo y se cita como evidencia; la decisión de `FAIL` sigue siendo un juicio registrado. `TBD` y `TODO` se buscan en mayúsculas y como palabra completa: en minúsculas, "todo" es una palabra común del español.

## 4. Resultado

```
SPEC_QUALITY_RESULT
  evaluated_at:   <fecha>
  artifacts:      <artefactos evaluados>
  | CHECK | RESULT (PASS | FAIL | NOT_APPLICABLE) | EVIDENCE | MATERIAL | REMEDIATION_TARGET |
  material_fails: NONE | <check · ubicación>
  result:         PASS | FAIL
```

`result: FAIL` si queda algún `FAIL` con `MATERIAL: YES` sin resolver. Un `FAIL` no material se registra y no bloquea.

## 5. Uso incremental y gate formal

```
DETECT EARLY. REMEDIATE LOCALLY. GATE FORMALLY AT THE END.
```

- Durante el pipeline, cada etapa aplica a lo que produce los checks que le corresponden: 02 → SQ1, SQ2, SQ8; 03 → SQ2–SQ10; 05 y 08 → SQ3, SQ5, SQ7. El defecto se corrige en la etapa, o se clasifica y entra en clarificación si es una decisión.
- Después de producir el contrato 07 se ejecuta la revisión formal sobre todos los artefactos activos y se emite el `SPEC_QUALITY_RESULT` (`07-execution-contract.md`).
- Corregir un `FAIL` nunca consiste en inventar el dato: si para que el requisito sea verificable hace falta una decisión, es una clarificación.

`SPEC_QUALITY_RESULT` **no** sustituye al readiness gate C1–C4 ni a la revisión de coherencia.
