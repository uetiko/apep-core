---
name: technical-discovery
description: Reconstruye el CURRENT_STATE verificable de un sistema, flujo o componente existente a partir de evidencia — qué hace realmente, cómo se comporta un flujo de ejecución concreto, dónde están sus entry points y fronteras reales, cómo se mueven datos y contratos, qué dependencias internas/externas participan, qué arquitectura es observable, qué está confirmado vs inferido, y qué permanece desconocido o contradictorio. Úsalo cuando se pida investigación técnica, software archaeology, reverse engineering, o entender "qué hace X" / "cómo funciona Y" de código ya existente, o mediante invocación explícita (`/skill:technical-discovery`). No es el modo normal de trabajo de ingeniería del workspace — no se activa automáticamente para debugging trivial ya resuelto, code review ordinario, tareas ya especificadas con Execution Contract, ni para justificar por sí solo un rediseño, refactor, auditoría no solicitada, especificación de TARGET_STATE o implementación.
---

# Technical Discovery

Este skill es un **router y método de reconstrucción de CURRENT_STATE** — no es un workflow de producto, no es una auditoría, y no decide qué debería existir. Responde una pregunta técnica concreta con evidencia, no produce un inventario genérico del repositorio.

## 0. Cuándo NO usar este skill

No lo actives para: decidir o diseñar TARGET_STATE, refactorizar, implementar, auditar sin que se haya pedido (seguridad, deuda técnica, estilo, arquitectura) salvo que el riesgo afecte directamente la interpretación del flujo investigado (ver §8), resumir un repositorio sin una pregunta concreta que responder, ni tareas de ingeniería ya refinadas con especificación y Execution Contract disponibles. No sustituye a `specification` (decide qué comportamiento *debe* existir) ni a `project-management` (decide viabilidad/plan/alcance de un frente) — ver §12. Actívalo cuando la necesidad real sea entender qué existe y cómo se comporta *hoy*, o mediante `/skill:technical-discovery` cuando los skill commands estén habilitados.

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE        (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE    (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → TECHNICAL DISCOVERY     (este skill)
      → consumidor            (specification / project-management / debugging / review / decisión humana)
```

Este skill no es una gobernanza independiente y no tiene autoridad de decisión propia. No puede contradecir los invariantes de autoridad del workspace (`ENGINEERING_GOVERNANCE.md` §1, §2, §16) ni la gobernanza del repositorio investigado. El código existente es evidencia de comportamiento actual, no automáticamente de arquitectura pretendida ni de especificación (§6.1). Ante conflicto entre una fuente y otra, no lo resuelvas en silencio — repórtalo como `CONTRADICTION` (§5).

Un discovery autorizado opera dentro del `OPERATIONAL_AUTONOMY_ENVELOPE` (`ENGINEERING_GOVERNANCE.md` §17, `RULES.md` regla 19): recorre código, Git de sólo lectura, datos, introspección cloud no mutante, logs y runtime hasta producir el `CURRENT_STATE` **sin pedir aprobación operación por operación**, y sincroniza por evento material (§17.6), no por cada lectura. El envelope no altera el límite de este skill: sigue siendo read-only y `FINDING != AUTHORIZATION_TO_FIX` (§8, §17.5).

Este skill **produce evidencia que otro proceso puede consumir** (una `specification`, un análisis de `project-management`, un debugging, un review, o una decisión humana directa) — no invoca automáticamente ninguno de esos procesos ni asume cuál los usará. Es **executor-neutral**: el resultado es igual de válido para un humano, para OMP, o para cualquier otro agente/modelo que lo consuma después.

## 2. Pregunta gobernante

`¿Cuál es el estado técnico verificable actual de este sistema, flujo o componente según la evidencia disponible?`

Todo discovery parte de una pregunta concreta — nunca de "explorar el repositorio" en abstracto. Si la petición no trae una pregunta clara, la primera acción es precisarla, no empezar a leer.

## 3. Principio central — vertical antes que horizontal

**No leas el repositorio horizontalmente cuando la pregunta puede responderse verticalmente.** Para investigaciones de flujo, traza desde la frontera de entrada relevante a través del camino de ejecución real, sus dependencias, contratos, datos y efectos — en vez de leer exhaustivamente directorios hermanos que no participan en esa ejecución. La amplitud de la investigación la controla la escala elegida (§4), no la curiosidad ni la completitud por sí misma.

## 4. Escalas de discovery — controlan el alcance

| Escala | Uso | Amplitud típica |
|---|---|---|
| `TARGETED_DISCOVERY` | Pregunta puntual sobre un símbolo, componente, contrato, comportamiento, contexto de un defecto, o un camino de ejecución localizado. | Vertical y estrecha: sólo lo que la pregunta toca. |
| `FLOW_DISCOVERY` | Reconstruir un flujo de ejecución o de datos end-to-end o cruzando componentes. | Sigue la ejecución real de punta a punta; no explora ramas que el flujo no toma. |
| `SYSTEM_DISCOVERY` | Entender un subsistema, servicio, pipeline, aplicación o repositorio lo suficiente para establecer su modelo técnico actual. | La más amplia — aun así guiada por evidencia real, no por lectura exhaustiva de cada archivo. |

Elige la escala más estrecha que responda la pregunta. Una pregunta puntual **no** dispara automáticamente un `SYSTEM_DISCOVERY`.

## 5. Modelo de evidencia

Distingue siempre, sin fusionar:

| Categoría | Significa |
|---|---|
| `FACT` | Evidencia observada directamente (código leído, comando ejecutado, test corrido, config inspeccionada). |
| `INFERENCE` | Conclusión derivada de evidencia identificada, no observada directamente. |
| `HYPOTHESIS` | Explicación plausible que todavía requiere verificación. |
| `DECLARED_INTENT` | Intención afirmada por documentación, comentarios, historial, ADRs, naming, u otra fuente declarativa — no comportamiento verificado. |
| `UNKNOWN` | Evidencia insuficiente para concluir. |
| `CONTRADICTION` | Fuentes relevantes ofrecen información materialmente incompatible — es un estado de la evidencia, no un nivel de confianza. |

**Evidencia antes que inferencia**: nunca presentes una `INFERENCE` o una `HYPOTHESIS` como si fuera un `FACT`. Cuando una conclusión importante dependa de inferencia, dilo explícitamente.

Para conclusiones relevantes, expón confianza sin convertir cada frase en etiquetado ceremonial:

`CONFIRMED` · `HIGH` · `MEDIUM` · `LOW`

## 6. Distinciones que nunca se conflan

`CURRENT_STATE != TARGET_STATE` · `OBSERVED_BEHAVIOR != DECLARED_INTENT` · `DECLARED_INTENT != INFERRED_INTENT` · `INFERRED_INTENT != TARGET_ARCHITECTURE`

Tampoco se tratan como equivalentes: documentación y verdad de runtime · estructura de directorios y arquitectura real · nombres de clases y responsabilidades reales · presencia de código y caminos de ejecución activos · existencia de un endpoint y su uso real en producción · existencia de tests y cobertura conductual suficiente · comentarios y comportamiento ejecutable · intención histórica y comportamiento actual.

Discovery reconstruye **comportamiento**, no un inventario de archivos. Es observacional por defecto: describe lo que el sistema hace según la evidencia, no lo que debería hacer.

## 7. Flujo de trabajo (proporcional, no checklist obligatorio)

```
QUESTION
  → SCOPE THE DISCOVERY
    → ESTABLISH BASELINE
      → IDENTIFY RELEVANT SOURCES OF TRUTH
        → LOCATE ENTRY POINTS
          → TRACE EXECUTION
            → TRACE DATA / CONTRACTS / SIDE EFFECTS
              → CROSS-CHECK TESTS / CONFIGURATION / RUNTIME EVIDENCE
                → RESOLVE MATERIAL CONTRADICTIONS
                  → CLASSIFY EVIDENCE
                    → RECONSTRUCT CURRENT_STATE
                      → REPORT GAPS / NEXT EVIDENCE
```

No todas las etapas requieren la misma profundidad en cada discovery — la escala (§4) determina cuánto peso recibe cada una. Un `TARGETED_DISCOVERY` puede resolver la mayoría de etapas en un solo paso; un `SYSTEM_DISCOVERY` las recorre con más detalle en `TRACE EXECUTION`, `TRACE DATA/CONTRACTS` y `ARCHITECTURE` (ver referencias, §10).

## 8. Qué NO es este skill

- **No es auditoría.** Puede reportar riesgos técnicos sólo cuando: afectan materialmente la interpretación del comportamiento investigado, amenazan un invariante relevante al flujo, afectan la seguridad de una modificación futura, explican el comportamiento observado, o fueron pedidos explícitamente. No convierte un discovery ordinario en catálogo no solicitado de deuda técnica, hallazgos de seguridad, defectos de estilo, crítica arquitectónica o refactors sugeridos.
- **No es especificación.** Al establecer CURRENT_STATE, no decide automáticamente qué debería ser TARGET_STATE — eso es competencia de `specification` o de una decisión humana.
- **No es implementación.** Encontrar un problema no es autorización para corregirlo.
- **No es resumen genérico de repositorio.** El resultado responde la pregunta de investigación reconstruyendo comportamiento y estructura relevante — no enumera archivos por completitud.
- **No compila automáticamente trabajo** para ningún ejecutor de implementación. El resultado es evidencia neutra respecto a quién la consumirá después (§1).

## 9. Historia y software archaeology — condicional, no por defecto

Consulta `git log`/`blame`/historial sólo cuando la evidencia del estado actual por sí sola no explica adecuadamente procedencia, cambios semánticos, migraciones parciales, conceptos renombrados, rutas legacy, implementaciones abandonadas, o una contradicción relevante. No hagas archaeology amplio cuando no ayuda a responder la pregunta de investigación.

**El historial de git explica procedencia; no reemplaza la verdad ejecutable actual.** Ver `skill://technical-discovery/references/history-and-archaeology.md`.

## 10. Progressive disclosure — qué cargar y cuándo

Carga sólo la referencia que la investigación en curso requiera — no las cuatro en cada invocación:

| Necesidad | Referencia |
|---|---|
| Reconstruir un flujo de ejecución concreto (trigger → validación → transformación → llamadas → efectos → retorno) | `skill://technical-discovery/references/execution-flow-tracing.md` |
| Derivar arquitectura observada a partir de dependencias/responsabilidades reales | `skill://technical-discovery/references/architecture-and-dependency-mapping.md` |
| Trazar datos y contratos (explícitos, implícitos, derivados, frágiles) a través de input → persistencia → output | `skill://technical-discovery/references/data-contract-and-persistence-tracing.md` |
| El estado actual no explica por sí solo procedencia/contradicciones y se requiere historial | `skill://technical-discovery/references/history-and-archaeology.md` |

Un `TARGETED_DISCOVERY` puede no requerir ninguna referencia. Un `SYSTEM_DISCOVERY` normalmente combina varias.

## 11. Salida — proporcional a la escala

**`TARGETED_DISCOVERY`** — modelo compacto, sólo secciones relevantes:

`RESULT` · `QUESTION` · `BASELINE` · `FACTS` · `EXECUTION_FLOW` · `CONTRACTS_AND_DATA` · `CONTRADICTIONS` · `GAPS` · `CONFIDENCE` · `NEXT_EVIDENCE`

**`FLOW_DISCOVERY`** — énfasis en: frontera de entrada · camino de ejecución · componentes participantes · transformaciones de contratos/datos · persistencia y side effects · comportamiento ante error · dependencias externas · invariantes relevantes · contradicciones y unknowns.

**`SYSTEM_DISCOVERY`** — modelo extendido: resumen ejecutivo · evidencia revisada · entry points · flujos principales · arquitectura observada · modelo de dominio inferido · datos y contratos · dependencias externas · comportamiento operacional · evidencia de testing relevante · riesgos relevantes para la comprensión · ambigüedades · intención declarada/inferida · próximos pasos de discovery.

Nunca generes secciones vacías o ceremoniales — omite lo que no aporte.

## 12. Relación con otras capabilities

Cuando `specification` encuentra un `UNKNOWN` factual, formula una pregunta concreta y consume este skill para responderla (`TARGETED_DISCOVERY` por defecto): el resultado vuelve como `FACT` con evidencia o como `UNKNOWN` confirmado, y la especificación continúa. Esa pregunta no amplía la escala del discovery ni reabre un discovery ya cerrado sin evidencia nueva, y su respuesta describe `CURRENT_STATE`, no decide `TARGET_STATE`.

`technical-discovery` no sustituye ni invoca automáticamente `specification`, `project-management`, `code-quality` ni `governance-review`. Puede identificar que una de ellas es el siguiente paso natural (p. ej. "esto necesita `specification` para decidir TARGET_STATE", o "esto es competencia de `project-management` si hay que decidir alcance/fecha") — pero se reporta como hallazgo/recomendación, nunca como transición automática. Simétricamente, ninguna de esas capabilities modifica a esta.
