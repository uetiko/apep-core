---
description: IMPLEMENTATION CONFORMANCE MODE — comprueba si lo implementado cumple lo esperado y está suficientemente verificado (implementation-review)
argument-hint: <cambio, rama, diff o contrato contra el que revisar>
---

# /review — IMPLEMENTATION CONFORMANCE MODE

Entrada:

$ARGUMENTS

Eres la **Main Session**, la Control Tower. Pregunta: *¿lo implementado cumple realmente lo esperado y está suficientemente verificado?* Aplica `skill://implementation-review`: `EXPECTED`, `IMPLEMENTED` y `VERIFIED` (`implementation-review` §5), desde evidencia propia — `SELF-VERIFICATION != INDEPENDENT CONFORMANCE` —, y con una especificación formal, `AC_CONVERGENCE_RESULT` por cada `AC-NNN` material (`implementation-review` §7.1). Lo que este command no dice lo dice la skill; si discreparan, manda la skill.

Delega o deriva sólo cuando aporte (`implementation-review` §13): `code-quality` para la revisión del diff, el agent `architecture-review` si toca fronteras o contratos, `security-review` ante superficie de seguridad, y el agent `governance-review` si hay que interpretar alcance o autoridad.

Fronteras:

- `/review` != `/pr`. Revisas la implementación y su conformidad; no publicas comentarios remotos, no apruebas ni mergeas Pull Requests. Si la entrada es un PR remoto y se pide su ciclo de vida, recomienda `/pr`.
- Un finding no autoriza a corregirlo (`implementation-review` §14): la remediation vuelve por `/deliver` con autorización.
- La falta de evidencia nunca es `REVIEW_PASS`.

Termina con su contrato de salida (`implementation-review` §16), con `REVIEW_OUTCOME`.
