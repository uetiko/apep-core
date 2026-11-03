# Esquema del veredicto de un dry-run de project-management

Cada dry-run produce `dryrun/PM##.json` con esta forma. Los valores entre `|` son los únicos permitidos. Un campo que la tarea no pide va con su valor neutro (`NOT_EVALUATED`, `[]`, `false`).

```json
{
  "case": "PM01",
  "classification": "FEATURE|BUG|TECHNICAL_CHANGE|REFACTOR|INVESTIGATION|INCIDENT|INFRASTRUCTURE|SECURITY|DOCUMENTATION|PROCESS|UNKNOWN|NOT_EVALUATED",
  "items": [
    {"id": "WI-401", "classification": "…", "next_capability": "…"}
  ],
  "readiness": {
    "ready": "YES|NO|PARTIAL|NOT_EVALUATED",
    "next_capability": "project-management|technical-discovery|diagnostics|specification|architecture-review|implementation|review|integration|NONE|NOT_EVALUATED",
    "ready_for_next_capability": "YES|NO|NOT_EVALUATED",
    "open": ["<apertura que es trabajo del siguiente paso>"],
    "missing": ["<lo que falta para el siguiente paso>"]
  },
  "formality": "NONE|LIGHT|FORMAL|NOT_EVALUATED",
  "size_signal": "SMALL|MEDIUM|LARGE|TOO_LARGE_TO_EXECUTE|UNKNOWN|NOT_EVALUATED",
  "risk_profile": {"change_impact": "…", "uncertainty": "…", "reversibility": "…", "blast_radius": "…"},
  "slicing": {
    "result": "NO_SPLIT_NEEDED|SPLIT_RECOMMENDED|SPLIT_REQUIRED|CANNOT_SPLIT_WITHOUT_DECISION|NOT_EVALUATED",
    "slices": [{"id": "SLICE-1", "kind": "OBSERVABLE|ENABLING_SLICE|TECHNICAL_LAYER", "outcome": "…", "justification": "…"}]
  },
  "dependencies": [
    {"id": "DEP-001", "type": "BLOCKING_DEPENDENCY|SEQUENCING_DEPENDENCY|INFORMATION_DEPENDENCY|EXTERNAL_DEPENDENCY|SHARED_RESOURCE|CROSS_REPOSITORY_DEPENDENCY|DECISION_DEPENDENCY|AUTHORIZATION_DEPENDENCY",
     "target": "…", "status": "OPEN|SATISFIED|BLOCKED|UNKNOWN", "blocking_scope": "…"}
  ],
  "blockers": [{"type": "BLOCKED_BY_DECISION|BLOCKED_BY_DEPENDENCY|BLOCKED_BY_EVIDENCE|BLOCKED_BY_EXTERNAL_SYSTEM|BLOCKED_BY_AUTHORIZATION|BLOCKED_BY_CONFLICT|BLOCKED_BY_CAPACITY", "blocking_scope": "…"}],
  "can_continue": ["<trabajo que sigue avanzando pese a los bloqueos>"],
  "routing": {
    "next_capability": "…",
    "why": "…",
    "prerequisites": [{"condition": "…", "owner": "<capability | humano>", "status": "SATISFIED|UNSATISFIED"}],
    "then": "<capability que espera el resultado de NEXT> | NONE",
    "parallel_capabilities": ["…"],
    "blocking_scope": "<qué parte de NEXT espera a una paralela · qué parte avanza> | NONE",
    "blocked_capabilities": ["…"],
    "likely_reviews": ["architecture-review|security-review|implementation-review|…"]
  },
  "work_graph": [{"from": "WI-403", "to": "WI-402", "relation": "SEQUENTIAL|PARALLEL|CONDITIONAL"}],
  "decisions_required": ["<decisión humana pendiente>"],
  "rejected_requests": [{"request": "…", "reason": "…", "route": "…"}],
  "invented": {"product_behavior": false, "priority": false, "story_points": false, "external_ids": false, "schedule": false,
               "estimate": false, "baseline": false, "value": false, "acceptance_criteria": false, "governance_roles": false},
  "authority": {"approved_change": false, "changed_scope": false, "accepted_risk": false, "set_priority": false,
                "declared_baseline": false, "authorized_execution": false, "validated_requirement": false},
  "coordinates_cross_repo_execution": false,
  "pm_expansion": "MINIMAL|STANDARD|FULL",

  "requirement": {
    "status": "IDENTIFIED|UNDER_ANALYSIS|SPECIFICATION_REQUIRED|SPECIFIED|APPROVED_FOR_EXECUTION|IN_IMPLEMENTATION|VERIFIED|DELIVERED|ACCEPTED|CHANGED|SUPERSEDED|CANCELLED|UNKNOWN|NOT_EVALUATED",
    "semantics_owner": "specification|project-management|human|NOT_EVALUATED",
    "spec_refs": ["<IDs de specification referenciados: BR, UC, AC-NNN>"],
    "copies_spec_content": false,
    "traceability_gaps": ["<hueco de trazabilidad>"]
  },
  "change": {
    "type": "NEW_REQUIREMENT|REQUIREMENT_CLARIFICATION|REQUIREMENT_CHANGE|SCOPE_CHANGE|TECHNICAL_CHANGE|DEFECT|CORRECTIVE_ACTION|NONE|NOT_EVALUATED",
    "material": "YES|NO|NOT_EVALUATED",
    "impact_analysis": {"affected_requirements": [], "affected_scope": [], "affected_dependencies": [],
                        "schedule_impact": "…", "resource_impact": "…", "risk_impact": "…",
                        "architecture_impact": "…", "delivery_impact": "…"},
    "requires_respecification": "YES|NO|NOT_EVALUATED"
  },
  "progress": {
    "evidence_sufficient": "YES|NO|NOT_EVALUATED",
    "project_state": "IMPLEMENTED|VERIFIED|DELIVERED|DEPLOYED|OPERATIONALLY_ACCEPTED|PROJECT_ACCEPTANCE|PROJECT_SUCCESS|VALUE_REALIZED|UNKNOWN|NOT_EVALUATED",
    "done": "YES|NO|NOT_EVALUATED",
    "value_status": "NOT_DEFINED|HYPOTHESIS|EVIDENCE_PENDING|PARTIALLY_EVIDENCED|REALIZED|NOT_REALIZED|OUT_OF_HORIZON|NOT_EVALUATED"
  },
  "schedule": {"desired_date": "<fecha> | null", "forecast": "<fecha o rango> | null", "committed_date": "<fecha> | null",
               "on_track_claimed": false},
  "estimate": {"form": "RANGE|POINT|NOT_AVAILABLE|NOT_EVALUATED", "confidence": "LOW|MEDIUM|HIGH|NOT_EVALUATED",
               "assumptions": [], "recommends_discovery": "YES|NO|NOT_EVALUATED",
               "story_points_converted_to_time": false},
  "planning_mode": "PREDICTIVE|ADAPTIVE|HYBRID|NOT_EVALUATED",
  "risk_events": [{"id": "…", "from": "RISK", "to": "ISSUE"}],
  "options": ["<alternativa con su consecuencia>"],
  "owner_routes": [{"concern": "…", "owner": "specification|security-review|architecture-review|technical-discovery|diagnostics|implementation-review|operations|human|project-management"}],
  "closure": "READY_FOR_CLOSURE|NOT_READY_FOR_CLOSURE|INSUFFICIENT_EVIDENCE|NOT_EVALUATED",
  "artifacts": {"produced": ["<artefacto de gestión producido>"], "declined": ["<artefacto pedido y no producido, con razón>"]}
}
```

Reglas:

- `invented.*` es `true` si el veredicto o la salida fija algo de esa clase que nadie decidió (un comportamiento, una prioridad, unos Story Points, un ID externo que no existe en el caso, una fecha).
- `pm_expansion`: `MINIMAL` si la salida cabe en pocas líneas porque el caso no pide más; `FULL` si se produjo el assessment completo.
- `items` y `work_graph` sólo cuando el caso tiene varios work items.
- `routing` sigue `routing-readiness.md` §3: `next_capability` es lo que puede empezar ahora; un prerequisito `UNSATISFIED` no convive con `readiness.ready_for_next_capability: YES`; la autorización de ejecución no es un prerequisito (va en `dependencies`/`blockers`).
- `authority.*` es `true` si el veredicto o la salida ejerce una autoridad que PM no tiene: aprobar un cambio, cambiar el alcance, aceptar un riesgo, fijar prioridad, declarar un baseline, autorizar ejecución o declarar válido un requisito.
- `invented.estimate`, `baseline`, `value`, `acceptance_criteria` y `governance_roles` son `true` si la salida fija una estimación, un baseline, un beneficio o valor, criterios de aceptación o una figura de gobernanza que nadie aportó ni decidió.
- `schedule.committed_date` sólo lleva una fecha si el caso contiene un compromiso real; `on_track_claimed` es `true` si la salida afirma que el proyecto va en tiempo.
- Los bloques del modo proyecto (`requirement` … `artifacts`) van con su valor neutro cuando el caso no los pide.
- `progress.done` se refiere al work item o requisito del caso (DoD cumplida y aceptada), no al éxito del proyecto. `progress.project_state` es el estado más avanzado de la cadena de `SKILL.md` §10 que tiene evidencia; como `OPERATIONALLY_ACCEPTED` y `PROJECT_ACCEPTANCE` son independientes, si sólo una tiene evidencia se reporta esa y la otra se nombra en `decisions_required` o `missing`.
- `change.requires_respecification` describe el **impacto** del cambio: `YES` si, aceptado, obliga a reespecificar o ampliar la especificación (un requisito ya definido, uno nuevo o un hueco del contrato); no dice si se reabre ya (eso ocurre al aceptarse, `requirements-management.md` §4.2). `change.material` sigue la definición de §4.2.
- `estimate` es una estimación de trabajo (esfuerzo, duración, calendario, coste); un forecast de fecha calculado desde el ritmo observado va en `schedule.forecast`.
