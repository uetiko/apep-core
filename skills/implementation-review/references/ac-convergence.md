# AC convergence — cada criterio material, con su evidencia

Referencia de `implementation-review` (`SKILL.md` §7.1). Se aplica cuando existe una especificación formal con registro `AC-NNN`; con un task contract ligero, la cobertura de requisitos de §7.1 basta. Responde: ¿cada criterio de aceptación material está implementado, demostrado y sin contradicción?

```
EVERY MATERIAL AC REQUIRES EVIDENCE.
SELF-VERIFICATION != INDEPENDENT CONFORMANCE.
IMPLEMENTED != VERIFIED != CONFORMANT
```

El owner es `implementation-review`. `implementation` aporta evidencia; no declara la convergencia.

## 1. Estados por AC

| Estado | Significa |
|---|---|
| `PASS` | El comportamiento está implementado, la verificación aplicable se ejecutó sobre el diff revisado, la evidencia basta y nada contradice el contrato |
| `UNVERIFIED` | Parece implementado, pero no hay evidencia suficiente del comportamiento, o la verificación no se ejecutó o es anterior al último cambio |
| `UNIMPLEMENTED` | El comportamiento contractual no está en el cambio |
| `CONTRADICTED` | La implementación o la evidencia contradicen explícitamente el AC |

Cuatro estados, ninguno más. Un AC `UNVERIFIED` no es "probablemente `PASS`": falta evidencia.

## 2. Evidencia

Por cada AC material, cuando sea posible:

```
AC-NNN
  IMPLEMENTATION_EVIDENCE:  <dónde y cómo el diff produce el comportamiento>
  VERIFICATION_EVIDENCE:    <test, comando o ejecución observada · resultado · procedencia>
  CONFORMANCE_RESULT:       PASS | UNVERIFIED | UNIMPLEMENTED | CONTRADICTED
```

- **Procedencia de la verificación:** `INDEPENDENT` (la observó o re-ejecutó quien revisa) · `RECORDED` (comando y resultado registrados por el implementador, sobre el mismo estado del diff) · `CLAIMED` (afirmación sin comando ni resultado). `CLAIMED` nunca sostiene un `PASS`. En `FORMAL`, quien revisa re-ejecuta la verificación decisiva cuando es local, barata y no toca estado compartido; si no puede, `RECORDED` vale y la razón queda en `LIMITATIONS`.
- **Evidencia vigente:** una verificación anterior al último cambio de código (por ejemplo, previa a una remediation) no cubre el diff actual: el AC vuelve a `UNVERIFIED` hasta que se ejecute de nuevo.
- **Muchos a muchos:** un test puede cubrir varios AC y un AC puede necesitar varias evidencias. No se fuerza un mapeo 1:1 ni números de línea que no aporten fiabilidad.
- Un test en verde demuestra lo que ejercita, no el AC (`SKILL.md` §7.6): la evidencia se juzga por lo que demuestra.

## 3. Findings transversales

Lo que no es el estado de un AC se reporta como finding (`SKILL.md` §9), no como estado:

| Señal | Finding |
|---|---|
| Cambio fuera del contrato | `OUT_OF_SCOPE_CHANGE` (se deriva a `governance-review`) |
| Lo implementado diverge del contrato | `CONTRACT_MISMATCH` |
| Path material sin prueba | `MISSING_TEST` |
| Regresión de comportamiento existente | `DEFECT` si está demostrada; `REGRESSION_RISK` si sólo hay evidencia de la relación |
| Comportamiento añadido que ningún requisito pidió | `UNREQUESTED_BEHAVIOR` |

Un cambio fuera de alcance nunca es "el estado" de un AC: puede coexistir con todos los AC en `PASS`.

## 4. `AC_CONVERGENCE_RESULT`

```
AC_CONVERGENCE_RESULT
  contract:          <ruta · fingerprint revisado>
  diff_base:         <commit de la baseline> → <estado revisado>
  ac:                <AC-NNN: estado · evidencia> …
  material_non_pass: NONE | <AC-NNN: estado>
  transverse:        NONE | <findings de §3>
  result:            CONVERGED | NOT_CONVERGED
```

`CONVERGED` sólo con todos los AC materiales aplicables en `PASS`. Un AC no material o no aplicable se declara como tal con su razón; no se omite en silencio. Si sólo se evaluó parte del inventario, cada AC evaluado lleva su estado y el `result` queda pendiente hasta cubrir el resto: una convergencia parcial no es `CONVERGED`.

Relación con el outcome de la review (`SKILL.md` §11): un AC material en `UNIMPLEMENTED` o `CONTRADICTED` es un finding `BLOCKING` (`CONTRACT_MISMATCH` o `DEFECT`) → `REVIEW_BLOCKED`. Uno en `UNVERIFIED` es `UNVERIFIED_BEHAVIOR` `BLOCKING`, o `INSUFFICIENT_EVIDENCE` si la evidencia no puede obtenerse en absoluto. La convergencia no corrige nada: qué se hace con un AC fuera de `PASS` lo decide el lifecycle (`skill://delivery-lifecycle/references/delivery-evidence.md` §3).
