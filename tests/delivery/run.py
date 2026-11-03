#!/usr/bin/env python3
"""Validación determinista de la Línea 2 (Delivery Factory).

Dos capas, sin dependencias externas y sin llamar a ningún modelo:

  STRUCTURE  el contrato está presente: snapshot autorizado, preflight, baseline congelada,
             worktree de ejecución y su limpieza, verificación y atribución de fallos,
             IMPLEMENTATION_RESULT, convergencia por AC (owner implementation-review),
             remediation acotada, DELIVERY_EVIDENCE y gate de INTEGRATION_READY; fronteras
             entre delivery-lifecycle, delivery-orchestrator, implementation, implementation-review,
             git-workflow y los work modes; regresión de approvals del worktree.
  DRYRUN     compara los veredictos registrados en `dryrun/L2-NN.json` (producidos por un agente
             que aplicó la Línea 2 sin ver `expected/`) con `expected/L2-NN.json`.
             Un veredicto ausente es NOT_RUN, nunca PASS.

Uso:  python3 -I .omp/tests/delivery/run.py
Exit: 0 todo PASS · 1 algún FAIL · 2 algún NOT_RUN sin FAIL.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OMP = HERE.parent.parent
SK = OMP / "skills"

rows = []


def record(layer, case, ok, detail):
    rows.append((layer, case, "PASS" if ok is True else ("NOT_RUN" if ok is None else "FAIL"), detail))


def text(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


# ── STRUCTURE ────────────────────────────────────────────────────────────────
REQ = {
    "skills/delivery-lifecycle/SKILL.md": [
        "LINE 2 MATERIALIZES AN AUTHORIZED CONTRACT", "IMPLEMENTATION MAY NOT CHANGE WHAT", "| `EXECUTION_PREFLIGHT` |",
        "→ EXECUTION_PREFLIGHT →", "REMEDIATION_EXHAUSTED", "integration_ready: YES", "INTEGRATION_READY != COMPLETE",
        "`implementation` es el único que escribe producto", "LINE 2 STATUS: USABLE",
        "references/execution-preflight.md", "references/delivery-evidence.md", "references/ac-convergence.md"],
    "skills/delivery-lifecycle/references/execution-preflight.md": [
        "AUTHORIZED_EXECUTION_SNAPSHOT", "AUTHORIZED CONTRACT MUTATED → AUTHORIZATION_STALE → EXECUTION MUST NOT CONTINUE",
        "sha256sum", "NOT_AVAILABLE (contrato en sesión)", "EXECUTION_PREFLIGHT_RESULT",
        "PASS | BLOCKED | DECISION_REQUIRED | AUTHORIZATION_STALE", "EXECUTION_BASELINE", "THE EXECUTION BASELINE IS FROZEN",
        "preexisting_failures", "CONTROL CHECKOUT", "EXECUTION WORKTREE", ".worktrees/exec-<ID>", "Worktree obligatorio",
        "Los ejecuta **la Main Session**", "WORKSPACE_ISOLATION_WAIVED", "Nunca `--force`", "`git status --porcelain`"],
    "skills/delivery-lifecycle/references/delivery-evidence.md": [
        "CHEAPEST RELEVANT CHECK → TARGETED VERIFICATION → BROADER REGRESSION WHEN JUSTIFIED",
        "PREEXISTING_FAILURE", "INTRODUCED_FAILURE", "UNKNOWN_ATTRIBUTION", "SELF-VERIFICATION != INDEPENDENT CONFORMANCE",
        "FIX_ALREADY_AUTHORIZED", "CONTRACT_CONTRADICTION", "REMEDIATION MAY NOT REWRITE THE CONTRACT",
        "OUT-OF-SCOPE DISCOVERY IS REPORTED, NOT ABSORBED", "**una vez**", "REMEDIATION_EXHAUSTED", "DELIVERY_EVIDENCE",
        "**todo AC material aplicable en `PASS`**", "INTEGRATION_READY != AUTHORIZED_TO_COMMIT",
        "INTEGRATION_READY != AUTHORIZED_TO_PUSH", "INTEGRATION_READY != AUTHORIZED_TO_PUBLISH_PR",
        "INTEGRATION_READY != AUTHORIZED_TO_MERGE", "REMOTE INTEGRATION BELONGS TO THE PR LIFECYCLE"],
    "skills/implementation-review/references/ac-convergence.md": [
        "EVERY MATERIAL AC REQUIRES EVIDENCE", "`PASS`", "`UNVERIFIED`", "`UNIMPLEMENTED`", "`CONTRADICTED`",
        "Cuatro estados, ninguno más", "IMPLEMENTATION_EVIDENCE", "VERIFICATION_EVIDENCE", "CONFORMANCE_RESULT",
        "`CLAIMED` nunca sostiene un `PASS`", "Muchos a muchos", "UNREQUESTED_BEHAVIOR", "AC_CONVERGENCE_RESULT",
        "CONVERGED | NOT_CONVERGED", "El owner es `implementation-review`"],
    "skills/implementation-review/SKILL.md": [
        "SELF-VERIFICATION != INDEPENDENT CONFORMANCE", "references/ac-convergence.md", "| `UNREQUESTED_BEHAVIOR` |",
        "`AC_CONVERGENCE_RESULT`", "Esa clasificación no la hace este skill"],
    "agents/implementation.md": [
        "IMPLEMENTATION MAY NOT CHANGE WHAT", "<preflight>", "AUTHORIZATION_STALE", "IMPLEMENTATION_RESULT",
        "failures:            preexisting", "No lo creas ni lo borras", "la convergencia por AC la declara `implementation-review`"],
    "agents/delivery-orchestrator.md": [
        "EXECUTION_PREFLIGHT", "No creas ni borras worktrees", "No declaras conformidad", "DELIVERY_EVIDENCE"],
    "skills/git-workflow/SKILL.md": ["**Worktree de ejecución.**", "los ejecuta la Main Session"],
    "commands/deliver.md": ["EXECUTION_PREFLIGHT", "DELIVERY_EVIDENCE", "`INTEGRATION_READY != COMPLETE`"],
    "commands/review.md": ["SELF-VERIFICATION != INDEPENDENT CONFORMANCE", "AC_CONVERGENCE_RESULT"],
}


def structure():
    for name, needles in REQ.items():
        body = text(OMP / name)
        missing = [n for n in needles if n not in body]
        record("STRUCTURE", name, bool(body) and not missing, "ok" if not missing else f"falta {missing}")

    ac = text(SK / "implementation-review" / "references" / "ac-convergence.md")
    table = ac.split("## 1.")[1].split("## 2.")[0]
    states = set(re.findall(r"^\| `([A-Z_]+)` \|", table, re.M))
    record("STRUCTURE", "estados de AC: exactamente PASS · UNVERIFIED · UNIMPLEMENTED · CONTRADICTED",
           states == {"PASS", "UNVERIFIED", "UNIMPLEMENTED", "CONTRADICTED"}, str(sorted(states)))
    record("STRUCTURE", "OUT_OF_SCOPE_CHANGE no es un estado de AC", "OUT_OF_SCOPE_CHANGE" not in states, "transversal (§3)")

    impl = text(OMP / "agents" / "implementation.md")
    record("STRUCTURE", "implementation no declara conformidad ni crea worktrees",
           "AC_CONVERGENCE_RESULT" not in impl and "git worktree add" not in impl, "owner: implementation-review · Main Session")
    orch = text(OMP / "agents" / "delivery-orchestrator.md")
    record("STRUCTURE", "el orchestrator no muta repositorios (bash sólo evidencia)",
           "Nunca para mutar repositorios" in orch and "git worktree add" not in orch, "")
    ir = text(SK / "implementation-review" / "SKILL.md")
    record("STRUCTURE", "implementation-review sigue sin corregir (REVIEW != REMEDIATION)",
           "`REVIEW_FINDING != AUTHORIZATION_TO_FIX`" in ir and "no se aplican patches" in ir, "§14")

    cases = text(OMP / "tests" / "approvals" / "cases.ts")
    need = {"W01": "PROMPT", "W02": "PROMPT", "W03": "PROMPT", "W04": "PROMPT", "W05": "PROMPT", "W06": "PROMPT", "W07": "ALLOW"}
    bad = [k for k, v in need.items() if not re.search(rf'bash\("{k}", "exec-worktree", "[^"]+", "{v}"', cases)]
    record("STRUCTURE", "approvals: el worktree de ejecución conserva su gate (W01–W07)", not bad, str(bad or "ok"))

    spec = text(SK / "specification" / "SKILL.md")
    record("STRUCTURE", "Línea 1 intacta: EXECUTION_READY sigue sin autorizar",
           "`EXECUTION_READY` es el resultado del readiness gate, no una autorización" in spec, "specification §6")


# ── DRYRUN ───────────────────────────────────────────────────────────────────
def collect(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, list):
            cur = [x.get(part) for x in cur if isinstance(x, dict)]
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def flat(val):
    lst = val if isinstance(val, list) else [val]
    return [y for x in lst for y in (x if isinstance(x, list) else [x]) if y is not None]


def match(el, crit):
    for k, v in crit.items():
        if k.startswith("_regex_"):
            if not re.search(v, str(el.get(k[7:], ""))):
                return False
        elif el.get(k) != v:
            return False
    return True


def check(v, op, path, arg):
    val = collect(v, path) if path else None
    items = flat(val)
    if op == "eq":
        return val == arg, f"{path}={val!r}"
    if op == "in":
        return val in arg, f"{path}={val!r}"
    if op == "not_in":
        return val not in arg, f"{path}={val!r}"
    if op == "min_len":
        return isinstance(val, list) and len(val) >= arg, f"len({path})={len(val) if isinstance(val, list) else '—'}"
    if op == "contains":
        return arg in items, f"{path}={items}"
    if op == "any_match_in":
        return any(x in arg for x in items), f"{path}={items}"
    if op in ("any_match", "none_match"):
        found = any(isinstance(e, dict) and match(e, arg) for e in (val if isinstance(val, list) else []))
        return found if op == "any_match" else not found, f"{op} {arg}"
    if op == "any_regex":
        return any(re.search(arg, str(x)) for x in items), f"{path} ~ {arg}"
    if op == "none_regex":
        return not any(re.search(arg, str(x)) for x in items), f"{path} !~ {arg}: {items}"
    if op == "all_nonempty":
        return bool(items) and all(str(x).strip() for x in items), f"{path} no vacío"
    if op == "all_nonempty_where":
        sel = [e for e in (val or []) if isinstance(e, dict) and e.get("kind") == arg["kind"]]
        return bool(sel) and all(str(e.get(arg["field"]) or "").strip() for e in sel), f"{arg}"
    if op == "all_false":
        d = v.get(path)
        if not isinstance(d, dict) or not d:
            return False, f"{path} ausente"
        bad = [k for k, x in d.items() if x is not False]
        return not bad, f"{path}: {bad or 'nada'}"
    if op == "auth_recorded":
        # Contrato listo sin autorización: la autorización se registra aparte (routing-readiness.md §2).
        deps = [d.get("type") for d in v.get("dependencies") or []]
        blk = [b.get("type") for b in v.get("blockers") or []]
        ok = "AUTHORIZATION_DEPENDENCY" in deps or "BLOCKED_BY_AUTHORIZATION" in blk
        return ok, f"deps={deps} blockers={blk}"
    if op == "item":
        it = [i for i in v.get("items", []) if i.get("id") == path]
        return bool(it) and it[0].get("next_capability") == arg, f"{path}→{it[0].get('next_capability') if it else '—'}"
    raise ValueError(op)


def dryrun():
    for exp_path in sorted((HERE / "expected").glob("L2-*.json")):
        case = exp_path.stem
        exp = json.loads(text(exp_path))
        vpath = HERE / "dryrun" / f"{case}.json"
        if not vpath.exists():
            record("DRYRUN", f"{case} {exp['desc']}", None, "sin veredicto registrado")
            continue
        verdict = json.loads(text(vpath))
        bad = []
        for op, path, arg in exp["assert"]:
            ok, why = check(verdict, op, path, arg)
            if not ok:
                bad.append(f"{op} {path}: {why}")
        record("DRYRUN", f"{case} {exp['desc']}", not bad, "; ".join(bad) or f"{len(exp['assert'])} aserciones")


def main():
    structure()
    dryrun()
    width = max(len(r[1]) for r in rows)
    for layer, case, res, detail in rows:
        print(f"{layer:<10} {res:<8} {case:<{width}}  {detail}")
    counts = {k: sum(1 for r in rows if r[2] == k) for k in ("PASS", "FAIL", "NOT_RUN")}
    print(f"\nTOTAL: {len(rows)}  PASS: {counts['PASS']}  FAIL: {counts['FAIL']}  NOT_RUN: {counts['NOT_RUN']}")
    sys.exit(1 if counts["FAIL"] else 2 if counts["NOT_RUN"] else 0)


if __name__ == "__main__":
    main()
