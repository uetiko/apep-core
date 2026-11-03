SOURCE: harness Apep 0.5.0 — metodología propia. Adapta, sin copiar, el análisis de consistencia entre artefactos de GitHub Spec Kit (`templates/commands/analyze.md` @67e0f72): evaluación estrictamente read-only, pasadas de detección (duplicación, ambigüedad, infraespecificación, alineación con principios, cobertura, inconsistencia) y severidad CRITICAL/HIGH/MEDIUM/LOW. Sustituye su "constitution" por la gobernanza Apep y las decisiones humanas cerradas, y no aplica remediaciones por su cuenta. Spec Kit es fuente de referencia, no de autoridad.
ADAPTATION: OMP Specification Skill v0.2

# Specification Coherence Review

**Pregunta:** ¿todos los artefactos activos de la especificación cuentan la misma historia?

```
COHERENCE   ¿los artefactos cuentan una historia compatible?
REFERENCE_INTEGRITY  !=  SEMANTIC_COHERENCE
```

C2 (`07-execution-contract.md`) demuestra que `AC-004` **existe** donde se le referencia. La coherencia demuestra que `AC-004` **expresa un comportamiento compatible con sus fuentes** (la BR de la que deriva, el escenario que lo ilustra, la tarea que lo implementa, el test que lo verifica y las clarificaciones aplicadas). Una spec puede pasar C2 y fallar en coherencia.

## 1. Reglas

- **Read-only durante la evaluación.** Primero se evalúa todo y se emite el resultado; las correcciones se hacen después y se vuelven a evaluar las pasadas afectadas.
- **Nunca se corrige una contradicción material eligiendo una versión.** Si dos artefactos dicen cosas incompatibles sobre algo material, la ruta es clarificación o `DECISION_REQUIRED`, no una edición.
- Sólo se corrigen directamente (`SPEC_REMEDIATION`) los defectos no materiales o aquellos cuya versión correcta ya está fijada por una fuente de mayor autoridad citada (una clarificación `APPLIED`, una decisión cerrada, gobernanza).
- Cada finding cita los fragmentos y su ubicación. Las matrices y resúmenes de cobertura autoproducidos no son evidencia de coherencia por sí mismos.
- Entradas: los artefactos activos (01–08 aplicables), `CLARIFICATION_LEDGER.md`, los `ASM-NNN`, las decisiones humanas cerradas y la gobernanza aplicable (workspace y repositorio).
- Proporcionalidad: una pasada sin objeto (p. ej. `AC_TO_TASK` sin Task Breakdown) se marca `NOT_APPLICABLE`.
- **Un finding por problema distinto.** Dos invenciones independientes en un mismo test son dos findings; la misma contradicción repetida en varios artefactos es un solo finding que lista todos los artefactos.
- Un finding corregido durante la revisión se sigue listando, con su corrección y la fuente que la autorizó. El `result` se calcula sobre los findings **sin resolver**.
- **Comportamiento añadido aguas abajo.** Si una tarea, un escenario o un test añade comportamiento que no está en su fuente, ese comportamiento nunca se promueve a la Hard Specification por haber aparecido ahí. Se elimina del artefacto aguas abajo (`SPEC_REMEDIATION`) cuando nada indica que se desee, o se pregunta (`CLARIFICATION_REQUIRED`) cuando puede ser deseado, cuando choca con algo explícito de la spec o cuando el artefacto que lo añade es la única fuente de un comportamiento material.

## 2. Pasadas

| # | Pasada | Qué busca |
|---|---|---|
| 1 | `DUPLICATION` | Dos requisitos, reglas o AC que dicen lo mismo con palabras distintas, o casi lo mismo con una diferencia no explicada |
| 2 | `TERMINOLOGY_DRIFT` | Un concepto con varios nombres, o un nombre con varios significados, entre artefactos |
| 3 | `SEMANTIC_CONTRADICTION` | Afirmaciones incompatibles entre artefactos o dentro de uno (un BR prohíbe lo que un AC exige; un estado que un artefacto permite y otro prohíbe) |
| 4 | `UNDER_SPECIFICATION` | Un elemento referenciado o usado sin definición suficiente (una entidad del escenario que no existe en la Hard Specification; un verbo sin objeto o sin resultado) |
| 5 | `SCOPE_INCONSISTENCY` | Algo fuera de alcance en un artefacto que otro trata como dentro, o comportamiento en alcance que ningún artefacto cubre |
| 6 | `BUSINESS_RULE_TO_BEHAVIOR` | Cada BR material se refleja en comportamiento (flujo, caso límite o escenario) compatible con su texto |
| 7 | `BEHAVIOR_TO_AC` | Cada comportamiento material tiene un AC que lo verifica, y cada AC verifica comportamiento especificado, no uno nuevo |
| 8 | `AC_TO_TASK` | Las tareas que citan un AC lo implementan sin cambiarlo, y **ninguna tarea introduce comportamiento** que no esté en la especificación |
| 9 | `AC_TO_ACCEPTANCE_TEST` | Cada AT verifica el AC que cita con su mismo significado: mismos datos de frontera, mismo resultado esperado. **Un AT no inventa semántica** (umbrales, mensajes, estados) ausente de BR/AC/SC |
| 10 | `EXECUTION_CONTRACT_PRESERVATION` | El contrato 07 conserva el alcance, las exclusiones, los AC, las decisiones cerradas y las restricciones de las etapas previas, sin añadir ni quitar; sus `ASSUMPTIONS` e `IMPLEMENTATION_GUIDELINES` no esconden comportamiento |
| 11 | `GOVERNANCE_CONSISTENCY` | Nada en la spec contradice la gobernanza de workspace o de repositorio, ni una decisión humana cerrada |
| 12 | `CLARIFICATION_APPLICATION` | Cada `CLAR-NNN` `APPLIED` está integrada en los artefactos que lista en `AFFECTS`; ningún artefacto conserva el texto que la respuesta sustituyó; ninguna `SUPERSEDED` sigue vigente en un artefacto; ningún requisito existe sólo en el ledger. Los `SOURCE` / `DERIVED_FROM` de BR y AC materiales apuntan a fuentes que respaldan **su contenido**: un requisito material respaldado por una inferencia del agente, o por una `CLAR` cuya respuesta no dice lo que el requisito afirma (incluida una respuesta "fuera de alcance"), es un finding `HIGH` material con ruta `CLARIFICATION_REQUIRED` |

Las pasadas 6–9 recorren las relaciones **que existen**. No exigen una cadena 1:1 `BR → UC → SC → AC → TASK → AT`: verifican que, donde hay relación, el significado se conserva, y que todo requisito material tiene cobertura semántica suficiente.

## 3. Finding

```
COH-001
SEVERITY:                CRITICAL | HIGH | MEDIUM | LOW
TYPE:                    <pasada>
ARTIFACTS:               <artefacto · sección · ID>
ISSUE:                   <qué no encaja, en una frase>
EVIDENCE:                <fragmentos citados>
WHY_IT_MATTERS:          <qué se construiría o verificaría mal>
MATERIAL_FOR_EXECUTION:  YES | NO | AMBIGUOUS
RESOLUTION_ROUTE:        SPEC_REMEDIATION | CLARIFICATION_REQUIRED | DISCOVERY | DECISION_REQUIRED
```

| Severidad | Cuándo |
|---|---|
| `CRITICAL` | Contradicción con gobernanza o con una decisión cerrada; contradicción material que hace imposible saber qué construir; requisito material sin ninguna cobertura de comportamiento |
| `HIGH` | Contradicción material entre artefactos; tarea que introduce comportamiento; AT que inventa semántica; clarificación no aplicada o texto sustituido todavía vigente |
| `MEDIUM` | Deriva terminológica que no cambia el comportamiento pero puede confundir; infraespecificación no material; duplicación con diferencias menores |
| `LOW` | Redacción, duplicación exacta, inconsistencias de formato |

| `RESOLUTION_ROUTE` | Cuándo |
|---|---|
| `SPEC_REMEDIATION` | No material, o la versión correcta ya la fija una fuente de mayor autoridad citada |
| `CLARIFICATION_REQUIRED` | Material y la versión correcta depende de una respuesta humana |
| `DISCOVERY` | El conflicto depende de un hecho verificable del sistema actual |
| `DECISION_REQUIRED` | Choque con una decisión cerrada o materia reservada (§1.4); `DECISION_CONTRADICTION` si una decisión cerrada choca con un hecho autoritativo (§16) |

## 4. Resultado

```
SPEC_COHERENCE_RESULT
  evaluated_at:      <fecha>
  artifacts:         <artefactos y ledger evaluados>
  passes:            <pasada · PASS | FINDINGS | NOT_APPLICABLE>
  findings:          NONE | <COH-NNN · severidad · material · ruta>
  blocking_findings: NONE | <COH-NNN>
  result:            PASS | FAIL
```

`result: FAIL` si queda sin resolver algún finding `CRITICAL` o `HIGH` con `MATERIAL_FOR_EXECUTION: YES`, o cualquier finding con `MATERIAL_FOR_EXECUTION: AMBIGUOUS`. Los demás se registran y no bloquean.

## 5. Uso incremental y gate formal

```
DETECT EARLY. REMEDIATE LOCALLY. GATE FORMALLY AT THE END.
```

- Al producir una etapa se aplican las pasadas que la tocan: 04 → 2, 3, 5; 05 → 3, 6, 7; 06 → 8; 08 → 9; tras aplicar una clarificación → 12 sobre sus `AFFECTS`.
- Después del `SPEC_QUALITY_RESULT` del contrato 07 se ejecuta la revisión formal completa y se emite el `SPEC_COHERENCE_RESULT`.

`SPEC_COHERENCE_RESULT` **no** sustituye al readiness gate C1–C4.

## 6. Ejemplo: C2 pasa, coherencia falla

```
03  BR-004: un reembolso sólo se aprueba si la compra tiene menos de 30 días.
03  AC-007 (DERIVED_FROM: BR-004): se aprueba un reembolso de una compra de 45 días.
05  SC-012 (AC asociados: AC-007): Given una compra de 45 días, Then el reembolso se aprueba.
08  AT-009 (verifica AC-007)
```

C2: todos los IDs existen y AC-007 tiene evidencia aguas abajo → `PASS`. Coherencia: AC-007 contradice la BR de la que dice derivar → `COH-001 · HIGH · SEMANTIC_CONTRADICTION · MATERIAL: YES · CLARIFICATION_REQUIRED` → `FAIL`. No se corrige eligiendo 30 o 45 días. Sólo si el `SOURCE` de BR-004 es una decisión cerrada o una `CLAR-NNN` aplicada que fija los 30 días, la ruta pasa a `SPEC_REMEDIATION` de AC-007, SC-012 y AT-009 citando esa fuente.
