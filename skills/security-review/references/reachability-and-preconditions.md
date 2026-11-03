# Reachability and Preconditions

Aplica junto con `.omp/skills/security-review/SKILL.md` — no lo repite. Úsalo cuando haya que decidir si un patrón sospechoso constituye un riesgo real.

Esta reference es el motor anti-especulación de la skill. Su única pregunta es:

`¿Puede esto ocurrir de verdad, y qué tendría que ser cierto para que ocurriera?`

## La cadena que hay que demostrar

Para pasar de `CODE_PATTERN_PRESENT` a `SECURITY_PATH_REACHABLE` hacen falta los cuatro eslabones:

1. **Control del atacante** — ¿existe una entrada que un actor no confiable controla realmente? Identifica el punto de entrada concreto (parámetro, header, body, mensaje de cola, archivo subido, variable de entorno, registro de base de datos escrito por un usuario), no "una entrada" en abstracto.
2. **Propagación** — ¿ese valor llega al sink sin transformarse en algo inocuo? Sigue el dato. Una normalización, un parseo a entero, un mapeo a enum o una whitelist intermedia pueden cortar la cadena.
3. **Control ausente o insuficiente** — ¿qué defensa existe ya, y por qué no basta? Un control que existe y es suficiente convierte la hipótesis en `REJECTED_SECURITY_HYPOTHESIS`. Inspecciona los controles **adyacentes**, no sólo la línea del sink: middleware, decoradores, validación en el borde, políticas del framework.
4. **Ejecución alcanzable** — ¿el código se ejecuta en una ruta que el atacante puede activar? Código muerto, una rama tras un feature flag apagado, un endpoint no registrado o un script que nadie invoca no son alcanzables.

Si un eslabón no puede demostrarse, el resultado **no** es `CONFIRMED_SECURITY_FINDING`.

## Clasificación de precondiciones

| Estado | Cuándo |
|---|---|
| `CONFIRMED` | Verificada directamente con evidencia (código leído, configuración inspeccionada, policy consultada, test ejecutado). |
| `SUPPORTED` | La evidencia apunta fuertemente a ella, pero no se verificó de forma directa. |
| `UNCONFIRMED` | No se pudo verificar con el acceso disponible. Limita el estado y la severidad del finding. |
| `REJECTED` | La evidencia la contradice. Corta la hipótesis. |

Una hipótesis cuya precondición crítica es `UNCONFIRMED` produce como mucho `SUPPORTED_SECURITY_CONCERN`, nunca un finding confirmado, y **nunca** se redacta como si la precondición fuera cierta.

## Secretos: parecer no es ser

Una cadena que parece un token **no es** automáticamente un secreto activo expuesto. Clasifícala antes de afirmar nada:

placeholder · valor de ejemplo en documentación · fixture de test · credencial inactiva o revocada · **secreto activo** · desconocido.

Señales útiles: ubicación (¿archivo de test, plantilla, `.env.example`?), forma (¿longitud y alfabeto plausibles?), historia (¿cuándo entró?, ¿se rotó después?), y si algún código lo consume realmente.

**Si no puedes verificar que está activo, no afirmes exposición activa como `FACT`.** Repórtalo como `SUPPORTED_SECURITY_CONCERN` indicando exactamente qué falta por comprobar — normalmente, una verificación que corresponde a una persona con acceso al proveedor.

Nunca intentes usar la credencial para comprobar si funciona: eso es explotación activa (`SKILL.md` §13).

## Permisos e IAM: amplitud no es explotabilidad

> **`BROAD_PERMISSION != EXPLOITABLE_RISK`**

Para evaluar un permiso, determina: **quién** lo obtiene (rol, principal, servicio) · **sobre qué recurso** (¿acotado o comodín?) · **desde qué runtime** se asume · **qué path puede invocarlo** · **qué impacto** tendría su abuso.

Un permiso amplio con recurso comodín asumible desde un runtime alcanzable por entrada no confiable es materialmente distinto de uno amplio en un rol de despliegue que sólo asume la CI.

`EXCESSIVE_PERMISSION` puede ser un finding real **aunque no exista un exploit externo inmediato** — por ejemplo, porque amplía el radio de alcance de cualquier compromiso posterior. Pero eso hay que **explicarlo materialmente**, no asumirlo por la sola presencia de un comodín.

## Dependencias: advisory no es riesgo

Distingue:

| | |
|---|---|
| `PACKAGE VERSION PRESENT` | La versión afectada está en el árbol de dependencias |
| `VULNERABLE AND REACHABLE DEPENDENCY` | La ruta vulnerable se ejecuta de verdad en esta aplicación |

Una advisory por sí sola no demuestra riesgo material en el producto. Comprueba, en la medida de lo razonable: si la dependencia es directa o transitiva · si la función afectada se usa · si la configuración vulnerable aplica · si es dependencia de producción o sólo de desarrollo/test.

Usa el tooling local cuando pueda verificarlo (lockfiles, árbol de dependencias, herramientas de auditoría del repositorio). **No inventes CVEs ni identificadores de advisory.** No hagas investigación en red salvo que el contexto lo autorice y la consulta sea necesaria; si no puedes verificarlo, es `UNCONFIRMED`.

## Endpoints y exposición de red

No infieras que un endpoint es alcanzable externamente porque exista una ruta. Comprueba lo que puedas: registro de la ruta · middleware de autenticación aplicable · configuración de red o del balanceador · si está tras VPN, security group o autorizador.

Si la exposición no puede verificarse, es una precondición `UNCONFIRMED` — dilo, y ajusta el estado del finding en consecuencia.

## Cuándo parar

Detente y reporta con lo que tienes cuando confirmar el finding exigiría explotación activa, payload destructivo, acceso no autorizado, modificación de datos o prueba ofensiva real (`SKILL.md` §13). La respuesta correcta en ese punto es `SUPPORTED_SECURITY_CONCERN` o `INSUFFICIENT_EVIDENCE` con la pieza exacta que falta — no un finding confirmado redactado con seguridad prestada.
