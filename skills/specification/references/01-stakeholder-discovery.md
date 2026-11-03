SOURCE: (internal methodology lineage, not required at runtime)
ADAPTATION: OMP Specification Skill v0.1

# Etapa 01 — Stakeholder Discovery

## Purpose

Capturar, preservar y estructurar la información inicial del stakeholder sin modificar su significado ni introducir interpretación funcional, técnica o arquitectónica. Transforma información desestructurada (notas, reuniones, correos, chats, tickets, ideas incompletas) en un documento organizado que preserva fielmente la intención original. Esta etapa no produce especificaciones — produce un registro organizado, listo para la Etapa 02.

## Role

Actúa como Business Discovery Recorder. No eres analista funcional, arquitecto, Product Owner ni desarrollador. Eres el primer eslabón de la cadena.

## Authority

**Puede:** reorganizar información; agrupar ideas relacionadas; identificar temas repetidos; separar hechos de opiniones; marcar inconsistencias; preservar citas textuales.

**No puede:** inventar requisitos; reinterpretar objetivos; inferir reglas de negocio; diseñar arquitectura; proponer implementación; escribir casos de uso; generar tareas; eliminar información aparentemente irrelevante; clasificar prioridades; dividir trabajo; producir Gherkin ni criterios de aceptación.

## Inputs

Stakeholder input crudo, en cualquier forma (notas, transcripciones, tickets, hilos de chat, lluvia de ideas).

## Process

1. Identificar bloques temáticos.
2. Conservar frases textuales relevantes.
3. Separar hechos de opiniones.
4. Identificar elementos repetidos.
5. Detectar contradicciones.
6. Detectar vacíos de información.
7. Detectar términos ambiguos.
8. Organizar toda la información sin reinterpretarla.

No alterar el significado original.

## Output

Documento: `01_STAKEHOLDER_DISCOVERY.md`

Secciones obligatorias: Resumen ejecutivo (descriptivo, no interpretativo) · Petición original (literal) · **Normalización de intake** (`skill://specification/references/ambiguity-assessment.md` §1: sólo con lo que la entrada dice explícitamente, `UNKNOWN` / `NONE_DECLARED` en el resto, y la separación `PROBLEM` / `PROPOSED_SOLUTION` con el estado de la solución sin suponerlo) · Información proporcionada (por temas) · Frases textuales relevantes · Necesidades expresadas (sólo explícitas, no inferidas) · Objetivos mencionados · Problemas observados · Sistemas/procesos/dominios mencionados · Actores mencionados · Restricciones mencionadas · Dependencias mencionadas · Información faltante (sin completarla) · Ambigüedades detectadas · Contradicciones detectadas (sin resolverlas) · Preguntas sugeridas para Discovery (sin responderlas).

## Quality Criteria

No perder información · no inventar requisitos · no resolver ambigüedades · no eliminar contradicciones · mantener trazabilidad con la entrada · diferenciar hechos, opiniones y preguntas · quedar listo como input directo de la Etapa 02.

## FACT_DECISION_MODEL en esta etapa

Todo lo registrado es `FACT` (lo que el stakeholder dijo) o, cuando se marca explícitamente como tal, `HYPOTHESIS`/pregunta abierta. Esta etapa no produce `PROPOSAL`, `RECOMMENDATION` ni `DECISION_REQUIRED` — su única salida es evidencia organizada. Las ambigüedades y preguntas que registra son la entrada del Ambiguity Assessment; esta etapa no las clasifica ni las prioriza (eso empieza en la Etapa 02).

## Failure / Stop Handling

Si la información es insuficiente: marcarla como insuficiente, identificar exactamente qué falta, y continuar estructurando el resto — no es una condición de `STOP_REPORT`, es un hallazgo a documentar en "Información faltante". Si existen contradicciones: no resolverlas, registrarlas. Si aparecen múltiples temas independientes: separarlos en bloques diferenciados.

## Deliverable

Único documento: `01_STAKEHOLDER_DISCOVERY.md`, listo para ser consumido por la Etapa 02.
