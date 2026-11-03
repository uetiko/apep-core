# PHP — convenciones de documentación y estilo

Aplican junto con `.omp/skills/code-quality/SKILL.md` — no lo repiten.

1. **Convención del repositorio primero** (PSR, PHPCS/PHP-CS-Fixer, guía interna) prevalece sobre lo siguiente.
2. **Preferir native types** (`declare(strict_types=1)`, tipos de parámetro/retorno nativos) sobre anotaciones que sólo existen en PHPDoc.
3. **No duplicar `@param`/`@return`** cuando únicamente repiten el tipo nativo ya declarado en la firma.
4. **PHPDoc sí aporta valor** para: generics/templates (`@template`), array shapes (`array<string, int>`), tipos que el sistema de tipos nativo no puede expresar, y requisitos de tooling (p. ej. PHPStan/Psalm).
5. Documentar contrato y semántica de negocio, no la implementación.
