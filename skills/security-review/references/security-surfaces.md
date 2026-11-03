# Security Surfaces

Aplica junto con `.omp/skills/security-review/SKILL.md` — no lo repite. Úsalo cuando el cambio toque una superficie concreta y haga falta saber **qué inspeccionar** en ella.

Carga sólo las secciones que el cambio realmente toca. Recorrer todas las superficies es ceremonia, no revisión (`SKILL.md` §4). Para decidir si lo que encuentres es un riesgo real, aplica `reachability-and-preconditions.md`.

Estas guías son **neutrales respecto de lenguaje y framework**. Las reglas concretas de un repositorio se obtienen de su gobernanza, su configuración y su código, no de aquí.

---

## Identidad, autorización y tenants

**Propiedades en juego:** integridad de la identidad autenticada · autorización · aislamiento entre tenants · frontera de privilegio.

Qué inspeccionar:

- **Autenticación** — ¿el cambio altera cómo se establece o se valida la identidad? Rutas nuevas sin el middleware habitual, excepciones añadidas a una lista de rutas públicas, verificación de token relajada, validación de firma/emisor/expiración/audiencia.
- **Autorización** — ¿se comprueba el permiso *después* de resolver el recurso? Un control que valida el rol pero no la propiedad del objeto permite IDOR. Condiciones invertidas, `OR` donde debía haber `AND`, un `return` temprano que salta la comprobación.
- **Aislamiento entre tenants** — el punto más crítico en sistemas multi-tenant: ¿de dónde sale el identificador de tenant? Si se acepta desde la petición en lugar de derivarse de la identidad autenticada, el bypass suele ser trivial. Revisa consultas nuevas que filtren por ID de recurso sin filtrar además por tenant.
- **Escalada de privilegio** — campos de rol/permiso asignables desde entrada de usuario; mass assignment sobre modelos con atributos sensibles.
- **Objetos indirectos** — identificadores secuenciales o adivinables expuestos y usados para recuperar recursos sin comprobar pertenencia.

Señal frecuente: el cambio añade un endpoint o una consulta **por analogía** con otro existente, pero copia la forma sin copiar el control.

---

## Entrada, ejecución e inyección

**Propiedades en juego:** integridad · frontera de ejecución de comandos · frontera de filesystem · frontera de confianza de red.

- **Inyección SQL** — concatenación o interpolación en consultas. Un ORM no inmuniza: revisa SQL crudo, fragmentos `where` construidos por cadena, nombres de tabla/columna dinámicos y cláusulas `ORDER BY` parametrizadas desde entrada.
- **Inyección de comandos** — invocación de shell con argumentos construidos desde entrada. Distingue ejecución con shell (vulnerable a metacaracteres) de ejecución con lista de argumentos (mucho más segura). Ver `SKILL.md` §5.5: la sola presencia de ejecución no es un finding.
- **Inyección de plantilla** — entrada de usuario que llega al *código* de la plantilla en vez de a sus datos.
- **Path traversal** — rutas de filesystem construidas con entrada de usuario. Comprueba si hay normalización y si la comprobación de contención ocurre **después** de resolver la ruta, no antes.
- **SSRF** — URLs de destino influidas por entrada. Importa si el cliente sigue redirecciones, si acepta esquemas no HTTP, y si el runtime tiene acceso a metadatos de instancia o a red interna: eso decide el impacto.
- **Deserialización y evaluación dinámica** — deserializar formatos que pueden instanciar tipos arbitrarios, o evaluar código/expresiones desde entrada.
- **Codificación de salida** — datos controlados por el usuario reflejados en HTML, cabeceras, logs estructurados o respuestas, sin la codificación del contexto de destino.

Para todas: identifica el sink concreto y demuestra la propagación desde una fuente controlable. Sin eso es `SECURITY_SMELL`, no `EXPLOITABLE_RISK`.

---

## Secretos, datos sensibles y divulgación

**Propiedades en juego:** confidencialidad · confidencialidad de un secreto.

- **Secretos en el cambio** — credenciales, tokens, claves privadas o cadenas de conexión añadidas al repositorio. **Clasifica antes de alarmar** (placeholder, ejemplo, fixture, inactivo, activo, desconocido) — ver `reachability-and-preconditions.md`.
- **Secretos en lugares equivocados** — credenciales en código en lugar de en un gestor de secretos, o inyectadas en imágenes/artefactos de build.
- **Datos sensibles en logs** — el cambio añade logging que incluye credenciales, tokens, PII, datos de pago o cuerpos completos de petición/respuesta. Revisa también el logging de excepciones: suele arrastrar el payload entero.
- **Divulgación por errores** — trazas de pila, mensajes de base de datos o rutas internas devueltas al cliente; modo debug activado en una configuración destinada a producción.
- **Exposición de datos en respuestas** — serializadores que devuelven el objeto completo y arrastran campos internos (hashes, flags de rol, identificadores de otros tenants) al añadir un campo nuevo al modelo.
- **Almacenamiento y transmisión** — datos sensibles persistidos sin protección esperada, o transmitidos por canales sin cifrar cuando la política aplicable lo exige.

---

## Configuración, permisos e infraestructura

**Propiedades en juego:** frontera de privilegio · frontera de confianza de red · confidencialidad · integridad.

- **IAM y policies** — permisos añadidos o ampliados. Aplica `BROAD_PERMISSION != EXPLOITABLE_RISK` y determina quién, sobre qué, desde dónde y con qué impacto (`reachability-and-preconditions.md`).
- **Exposición de red** — security groups, reglas de entrada, balanceadores o buckets que pasan de privado a público; rangos `0.0.0.0/0` añadidos; endpoints internos publicados.
- **Configuración por defecto** — cambios que desactivan verificación de certificados, validación de firma, autenticación en un entorno, o que activan CORS permisivo (`*` con credenciales).
- **Almacenamiento** — buckets, volúmenes o bases de datos con acceso público, cifrado desactivado o política de acceso ampliada.
- **Criptografía** — algoritmos o modos débiles, IV/nonce reutilizados o fijos, aleatoriedad no criptográfica para tokens o identificadores de sesión, comparación de secretos no resistente a temporización. Evalúa el uso real, no la preferencia de algoritmo.
- **Dependencias** — cambios de versión o dependencias nuevas: distingue advisory de riesgo alcanzable (`reachability-and-preconditions.md`).
- **Superficie de build y CI** — credenciales expuestas a pasos no confiables, o ejecución de código desde fuentes no verificadas durante el build.

---

## Qué NO es esta reference

No es un catálogo de cumplimiento ni una checklist que deba recorrerse entera. No define política organizacional de seguridad, no establece controles obligatorios, y no sustituye la gobernanza de seguridad de ningún repositorio. Es material de apoyo para saber dónde mirar cuando el cambio ya señaló una superficie.
