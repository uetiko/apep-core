# Esquema del veredicto de un dry-run de la Línea 2

Cada dry-run produce `dryrun/L2-NN.json` con esta forma. Los valores entre `|` son los únicos permitidos. Un campo que el caso no pide va con su valor neutro (`NOT_EVALUATED`, `[]`, `false`, `null`).

```json
{
  "case": "L2-01",
  "formality": "NONE|LIGHT|FORMAL|NOT_EVALUATED",
  "preflight": {"result": "PASS|BLOCKED|DECISION_REQUIRED|AUTHORIZATION_STALE|NOT_EVALUATED", "blocking_reasons": []},
  "execution_starts": "YES|NO|NOT_EVALUATED",
  "product_write": "ALLOWED|NOT_ALLOWED|NOT_EVALUATED",
  "writes_current_checkout": "YES|NO|NOT_EVALUATED",
  "workspace": {"kind": "WORKTREE|CURRENT_BRANCH|NOT_EVALUATED",
                "required": "YES|NO|RECOMMENDED|NOT_EVALUATED",
                "created_by": "MAIN_SESSION|IMPLEMENTATION|ORCHESTRATOR|NOT_APPLICABLE|NOT_EVALUATED"},
  "baseline": {"base_commit": "<commit> | null", "evidence_tied_to": "<commit> | null"},
  "implementation": {"action": "CONTINUE|FIX_AND_RETEST|DECISION_REQUIRED|STOP_REPORT|NOT_EVALUATED",
                     "autonomous": "YES|NO|NOT_EVALUATED"},
  "failures": {"preexisting": [], "introduced": [], "unknown": []},
  "ac_convergence": [{"ac": "AC-001", "state": "PASS|UNVERIFIED|UNIMPLEMENTED|CONTRADICTED", "evidence": "…"}],
  "convergence_result": "CONVERGED|NOT_CONVERGED|NOT_APPLICABLE|NOT_EVALUATED",
  "transverse_findings": [{"type": "OUT_OF_SCOPE_CHANGE|CONTRACT_MISMATCH|MISSING_TEST|DEFECT|REGRESSION_RISK|UNREQUESTED_BEHAVIOR|UNVERIFIED_BEHAVIOR|…", "detail": "…"}],
  "remediation": {"classification": "FIX_ALREADY_AUTHORIZED|DECISION_REQUIRED|OUT_OF_SCOPE|CONTRACT_CONTRADICTION|NOT_APPLICABLE|NOT_EVALUATED",
                  "result": "REMEDIATION_REQUIRED|REMEDIATED|REMEDIATION_EXHAUSTED|NOT_APPLICABLE|NOT_EVALUATED"},
  "integration_ready": "YES|NO|NOT_EVALUATED",
  "lifecycle_state": "<estado de delivery-lifecycle §2> | NOT_EVALUATED",
  "actions": {"commit": false, "push": false, "publish_pr": false, "merge": false, "declare_complete": false,
              "remove_worktree": false, "weaken_test": false, "rebase_or_merge_base": false,
              "change_contract": false, "change_product_semantics": false},
  "formal_artifacts": ["<artefactos de trabajo FORMAL producidos: snapshot con fingerprint, worktree, AC_CONVERGENCE_RESULT…>"],
  "rejected_requests": [{"request": "…", "reason": "…"}],
  "decisions_required": ["<decisión humana pendiente>"],
  "invented": {"authorization": false, "evidence": false, "acceptance_criteria": false, "fingerprint": false}
}
```

Reglas:

- `actions.*` es `true` si el veredicto ejecuta o declara esa acción por su cuenta en el caso (hacer commit, borrar el worktree, debilitar un test, declarar `COMPLETE`…). Preparar un mensaje de commit no es hacer commit.
- `product_write`: si en el estado descrito se puede escribir producto **ahora**. Tras un preflight que crea el espacio de ejecución, se refiere a ese espacio.
- `writes_current_checkout`: si se escribe producto en el checkout que el caso describe como actual (no en un worktree nuevo).
- `workspace.created_by`: quién crea el espacio de ejecución cuando hay que crearlo.
- `invented.*` es `true` si la salida da por existente una autorización, una evidencia, un criterio de aceptación o un fingerprint que el caso no aporta.
