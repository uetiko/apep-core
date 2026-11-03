# T13 — Ítem abierto no material

TIPO DE ENTRADA: especificación completa con un supuesto no material registrado.
TAREA: decidir si la especificación puede declararse lista para ejecutar.

---

Especificación "archivar widget":

- **BR-001** Un Operador puede archivar un widget propio.
- **BR-002** Un widget archivado no aparece en el listado por defecto.

- **AC-001** Dado un widget propio, cuando el Operador lo archiva, entonces deja de aparecer en el listado por defecto.
- **AC-002** Dado un widget de otra organización, cuando el Operador intenta archivarlo, entonces recibe 403.

- **ASM-001** El texto del botón será "Archivar". Razón: no afecta al comportamiento, es reversible y cumple los criterios A1–A8; el owner puede cambiarlo sin rehacer nada.
