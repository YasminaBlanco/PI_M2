-- Modelo de agregación para calcular el crecimiento de ventas mensual de los productos.
-- Ideal para responder al KPI "¿Qué productos están creciendo más rápidamente en ventas?".

WITH ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', fo.fecha_orden) AS mes_orden,
        fo.producto_id,
        fo.nombre_producto_final AS nombre_producto,
        fo.nombre_categoria_final AS nombre_categoria,
        SUM(fo.subtotal_linea) AS ventas_mensuales
    FROM {{ ref('fact_ordenes') }} fo
    GROUP BY
        1,
        fo.producto_id,
        fo.nombre_producto_final, -- Agrupar por el nombre final
        fo.nombre_categoria_final -- Agrupar por el nombre final
),
ventas_con_periodo_anterior AS (
    -- Paso 2: Calcular ventas del mes anterior para cada producto
    SELECT
        vm.mes_orden,
        vm.producto_id,
        vm.nombre_producto,
        vm.nombre_categoria,
        vm.ventas_mensuales,
        LAG(vm.ventas_mensuales, 1) OVER (PARTITION BY vm.producto_id ORDER BY vm.mes_orden) AS ventas_mes_anterior
    FROM ventas_mensuales vm
)
SELECT
    vpa.mes_orden,
    vpa.producto_id,
    vpa.nombre_producto,
    vpa.nombre_categoria,
    vpa.ventas_mensuales,
    COALESCE(vpa.ventas_mes_anterior, 0) AS ventas_mes_anterior,
    CASE
        WHEN COALESCE(vpa.ventas_mes_anterior, 0) = 0 THEN NULL
        ELSE ((vpa.ventas_mensuales - vpa.ventas_mes_anterior) * 100.0) / vpa.ventas_mes_anterior
    END AS crecimiento_porcentual
FROM ventas_con_periodo_anterior vpa
WHERE vpa.mes_orden IS NOT NULL
  AND vpa.ventas_mensuales > 0
ORDER BY
    vpa.mes_orden DESC,
    crecimiento_porcentual DESC
    