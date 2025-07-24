{{ config(
    materialized='table'
) }}

-- Modelo combinado que une las métricas de ingresos, crecimiento e intención de compra por producto.
-- Ideal para análisis cruzados de KPIs y para dashboards de alto nivel.
WITH base_productos_mensual AS (
    -- Obtener una lista única de productos y meses con sus nombres históricos
    -- de todos los modelos de agregación para asegurar que se incluyan todos los productos que aparecen en cualquier métrica.
    SELECT
        producto_id,
        nombre_producto,
        nombre_categoria,
        mes_orden
    FROM {{ ref('agg_ingresos_productos') }}
    UNION ALL
    SELECT
        producto_id,
        nombre_producto,
        nombre_categoria,
        mes_orden
    FROM {{ ref('agg_crecimiento_ventas_productos') }}
    UNION ALL
    SELECT
        producto_id,
        nombre_producto,
        nombre_categoria,
        mes_orden
    FROM {{ ref('agg_intencion_compra_productos') }}
    GROUP BY 1,2,3,4 -- Asegurar unicidad de producto_id, nombre_producto, nombre_categoria, mes_orden
),
-- NUEVA CTE: Asegura la unicidad de la combinación de todas las métricas antes del SELECT final
final_unique_data AS (
    SELECT
        bpm.producto_id,
        bpm.nombre_producto,
        bpm.nombre_categoria,
        bpm.mes_orden,
        COALESCE(ingresos_productos.ingresos_totales, 0) AS ingresos_totales,
        COALESCE(crecimiento_productos.crecimiento_porcentual, 0) AS crecimiento_porcentual_ventas,
        COALESCE(intencion_compra.veces_agregado_al_carrito, 0) AS veces_agregado_al_carrito,
        COALESCE(intencion_compra.cantidad_total_agregada_carrito, 0) AS cantidad_total_agregada_carrito,
        RANK() OVER (PARTITION BY bpm.mes_orden ORDER BY COALESCE(ingresos_productos.ingresos_totales, 0) DESC) AS rank_ingresos_totales,
        RANK() OVER (PARTITION BY bpm.mes_orden ORDER BY COALESCE(crecimiento_productos.crecimiento_porcentual, 0) DESC) AS rank_crecimiento_ventas,
        RANK() OVER (PARTITION BY bpm.mes_orden ORDER BY COALESCE(intencion_compra.veces_agregado_al_carrito, 0) DESC) AS rank_veces_agregado_carrito
    FROM base_productos_mensual bpm
    LEFT JOIN {{ ref('agg_crecimiento_ventas_productos') }} crecimiento_productos
        ON bpm.producto_id = crecimiento_productos.producto_id
        AND bpm.mes_orden = crecimiento_productos.mes_orden
    LEFT JOIN {{ ref('agg_ingresos_productos') }} ingresos_productos
        ON bpm.producto_id = ingresos_productos.producto_id
        AND bpm.mes_orden = ingresos_productos.mes_orden
    LEFT JOIN {{ ref('agg_intencion_compra_productos') }} intencion_compra
        ON bpm.producto_id = intencion_compra.producto_id
        AND bpm.mes_orden = intencion_compra.mes_orden
)
SELECT *
FROM final_unique_data
GROUP BY
    producto_id,
    nombre_producto,
    nombre_categoria,
    mes_orden,
    ingresos_totales,
    crecimiento_porcentual_ventas,
    veces_agregado_al_carrito,
    cantidad_total_agregada_carrito,
    rank_ingresos_totales,
    rank_crecimiento_ventas,
    rank_veces_agregado_carrito
ORDER BY
    mes_orden DESC,
    ingresos_totales DESC,
    crecimiento_porcentual_ventas DESC,
    veces_agregado_al_carrito DESC