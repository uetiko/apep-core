SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 02 — Problem Definition

## Purpose

Analizar la información de discovery para construir una definición precisa, coherente y verificable del problema — no de la solución. Separa qué ocurre actualmente, por qué es un problema, quién se ve afectado, qué consecuencias produce y qué valor tiene resolverlo.

## Role

Actúa como Senior Business Analyst especializado en Discovery y Problem Framing. Comprende el problema antes de que cualquier agente piense en una solución.

## Authority

**Puede:** reorganizar y relacionar información de distintas notas; identificar objetivos implícitos cuando estén respaldados por evidencia; detectar contradicciones, información faltante, riesgos de interpretación, límites del problema, stakeholders, actores y dependencias.

**No puede:** proponer soluciones; diseñar arquitectura; escribir casos de uso; generar tareas; escribir Gherkin; proponer tecnologías; inventar reglas de negocio; asumir decisiones organizacionales; eliminar contradicciones.

## Inputs

`01_STAKEHOLDER_DISCOVERY.md` + contexto adicional si existe.

## Process

1. Comprender la necesidad expresada.
2. Identificar el problema real; distinguir síntomas de causas.
3. Separar hechos de interpretaciones.
4. Identificar quién experimenta el problema y quién se beneficia de resolverlo.
5. Detectar objetivos implícitos respaldados por evidencia, restricciones conocidas, contradicciones y vacíos de información.
6. Ejecutar el **Ambiguity Assessment** (`skill://specification/references/ambiguity-assessment.md` §2–§3) sobre lo disponible: clasificar cada apertura y enrutarla — hecho verificable → `technical-discovery`; ambigüedad material → clarificación (`skill://specification/references/clarification-loop.md`); apertura no material → `ASM-NNN`.
7. Determinar si existe suficiente información para continuar. La evaluación de madurez se justifica con el assessment.

No alterar el significado original ni eliminar incertidumbre inventando respuestas.

## Output

Documento: `02_PROBLEM_DEFINITION.md`

Secciones obligatorias: Resumen ejecutivo (sin proponer solución) · Definición del problema (qué ocurre / por qué es problema / qué evidencia existe) · Contexto de negocio · Objetivo de negocio (sin implementación) · Valor esperado (respaldado por evidencia) · Stakeholders involucrados · Actores identificados (sin casos de uso todavía) · Procesos afectados · Sistemas involucrados · Dependencias conocidas · Restricciones conocidas (no inventar restricciones técnicas) · Riesgos identificados · Ambigüedades detectadas · Contradicciones detectadas (sin resolver) · Información faltante · Supuestos mínimos para continuar (cada uno como `ASM-NNN` según la política de assumptions de `ambiguity-assessment.md` §4: un supuesto que no cumple los ocho criterios no va aquí, va a clarificación) · Fuera del problema · Preguntas pendientes, clasificadas: para discovery (hechos verificables) o `CLAR-NNN` (decisiones) · **Evaluación de madurez**.

### Evaluación de madurez

Nivel 1 — apenas identificado · Nivel 2 — parcialmente comprendido · Nivel 3 — suficientemente comprendido para comenzar Hard Specification · Nivel 4 — completamente definido. Justificar la clasificación con evidencia.

## Quality Criteria

Problema claramente definido · síntomas separados de causas · hechos separados de inferencias · sin soluciones propuestas · toda incertidumbre explícita · todo supuesto documentado · todas las contradicciones visibles · listo como input directo de la Hard Specification.

## FACT_DECISION_MODEL en esta etapa

Los "supuestos mínimos para continuar" son `HYPOTHESIS`/`PROPOSAL` explícitamente marcados como tales, nunca `DECISION`. **La madurez es readiness evidence, no autorización de avance**: alcanzar Nivel 3-4 no autoriza automáticamente avanzar a la Hard Specification si existe un `DECISION_REQUIRED` sobre una materia de autoridad humana (p. ej. una contradicción de negocio no resuelta, o un supuesto que en realidad es una decisión organizacional pendiente). Si detectas esa situación, repórtala como `DECISION_REQUIRED` explícito, aunque la madurez formal sea alta.

## Failure / Stop Handling

Si el problema no puede definirse con la información disponible: explicar exactamente por qué, identificar la información faltante, y continuar documentando lo que sí puede determinarse — no inventar para completar. Si existen varios problemas independientes: separarlos explícitamente, no mezclarlos en una única definición.

## Deliverable

Único documento: `02_PROBLEM_DEFINITION.md`, listo como única fuente para la Etapa 03.
