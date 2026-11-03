---
name: security-review
description: Evalúa si un cambio concreto introduce un riesgo de seguridad material, alcanzable y respaldado por evidencia — identificando superficies de seguridad tocadas, la propiedad en riesgo, el path de violación, sus precondiciones, su reachability, la evidencia y el impacto. Úsalo cuando exista un diff, PR, commit/rango, archivos modificados o cambio de configuración/infraestructura que revisar con lente de seguridad, o mediante invocación explícita (`/skill:security-review`). Read-only: nunca parchea, rota secretos, cambia IAM/config/red, actualiza dependencias ni ejecuta exploits o payloads. No es pentesting, ni auditoría exhaustiva, ni threat modeling del producto, ni hardening genérico. No sustituye `implementation-review` (correctness), `pr-review` (readiness del PR), `architecture-review` (boundaries), `governance-review` (autoridad/alcance) ni `diagnostics` (causa de un incidente real). No convierte posibilidades teóricas en vulnerabilidades.
---

# Security Review

Este skill evalúa **un cambio concreto** con lente de seguridad. Su producto es evidencia de riesgo, no una lista de miedos. Existe para **reducir riesgo real**, no para maximizar la cantidad de findings.

## 0. Cuándo NO usar este skill

No lo actives para: entender cómo funciona un sistema (`technical-discovery`), determinar la causa de un incidente real (`diagnostics`), verificar si la implementación funciona (`implementation-review`), evaluar la calidad/readiness de un PR (`pr-review`), evaluar boundaries arquitectónicos (`architecture-review`), o decidir si un cambio estaba autorizado (`governance-review`).

Tampoco es pentesting, auditoría general del sistema, threat modeling completo del producto, ni una campaña de hardening.

Actívalo cuando exista un cambio concreto revisable — diff, Pull Request, commit/rango, archivos modificados, resultado de implementación, o configuración/infraestructura modificada — y la pregunta sea de seguridad.

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE       (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE  (p. ej. <repo>/AGENTS.md o <repo>/IA.md — cuando el repositorio lo tenga)
    → SECURITY REVIEW      (este skill)
      → consumidor         (decisión humana / specification / implementation)
```

No es gobernanza independiente ni tiene autoridad de decisión propia. Es executor-neutral: su resultado es evidencia consumible — nunca invoca automáticamente una corrección.

## 2. Pregunta gobernante

`¿El cambio introduce un riesgo de seguridad material, demostrable y relevante que deba atenderse antes de continuar?`

## 3. Invariantes

`POSSIBLE_ATTACK != VULNERABILITY` · `SECURITY_SMELL != EXPLOITABLE_RISK` · `MISSING_HARDENING != SECURITY_DEFECT` · `THEORETICAL_PATH != REACHABLE_PATH` · `UNPROVEN_PRECONDITION != FACT` · `BROAD_PERMISSION != EXPLOITABLE_RISK` · `SECURITY_FINDING != AUTHORIZATION_TO_FIX` · `SECURITY_REVIEW != REMEDIATION`.

Cuatro reglas rectoras:

> **`EVIDENCE BEFORE CLAIM`** — no afirmes lo que puedes comprobar.
>
> **`REACHABILITY BEFORE SEVERITY`** — determina si el path es alcanzable *antes* de asignar gravedad.
>
> **`PROVE RISK, DON'T IMAGINE IT`** — un patrón sospechoso no es un riesgo hasta que se demuestra el camino.
>
> **`CONTINUITY OVER SECURITY THEATER`** — reducir riesgo real, no bloquear por posibilidades abstractas.

Fronteras adicionales: un finding de seguridad **puede existir aunque el código sea funcionalmente correcto**, y un finding funcional **no es automáticamente** un finding de seguridad. **La severidad nunca supera la evidencia disponible.** No encontrar nada es un resultado válido.

## 4. Alcance

Se revisa **el cambio y su impacto razonablemente relacionado**, no el sistema entero. Leer un archivo completo, seguir una llamada o inspeccionar un control adyacente es legítimo cuando hace falta para establecer reachability; barrer subsistemas no relacionados no lo es (`.omp/RULES.md` regla 5).

No fabriques un threat model completo del producto cuando el diff no lo exige.

## 5. Modelo de revisión

```
SECURITY_SURFACES → SECURITY_PROPERTY → THREAT_HYPOTHESIS → PRECONDITIONS
  → REACHABILITY → EVIDENCE → IMPACT → FINDING
```

Cada eslabón puede cortar la cadena. Una hipótesis cuyas precondiciones se rechazan, o cuyo path no es alcanzable, **no se convierte en finding** — se descarta (§9, `REJECTED_SECURITY_HYPOTHESIS`).

### 5.1 Superficies de seguridad

Primero identifica qué superficies toca **realmente** el cambio. Revisa sólo las materialmente relacionadas; recorrer la lista entera es ceremonia, no revisión.

Autenticación · autorización · aislamiento entre tenants · identidad/claims · permisos/IAM · secretos · datos sensibles · validación de entrada · codificación de salida · inyección (SQL/comando/plantilla) · SSRF · acceso a filesystem · path traversal · URLs/endpoints externos · deserialización · ejecución de comandos · subprocesos · evaluación dinámica · logging · divulgación por errores · configuración · exposición de red · cambios de dependencias · uso criptográfico · almacenamiento y transmisión de información sensible.

Detalle por superficie: `skill://security-review/references/security-surfaces.md`.

### 5.2 Propiedad de seguridad

Todo finding identifica **qué propiedad debería preservarse**: integridad de la identidad autenticada · autorización · aislamiento entre tenants · confidencialidad · integridad · frontera de privilegio · confidencialidad de un secreto · frontera de ejecución de comandos · frontera de filesystem · frontera de confianza de red.

*"Esto parece inseguro"* no es una propiedad de seguridad y no sostiene un finding.

### 5.3 Threat hypothesis

Cuando exista incertidumbre, formula explícitamente `THREAT_HYPOTHESIS`: *¿cómo podría este cambio violar la propiedad identificada?*

**Una hipótesis no es todavía un finding.** Debe verificarse.

### 5.4 Precondiciones

Toda hipótesis material declara qué debe ser cierto para que funcione — por ejemplo: el atacante está autenticado · el atacante controla el parámetro X · el endpoint es alcanzable externamente · el permiso IAM Y existe · el servicio sigue redirecciones · el usuario controla una ruta de filesystem · el identificador de tenant se acepta desde la petición · el secreto está realmente activo · la ruta vulnerable de la dependencia se ejecuta.

Cada precondición se clasifica: `CONFIRMED` · `SUPPORTED` · `UNCONFIRMED` · `REJECTED`.

**`UNPROVEN_PRECONDITION != FACT`.** No las asumas en silencio: una precondición no verificada es `UNCONFIRMED`, y eso limita el estado y la severidad del finding.

### 5.5 Reachability

Distingue siempre:

| | |
|---|---|
| `CODE_PATTERN_PRESENT` | El patrón existe en el código |
| `SECURITY_PATH_REACHABLE` | El path puede alcanzarse de verdad |

Una función que ejecuta comandos **no es** command injection por existir. Hay que demostrar: entrada controlable por el atacante · propagación hasta el sink · ausencia o insuficiencia del control · ejecución alcanzable.

Método completo: `skill://security-review/references/reachability-and-preconditions.md`.

### 5.6 Evidencia e impacto

**`EVIDENCE BEFORE CLAIM`.** Prefiere tooling determinista cuando exista: Git · búsqueda de código y LSP · tooling de dependencias y lockfiles · inspección de schema/config · tests existentes · inspección de policies/IAM · definiciones de infraestructura · evidencia de runtime/configuración cuando esté disponible y autorizada.

No infieras un permiso existente, un endpoint público, una dependencia vulnerable, un secreto activo, una ruta alcanzable o un bypass de tenant **cuando puedan comprobarse razonablemente**.

`IMPACT` describe qué quedaría comprometido — qué datos, qué privilegio, qué frontera, qué radio de alcance — en términos materiales, no adjetivos.

## 6. Estándar de finding

Todo finding incluye:

`OBSERVED` (qué hace realmente el cambio/código/configuración) · `SECURITY_PROPERTY` · `ATTACK_OR_FAILURE_PATH` · `PRECONDITIONS` (con su clasificación) · `REACHABILITY` · `EVIDENCE` · `IMPACT`.

Y cuando aplique: `AFFECTED_BOUNDARY` · `LOCATION` · `REPRODUCTION` (observacional, nunca explotación activa) · `FAULT_OWNER` · `FIX_BOUNDARY`.

Formato completo: `ID` · `SEVERITY` · `TYPE` · `STATUS` · los campos anteriores.

## 7. Taxonomía

`AUTHENTICATION_RISK` · `AUTHORIZATION_RISK` · `TENANT_ISOLATION_RISK` · `DATA_EXPOSURE` · `SECRET_EXPOSURE` · `INJECTION_RISK` · `SSRF_RISK` · `COMMAND_EXECUTION_RISK` · `FILESYSTEM_RISK` · `DEPENDENCY_RISK` · `SENSITIVE_LOGGING` · `ERROR_DISCLOSURE` · `MISCONFIGURATION` · `EXCESSIVE_PERMISSION` · `OTHER_SECURITY_RISK`.

La taxonomía **clasifica**; no sustituye la explicación ni la evidencia. `TYPE: INJECTION_RISK` sin path, precondiciones y reachability es una etiqueta, no un finding.

## 8. Estados de finding

| Estado | Significa | Bloquea |
|---|---|---|
| `CONFIRMED_SECURITY_FINDING` | El riesgo y su path relevante están suficientemente demostrados. | Según severidad |
| `SUPPORTED_SECURITY_CONCERN` | Hay evidencia material, pero falta una pieza relevante para confirmar reachability o impacto. **No se presenta como vulnerabilidad confirmada.** | No por defecto |
| `HARDENING_OPPORTUNITY` | Mejora defensiva útil **sin defecto de seguridad demostrado**. | **Nunca por sí sola** |
| `REJECTED_SECURITY_HYPOTHESIS` | La evidencia contradice la hipótesis. Puede omitirse del output salvo que explique una decisión relevante. | No |

Si existe un patrón sospechoso pero **no puedes demostrar** control del atacante, reachability, precondiciones o impacto, **MUST NOT** emitir `CONFIRMED_SECURITY_FINDING`: usa `SUPPORTED_SECURITY_CONCERN`, `HARDENING_OPPORTUNITY` o `INSUFFICIENT_EVIDENCE` según corresponda.

## 9. Severidad

Sólo tres niveles: `BLOCKING` · `MAJOR` · `MINOR`.

- **`BLOCKING`** — riesgo demostrado o suficientemente material que no debería integrarse sin atención: bypass de autorización alcanzable, acceso entre tenants, secreto activo expuesto, inyección alcanzable, ejecución arbitraria de comandos, escalada de privilegio material, pérdida clara de confidencialidad o integridad.
- **`MAJOR`** — riesgo real y relevante, con impacto o precondiciones más limitadas.
- **`MINOR`** — debilidad real de impacto reducido.

La severidad **debe** considerar reachability, precondiciones, control del atacante, privilegio requerido, datos afectados, radio de alcance y evidencia de explotabilidad.

**MUST NOT usar la severidad para compensar falta de evidencia.** Si la evidencia es débil, lo que baja es el *estado* (§8), no lo que sube es la severidad.

**No se introduce CVSS ni scoring numérico** en este skill (ver §12 para consumir output externo que sí los use).

## 10. Frontera de hardening

> **`MISSING_HARDENING != SECURITY_DEFECT`**

La ausencia de una defensa adicional no es, por sí sola, un finding. Suelen ser `HARDENING_OPPORTUNITY`, no defectos: rate limiting adicional · headers defensivos adicionales · logging extra · defensa en profundidad adicional · timeouts más estrictos · una policy más restrictiva que seguiría siendo compatible · validación extra que no protege ningún path actualmente alcanzable.

Se reportan como oportunidad y **no bloquean por defecto**. Una recomendación defensiva opcional nunca se presenta como vulnerabilidad.

## 11. Continuity over security theater

`CONTINUITY OVER SECURITY THEATER` significa, en concreto:

- no minimizar riesgos reales;
- no bloquear por posibilidades abstractas;
- no convertir hardening opcional en bloqueo;
- no elevar la severidad mediante vocabulario alarmista;
- no exigir perfección defensiva para integrar cambios razonables.

El objetivo es reducir riesgo real, no acumular findings.

## 12. Relación con otras capabilities

- **`implementation-review`** (`skill://implementation-review/SKILL.md`) — la correctness funcional es suya. Un mismo hecho puede ser dos cosas: una condición de autorización invertida es un `DEFECT` funcional **y** un `AUTHORIZATION_RISK`. Este skill se limita al **impacto de seguridad**; no repite la review funcional completa. Se preservan sus principios: `PREFERENCE != DEFECT`, findings respaldados por evidencia, y review distinta de remediation.
- **`pr-review`** (`skill://pr-review/SKILL.md`) — puede derivar señales hacia aquí, y este skill puede revisar el mismo diff con lente especializada. Mergeability, approvals, comentarios y readiness general **no** son responsabilidad de este skill; a lo sumo, contexto.
- **`architecture-review`** — si el riesgo nace de ownership de boundary, dirección de dependencias, responsabilidad mal ubicada o estado compartido, produce un referred finding. **No rediseñes la arquitectura ni inventes un control nuevo.**
- **`governance-review`** — si aparece un recurso fuera de alcance, un permiso no autorizado o un cambio no aprobado, defiérelo. Este skill no decide autoridad ni alcance.
- **`diagnostics`** — si existe un incidente de seguridad real cuya causa hay que determinar, la investigación causal es suya. Este skill revisa el cambio o el riesgo relacionado; no sustituye incident diagnosis.
- **`code-quality`** — always-on. Una preferencia de estilo **nunca** se convierte en finding de seguridad.

Registra estas señales como `REFERRED_FINDINGS`, con la evidencia observada y **sin veredicto especializado**. Nunca finjas haber completado la revisión de otra capability.

### Capability de seguridad bundled de OMP

OMP trae el agent `security-reviewer` (read-only: `read`, `grep`, `glob`, `lsp`, `ast_grep`), orientado a **descubrimiento de vulnerabilidades sobre un alcance de repositorio** y con su propio esquema de salida (`severity: critical|high|medium|low|informational`, `confidence`, `cwe`). Comparte el principio rector de este skill — rechaza findings especulativos sin un camino de ejecución creíble — pero **su unidad de trabajo es el repositorio, no el cambio**.

Coexisten: delega en el bundled cuando quieras un barrido de descubrimiento sobre un alcance dado; usa este skill cuando la pregunta sea si **un cambio concreto** introduce riesgo. Este skill **no adopta** su vocabulario de severidad; al consumir su output, tradúcelo con criterio — `critical`/`high` suelen corresponder a `BLOCKING`/`MAJOR`, y `low`/`informational` a `MINOR` o a `HARDENING_OPPORTUNITY` — sin heredar automáticamente la severidad ajena: revalida reachability y precondiciones con §5 antes de adoptar un finding externo.

> La herramienta nativa `security_scan` y el comando `/security` dependen de `security.enabled`, que en este workspace está **deshabilitado** (valor por defecto de OMP, no declarado en la configuración de proyecto ni de usuario). No los presentes como disponibles sin comprobarlo; habilitarlos es una decisión humana de configuración, fuera del alcance de este skill.

## 13. Remediation boundary

> **`SECURITY_FINDING != AUTHORIZATION_TO_FIX`**

Durante la revisión **MUST NOT**: aplicar patches · rotar secretos · cambiar IAM · editar configuración · modificar security groups · cambiar policies · actualizar dependencias · desactivar endpoints · desplegar · modificar datos · implementar hardening.

Tampoco **MUST NOT**: ejecutar exploits, payloads destructivos, pruebas ofensivas reales, ni accesos no autorizados. Si confirmar un finding exigiera explotación activa, **no la ejecutes**: reporta la evidencia disponible como `SUPPORTED_SECURITY_CONCERN` o `INSUFFICIENT_EVIDENCE`.

Puedes identificar `FAULT_OWNER`, `FIX_BOUNDARY` y una dirección correctiva de alto nivel. **Nada de eso constituye autorización.** La cadena es `finding → decisión humana → specification/task contract cuando corresponda → implementation`.

Una revisión normal reporta `SECURITY_STATE_CHANGED: NO`.

## 14. Outcomes

- **`SECURITY_PASS`** — no se encontraron riesgos materiales dentro del alcance revisado con la evidencia disponible. **No significa que el sistema sea seguro**, ni que no existan vulnerabilidades fuera de ese alcance, ni aprobación de arquitectura o gobernanza.
- **`SECURITY_PASS_WITH_FINDINGS`** — existen findings no bloqueantes, hardening opportunities o concerns suficientemente acotados.
- **`SECURITY_BLOCKED`** — existe al menos un finding `BLOCKING`.
- **`INSUFFICIENT_EVIDENCE`** — no hay evidencia suficiente para determinar responsablemente una dimensión material.

**La ausencia de evidencia nunca se convierte en `SECURITY_PASS`.** Declara qué conclusión concreta queda limitada y revisa el resto si puede hacerse responsablemente.

## 15. Progressive disclosure

| Cuándo | Cargar |
|---|---|
| Siempre | `SKILL.md` |
| El cambio toca una superficie concreta y hace falta saber qué inspeccionar | `references/security-surfaces.md` |
| Hay que establecer control del atacante, reachability, activación de un secreto, explotabilidad de un permiso o alcance real de una dependencia | `references/reachability-and-preconditions.md` |

No cargues ambas por defecto. Un cambio pequeño con una sola superficie evidente suele resolverse con `SKILL.md`.

## 16. Contrato de salida

`RESULT` · `REVIEW_SCOPE` · `SECURITY_SURFACES` · `FINDINGS` · `HARDENING_OPPORTUNITIES` · `REFERRED_FINDINGS` · `MISSING_EVIDENCE` · `SECURITY_STATE_CHANGED`.

Obligatorios al cerrar: `RESULT` y `SECURITY_STATE_CHANGED`. `MISSING_EVIDENCE` es obligatorio cuando el resultado es `INSUFFICIENT_EVIDENCE` o cuando alguna conclusión quedó limitada. Omite lo que no aplique — no fabriques secciones vacías, y no infles el reporte con superficies que el cambio no toca.
