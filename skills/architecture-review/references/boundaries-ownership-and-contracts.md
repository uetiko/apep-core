# Boundaries, Ownership and Contracts

Aplica junto con `.omp/skills/architecture-review/SKILL.md` — no lo repite. Cubre las dimensiones estructurales de la revisión: dependency direction, boundaries, ownership, contracts/integration, state/persistence/side effects, y — sólo cuando sea relevante — runtime/deployment topology y cross-repository boundaries.

Esta reference evalúa **si** una relación observada respeta la arquitectura aplicable. Para **reconstruir** el grafo de dependencias/responsabilidades desde cero, usa `skill://technical-discovery/references/architecture-and-dependency-mapping.md` — no dupliques esa técnica aquí.

## Dependency direction

Examina quién depende de quién, la dirección real de imports/calls, inversiones no autorizadas, ciclos, y dependencias de una capa/core hacia detalles externos. No asumas una dirección "correcta" por teoría general si el sistema no la declara o establece — la base arquitectónica debe ser una decisión/boundary real, no una preferencia de estilo (Clean Architecture, hexagonal, etc.) importada sin evidencia de que aplique aquí.

## Boundaries

Módulos, bounded contexts, services, packages, repositorios, procesos, infraestructura. Detecta cuándo una responsabilidad o dependencia cruza una boundary arquitectónica **aplicable** — es decir, una que ya está establecida (declarada u observablemente consistente), no una que el reviewer introduciría.

## Ownership

Quién posee una responsabilidad, quién posee los datos, quién puede mutar estado, quién posee un contrato, quién controla el lifecycle. Detecta ownership difuso o duplicado sólo cuando sea material — dos componentes escribiendo la misma fuente de verdad sin coordinación, por ejemplo, no una duplicación cosmética.

## Contracts / integration

APIs, ports, events/messages, colas, contratos de base de datos, archivos, object storage, schemas, modelos compartidos, integración cross-service. Detecta acoplamiento a detalles internos cuando contradiga una boundary existente (p. ej. un consumidor que depende de un detalle de implementación de otro lado del contrato en vez de su interfaz pública).

## State / persistence / side effects

Dónde vive el estado, quién lo escribe, quién lo lee, side effects, transactional boundaries, state sharing, persistence ownership. **No trates "usar una base de datos directamente" como violación por definición** — debe existir una boundary/decisión aplicable que lo prohíba para que sea un finding.

## Runtime / deployment topology (sólo cuando sea relevante)

Procesos, contenedores, colas, orquestación, fronteras de red, persistencia, dirección de dependencia en runtime. No conviertas toda revisión de arquitectura de código en una revisión de infraestructura — sólo entra aquí cuando la pregunta o el cambio realmente cruza esa frontera.

## Cross-repository boundaries

Cuando el cambio cruza repositorios: establece baseline independiente por repositorio (`.omp/RULES.md` regla 13, `MULTI-REPOSITORY`), identifica los contratos entre ambos lados, no asumas ownership compartido sin evidencia, no mezcles evidencia Git entre repositorios (`.omp/RULES.md` regla 18, `GIT / CHANGE DISCIPLINE`), y verifica ambos lados del contrato cuando sea material para la pregunta.
