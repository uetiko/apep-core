# Pull Request — plantilla genérica

Aplica cuando `POLICY_APPLICABILITY` (SKILL.md §1) no es contradicha por la gobernanza del repositorio. Si el repositorio define otra plantilla, manda el repositorio.

## Qué debe responder todo PR

1. ¿Qué problema o necesidad resuelve?
2. ¿Cómo se resuelve?
3. ¿Cómo se prueba?

Si el borrador no responde a las tres, no está listo.

## Una sola intención

El PR representa una intención coherente. No mezclar: funcionalidad + refactor masivo · historias no relacionadas · cambios oportunistas. Si el diff entre la work branch y su `PR_TARGET` contiene más de una intención, el borrador lo dice y propone cómo dividirlo — no lo disimula en la descripción.

## Destino

`PR_TARGET` es la rama que la gobernanza de este repositorio designa como su rama de integración para el tipo de rama de trabajo en curso (consulta su `BRANCH_PREFLIGHT`, SKILL.md §4). Si el repositorio no declara ninguna, `PR_TARGET` es `MISSING_DATA` y se presenta como `PROPOSAL` para confirmación.

Las promociones entre ramas permanentes y la sincronización descendente tras un hotfix son integraciones gateadas; un borrador para ellas usa la misma plantilla.

## Plantilla

```markdown
## Identificación
Referencia de ticket/historia: <ID | N/A>   (campo opcional, si la convención de tu organización lo exige)
Tareas relacionadas: <IDs | N/A>
Tipo: <feat | fix | refactor | docs | style | test | perf | ci | chore>

## Problema / Necesidad

## ¿Qué resuelve?

## Cómo probarlo

## Alcance del cambio

## Enfoque técnico

## Migraciones / DB

## Impacto y riesgos

## Checklist mínimo

## Notas / Comentarios adicionales
```

Reglas de llenado:

- **Sin texto ceremonial.** Cada sección dice algo verificable o es `N/A — <razón breve>` (p. ej. `N/A — el cambio no toca persistencia`).
- **Identificación:** IDs reales (SKILL.md §5). **Sin ticket o historia formal**: nunca un ID inventado; en su lugar, la justificación explícita que la convención del repositorio exija:

```markdown
## Identificación
Referencia de ticket/historia: Sin ticket — <justificación explícita>
Tareas relacionadas: N/A
Tipo: fix
```

Si la convención exige justificación y falta, el borrador lo marca como pendiente y el PR no está listo.
- **Cómo probarlo:** los comandos de verificación **realmente ejecutados** con su resultado, más los pasos manuales que el revisor debe reproducir, marcados como manuales. No presentes como ejecutado algo que no corrió.
- **Alcance del cambio:** qué entra y, cuando ayude, qué queda fuera deliberadamente.
- **Enfoque técnico:** la decisión de implementación relevante y por qué; las decisiones cerradas por el owner se citan como tales (`DECISIONS_USED`), no como iniciativa del agente.
- **Migraciones / DB:** qué migración, si es reversible, cómo se aplica. Una migración no autorizada no aparece aquí: es una parada.
- **Impacto y riesgos:** riesgos conocidos que el cambio no elimina, incluida deuda descubierta (`DISCOVERED_DEBT`).
- **Checklist mínimo:** verificable, no aspiracional. Sólo ítems que se marcaron con evidencia:

```markdown
- [x] Implementación conforme a la arquitectura del repositorio
- [x] Tests requeridos añadidos; tests existentes en verde (<comandos>)
- [x] Estilo / formato verificados (<formatter/linter>)
- [x] Criterios de aceptación verificados uno por uno (ver "Cómo probarlo")
- [x] Sin TODOs ni trabajo incompleto de la historia
- [ ] Documentación actualizada — N/A: no cambia comportamiento, arquitectura ni contratos
```

Los ítems siguen la Definition of Done (`skill://project-management/references/work-item-flow.md` §4); los que no tienen sentido para el cambio van como `N/A` + razón. "PR revisado/aprobado" no se marca en el borrador: lo cumple el revisor.

## Título

```
<tipo>(<componente-opcional>): <descripción breve>
```

- Tipos: los mismos que en commits — `feat` · `fix` · `refactor` · `docs` · `style` · `test` · `perf` · `ci` · `chore` (`commit-message.md`).
- Descripción breve, expresa la intención, sin punto final, componente opcional. Idioma: el que establezca la convención del repositorio.
- Nada de títulos genéricos (`fix: cambios`, `feat: mejoras`, `update`).
- **No incluye el ID de historia/ticket.** La trazabilidad vive en `## Identificación` del cuerpo; no se duplica.

```
feat(auth): add access-context validation
fix(listener): handle empty corpus before the report engine
refactor(auth): split permission resolution
```

`EL TÍTULO IDENTIFICA LA INTENCIÓN. EL CUERPO CONTIENE TRAZABILIDAD Y EVIDENCIA.`

## Salida

```
PR_DRAFT
  SOURCE_BRANCH:   <work branch>
  PR_TARGET:       <rama> | MISSING_DATA
  TITLE:           <tipo>(<componente>): <descripción>
  BODY:            <plantilla rellena>
  INTENTIONS:      1 | N (propuesta de división si N > 1)
  NEXT_GIT_ACTION: AUTHORIZATION_REQUIRED: <push de la rama y/o creación del PR> | AUTHORIZED (fuente)
```

Publicar el PR, hacer push de la rama y cualquier merge son operaciones separadas, cada una con su propia autorización (SKILL.md §3). Revisar un PR ya publicado es `pr-review`.
