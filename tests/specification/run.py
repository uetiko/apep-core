#!/usr/bin/env python3
"""Validación determinista de la Línea 1 (`specification`).

Tres capas, sin dependencias externas y sin llamar a ningún modelo:

  STRUCTURE   el contrato de la skill está presente: C1–C4 intactos, mecanismos
              nuevos con sus checks, pasadas y campos, catálogo sin skills nuevas.
  MECHANICAL  checks mecánicos sobre las fixtures: integridad de referencias (C2)
              y señales léxicas de SQ5 / SQ10.
  DRYRUN      compara los veredictos registrados en `dryrun/T##.json` (producidos
              por un agente que aplicó la skill sin ver `expected/`) contra
              `expected/T##.json`. Un veredicto ausente es NOT_RUN, nunca PASS.

Uso:  python3 -I .omp/tests/specification/run.py
Exit: 0 todo PASS · 1 algún FAIL · 2 algún NOT_RUN sin FAIL.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OMP = HERE.parent.parent
SKILL = OMP / "skills" / "specification"
REFS = SKILL / "references"

ID_RE = re.compile(r"\b(BR|UC|SC|AC|TASK|AT|CLAR|ASM)-\d{3}\b")
# Un ID se define en negrita (`**AC-001**`) o al inicio de una línea, de una viñeta, de un encabezado o
# de la primera celda de una tabla (`AC-001 Un cliente…`, `### AC-001`, `| AC-001 |`).
DEFINE_RE = re.compile(r"\*\*((?:BR|UC|SC|AC|TASK|AT|CLAR|ASM)-\d{3})\*\*"
                       r"|^[ \t]*(?:[-*#|]+[ \t]*)?((?:BR|UC|SC|AC|TASK|AT|CLAR|ASM)-\d{3})\b", re.M)
VAGUE = ["rápido", "rápida", "segur", "adecuad", "razonable", "correctamente", "fácil", "intuitiv",
         "robust", "eficiente", "cuando sea necesario", "según corresponda", "si aplica", "etc."]
# `TBD` / `TODO` en mayúsculas: en minúsculas "todo" es una palabra común del español.
PLACEHOLDER_RE = re.compile(r"\bTBD\b|\bTODO\b|\?\?\?|\[(?i:pendiente)|\[NEEDS CLARIFICATION|\b(?i:a definir)\b")
CODE_EXT = {".php", ".py", ".ts", ".js", ".java", ".go", ".rb", ".sql", ".sh"}

rows = []


def record(layer, case, ok, detail):
    rows.append((layer, case, "PASS" if ok is True else ("NOT_RUN" if ok is None else "FAIL"), detail))


def text(path):
    return path.read_text(encoding="utf-8")


# ── STRUCTURE ────────────────────────────────────────────────────────────────
def structure():
    skill = text(SKILL / "SKILL.md")
    contract = text(REFS / "07-execution-contract.md")
    req = {
        "ambiguity-assessment.md": ["FUNCTIONAL_SCOPE", "ACTORS_AND_PERMISSIONS", "DOMAIN_RULES", "DATA_AND_STATE",
                                    "PRIMARY_FLOWS", "EDGE_AND_FAILURE_CASES", "EXTERNAL_INTEGRATIONS",
                                    "NON_FUNCTIONAL_REQUIREMENTS", "CONSTRAINTS", "TERMINOLOGY",
                                    "SUCCESS_AND_ACCEPTANCE", "OPEN_DECISIONS", "INTAKE_NORMALIZATION",
                                    "PROPOSED_SOLUTION", "IMPACT × UNCERTAINTY", "A1", "A8", "ASM-001",
                                    "DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US"],
        "clarification-loop.md": ["WHY_IT_MATTERS", "RECOMMENDED", "SUGGESTED", "CLARIFICATION_LEDGER.md",
                                  "OPEN", "APPLIED", "SUPERSEDED", "MATERIAL_DECISION", "FACTUAL_UNKNOWN",
                                  "NON_MATERIAL_ASSUMPTION", "REPOSITORY_EVIDENCE", "DECISION_REQUIRED",
                                  "ASK THE MINIMUM SET OF QUESTIONS", "Una respuesta sólo cierra lo que dice",
                                  "\"Fuera de alcance\" no cierra lo que el alcance necesita"],
        "03-hard-specification.md": ["Provenance de requisitos materiales", "nunca es un `SOURCE` válido"],
        "specification-quality.md": [f"SQ{i} " for i in range(1, 11)] + ["SPEC_QUALITY_RESULT"],
        "coherence-review.md": ["DUPLICATION", "TERMINOLOGY_DRIFT", "SEMANTIC_CONTRADICTION", "UNDER_SPECIFICATION",
                                "SCOPE_INCONSISTENCY", "BUSINESS_RULE_TO_BEHAVIOR", "BEHAVIOR_TO_AC", "AC_TO_TASK",
                                "AC_TO_ACCEPTANCE_TEST", "EXECUTION_CONTRACT_PRESERVATION",
                                "GOVERNANCE_CONSISTENCY", "CLARIFICATION_APPLICATION", "SPEC_COHERENCE_RESULT",
                                "REFERENCE_INTEGRITY  !=  SEMANTIC_COHERENCE"],
    }
    for name, needles in req.items():
        body = text(REFS / name) if (REFS / name).exists() else ""
        missing = [n for n in needles if n not in body]
        record("STRUCTURE", f"ref:{name}", bool(body) and not missing, "ok" if not missing else f"falta {missing}")
        record("STRUCTURE", f"skill->{name}", name in skill, "referenciada desde SKILL.md")

    for c in ("### C1", "### C2", "### C3", "### C4", "MATERIAL_FOR_EXECUTION", "UNRESOLVED_MATERIAL", "CONTRADICTED"):
        record("STRUCTURE", f"07 conserva {c}", c in contract, "readiness gate intacto")
    for f in ("spec_quality:", "spec_coherence:", "clarifications:", "SPEC QUALITY REVIEW → SPEC COHERENCE REVIEW → READINESS C1–C4"):
        record("STRUCTURE", f"07 integra {f}", f in contract, "secuencia previa al gate")
    rule = contract[contract.find("EXECUTION_READY = YES"):]
    for f in ("spec_quality = PASS", "spec_coherence = PASS", "CLAR-NNN OPEN", "reference_integrity ≠ FAIL"):
        record("STRUCTURE", f"regla readiness: {f}", f in rule, "")

    for state in ("INTAKE", "AMBIGUITY_ASSESSMENT", "CLARIFICATION_REQUIRED", "CLARIFYING", "SPECIFYING",
                  "SPEC_QUALITY_REVIEW", "SPEC_COHERENCE_REVIEW", "SPEC_COMPLETE", "NOT_EXECUTION_READY",
                  "EXECUTION_READY"):
        record("STRUCTURE", f"estado {state}", f"`{state}`" in skill, "SKILL.md §12")
    for inv in ("SPEC_COMPLETE  !=  EXECUTION_READY  !=  AUTHORIZED_TO_EXECUTE", "AC-NNN", "MANDATORY_EXECUTION_GATE"):
        record("STRUCTURE", f"invariante {inv[:40]}", inv in skill, "")

    skills = sorted(p.name for p in (OMP / "skills").iterdir() if (p / "SKILL.md").exists())
    record("STRUCTURE", "catálogo de skills", len(skills) == 11 and not any(
        k in s for s in skills for k in ("clarif", "analyze", "checklist", "spec-kit", "speckit")), f"{len(skills)} skills")
    agents = sorted(p.stem for p in (OMP / "agents").glob("*.md"))
    record("STRUCTURE", "catálogo de agents", len(agents) == 6, f"{len(agents)} agents")
    record("STRUCTURE", "sin dependencia operacional de spec-kit",
           not any("spec-kit/" in text(p) and "templates/" in text(p).split("spec-kit/", 1)[1][:30]
                   for p in REFS.glob("*.md")), "las referencias no cargan archivos de spec-kit")


# ── MECHANICAL ───────────────────────────────────────────────────────────────
def c2(body):
    defined = {a or b for a, b in DEFINE_RE.findall(body)}
    referenced = set(m.group(0) for m in ID_RE.finditer(body))
    return referenced - defined, defined


def mechanical():
    fx = HERE / "fixtures"
    missing, defined = c2(text(fx / "T14-c2-pass-coherence-fail.md"))
    record("MECHANICAL", "T14 C2 reference integrity", not missing and len(defined) >= 8,
           f"{len(defined)} IDs definidos, inexistentes: {sorted(missing) or 'ninguno'}")
    for t in ("T08-br-vs-ac-contradiction.md", "T09-task-introduces-behavior.md", "T10-at-invents-semantics.md",
              "T12-unresolved-clarification.md", "T13-non-material-open-item.md"):
        missing, _ = c2(text(fx / t))
        record("MECHANICAL", f"{t[:3]} C2 reference integrity", not missing,
               f"inexistentes: {sorted(missing) or 'ninguno'} (los defectos de la fixture son semánticos, no de referencia)")

    req_lines = [l for l in text(fx / "T06-vague-requirement.md").splitlines() if l.startswith("- ")]
    hits = sorted({w for l in req_lines for w in VAGUE if w in l.lower()})
    record("MECHANICAL", "T06 señales SQ5", len(hits) >= 3, f"señales: {hits}")
    ph = PLACEHOLDER_RE.findall(text(fx / "T12-unresolved-clarification.md"))
    record("MECHANICAL", "T12 señales SQ10/C1", len(ph) >= 1, f"marcadores: {ph}")
    t13 = text(fx / "T13-non-material-open-item.md")
    record("MECHANICAL", "T13 sin placeholders", not PLACEHOLDER_RE.search(t13), "ningún marcador abierto")


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


def same_id(value, wanted):
    """`SQ5` casa con "SQ5" y con "SQ5 · ubicación", no con "SQ50"."""
    s = str(value)
    return s == wanted or (s.startswith(wanted) and not s[len(wanted):len(wanted) + 1].isalnum())


def match(el, crit):
    for k, v in crit.items():
        if k.startswith("_regex_"):
            if not re.search(v, str(el.get(k[7:], ""))):
                return False
        elif el.get(k) != v:
            return False
    return True


def check(verdict, op, path, arg):
    val = collect(verdict, path)
    lst = val if isinstance(val, list) else [val]
    flat = [y for x in lst for y in (x if isinstance(x, list) else [x])]
    if op == "eq":
        return val == arg, f"{path}={val!r}"
    if op == "in":
        return val in arg, f"{path}={val!r}"
    if op == "min_len":
        return isinstance(val, list) and len(val) >= arg, f"len({path})={len(val) if isinstance(val, list) else '—'}"
    if op == "max_len":
        return isinstance(val, list) and len(val) <= arg, f"len({path})={len(val) if isinstance(val, list) else '—'}"
    if op in ("contains", "any_contains"):
        return any(same_id(x, arg) for x in flat), f"{path}={flat}"
    if op in ("any_match", "none_match"):
        found = any(isinstance(e, dict) and match(e, arg) for e in (val if isinstance(val, list) else []))
        return found if op == "any_match" else not found, f"{op} {arg}"
    if op == "any_regex":
        return any(re.search(arg, str(x)) for x in flat), f"{path} ~ {arg}"
    if op == "all_regex":
        return bool(flat) and all(re.search(arg, str(x)) for x in flat), f"{path} ~ {arg}"
    if op == "all_nonempty":
        return bool(flat) and all(str(x or "").strip() for x in flat), f"{path} no vacío"
    raise ValueError(op)


def files(case, spec):
    d = HERE / spec["dir"]
    for name in spec.get("require", []):
        record("DRYRUN", f"{case} archivo {name}", (d / name).exists(), str(d / name))
    for name, rx in spec.get("regex_present", []):
        p = d / name
        record("DRYRUN", f"{case} {name} contiene /{rx}/", p.exists() and bool(re.search(rx, text(p))), "")
    for name, rx in spec.get("regex_absent", []):
        p = d / name
        # Un artefacto no producido no puede contener el texto prohibido.
        record("DRYRUN", f"{case} {name} no contiene /{rx}/", not p.exists() or not re.search(rx, text(p)),
               "" if p.exists() else "archivo no producido")
    if spec.get("c2"):
        body = "\n".join(text(p) for p in sorted(d.glob("*.md")))
        missing, defined = c2(body)
        record("DRYRUN", f"{case} C2 sobre artefactos producidos", bool(defined) and not missing,
               f"{len(defined)} IDs, inexistentes: {sorted(missing) or 'ninguno'}")
    if spec.get("provenance_no_inference"):
        # Un requisito material no puede tener como origen una inferencia del agente (03, provenance).
        bad = [f"{p.name}:{i}" for p in sorted(d.glob("*.md"))
               for i, line in enumerate(text(p).splitlines(), 1)
               if re.match(r"\s*(?:[-*]\s*)?(SOURCE|DERIVED_FROM)\s*:", line)
               and re.search(r"INFEREN|inferenc|HYPOTHES|hipótesis", line)]
        record("DRYRUN", f"{case} provenance sin inferencias del agente", not bad, str(bad or "ninguna"))
    if spec.get("ledger_no_unanswered_applied"):
        # Una entrada APPLIED no puede admitir que algo quedó sin responder (clarification-loop §3),
        # salvo una delegación explícita del owner sobre algo clasificado como no material.
        p = d / "CLARIFICATION_LEDGER.md"
        bad = []
        if p.exists():
            for block in re.split(r"\n(?=CLAR-\d{3}\s*$)", text(p), flags=re.M):
                head = block.strip().splitlines()[0] if block.strip() else ""
                answer = re.search(r"ANSWER:\s*(.*)", block)
                if not re.search(r"STATUS:\s*APPLIED", block) or not answer:
                    continue
                unanswered = re.search(r"(?i)no se respondi|sin respuesta|no respondid|no fue respondid", answer.group(1))
                delegated = (re.search(r"CLASSIFICATION:\s*NON_MATERIAL_ASSUMPTION", block)
                             and re.search(r"(?i)delegaci", answer.group(1)))
                if unanswered and not delegated:
                    bad.append(head)
        record("DRYRUN", f"{case} ledger sin APPLIED a medio responder", p.exists() and not bad, str(bad or "ninguna"))
    if spec.get("no_code"):
        code = [p.name for p in d.rglob("*") if p.suffix in CODE_EXT]
        record("DRYRUN", f"{case} sin código de producto (Línea 2 no ejecutada)", not code, str(code or "ninguno"))


def dryrun():
    for exp_path in sorted((HERE / "expected").glob("T*.json")):
        case = exp_path.stem
        exp = json.loads(text(exp_path))
        if "mechanical" in exp:
            missing, _ = c2(text(HERE / exp["mechanical"]["c2_fixture"]))
            record("DRYRUN", f"{case} C2 mecánico = {exp['mechanical']['expect']}", not missing, "")
        vpath = HERE / "dryrun" / f"{case}.json"
        if not vpath.exists():
            record("DRYRUN", f"{case} {exp['desc']}", None, "sin veredicto registrado")
            continue
        verdict = json.loads(text(vpath))
        results = [(op, path, *check(verdict, op, path, arg)) for op, path, arg in exp["assert"]]
        bad = [f"{op} {path}: {why}" for op, path, ok, why in results if not ok]
        record("DRYRUN", f"{case} {exp['desc']}", not bad, "; ".join(bad) or f"{len(results)} aserciones")
        if "files" in exp:
            files(case, exp["files"])


def main():
    structure()
    mechanical()
    dryrun()
    width = max(len(r[1]) for r in rows)
    for layer, case, res, detail in rows:
        print(f"{layer:<10} {res:<8} {case:<{width}}  {detail}")
    counts = {k: sum(1 for r in rows if r[2] == k) for k in ("PASS", "FAIL", "NOT_RUN")}
    print(f"\nTOTAL: {len(rows)}  PASS: {counts['PASS']}  FAIL: {counts['FAIL']}  NOT_RUN: {counts['NOT_RUN']}")
    sys.exit(1 if counts["FAIL"] else 2 if counts["NOT_RUN"] else 0)


if __name__ == "__main__":
    main()
