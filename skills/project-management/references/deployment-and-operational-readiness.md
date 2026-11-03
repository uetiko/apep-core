# Deployment and Operational Readiness

Carga esta referencia cuando el proyecto se aproxime a una liberación real (release, go-live, cutover) — no para cambios triviales de configuración ya cubiertos por el flujo ordinario de ingeniería del workspace (ver `SKILL.md` §0).

## No confundir "código terminado" con "listo"

Código completo no implica readiness. Evalúa explícitamente cada dimensión siguiente; si una no aplica al frente concreto, decláralo `NOT_APPLICABLE` en vez de omitirla en silencio. Si falta evidencia material para evaluar una dimensión, decláralo explícitamente — no asumas que está lista por defecto.

| Dimensión | Qué verificar |
|---|---|
| `BUILD_READY` | El artefacto a desplegar está construido, versionado y es el que realmente se probó. |
| `CONFIGURATION_READY` | Configuración del entorno destino revisada — nada apuntando a valores de desarrollo/staging por descuido. |
| `INFRASTRUCTURE_READY` | Capacidad, redes, permisos y recursos de infraestructura existen y están provisionados para el entorno destino. |
| `DATA_READY` | Migraciones, seeds, datos requeridos o de referencia están preparados y, si aplica, hay plan de migración de datos existentes. |
| `SECURITY_READY` | Credenciales, secretos, permisos y superficie de exposición revisados para el entorno destino — sin secretos hardcodeados ni permisos heredados de un entorno menos restrictivo. |
| `OBSERVABILITY_READY` | Logs, métricas y trazas suficientes para diagnosticar el comportamiento en producción desde el primer minuto. |
| `ROLLBACK_READY` | Existe un procedimiento de reversión probado o al menos definido, con su propio costo y tiempo conocidos. |
| `SUPPORT_READY` | Hay quién responde si algo falla, con la información necesaria para hacerlo (runbook, contacto, escalación). |
| `COMMUNICATION_READY` | Los stakeholders relevantes (usuarios, operación, dirección, proveedores si aplica) saben qué va a pasar y cuándo. |
| `VALIDATION_READY` | Existe un plan concreto de verificación post-deployment — qué se va a comprobar, cómo, y quién lo hace. |

## Deployment procedure

Cuando sea proporcional, define explícitamente: ambientes involucrados, ventana de despliegue, orden de pasos, responsables por paso, criterio de éxito de cada paso, y punto de decisión go/no-go. No fabricar un procedimiento detallado para un despliegue trivial y reversible — sí definirlo cuando el costo de reversión, el impacto operativo o la ventana de tiempo lo justifiquen (proportional rigor, `SKILL.md` §3).

## Post-deployment verification y contingencia

Un deployment sin errores visibles no es evidencia suficiente de éxito — define qué se observa después (métricas, comportamiento funcional, señales de usuarios reales) y durante cuánto tiempo antes de considerar el despliegue estable. Define contingencia: bajo qué señal se activa rollback o mitigación, y quién decide activarlo.

## No conflar estados (ver `SKILL.md` §10)

`DEPLOYMENT_SUCCESS` (el cambio se desplegó correctamente) no equivale a `OPERATIONAL_ACCEPTANCE` (operación puede sostenerlo) ni a `DELIVERY_ACCEPTANCE` (el entregable cumple lo acordado) ni a `PROJECT_SUCCESS`. Un despliegue sin incidentes inmediatos no demuestra por sí mismo que el proyecto tuvo éxito — sólo que ese paso técnico se ejecutó sin fallo observado hasta el momento de la verificación.

## Qué NO hacer

No declarar `*_READY` en una dimensión sin evidencia concreta. No tratar "el código pasó los tests" como sustituto de readiness operativa. No omitir `SECURITY_READY` u `OBSERVABILITY_READY` por presión de fecha sin reportarlo explícitamente como riesgo aceptado pendiente de `DECISION`. No autorizar el go-live tú mismo cuando requiera autorización organizacional — repórtalo como `DECISION_REQUIRED`.
