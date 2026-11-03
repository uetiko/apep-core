# Coupling, Abstraction Justification and Cognitive Load

Aplica junto con `.omp/skills/architecture-review/SKILL.md` — no lo repite.

## Coupling / cohesion

Evalúa acoplamiento **material observable**, no estética. Considera: fan-in/fan-out relevante, conocimiento de detalles ajenos (un componente que asume la implementación interna de otro), cambios que obligan a modificar múltiples boundaries a la vez, responsabilidades incompatibles agrupadas en la misma unidad, sincronización implícita entre componentes que deberían ser independientes. El finding necesita evidencia concreta de esa relación — no la impresión de que "podría estar mejor organizado".

## Abstraction justification — pattern follows pressure

Aplica `code-quality` (`skill://code-quality/SKILL.md` §3): un patrón o abstracción puede cuestionarse si agrega indirección, coupling, lifecycle o superficie de mantenimiento **sin resolver una presión real identificable** (más de una implementación real, un límite de despliegue/equipo, una dependencia externa con sustitución planificada, o un contrato de negocio que proteger). El reviewer **nunca** exige un patrón alternativo salvo que ya exista una decisión arquitectónica preexistente que lo establezca — cuestionar una abstracción especulativa no es lo mismo que prescribir cuál debería usarse en su lugar (ver `SKILL.md` §11, remediation boundary).

## Cognitive load arquitectónica

Puede reportarse cuando la estructura arquitectónica obliga materialmente a mantener demasiadas relaciones simultáneas, navegación excesiva entre componentes para seguir un flujo, capas sin boundary real, ownership ambiguo, o flujo de control no local — siempre con evidencia concreta de esa carga (p. ej. cuántos archivos/componentes hay que abrir para entender un cambio simple). No uses "cognitive load" como argumento genérico sin poder señalar la relación concreta que la produce.
