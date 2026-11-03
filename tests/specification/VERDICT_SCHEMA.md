# Esquema del veredicto de un dry-run

Cada dry-run produce `dryrun/T##.json` con exactamente esta forma. Los valores entre `|` son los únicos permitidos.

```json
{
  "fixture": "T01",
  "final_state": "INTAKE|AMBIGUITY_ASSESSMENT|CLARIFICATION_REQUIRED|CLARIFYING|SPECIFYING|SPEC_COMPLETE|SPEC_QUALITY_REVIEW|SPEC_COHERENCE_REVIEW|NOT_EXECUTION_READY|EXECUTION_READY",
  "next_step": "<texto breve>",
  "human_questions": [
    {"id": "CLAR-001", "question": "¿…?", "classification": "MATERIAL_DECISION|FACTUAL_UNKNOWN|CONTRADICTION|NON_MATERIAL_ASSUMPTION", "dimension": "<una de las 12>", "why_it_matters": "<frase>"}
  ],
  "discovery_questions": [
    {"question": "<pregunta>", "answer": "<FACT con evidencia | UNKNOWN>", "evidence": "<archivo:línea | —>"}
  ],
  "assumptions": [
    {"id": "ASM-001", "assumption": "<texto>", "reason": "<texto>", "criteria_A1_A8": "ALL_MET|NOT_MET"}
  ],
  "rejected_assumptions": [
    {"text": "<supuesto>", "failed_criteria": ["A6"], "route": "CLARIFICATION_REQUIRED|DECISION_REQUIRED"}
  ],
  "spec_quality": {
    "result": "PASS|FAIL|NOT_EVALUATED",
    "material_fails": ["SQ5"],
    "evidence": ["<check · fragmento · ubicación>"]
  },
  "spec_coherence": {
    "result": "PASS|FAIL|NOT_EVALUATED",
    "findings": [
      {"id": "COH-001", "type": "<una de las 12 pasadas>", "severity": "CRITICAL|HIGH|MEDIUM|LOW", "material": "YES|NO|AMBIGUOUS", "route": "SPEC_REMEDIATION|CLARIFICATION_REQUIRED|DISCOVERY|DECISION_REQUIRED", "issue": "<frase>"}
    ]
  },
  "readiness": {
    "evaluated": true,
    "reference_integrity": "PASS|WARN|FAIL|NOT_EVALUATED",
    "non_material_items": ["ASM-001"],
    "blocking_reasons": ["<texto>"],
    "execution_ready": "YES|NO|NOT_EVALUATED"
  },
  "line2_executed": false
}
```

Reglas:

- `human_questions` contiene sólo lo que se preguntaría **al humano**. Lo que se resuelve con evidencia del sistema va en `discovery_questions`.
- Si una revisión no aplica a la tarea de la fixture, su `result` es `NOT_EVALUATED` (y `readiness.evaluated: false` si no se ejecutó el gate).
- `line2_executed` es siempre `false` salvo que se haya implementado código de producto.
