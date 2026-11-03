# T14 — C2 pasa, la coherencia falla

TIPO DE ENTRADA: especificación con todas las referencias definidas pero un defecto semántico.
TAREA: ejecutar el readiness gate.

---

- **BR-001** Un Operador puede archivar un widget propio.
- **BR-002** Un widget archivado puede restaurarse en cualquier momento.
- **UC-001** El Operador archiva un widget (BR-001).
- **UC-002** El Operador restaura un widget archivado (BR-002).
- **AC-001** Dado un widget propio, cuando el Operador lo archiva, entonces deja de aparecer en el listado (UC-001, BR-001).
- **AC-002** Dado un widget archivado, cuando el Operador lo restaura, entonces vuelve a aparecer (UC-002, BR-002).
- **AC-003** Dado un widget archivado, cuando se restaura, entonces conserva su historial (BR-002).
- **AC-004** Un widget archivado no puede restaurarse (BR-001): contradice BR-002.
- **TASK-001** Implementar archivado y restauración (AC-001, AC-002, AC-003).
- **AT-001** Verifica AC-001.
