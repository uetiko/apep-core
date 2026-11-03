# Distributed and CI Incidents

Aplica junto con `.omp/skills/diagnostics/SKILL.md` — no lo repite. Úsalo para `INCIDENT_DIAGNOSIS`: fallos operacionales o distribuidos (CI/CD, build/deploy, cloud, colas, contenedores, networking).

## Qué inspeccionar

CI/CD y build/deploy · ejecución distribuida · proveedores cloud (AWS u otro) · colas y workflows · contenedores · reintentos · networking · timeouts · race conditions · eventual consistency · configuration drift · diferencias entre configuración de build-time y de runtime.

## Principios específicos de incidentes distribuidos

- **Timeline reconstruible** — antes de asignar causa, reconstruye el orden real de los eventos (qué falló primero, qué lo siguió) con timestamps y evidencia, no con la narrativa más plausible.
- **Correlation/execution IDs** — cuando existan, úsalos para atar logs/eventos/trazas dispersos entre componentes al mismo incidente concreto, en vez de asumir que dos entradas de log "parecen" relacionadas.
- **Separar control plane de data plane** cuando sea relevante — un fallo en el plano de control (orquestación, scheduling, despliegue) tiene una causa distinta de un fallo en el plano de datos (el tráfico/carga real que se procesa), aunque ambos se manifiesten como el mismo síntoma externo.
- **Failure origin vs. propagation** — el componente que falló primero no es necesariamente el que se observa fallando más visiblemente; un fallo se propaga y amplifica aguas abajo.
- **No asumas que el último componente en fallar originó el incidente** — es el error de proximidad temporal aplicado a sistemas distribuidos (`SKILL.md` §3.3–3.4); traza hacia atrás desde ahí.
- **Transient symptom vs. persistent cause** — un síntoma puede desaparecer solo (timeout que se resuelve en el siguiente intento, pod que se reinicia) sin que la causa haya sido corregida; no confundas la desaparición del síntoma con la resolución de la causa.
- **Configuration drift** — diferencia entre lo que la configuración *debería* ser (template, IaC, valor esperado) y lo que efectivamente está activo en el entorno donde ocurrió el fallo; confírmalo con evidencia del entorno real, no con el archivo fuente de configuración.
- **Build-time vs. runtime** — un valor fijado en build-time puede no coincidir con el que el proceso usa en runtime (env var sobrescrita, imagen no reconstruida, config montada distinta a la esperada).

## Atribución al incidente concreto

En sistemas distribuidos, la distancia entre *"este mecanismo puede producir el síntoma"* y *"este mecanismo produjo esta ocurrencia"* es máxima: hay múltiples ejecuciones, réplicas y reintentos capaces de producir síntomas idénticos por causas distintas. Por eso aquí aplican con especial fuerza:

- **`COMPATIBLE_EXPLANATION != INCIDENT_ATTRIBUTION`** (`SKILL.md` §3.13)
- **`REPRODUCED_MECHANISM != HISTORICAL_PROOF`** (`SKILL.md` §3.14)

Evidencia que sostiene **atribución** (distinta de la que sostiene el mecanismo): correlation/execution/request/job IDs que atan los eventos a esa ocurrencia · timestamps dentro del intervalo real del fallo · identidad de ejecución (qué worker, pod, cuenta o credencial) · configuración efectiva *de esa ejecución concreta* · versión del artefacto realmente desplegado en ese momento (`SKILL.md` §4.2).

Sin al menos una de estas piezas, un mecanismo demostrado cierra como `ROOT_CAUSE_HIGH_CONFIDENCE`, no como `ROOT_CAUSE_CONFIRMED` (`SKILL.md` §8). Declara ambas dimensiones por separado cuando difieran (`SKILL.md` §8.1).

## Qué NO es esta reference

No es un runbook específico de AWS ni de ninguna plataforma concreta — los principios son transversales a cualquier proveedor/orquestador. No sustituye el `Preservar evidencia antes de mutar` de `runtime-and-logs.md`, que sigue aplicando a operaciones como restart/redeploy/rollback/requeue en este contexto.
