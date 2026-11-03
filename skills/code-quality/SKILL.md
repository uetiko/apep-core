---
name: code-quality
description: Reglas y criterio de calidad de código para toda escritura o modificación de código en este workspace. A diferencia de `specification` y `project-management`, NO es opt-in — aplica siempre que se escriba o modifique código, sin necesidad de invocación explícita ni de `/skill:code-quality`. Es referencia de fondo permanente para cualquier tarea de implementación, no un workflow que se activa a petición.
---

# Code Quality

Este skill no es un workflow con etapas ni un router — es una **capability de referencia permanente**. Codifica el criterio de calidad de `docs/governance/ENGINEERING_GOVERNANCE.md` (§3–§13) en una forma reutilizable por cualquier agente que escriba o modifique código, incluidos los agents delegados de `.omp/agents/`.

## 0. Cuándo aplica

Siempre que exista escritura o modificación de código — sin excepción y sin invocación manual. No equivale a `specification` ni a `project-management` (ver `.omp/skills/specification/`, `.omp/skills/project-management/`): esos son workflows opt-in de metodología de producto/proyecto; este es criterio de ingeniería de fondo, siempre activo.

## 1. Precedencia y fuente autoritativa

```
WORKSPACE GOVERNANCE       (docs/governance/ENGINEERING_GOVERNANCE.md, .omp/AGENTS.md, .omp/RULES.md)
  → REPOSITORY GOVERNANCE  (convenciones propias del repositorio, cuando existen)
    → CODE QUALITY         (este skill — el "cómo" transversal)
      → TASK CONTRACT
        → IMPLEMENTATION
```

Este skill no es una gobernanza independiente ni la sustituye. Cuando el repositorio en curso ya define convenciones propias (linter, formatter, arquitectura, guía de estilo), esas convenciones tienen autoridad local sobre las reglas generales de este skill cuando ambas se refieren al mismo caso (`ENGINEERING_GOVERNANCE.md` §4.3, §6.1). Este skill nunca convierte SOLID, Clean Code, Clean Architecture, KISS, YAGNI o DRY en objetivos de cumplimiento dogmático — son herramientas de diagnóstico (§3).

## 2. Carga cognitiva primero

Minimiza, en este orden cuando entren en tensión con otros objetivos de diseño no invariantes: conceptos simultáneos necesarios para seguir un flujo · saltos entre archivos · indirecciones sin frontera real · wrappers sin semántica propia · capas redundantes · estado implícito · side effects ocultos · nombres que requieren traducción mental · configuración dispersa · control de flujo no local. Una solución "arquitectónicamente pura" puede rechazarse si introduce carga cognitiva innecesaria frente a una alternativa más simple que satisface los mismos invariantes (`ENGINEERING_GOVERNANCE.md` §5).

## 3. SOLID, Clean Code, Clean Architecture — diagnóstico, no dogma

- **Clean Code**: legibilidad estructural e intención expresada, no métricas (longitud de función, número de parámetros) a optimizar por sí mismas.
- **Clean Architecture**: sólo cuando hay una frontera real — más de una implementación real que deba convivir, un límite de despliegue/equipo, una dependencia externa con sustitución ya planificada, o un contrato de negocio que proteger de infraestructura. "Podría necesitarse en el futuro" nunca es suficiente (§4.1). Donde el repositorio ya define capas, respeta su dirección de dependencias (lo habitual: infraestructura y entrega dependen del dominio/casos de uso, no al revés); una dependencia que la invierte es un hallazgo, no un atajo táctico.
- **SOLID** (§4.2): SRP es cohesión de razones de cambio, no una función por acción trivial. OCP no exige abstraer variación hipotética. LSP exige preservar semántica/contratos observables, no sólo tipos o firmas. ISP no exige fragmentar interfaces cohesivas. DIP se usa sólo cuando hay una frontera real que desacoplar — no se crean ports/adapters/interfaces por costumbre.
- **Programación pragmática**: evita la abstracción prematura; prioriza simplicidad suficiente, evolución razonablemente esperable, contratos explícitos, observabilidad, mantenibilidad y reversibilidad sobre "corrección abstracta" costosa de revertir. Favorece cambios pequeños, verificables y reversibles cuando sea razonable, y reduce acoplamiento y efectos colaterales innecesarios (ortogonalidad) en vez de maximizar cualquier otra virtud de diseño a costa de ellos. Ante un contrato o precondición violada, falla rápido y de forma explícita en vez de continuar con estado inválido o engañoso — no ocultes errores ni estados inválidos para mantener artificialmente el flujo. Introduce configuración sólo cuando representa variabilidad real ya demostrada, nunca como generalización especulativa. Evita depender de una solución sin entender por qué funciona (*programming by coincidence*).
- **YAGNI**: no diseñes para un requisito no demostrado. Una mención en conversación no es un requisito demostrado.
- **KISS**: menor número de conceptos simultáneos necesarios para razonar sobre la solución, no menos líneas.
- **DRY**: elimina duplicación de *conocimiento* (una regla o fórmula que debería evolucionar en un solo lugar), no similitud textual — mantén ese conocimiento en una única fuente autoritativa cuando realmente representa el mismo concepto. Unificar dos reglas de negocio independientes que sólo se parecen crea acoplamiento accidental.

**No introducir**, sin una frontera real demostrada: interfaces por costumbre, factories sin necesidad demostrada, services genéricos sin responsabilidad clara, strategies para variabilidad hipotética, wrappers sin semántica, helpers que sólo fragmentan lectura, ports/adapters sin frontera real, generalización para un futuro no requerido.

## 4. SEARCH BEFORE CREATE

Antes de crear un componente, patrón o abstracción nueva: busca equivalentes existentes (servicios, value objects, configuración, fixtures, excepciones, utilidades) en el repositorio. El código existente es evidencia de comportamiento actual, no automáticamente de arquitectura pretendida ni de especificación — una convención repetida puede ser deuda repetida. Sigue la convención existente dentro de tu autonomía táctica; si la consideras defectuosa, repórtala como hallazgo en vez de repetirla en silencio o corregirla sin autorización (`ENGINEERING_GOVERNANCE.md` §6.1).

## 5. Comentarios y documentación

Antes de explicar código mediante comentarios, prefiere que su intención pueda expresarse mediante, en este orden: diseño del código · nombres · tipos · contratos/interfaces · tests como ejemplos ejecutables · documentación formal de API/código · comentarios inline. Esta jerarquía no implica que todas las capas deban existir en cada unidad de código — es un orden de preferencia, no una checklist obligatoria.

**No usar comentarios para narrar qué hace el código** (`# Get user`, `# Validate result`, `// loop through records`, o equivalentes). Si un comentario compensa un nombre deficiente, una función compleja o control de flujo confuso, la corrección es mejorar el código, no comentarlo.

Comentarios aceptables sólo cuando documentan lo que el código no puede expresar razonablemente: restricción de un sistema externo, comportamiento contraintuitivo impuesto por una API o proveedor, requisito normativo, incompatibilidad conocida, o una decisión temporal con contexto indispensable para no revertirla por error (§10).

Documentación de API/contratos: sigue primero la convención ya autoritativa del repositorio; en ausencia de una, usa la referencia de lenguaje de este skill (§7). Nunca documentación arquitectónica dentro de comentarios inline — esa vive en la documentación del repositorio correspondiente.

Documentación técnica (README, docs del repositorio, ADRs): se escribe cuando reduce incertidumbre para quien mantendrá o consumirá el código, describe **intención y comportamiento**, no sintaxis, y **se actualiza en el mismo cambio** que altera el comportamiento que documenta. Documentación desactualizada respecto del diff es un defecto del diff.

## 6. Diff quality review — antes de COMPLETE

Antes de declarar una implementación `COMPLETE`, revisa el diff completo (no sólo el archivo que motivó el cambio) evaluando explícitamente: naming e intención de los nombres, cohesión, separación de responsabilidades, dirección de dependencias, duplicación de conocimiento, complejidad accidental, abstracciones especulativas, si el patrón o abstracción utilizado resuelve un problema real verificable, side effects, comentarios/docstrings innecesarios o que sólo repiten tipos/código, convenciones locales preservadas, y las verificaciones deterministas del repositorio que apliquen — formatter, linter, type checker, static analysis, tests y build, cuando existan. No inventes herramientas que el repositorio no tenga, ni ejecutes una irrelevante sólo para completar la lista. Tests en verde no son, por sí solos, evidencia suficiente de corrección (§12, §13). Esta revisión guía la inspección del diff — no requiere un reporte narrativo como evidencia de cumplimiento.

## 7. Convenciones específicas de lenguaje

No cargues todas las referencias en cada tarea — carga sólo la del lenguaje/stack de la tarea en curso:

| Lenguaje | Referencia |
|---|---|
| Python | `skill://code-quality/references/python.md` |
| PHP | `skill://code-quality/references/php.md` |
| TypeScript/JavaScript | `skill://code-quality/references/typescript.md` |
| Java | `skill://code-quality/references/java.md` |

Estas referencias contienen únicamente reglas específicas del lenguaje — no repiten lo ya establecido en las secciones anteriores. Si el repositorio ya tiene una convención propia y verificable para su stack (config de linter, guía de estilo interna), esa convención prevalece sobre la referencia genérica (§1).

## 8. Tests — comportamiento, no detalles de implementación

```
TEST BEHAVIOR, NOT IMPLEMENTATION DETAILS.
```

Compila la estrategia de testing de Apep. Las convenciones técnicas del repositorio (frameworks, carpetas, comandos) prevalecen en el *cómo* (§1); el criterio de *qué* se prueba es éste.

**Qué testear.** La unidad primaria es el **caso de uso / comportamiento observable**, no la clase ni el método. Para un caso de uso o comportamiento nuevo cubre, cuando aplique: el camino feliz · la regla de negocio violada · la excepción relevante. No se testean internals irrelevantes: un test que sólo comprueba qué métodos internos se llamaron prueba la implementación, no el comportamiento. **La cobertura de líneas no es un objetivo**: no se escriben tests para subir un porcentaje.

**Unit tests:**

- sin infraestructura real, sin base de datos real y sin servicios externos reales;
- deterministas (sin dependencia de reloj, orden, red ni aleatoriedad no fijada);
- independientes entre sí, **sin estado global compartido**.

| Puede mockearse | No se mockea |
|---|---|
| repositorios | entidades |
| servicios externos | value objects |
| interfaces de infraestructura | la regla de negocio que se está probando |

**Cuándo añadir o ajustar tests.**

- Al añadir comportamiento: tests que lo demuestren.
- Al modificar comportamiento existente: ajusta los tests que lo describen y añade los que falten. Un test que protege comportamiento que el contrato cambia explícitamente se actualiza; uno que protege comportamiento que el contrato no toca **no se debilita** para que pase (`implementation-review` §4).
- Al corregir un bug, preferentemente: (1) test de regresión que falla primero · (2) corrección · (3) el test pasa. Si reproducirlo no es práctico, dilo y explica qué evidencia lo sustituye.

**Qué no exigir.** Tests para getters triviales, wiring sin comportamiento, cambios exclusivamente documentales o configuración sin comportamiento verificable. Un test sin comportamiento que demostrar es coste sin evidencia.

**TDD** es la técnica preferida cuando reduce incertidumbre — reglas de negocio con casos claros, bugs reproducibles, contratos precisos —, **no un mandato universal**. Elige test-first o test-after por cuál da antes evidencia fiable, no por doctrina.
