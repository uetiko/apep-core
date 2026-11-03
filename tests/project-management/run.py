#!/usr/bin/env python3
"""Validación determinista de `project-management` (work shaping + flow).

Dos capas, sin dependencias externas y sin llamar a ningún modelo:

  STRUCTURE  el contrato de la skill está presente: modelos, valores, fronteras e
             invariantes en SKILL.md y sus referencias; baseline Kanban preservado;
             catálogo de skills y agents sin cambios.
  DRYRUN     compara los veredictos registrados en `dryrun/PM##.json` (producidos por
             un agente que aplicó la skill sin ver `expected/`) con `expected/PM##.json`.
             Un veredicto ausente es NOT_RUN, nunca PASS.

Uso:  python3 -I .omp/tests/project-management/run.py
Exit: 0 todo PASS · 1 algún FAIL · 2 algún NOT_RUN sin FAIL.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OMP = HERE.parent.parent
PM = OMP / "skills" / "project-management"
REFS = PM / "references"

rows = []


def record(layer, case, ok, detail):
    rows.append((layer, case, "PASS" if ok is True else ("NOT_RUN" if ok is None else "FAIL"), detail))


def text(path):
    return path.read_text(encoding="utf-8")


# ── STRUCTURE ────────────────────────────────────────────────────────────────
def structure():
    skill = text(PM / "SKILL.md")
    req = {
        "SKILL.md": ["PROJECT MANAGEMENT MANAGES THE WORK", "PM MUST NOT INVENT PRODUCT SEMANTICS",
                     "SPECIFICATION MUST NOT BECOME A WORK TRACKER", "READY MEANS READY FOR THE NEXT CAPABILITY",
                     "Backlog → Ready → In Progress → Review → Done", "WIP máximo de dos",
                     "READY != EXECUTION_READY != AUTHORIZED_TO_EXECUTE", "No fija prioridad", "No acepta riesgo",
                     "No inventa Story Points", "la Control Tower decide", "No afirma persistencia",
                     "no es un orchestrator"],
        "work-item-shaping.md": ["FEATURE", "BUG", "TECHNICAL_CHANGE", "REFACTOR", "INVESTIGATION", "INCIDENT",
                                 "INFRASTRUCTURE", "SECURITY", "DOCUMENTATION", "PROCESS", "UNKNOWN",
                                 "WORK_ITEM_ASSESSMENT", "ACCEPTANCE_SURFACE", "SIZE_SIGNAL",
                                 "TOO_LARGE_TO_EXECUTE", "WORK_FORMALITY", "**sin comportamiento nuevo**",
                                 "**Comportamiento nuevo acotado**"],
        "routing-readiness.md": ["READY_FOR_NEXT_CAPABILITY", "ROUTING_RECOMMENDATION", "PARALLEL_CAPABILITIES",
                                 "BLOCKED_CAPABILITIES", "READY != AUTHORIZED_TO_EXECUTE",
                                 "Readiness hacia `implementation` y autorización son cosas distintas"],
        "dependency-model.md": ["BLOCKING_DEPENDENCY", "SEQUENCING_DEPENDENCY", "INFORMATION_DEPENDENCY",
                                "EXTERNAL_DEPENDENCY", "SHARED_RESOURCE", "CROSS_REPOSITORY_DEPENDENCY",
                                "DECISION_DEPENDENCY", "AUTHORIZATION_DEPENDENCY", "BLOCKING_SCOPE",
                                "BLOCKED_BY_DECISION", "BLOCKED_BY_CAPACITY", "WORK_GRAPH", "CONDITIONAL",
                                "No se inventan IDs externos"],
        "work-slicing.md": ["NO_SPLIT_NEEDED", "SPLIT_RECOMMENDED", "SPLIT_REQUIRED",
                            "CANNOT_SPLIT_WITHOUT_DECISION", "ENABLING_SLICE", "SLICE BY OBSERVABLE VALUE"],
        "risk-and-issue-management.md": ["WORK_RISK_PROFILE", "CHANGE_IMPACT", "REVERSIBILITY", "BLAST_RADIUS",
                                         "DEPENDENCY_RISK", "SECURITY_DATA_SENSITIVITY", "OPERATIONAL_RISK"],
        "work-item-flow.md": ["SUFFICIENT CLARITY FOR THE NEXT CAPABILITY", "AGING", "BLOCKED_TIME", "WIP_PRESSURE",
                              "REWORK", "RETURN_TO_SPECIFICATION", "RETURN_TO_IMPLEMENTATION", "NOT_AVAILABLE",
                              "## 4. Definition of Done"],
        "requirements-management.md": ["PM MANAGES THE REQUIREMENT AS PROJECT WORK", "REQUIREMENT STATUS != REQUIREMENT SEMANTICS",
                                       "CHANGE ANALYSIS != CHANGE AUTHORIZATION", "MANAGED_REQUIREMENT", "SPECIFICATION_REF",
                                       "Referenciar, no copiar", "no otra máquina de estados", "APPROVED_FOR_EXECUTION",
                                       "NEW_REQUIREMENT", "REQUIREMENT_CLARIFICATION", "REQUIREMENT_CHANGE", "SCOPE_CHANGE",
                                       "TECHNICAL_CHANGE", "DEFECT", "CORRECTIVE_ACTION", "CHANGE_IMPACT_ANALYSIS",
                                       "TRACEABILITY_GAP", "DECISION → ACTION → OWNER → WORK ITEM → DELIVERY STATE",
                                       "REQUIREMENTS_BASELINE"],
        "project-governance.md": ["PROJECT_GOVERNANCE_MODEL", "PROJECT_SPONSORSHIP", "PROJECT_OWNER", "DECISION_AUTHORITY",
                                  "DELIVERY_OWNERSHIP", "TECHNICAL_OWNERSHIP", "REQUIREMENT_STAKEHOLDERS",
                                  "ACCEPTANCE_AUTHORITY", "RISK_ACCEPTANCE_AUTHORITY",
                                  "IDENTIFIABLE ACCOUNTABILITY != ARTIFICIAL RACI", "OUTPUT → OUTCOME → BENEFIT → VALUE",
                                  "VALUE_HYPOTHESIS", "VALUE_EVIDENCE", "VALUE_STATUS", "PROJECT_SCOPE", "PRODUCT_SCOPE",
                                  "DELIVERY_SCOPE", "TASK_SCOPE", "SCOPE_DRIFT", "SCOPE_CREEP_SIGNAL",
                                  "APPLY THE MANAGEMENT CONCERN", "INFORMATION_VALUE > PROCESS_COST"],
        "planning-and-control.md": ["PLAN != CONTRACT", "ESTIMATE != COMMITMENT", "BASELINE != CURRENT_STATE != FORECAST",
                                    "DETAIL DECREASES AS UNCERTAINTY INCREASES", "NEAR_TERM", "MID_TERM", "LONG_TERM",
                                    "DESIRED_DATE", "FORECAST", "COMMITTED_DATE", "`EFFORT`", "`DURATION`",
                                    "`CALENDAR_TIME`", "`COST`", "`CONFIDENCE`", "ACTIVITY_METRIC", "FLOW_METRIC",
                                    "DELIVERY_METRIC", "QUALITY_METRIC", "OUTCOME_METRIC", "VALUE_METRIC", "LEAD_TIME",
                                    "DEVIATION", "ON_TRACK", "NO_BASELINE", "no exige sprints"],
        "software-project-management.md": ["SOFTWARE PROGRESS MUST BE EVIDENCE-BASED", "PROGRESS_EVIDENCE: INSUFFICIENT",
                                           "REQUIREMENT_UNCERTAINTY", "DOMAIN_UNCERTAINTY", "TECHNICAL_UNCERTAINTY",
                                           "ESTIMATION_UNCERTAINTY", "DEPENDENCY_UNCERTAINTY", "OPERATIONAL_UNCERTAINTY",
                                           "SKILL_NEEDS", "BUS_FACTOR", "CONTEXT_SWITCHING", "PRODUCT_EVOLUTION",
                                           "no es Product Owner"],
        "project-closure.md": ["NOT_READY_FOR_CLOSURE"],
    }
    for name, needles in req.items():
        path = PM / name if name == "SKILL.md" else REFS / name
        body = text(path) if path.exists() else ""
        missing = [n for n in needles if n not in body]
        record("STRUCTURE", f"{name}", bool(body) and not missing, "ok" if not missing else f"falta {missing}")
        if name != "SKILL.md":
            record("STRUCTURE", f"SKILL.md → {name}", name in skill, "referenciada desde SKILL.md")

    record("STRUCTURE", "PM no figura como capa de la cadena de autoridad",
           "PROJECT MANAGEMENT METHOD" not in skill and "que este análisis produce" not in skill
           and "no es una capa de esa cadena" in skill and "HUMAN DECISIONS / TASK AUTHORITY" in skill, "SKILL.md §1")
    record("STRUCTURE", "estado USABLE / FIELD_VALIDATION y política de evolución",
           "PROJECT_MANAGEMENT_STATUS: USABLE" in skill and "NO MORE PROJECT-MANAGEMENT FEATURES BY IDEA ALONE" in skill,
           "SKILL.md §16")

    heads = set(re.findall(r"^## (\d+)\.", skill, re.M))
    bad = [f"{r.name}:{n}" for r in sorted(REFS.glob("*.md"))
           for n in re.findall(r"SKILL\.md`? §(\d+)", text(r)) if n not in heads]
    record("STRUCTURE", "citas SKILL.md §N desde las referencias existen", not bad, str(bad or "todas existen"))

    # 0.7.0: requirements management, gobernanza de proyecto, planificación y control.
    for needle in ["PM MANAGES THE REQUIREMENT AS PROJECT WORK", "REQUIREMENTS MANAGEMENT != REQUIREMENTS ENGINEERING",
                   "IMPLEMENTED != VERIFIED != DELIVERED != DEPLOYED != OPERATIONALLY_ACCEPTED != PROJECT_SUCCESS != VALUE_REALIZED",
                   "No aprueba alcance ni cambios materiales", "No declara válido un requisito",
                   "no implementa PMBOK ni afirma conformidad", "APPLY THE MANAGEMENT CONCERN"]:
        record("STRUCTURE", f"SKILL.md: {needle[:60]}", needle in skill, "")
    risk = text(REFS / "risk-and-issue-management.md")
    cats = ["PROJECT_RISK", "TECHNICAL_RISK", "DELIVERY_RISK", "REQUIREMENTS_RISK", "SECURITY_RISK", "ORGANIZATIONAL_RISK",
            "SCHEDULE_RISK", "RESOURCE_RISK", "RESPONSE_PROPOSED", "MATERIALIZED", "HUMAN AUTHORITY ACCEPTS THE RISK"]
    miss = [c for c in cats if c not in risk]
    record("STRUCTURE", "riesgo de proyecto: categorías, estados y reparto", not miss, f"falta {miss}" if miss else "ok")
    record("STRUCTURE", "el orden de riesgos no es prioridad de trabajo (sin 'Prioriza por')",
           "Prioriza por" not in risk and "no una prioridad de trabajo" in risk, "risk-and-issue-management.md")

    # Estado del requisito: mapeo sobre estados existentes, no una máquina paralela (DUPLICATE_STATE).
    rm = text(REFS / "requirements-management.md")
    dl = text(OMP / "skills" / "delivery-lifecycle" / "SKILL.md")
    spec = text(OMP / "skills" / "specification" / "SKILL.md")
    dl_states = set(re.findall(r"^\| `([A-Z_]+)` \|", dl, re.M))
    sec3 = rm.split("## 3.")[1].split("## 4.")[0]
    cited = set(re.findall(r"`([A-Z][A-Z_]+)`", sec3.split("| Owner del estado de origen |")[1].split("Reglas:")[0]))
    req_status = {"IDENTIFIED", "UNDER_ANALYSIS", "SPECIFICATION_REQUIRED", "SPECIFIED", "APPROVED_FOR_EXECUTION",
                  "IN_IMPLEMENTATION", "VERIFIED", "DELIVERED", "ACCEPTED", "CHANGED", "SUPERSEDED", "CANCELLED"}
    known = dl_states | {"EXECUTION_READY", "NONE", "LIGHT", "FORMAL", "ACCEPTANCE_OWNER"} | req_status
    unknown = sorted(cited - known)
    record("STRUCTURE", "estado del requisito: los estados de origen existen en delivery-lifecycle/specification",
           not unknown and "EXECUTION_READY" in spec, f"desconocidos {unknown}" if unknown else f"{len(cited)} estados")

    # Presentación (0.8.1): plantillas de reporte, comandos finos, decisiones con semántica canónica.
    wr = text(REFS / "work-item-shaping-report.md")
    pr = text(REFS / "project-management-report.md")
    pres_need = {
        "work-item-shaping-report.md": (wr, ["THE METHOD DETERMINES WHAT IS TRUE", "THE TEMPLATE DETERMINES HOW IT IS COMMUNICATED",
            "ONE ANALYSIS. MULTIPLE READERS.", "EMPTY TEMPLATE SLOT != PERMISSION TO INVENT", "UNKNOWN REMAINS UNKNOWN",
            "RECOMMENDATION REMAINS RECOMMENDATION", "DECISION REMAINS HUMAN", "SMALL INFORMATION NEED → SMALL REPORT",
            "## Resumen", "## Registro de proceso", "(siempre)", "(si aplica)", "**No son criterios de aceptación**",
            "Sin vocabulario interno", "No redefine el alcance", "el reporte humano nunca la sustituye"]),
        "project-management-report.md": (pr, ["no como un dashboard", "APPLY THE MANAGEMENT CONCERN",
            "**Nunca un porcentaje de avance inventado.**", "**deseada**", "**forecast**", "**comprometida**",
            "No es reporting periódico", "## Registro de proceso", "work-item-shaping-report.md"]),
    }
    for name, (body, needles) in pres_need.items():
        miss = [n for n in needles if n not in body]
        record("STRUCTURE", f"presentación: {name}", bool(body) and not miss, f"falta {miss}" if miss else "ok")
    canon = ["`DECISION`", "`FACTS`", "`OPTIONS`", "`TRADEOFFS`", "`CONSEQUENCES`", "`RECOMMENDATION`", "`BLOCKING_SCOPE`"]
    record("STRUCTURE", "PM-PRES-19 decisiones: reutilizan DECISION_REQUIRED canónico (sin semántica nueva)",
           all(c in wr for c in canon) and "ENGINEERING_GOVERNANCE.md` §1.4" in wr and "DECISION_BRIEF" not in wr + pr
           and not (REFS / "decision-brief.md").exists(), "governance §1.4")
    for cmd, ref in (("shape", "work-item-shaping-report.md"), ("project", "project-management-report.md")):
        body = text(OMP / "commands" / f"{cmd}.md")
        thin = ref in body and not re.search(r"^## ", body, re.M) and "Registro de proceso" not in body.split(ref)[0][-400:] \
            and not any(h in body for h in ("## Resumen", "## Estado ejecutivo", "| Para gestión |"))
        record("STRUCTURE", f"PM-PRES-{14 if cmd == 'shape' else 15} /{cmd} fino: remite a la plantilla sin copiarla", thin, ref)
    record("STRUCTURE", "SKILL.md remite a ambas plantillas de presentación",
           "references/work-item-shaping-report.md" in skill and "references/project-management-report.md" in skill, "§6, §12, §13")

    # Coherencia de readiness y ruta (0.8.2, OBSERVED_FAILURE-PM-002).
    rr = text(REFS / "routing-readiness.md")
    need = ["IF A MUST FINISH BEFORE B CAN START, THEN B IS NOT THE IMMEDIATE NEXT CAPABILITY",
            "READY FOR B MEANS B CAN ACTUALLY START NOW", "PREREQUISITE != PARALLEL_SUPPORT", "NEXT_CAPABILITY != EVENTUAL_CAPABILITY",
            "THEN:", "BLOCKING_SCOPE:", "| `PREREQUISITES` |", "| `THEN` |", "Un prerequisito **insatisfecho**",
            "DO NOT ASK THE HUMAN WHAT THE SYSTEM CAN TELL US", "UNKNOWN FACTUAL != DECISION_REQUIRED",
            "no elegir a qué superficie de producto material"]
    miss = [n for n in need if n not in rr]
    record("STRUCTURE", "routing-readiness: NEXT = lo que puede empezar ahora; prerequisitos, THEN, paralelas y ownership",
           not miss, f"falta {miss}" if miss else "ok")
    record("STRUCTURE", "regresión del método: el ejemplo canónico no pone un prerequisito insatisfecho bajo NEXT",
           "PREREQUISITES:          technical-discovery:" not in rr, "routing-readiness.md §3")
    dm = text(REFS / "dependency-model.md")
    record("STRUCTURE", "dependency-model: referencia desconocida = INFORMATION_DEPENDENCY UNKNOWN, no decisión",
           "es una `INFORMATION_DEPENDENCY` con `STATUS: UNKNOWN`" in dm, "dependency-model.md §1")
    record("STRUCTURE", "presentación: el resumen no contradice la ruta",
           "**El resumen no contradice la ruta.**" in text(REFS / "work-item-shaping-report.md"), "work-item-shaping-report.md §3")

    # Fronteras y handoffs con otras skills.
    record("STRUCTURE", "specification: frontera con requirements management y PROJECT_DECISION_REQUIRED",
           "requirements-management.md" in spec and "PROJECT_DECISION_REQUIRED" in spec, "specification §11")
    record("STRUCTURE", "delivery-lifecycle: NONE = sin comportamiento nuevo (misma escala que PM)",
           "Micro cambio local, reversible y verificable, sin comportamiento nuevo" in dl, "delivery-lifecycle §4")
    flow = text(REFS / "work-item-flow.md")
    record("STRUCTURE", "READINESS_CHECK de flujo extiende el de routing (REASON)",
           "REASON:" in flow.split("## 7.")[1] and "no es un segundo esquema" in flow, "work-item-flow.md §7")
    manual = text(OMP / "MANUAL.md")
    record("STRUCTURE", "MANUAL: el readiness hacia implementation no incluye la autorización",
           "decisiones materiales cerradas y autorización" not in manual, "routing-readiness.md §2")
    spm = text(REFS / "software-project-management.md")
    for name in ["architecture-review", "security-review", "implementation-review", "code-quality"]:
        record("STRUCTURE", f"calidad de proyecto: {name} sigue siendo owner de su análisis",
               f"`{name}`" in spm.split("## 4.")[1].split("## 5.")[0], "software-project-management.md §4")

    dl = text(OMP / "skills" / "delivery-lifecycle" / "SKILL.md")
    record("STRUCTURE", "delivery-lifecycle consume la clasificación de PM",
           "La clasificación **la produce `project-management`**" in dl and "WORK_ITEM_CLASSIFICATION" in dl, "")
    record("STRUCTURE", "delivery-lifecycle sin WORK_TYPE paralelo", "| `WORK_TYPE` |" not in dl, "")
    gw = text(OMP / "skills" / "git-workflow" / "references" / "pull-request.md")
    record("STRUCTURE", "git-workflow sigue citando la DoD en work-item-flow §4",
           "work-item-flow.md` §4" in gw, "referencia externa preservada")

    skills = sorted(p.name for p in (OMP / "skills").iterdir() if (p / "SKILL.md").exists())
    record("STRUCTURE", "catálogo de skills", len(skills) == 11, f"{len(skills)} skills")
    agents = sorted(p.stem for p in (OMP / "agents").glob("*.md"))
    record("STRUCTURE", "catálogo de agents (sin agent PM)", len(agents) == 6 and "project-management" not in agents,
           f"{len(agents)} agents")


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
    if op == "routing_coherent":
        return routing_coherent(v)
    if op == "item":
        it = [i for i in v.get("items", []) if i.get("id") == path]
        return bool(it) and it[0].get("next_capability") == arg, f"{path}→{it[0].get('next_capability') if it else '—'}"
    raise ValueError(op)


def routing_coherent(v):
    """routing-readiness.md §3: readiness y ruta describen una sola realidad."""
    r, rd = v.get("routing") or {}, v.get("readiness") or {}
    nxt, ready = r.get("next_capability"), rd.get("ready_for_next_capability")
    if not nxt or nxt == "NOT_EVALUATED":
        return True, "sin ruta evaluada"
    bad = []
    for pre in r.get("prerequisites") or []:
        if isinstance(pre, dict):
            unsatisfied = pre.get("status") != "SATISFIED"
            txt = " ".join(str(x) for x in pre.values())
        else:  # forma anterior: texto libre sin estado
            unsatisfied, txt = True, str(pre)
        if re.search(r"(?i)autoriz", txt):
            bad.append(f"autorización como prerequisito: {txt[:60]}")
        elif unsatisfied and ready == "YES":
            bad.append(f"prerequisito insatisfecho con NEXT listo: {txt[:60]}")
    blocked = " ".join(str(x) for x in r.get("blocked_capabilities") or [])
    partial = rd.get("ready") == "PARTIAL" and str(r.get("blocking_scope") or "").strip() not in ("", "NONE")
    if re.search(rf"(?<![\w-]){re.escape(nxt)}(?![\w-])", blocked) and not partial:
        bad.append(f"NEXT ({nxt}) figura como bloqueada sin bloqueo parcial declarado")
    if r.get("then") not in (None, "", "NONE") and r.get("then") == nxt:
        bad.append("THEN = NEXT")
    if rd.get("ready") == "PARTIAL" and not str(r.get("blocking_scope") or "").strip("NONE ").strip() \
            and not (v.get("blockers") or []):
        bad.append("READY PARTIAL sin BLOCKING_SCOPE ni blockers")
    return not bad, "; ".join(bad) or f"coherente (NEXT {nxt}, ready {ready})"


def dryrun():
    for exp_path in sorted((HERE / "expected").glob("PM*.json")):
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
        ok, why = routing_coherent(verdict)  # invariante global (routing-readiness.md §3)
        if not ok:
            bad.append(f"routing_coherent: {why}")
        record("DRYRUN", f"{case} {exp['desc']}", not bad, "; ".join(bad) or f"{len(exp['assert'])} aserciones")


# ── PRESENTATION ─────────────────────────────────────────────────────────────
# Contrato de presentación (work-item-shaping-report.md, project-management-report.md). Cada caso
# reutiliza un fixture existente: el agente produce el reporte (`<id>.md`) y el veredicto canónico
# (`<id>.json`). El veredicto debe seguir cumpliendo la expectativa del fixture (la presentación no
# cambia el método, PM-PRES-13) y el reporte se contrasta con él (una sola verdad, tres vistas).
PRES = HERE / "presentation"
INTERNAL = re.compile(r"\b(WORK_ITEM_[A-Z_]+|READINESS_CHECK|ROUTING_RECOMMENDATION|WORK_RISK_PROFILE|SIZE_SIGNAL|"
                      r"WORK_FORMALITY|DECISION_REQUIRED|NEXT_CAPABILITY|DEP-\d+|CHANGE_IMPACT_ANALYSIS|DEVIATION)\b"
                      r"|`(technical-discovery|specification|diagnostics|architecture-review|security-review|implementation|"
                      r"project-management|delivery-lifecycle|delivery-orchestrator)`|\bagent\b")
PLAIN_NEXT = {"specification": r"(?i)defin", "technical-discovery": r"(?i)investig|cómo funciona", "diagnostics": r"(?i)causa",
              "architecture-review": r"(?i)diseño|fronteras|arquitect", "security-review": r"(?i)seguridad",
              "implementation": r"(?i)constru|implement", "NONE": r"(?i)decisi"}
UNKNOWN_MARK = re.compile(r"(?i)todavía no|aún no|no sabemos|no se sabe|desconoc|\bUNKNOWN\b|sin definir|por definir|no está definid|no consta|abiert")


def sections(md):
    """[(título, cuerpo)] de los encabezados `## `."""
    parts = re.split(r"^## +(.+)$", md, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def pres_check(md, verdict, op, arg=None):
    secs = sections(md)
    titles = [t for t, _ in secs]
    summary = secs[0][1] if secs else ""
    process = next((b for t, b in secs if re.search(r"(?i)registro de proceso|process record", t)), "")
    if op == "summary_first":
        return bool(titles) and bool(re.search(r"(?i)resumen|estado ejecutivo|management summary|executive", titles[0])), f"primera sección: {titles[:1]}"
    if op == "summary_plain":
        hits = sorted({m.group(0) for m in INTERNAL.finditer(summary)})
        return bool(summary.strip()) and not hits, f"vocabulario interno en el resumen: {hits or 'ninguno'}"
    if op == "process_last":
        return bool(titles) and bool(re.search(r"(?i)registro de proceso|process record", titles[-1])), f"última sección: {titles[-1:]}"
    if op == "max_sections":
        return len(secs) <= arg, f"{len(secs)} secciones (máx. {arg})"
    if op == "min_sections":
        return len(secs) >= arg, f"{len(secs)} secciones (mín. {arg})"
    if op == "process_has":
        miss = [x for x in arg if x not in process]
        return bool(process) and not miss, f"registro sin {miss}" if miss else "ok"
    nxt = ((verdict.get("routing") or {}).get("next_capability")) or ((verdict.get("readiness") or {}).get("next_capability"))
    if op == "summary_no_wait":
        r = verdict.get("readiness") or {}
        rx = PLAIN_NEXT.get(nxt)
        if r.get("ready_for_next_capability") != "YES" or not rx:
            return True, "sin siguiente paso listo que contrastar"
        wait = re.compile(r"(?i)(no (lanzar|iniciar|empezar|arrancar|comenzar|abrir)|todavía no (lanzar|iniciar|empezar|arrancar|comenzar|se puede)|antes de (lanzar|iniciar|empezar|arrancar|comenzar)|esperar (a|antes))[^.]{0,60}")
        hits = [m.group(0) for m in wait.finditer(summary) if re.search(rx, m.group(0))]
        return not hits, f"el resumen pide esperar al siguiente paso listo: {hits or 'no'}"
    if op == "process_next_matches_verdict":
        return bool(nxt) and nxt in process, f"next_capability del veredicto: {nxt}"
    if op == "summary_next_plain":
        rx = PLAIN_NEXT.get(nxt)
        return bool(rx) and bool(re.search(rx, summary)), f"siguiente paso {nxt} dicho en lenguaje corriente"
    if op == "unknown_marked":
        r = verdict.get("readiness") or {}
        needs = bool(r.get("open") or r.get("missing"))
        return (not needs) or bool(UNKNOWN_MARK.search(md)), "aperturas presentadas como desconocidas"
    if op == "no_ac_ids":
        return not re.search(r"\bAC-\d{3}\b", md), "sin AC-NNN inventados"
    if op == "evidence_labels":
        eng = "\n".join(b for t, b in secs if re.search(r"(?i)ingenier|evidencia|engineering", t))
        return bool(eng) and bool(re.search(r"(?i)\bhecho|\bFACT", eng)) and bool(re.search(r"(?i)inferen", eng)), "hechos e inferencias etiquetados"
    if op == "decision_not_closed":
        # Cerrar la decisión pendiente en el texto; "lo que ya está decidido" (hechos del caso) no lo es.
        bad = re.search(r"(?i)\b(se decidió|hemos decidido|queda decidido|decidimos|se aprobó|queda aprobado|la decisión fue)\b", md)
        return not bad and bool(re.search(r"(?i)recomend", md)), f"decisión cerrada en el texto: {bad.group(0) if bad else 'no'}"
    if op == "percent_quoted":
        # Un porcentaje afirmado como estado del proyecto, sin atribuirlo a quien lo dijo.
        state = re.compile(r"(?i)(avance|progreso|completad|terminad|está|estamos|va |vamos|llevamos)\D{0,25}\d+\s*%")
        bad = [ln.strip()[:80] for ln in md.splitlines() if state.search(ln)
               and not re.search(r"(?i)report|declar|afirm|según|dice|indica|cita|\"|«|no es|no son|sin estados", ln)]
        return not bad, f"porcentajes presentados como estado: {bad or 'ninguno'}"
    if op == "dates_distinct":
        return bool(re.search(r"(?i)comprometid", md)) and bool(re.search(r"(?i)forecast|previs|pronóst|estimad", md)), "comprometida y forecast distinguidas"
    if op == "value_not_realized":
        ok = re.search(r"(?i)no (se )?(ha |han )?(sido )?medid|sin medir|sin evidencia|no hay evidencia|EVIDENCE_PENDING|OUT_OF_HORIZON|NOT_DEFINED|pendiente de (evidencia|medi)|nadie (lo )?está midiendo|nadie mide", md)
        bad = [ln.strip()[:80] for ln in md.splitlines() if re.search(r"(?i)(valor|beneficio)\s+(realizado|obtenido|logrado|alcanzado)", ln)
               and not re.search(r"(?i)\bno\b|sin |pendiente|todavía|aún|VALUE_REALIZED", ln)]
        return bool(ok) and not bad, f"valor dado por obtenido: {bad or 'no'}"
    raise ValueError(op)


def presentation():
    spec = PRES / "cases.json"
    if not spec.exists():
        return
    for case in json.loads(text(spec)):
        cid, label = case["id"], f"{case['id']} {case['desc']}"
        md_p, js_p = PRES / "dryrun" / f"{cid}.md", PRES / "dryrun" / f"{cid}.json"
        if not (md_p.exists() and js_p.exists()):
            record("PRESENTATION", label, None, "sin reporte o veredicto registrado")
            continue
        md, verdict = text(md_p), json.loads(text(js_p))
        bad = []
        exp = json.loads(text(HERE / "expected" / f"{case['fixture']}.json"))
        for op, path, arg in exp["assert"]:
            ok, why = check(verdict, op, path, arg)
            if not ok:
                bad.append(f"[{case['fixture']}] {op} {path}: {why}")
        ok, why = routing_coherent(verdict)
        if not ok:
            bad.append(f"routing_coherent: {why}")
        for c in case["checks"]:
            ok, why = pres_check(md, verdict, c[0], c[1] if len(c) > 1 else None)
            if not ok:
                bad.append(f"{c[0]}: {why}")
        record("PRESENTATION", label, not bad, "; ".join(bad) or f"{' · '.join(case['pres'])}")


def main():
    structure()
    dryrun()
    presentation()
    width = max(len(r[1]) for r in rows)
    for layer, case, res, detail in rows:
        print(f"{layer:<10} {res:<8} {case:<{width}}  {detail}")
    counts = {k: sum(1 for r in rows if r[2] == k) for k in ("PASS", "FAIL", "NOT_RUN")}
    print(f"\nTOTAL: {len(rows)}  PASS: {counts['PASS']}  FAIL: {counts['FAIL']}  NOT_RUN: {counts['NOT_RUN']}")
    sys.exit(1 if counts["FAIL"] else 2 if counts["NOT_RUN"] else 0)


if __name__ == "__main__":
    main()
