# Python — convenciones de documentación y estilo

Aplican junto con `.omp/skills/code-quality/SKILL.md` — no lo repiten.

1. **Convención del repositorio primero.** Si el repositorio ya define un estilo de docstring, linter (`ruff`, `flake8`, `pylint`) o guía de estilo propia, esa convención prevalece.
2. **En ausencia de convención propia**, usa docstrings estilo Google (`Args:`, `Returns:`, `Raises:`) sólo en funciones/clases públicas cuyo contrato no sea evidente por firma y nombres.
3. **No generar docstrings redundantes** que sólo repitan el nombre de la función o los tipos ya expresados por type hints.
4. **Usar type hints** en firmas públicas; no sustituyen la necesidad de nombres claros.
5. El docstring documenta contrato y semántica (precondiciones, postcondiciones, invariantes, efectos secundarios no evidentes) — no narra la implementación línea por línea.
