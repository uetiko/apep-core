# Versionado — SemVer

Aplica cuando `POLICY_APPLICABILITY` (SKILL.md §1) no es contradicha por la gobernanza del repositorio.

## Formato

```
vMAJOR.MINOR.PATCH          versión final
vMAJOR.MINOR.PATCH-rc.N     pre-release
```

| Incremento | Cuándo |
|---|---|
| `MAJOR` | se rompe un contrato público (API, formato, comportamiento del que dependen consumidores) |
| `MINOR` | funcionalidad nueva compatible |
| `PATCH` | correcciones o cambios internos que no rompen contratos |

## Dónde viven los tags

La ubicación de tags finales y pre-releases sigue las ramas que la gobernanza de este repositorio designe como ramas de release. Este skill no fija nombres de rama. Si el repositorio no declara ninguna, la ubicación es `MISSING_DATA` y se pregunta.

Un hotfix, cuando el repositorio lo define, suele llevar un tag `PATCH` al integrarse en la rama de producción, seguido de la sincronización descendente que el repositorio declare.

## Autoridad

```
COMPUTE AND PROPOSE  !=  DECIDE AND TAG
```

- **El número de versión no se decide automáticamente.** Lo evalúa —`MAJOR`, `MINOR` o `PATCH`— el **responsable técnico del release** (Tech Lead, Head de Desarrollo o equivalente).
- El agente puede analizar el impacto, **proponer** una versión y explicar por qué. No toma la decisión material del release, ni siquiera cuando la clasificación parece obvia.
- Si la propuesta depende de juzgar si un cambio rompe un contrato público, el agente lo señala (`CONTRACT_BREAK: UNCERTAIN`) con la evidencia; ese juicio también es del responsable técnico.
- Crear, mover, borrar o publicar un tag es Git gateado (`git tag*`, `git push*`), incluso con la versión ya decidida.

## Cómo proponer

1. Último tag aplicable en la rama correspondiente: `git describe --tags --abbrev=0`, `git tag -l 'v*'` (lectura).
2. Cambios desde ese tag: `git log <tag>..HEAD` — tipos de commit, PRs integrados.
3. Clasifica el incremento por el cambio de mayor impacto. Un `feat` sugiere `MINOR`; un `fix` sugiere `PATCH`; **el tipo del commit no decide por sí solo** si hubo ruptura de contrato — eso lo dicen el diff y los contratos.
4. Para un rc: siguiente `N` sobre la misma `X.Y.Z` si ya existe `vX.Y.Z-rc.*`; si no, `rc.1`.

Si no hay tags previos, o la historia no permite clasificar, dilo: `INSUFFICIENT_EVIDENCE`. No inventes una versión base.

## Salida

```
VERSION_PROPOSAL
  BRANCH:              <rama de release designada por el repositorio> | MISSING_DATA
  CURRENT_VERSION:     <último tag> | NONE
  CHANGES_CONSIDERED:  <rango y resumen>
  PROPOSED_VERSION:    vX.Y.Z | vX.Y.Z-rc.N
  RATIONALE:           <qué cambio determina el incremento>
  CONTRACT_BREAK:      NO | YES | UNCERTAIN (evidencia)
  DECIDES:             responsable técnico del release
  NEXT_GIT_ACTION:     AUTHORIZATION_REQUIRED: git tag … && git push … | AUTHORIZED (fuente)
```
