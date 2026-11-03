# Commit message — estándar Apep

Aplica cuando `POLICY_APPLICABILITY` (SKILL.md §1) no es contradicha por la gobernanza del repositorio. Si el repositorio define otro formato, manda el repositorio.

## Primera línea

```
<tipo>(<componente-opcional>): <descripción breve en español>
```

| Tipo | Úsalo cuando el commit… |
|---|---|
| `feat` | añade funcionalidad |
| `fix` | corrige un defecto |
| `refactor` | cambia estructura sin cambiar comportamiento observable |
| `docs` | sólo cambia documentación |
| `style` | sólo cambia formato, sin efecto en comportamiento |
| `test` | sólo añade o ajusta tests |
| `perf` | mejora rendimiento |
| `ci` | cambia integración continua / pipelines |
| `chore` | mantenimiento sin efecto funcional |

Reglas:

- español, modo imperativo (`agrega`, `corrige`, `elimina` — no `agregado`, `corrigiendo`);
- la línea completa, incluido `tipo(componente): `, no supera **72 caracteres**;
- sin punto final;
- `componente` es opcional: úsalo cuando el repositorio ya muestre componentes reconocibles; no inventes una taxonomía;
- comunica **intención**, no los archivos tocados (`fix(auth): evita sesión expirada al refrescar token`, no `fix: cambios en auth.py`).

## Una intención, un commit

Un commit es atómico: se puede revertir sin arrastrar un cambio ajeno. Si el diff contiene dos intenciones (p. ej. un `feat` y un `refactor` no necesario para él), **no las fusiones en un mensaje**: señala que hacen falta dos commits y cuáles archivos/hunks van en cada uno. Separar requiere staging selectivo, que forma parte del commit autorizado — no lo hagas sin esa autorización (`RULES.md` 18).

El tipo se elige por la intención dominante **autorizada**. Si el diff mezcla algo no autorizado, eso no es un problema de mensaje: es un hallazgo de alcance.

## Cuerpo

Se añade cuando el encabezado no es suficiente para entender qué resuelve, cómo verificarlo o qué impacto tiene. Un `docs` o `style` trivial normalmente no lo necesita.

```
Historia: <ID del work item>
Qué resuelve: <problema o necesidad, en una o dos frases>
Cómo probarlo: <comandos o pasos realmente ejecutables>
Notas adicionales: <contexto que el revisor necesita>
Migraciones: <N/A | qué migración y cómo se aplica>
Impacto: <qué cambia para usuarios, otros módulos u operación>
```

- `Historia:` enlaza la historia cuando existe, con su ID real. Si no existe historia formal, el campo se omite: no se fabrica trazabilidad inexistente (SKILL.md §5). La justificación de trabajo sin ticket es un requisito del PR, no del commit.
- `Cómo probarlo:` contiene comandos que **se ejecutaron** durante la verificación, o pasos manuales marcados como tales. No listes una prueba que no corriste como si la hubieras corrido.
- Campos que no aplican: omítelos, o `N/A` cuando su ausencia sea información útil (p. ej. `Migraciones: N/A` en un cambio que toca persistencia).

## Ejemplo

```
fix(reportes): conserva el orden de secciones al regenerar PDF

Historia: E1-48
Qué resuelve: al regenerar un informe, las secciones se reordenaban por
fecha de creación en lugar de por la posición definida por el usuario.
Cómo probarlo: make test-unit; regenerar un informe con secciones movidas
y comprobar el orden en el PDF.
Migraciones: N/A
Impacto: sólo afecta a la regeneración; la primera generación no cambia.
```

## Salida

```
COMMIT_MESSAGE
  <mensaje completo>
INTENTIONS_IN_DIFF:  1 | N (detalle si N > 1)
FIRST_LINE_LENGTH:   <n> / 72
NEXT_GIT_ACTION:     AUTHORIZATION_REQUIRED: git commit … | AUTHORIZED (fuente)
```
