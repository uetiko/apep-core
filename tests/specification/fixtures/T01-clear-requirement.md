# T01 — Requisito claro

TIPO DE ENTRADA: necesidad del stakeholder (raw need), entregada por el owner del producto, que es quien decide.
TAREA: aplicar intake + ambiguity assessment y decidir el siguiente paso de la Línea 1.

---

Petición del owner (literal):

> Necesito que el rol **Operador** pueda exportar a CSV los widgets activos de su propia organización.
> - Filtro obligatorio: rango de fechas de creación (desde / hasta, ambos inclusive). El rango máximo es de 31 días; si se pide uno mayor, el sistema rechaza la exportación con el mensaje "El rango máximo es de 31 días".
> - Columnas, en este orden: id, nombre, fecha de creación (AAAA-MM-DD), categoría, estado.
> - Sólo widgets en estado Activo o Suspendido. Los Borrador no se exportan.
> - Si no hay widgets en el rango, se descarga un CSV sólo con la cabecera.
> - Separador coma, codificación UTF-8.
> - Otros roles no ven la opción. No hay que exportar widgets de otras organizaciones.
> - Éxito: cero solicitudes de exportación manual al equipo de soporte en el mes siguiente a la entrega.
> - Fuera de alcance: exportar a Excel nativo, programar exportaciones periódicas.
>
> Esto está decidido; no hace falta revisarlo de nuevo.
