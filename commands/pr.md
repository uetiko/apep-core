---
description: PR LIFECYCLE MODE — conduce el ciclo de vida canónico de Pull Requests / merge requests (pr-review) desde la Main Session
---

# /pr — PR LIFECYCLE MODE

Entrada:

$ARGUMENTS

Eres la **Main Session**, la Control Tower de este ciclo. `/pr` es un punto de entrada: no es una skill, ni un agent, ni una fuente de autoridad. La metodología es `skill://pr-review`: léela y aplica su ciclo de vida canónico (`pr-review` §19) a la entrada de arriba. Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Este command invoca `pr-review` para la metodología genérica de revisión y lifecycle de PRs; la mecánica concreta contra un remote (CodeCommit, GitHub u otro) es una capability que el provider configurado por la composición debe aportar — ver la documentación de ese provider.

1. **Conjunto.** Interpreta la entrada — un PR, varios, repositorio + PR o un lote acotado — y fija `CYCLE_ID`, `AUTHORIZED_SET` y `AUTHORIZED_ACTIONS` como indican `pr-review` §11.9 y §19.2. Si la entrada no permite enumerar el conjunto de forma determinista, o las acciones son ambiguas, aplica STOP-1 (`pr-review` §17): revisa lo inequívoco y pide sólo la precisión que falta. Sin entrada, pregunta qué PRs; listar los abiertos es lectura y puede ayudar a delimitarlos.
2. **Ciclo por PR.** Fases, estados, findings, outcomes, routing, merge y paradas son los de `pr-review` §19; no hay otros. Cada PR se carga, revisa y decide por separado, y un blocker local no detiene el resto (`pr-review` §19.6).
3. **Capabilities de apoyo**, sólo cuando reducen incertidumbre, protegen una frontera o aportan evidencia necesaria (`pr-review` §7): `implementation-review` para correctness a fondo; `security-review` y `architecture-review` por derivación, sin veredicto especializado propio; `governance-review` (agent) si hay que interpretar alcance o autoridad; `git-workflow` para convenciones de ramas y PRs; y el agent `implementation` sólo para una reconciliación mecánica autorizada que el provider configurado defina, nunca para decidir cómo resolver un finding.
4. **Ejecución.** Todo el ciclo corre en esta sesión. No lo delegues en `delivery-orchestrator` ni en otro subagent: las mutaciones remotas conservan el contexto de autorización de la Main Session (`pr-review` §11.8).

Invariantes que este command no relaja:

```
AUTHORIZED_SET IS CLOSED.          AUTHORIZED_ACTIONS ARE CLOSED.
AUTONOMY != AUTHORITY              TOOL APPROVAL != TASK AUTHORITY
AUTHORIZED != ELIGIBLE             EXECUTION CLAIM != REMOTE EVIDENCE
```

- Que la configuración de aprobación del proyecto no pida confirmación para un comando no lo autoriza (`pr-review` §11).
- Tras cada mutación remota, relee el estado real (`VERIFY_REMOTE`, `pr-review` §19.7); un exit 0 no es evidencia.
- Antes de cada efecto repetible, aplica la idempotencia y el ledger existentes (`pr-review` §19.8); `/pr` no tiene estado ni ledger propios.
- Ante una decisión material, un conflicto funcional, drift o evidencia insuficiente, emite para ese PR el artefacto canónico: `DECISION_REQUIRED`, `DECISION_CONTRADICTION` o `STOP_REPORT`.

Salida: el contrato de `pr-review` §16 — siempre `PR_REVIEW_REPORT`, y `BATCH_RESULT` cuando hay más de un PR.
