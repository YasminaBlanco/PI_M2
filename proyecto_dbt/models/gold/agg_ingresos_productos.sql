-- Modelo de agregación para calcular los ingresos totales generados por cada producto y MES.
-- Ideal para responder al KPI "¿Qué producto genera más ingresos totales por mes?".
SELECT
    fo.producto_id,
    fo.nombre_producto_final AS nombre_producto, -- Usamos el nombre histórico del producto
    fo.nombre_categoria_final AS nombre_categoria, -- Usamos el nombre histórico de la categoría
    DATE_TRUNC('month', fo.fecha_orden)::DATE AS mes_orden,

    SUM(fo.subtotal_linea) AS ingresos_totales
FROM {{ ref('fact_ordenes') }} fo
GROUP BY
    fo.producto_id,
    fo.nombre_producto_final,
    fo.nombre_categoria_final,
    DATE_TRUNC('month', fo.fecha_orden)::DATE
ORDER BY
    mes_orden DESC,
    ingresos_totales DESC