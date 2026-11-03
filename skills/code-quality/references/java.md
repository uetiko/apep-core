# Java — convenciones de documentación y estilo

Aplican junto con `.omp/skills/code-quality/SKILL.md` — no lo repiten.

1. **Convención del repositorio primero** (Checkstyle/Spotless, guía interna) prevalece sobre lo siguiente.
2. **Javadoc para contratos y APIs** donde corresponda: clases/métodos públicos cuyo contrato no sea evidente desde la firma, excepciones lanzadas y su significado, invariantes de la clase.
3. **No documentar trivialidades** (getters/setters triviales, implementación obvia) ni narrar el cuerpo del método.
4. Documentar precondiciones, postcondiciones y efectos secundarios no evidentes — no la implementación línea por línea.
