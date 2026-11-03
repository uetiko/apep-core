# Runtime and Logs

Aplica junto con `.omp/skills/diagnostics/SKILL.md` — no lo repite. Úsalo cuando el fallo se manifiesta en tiempo de ejecución: excepciones, logs, configuración efectiva, procesos, contenedores.

## Baseline de realidad runtime

Antes de concluir sobre un fallo de runtime, establece con evidencia lo que sea material para la conclusión (`SKILL.md` §4.2). Dos anti-supuestos gobiernan esta reference:

- **`SOURCE_CODE_CURRENT != RUNTIME_DEPLOYED`** — el código que lees en el working tree no es necesariamente el que se estaba ejecutando cuando ocurrió el fallo. Verifica el artefacto/imagen/versión realmente desplegada antes de razonar sobre "el código". Un diagnóstico construido sobre código que nunca corrió explica un fallo que no ocurrió.
- **`CONFIG_PRESENT != CONFIG_LOADED`** — que un valor exista en un archivo, template o IaC no prueba que el proceso lo cargó. Confirma la configuración **efectiva** del proceso en ese entorno y momento.

Cuando un baseline material no pueda establecerse, declárarlo `UNKNOWN` y evalúa si eso degrada el resultado a `ROOT_CAUSE_HIGH_CONFIDENCE` o `INSUFFICIENT_EVIDENCE` (`SKILL.md` §8) — no lo rellenes por inferencia.

## Qué inspeccionar

- **Excepciones y stack traces** — el stack muestra dónde se detectó el error, no necesariamente dónde nació (`SKILL.md` §3.2). Traza hacia atrás desde ahí, no te detengas en la primera línea.
- **Logs de runtime** — evidencia de lo que el sistema observó/reportó, no verdad infalible (`SKILL.md` §3.7). Un log ausente no prueba que algo no ocurrió; puede indicar un `swallowed error` o un nivel de log insuficiente.
- **Configuración efectiva** — la que el proceso realmente carga en ese momento/entorno, no el template o el valor por defecto documentado. Confirma con evidencia (variables de entorno resueltas, archivo de config efectivo, output de un comando de inspección) que la configuración asumida es la que realmente está activa.
- **Variables de entorno** — cuáles están presentes, cuáles faltan, y si su valor efectivo coincide con lo esperado en ese entorno concreto.
- **Estado del proceso** — vivo/reiniciado/OOM-killed, versión desplegada, uptime, si hubo un restart reciente que pudo alterar el estado observado.
- **Contenedores** — imagen y versión efectivamente corriendo, variables inyectadas, límites de recursos, logs del propio runtime del contenedor (no sólo de la aplicación).
- **Filesystem/mounts relevantes** — sólo cuando participan causalmente (un volumen no montado, un archivo de config ausente, permisos).
- **Reproducción controlada** — de alto valor cuando es razonable y segura; no obligatoria para toda causa raíz (`SKILL.md` §3.8).
- **Mocks vs. runtime real** — un mock verifica el comportamiento asumido de una dependencia, no su comportamiento real; una discrepancia entre ambos es evidencia relevante, no una contradicción a ignorar.
- **Evidencia antes/después de restart o retry** — un restart puede "arreglar" el síntoma sin tocar la causa; compara el estado antes y después para no confundir la desaparición del síntoma con su resolución.

## Preservar evidencia antes de mutar

**Antes de** ejecutar cualquiera de estas operaciones, evalúa si destruiría evidencia todavía necesaria:

`restart` · `redeploy` · `retry` · `requeue` · `rollback` · `clear cache` · `truncate` · `delete` · `reset`

Si existe riesgo material de perder evidencia relevante: recopila esa evidencia primero (captura logs, estado, config efectiva, stack completo), o detente si la operación no está autorizada (`SKILL.md` §13, condiciones 1–3) — no ejecutes la operación "para ver si ayuda" cuando eso comprometería la capacidad de explicar la causa después.

Esta política no es una guía general de observabilidad — se limita a lo necesario para no destruir evidencia relevante a un diagnóstico en curso.
