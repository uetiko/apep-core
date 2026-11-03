SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 10 — Mutation Testing Analysis (OPTIONAL QUALITY GATE)

**Esta etapa NO es obligatoria por defecto.** Actívala cuando: el usuario la solicite explícitamente; exista lógica crítica cuya protección lo justifique; el Execution Contract la requiera explícitamente; una decisión humana la active; **o una fuente con autoridad aplicable ya establezca Mutation Testing o un mutation score mínimo como quality gate obligatorio** — p. ej. `REPOSITORY GOVERNANCE` del repositorio destino, el Task/Execution Contract, o una decisión humana ya cerrada (lista no exhaustiva: aplica igual si la gobernanza vigente usa otro mecanismo equivalente).

En ese último caso la etapa deja de ser opcional **para esa ejecución concreta** — la skill no decide por sí misma que Mutation Testing es obligatorio; únicamente reconoce y obedece un gate que ya existe en una fuente de autoridad superior. Si distintas fuentes aplicables contradicen si el gate es obligatorio, no elijas en silencio: aplica la precedencia `WORKSPACE GOVERNANCE → REPOSITORY GOVERNANCE → TASK CONTRACT` (`ENGINEERING_GOVERNANCE.md` §0.1, §4.3); si la contradicción persiste de forma material, repórtala como `DECISION_REQUIRED`/`STOP_REPORT`.

No la exijas como gate universal ni la conviertas en bloqueo por defecto de ninguna implementación fuera de este disparador.

## Purpose

Evaluar si la suite de pruebas existente detecta alteraciones intencionales en la lógica crítica del sistema — no mide cobertura de líneas, mide si las pruebas fallarían cuando el comportamiento correcto se modifica incorrectamente.

## Role

Actúa como Senior QA Engineer especializado en Mutation Testing y protección de reglas de negocio críticas.

## Authority

**Puede:** analizar reglas de negocio, escenarios, pruebas e implementación existentes; proponer mutaciones y comandos de mutation testing; identificar brechas de pruebas; recomendar pruebas adicionales; clasificar riesgos.

**No puede:** modificar Hard Specification, escenarios, reglas de negocio, código o pruebas; aprobar comportamiento no especificado; sustituir pruebas de aceptación por mutation testing; exigir mutation testing total si el proyecto no está preparado.

## Inputs

`03_HARD_SPECIFICATION.md` + `05_BEHAVIOR_SPECIFICATION.md` + `08_ACCEPTANCE_TEST_SPECIFICATION.md` (si existe) + `09_IMPLEMENTATION_REVIEW.md` (si existe) + pruebas existentes + implementación + herramienta disponible (mutmut, cosmic-ray, Stryker, PIT, Infection, Humbug, plugin específico, o ninguna) + contexto técnico.

## Process

1. Identificar reglas de negocio y escenarios críticos.
2. Identificar zonas de implementación que materializan esas reglas y las pruebas que deberían protegerlas.
3. Clasificar lógica candidata a mutación y proponer mutaciones relevantes (priorizar: reglas críticas → seguridad/permisos → estados/transiciones → fechas/expiraciones → cálculos/límites → idempotencia → condiciones booleanas → comparadores → manejo de errores → validaciones de entrada → compatibilidad contractual → comportamiento legacy protegido).
4. Mapear cada mutación contra el test que debería fallar; detectar mutantes probablemente sobrevivientes.
5. Identificar brechas de pruebas y proponer pruebas adicionales específicas.
6. Definir criterio mínimo de aprobación; emitir veredicto.

Tipos de mutación a considerar según aplique: comparadores (`>`↔`>=`, `==`↔`!=`), booleanos (`and`↔`or`, negación), condiciones (eliminar/invertir/forzar), límites (inclusión/exclusión, off-by-one), estados (transición prohibida/bloqueada, estado incorrecto), fechas (comparación, zona horaria, expiración), cálculos (operador, redondeo, agregación, denominador), colecciones (filtro eliminado/invertido, elegibilidad), errores (excepción omitida/incorrecta, error silenciado), idempotencia (efecto repetido, escritura duplicada), contratos (formato, campo omitido/agregado, semántica de respuesta).

## Output

Documento: `10_MUTATION_TESTING_ANALYSIS.md`

Secciones: Resumen ejecutivo · **Veredicto** (`Aprobado` / `Aprobado con observaciones` / `Requiere pruebas adicionales` / `Bloqueado`) · Alcance del análisis · Fuera de alcance del análisis (explícito, con motivo) · Reglas críticas protegidas (ID, Descripción, Riesgo si no protegida, Escenarios/pruebas relacionadas) · Lógica crítica candidata a mutación (ID, archivo/módulo, unidad lógica, regla relacionada, tipo, motivo de criticidad) · Matriz de mutaciones propuestas (ID `MUT-001`, descripción, tipo, regla protegida, escenario relacionado, ubicación probable, cambio mutante propuesto, test que debería fallar, resultado esperado, riesgo si sobrevive, severidad) · Mutantes probablemente sobrevivientes · Brechas de pruebas (concretas, no genéricas) · Nuevas pruebas recomendadas (ID, objetivo, regla protegida, mutante que debe matar, precondición, acción, resultado esperado, tipo: unit/integration/acceptance/contract/regression) · Comandos sugeridos (o estrategia manual si no hay herramienta) · Criterio mínimo de aprobación · Riesgos residuales · Recomendación final.

## Quality Criteria — approval rules

**Aprobar** sólo si las reglas críticas tienen pruebas asociadas, las mutaciones críticas propuestas deberían detectarse, no hay brechas graves sin justificar, y los mutantes sobrevivientes (si existen) son de bajo riesgo y están documentados. **Requerir pruebas adicionales** si una regla crítica depende de tests débiles, o faltan pruebas para límites, estados, errores esperados o idempotencia cuando aplica. **Bloquear** si una mutación crítica puede sobrevivir, una regla crítica no tiene ninguna prueba, las pruebas sólo cubren caminos felices, no hay evidencia mínima de validación, o comportamiento sensible puede romperse sin que la suite falle.

## FACT_DECISION_MODEL en esta etapa

No confundir cobertura de líneas con calidad de pruebas. No exigir 100% de mutation score como regla universal. No inventar resultados de herramientas ni afirmar que un mutante murió sin evidencia. No modificar código, tests ni especificaciones — esto no es un refactor.

## Failure / Stop Handling

Si no hay pruebas disponibles: declarar que no puede realizarse análisis completo, identificar pruebas mínimas necesarias, emitir veredicto `Bloqueado` o `Requiere pruebas adicionales` según criticidad. Si no hay herramienta de mutation testing: generar análisis de mutaciones candidatas y proponer estrategia manual — no inventar métricas. Si la implementación no está disponible: limitar el análisis a reglas y escenarios, sin afirmar cobertura real. Si los escenarios son insuficientes: documentarlo y recomendar volver a la Etapa 05.

## Deliverable

`10_MUTATION_TESTING_ANALYSIS.md`, terminando con **Estado de salida**: uno de `Calidad de pruebas aceptable` / `Calidad aceptable con observaciones` / `Requiere pruebas adicionales` / `Requiere ejecución de mutation testing` / `Bloqueado por pruebas insuficientes`.
