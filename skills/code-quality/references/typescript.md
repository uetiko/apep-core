# TypeScript / JavaScript — convenciones de documentación y estilo

Aplican junto con `.omp/skills/code-quality/SKILL.md` — no lo repiten.

1. **Convención del repositorio primero** (ESLint/Prettier, guía interna) prevalece sobre lo siguiente.
2. **Tipos y nombres primero.** El sistema de tipos (TypeScript) y nombres con intención explícita cubren la mayoría de lo que un comentario intentaría explicar.
3. **TSDoc/JSDoc sólo cuando aporte valor real**: contrato de una API pública, comportamiento no evidente desde la firma, o requisito de tooling (generación de documentación, IDE hints en JS sin tipos).
4. **No documentar lo que el tipo ya expresa** (p. ej. `@param {string} name - the name`, sin información adicional).
5. En JavaScript puro (sin tipos), JSDoc puede sustituir parcialmente al type-checking para tooling — con la misma disciplina: contrato, no narración.
