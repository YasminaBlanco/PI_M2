SELECT
    detalle_o.detalle_id,
    o.orden_id,
    o.usuario_id,
    detalle_o.producto_id,
    detalle_o.cantidad,
    detalle_o.precio_unitario AS precio_unitario_orden,
    (detalle_o.cantidad * detalle_o.precio_unitario) AS subtotal_linea,
    o.fecha_orden::DATE AS fecha_orden,
    o.total AS total_orden,
    TRIM(o.estado) AS estado_orden,
    -- Usa COALESCE para obtener el nombre histórico si existe, de lo contrario, el actual
    COALESCE(ps.nombre, dp_actual.nombre_producto) AS nombre_producto_final,
    COALESCE(cs.nombre, dc_actual.nombre_categoria) AS nombre_categoria_final
FROM {{ ref('stg_detalle_ordenes') }} AS detalle_o
JOIN {{ ref('stg_ordenes') }} AS o ON detalle_o.orden_id = o.orden_id

-- 1. LEFT JOIN al snapshot de productos históricos (para el nombre en la fecha de la orden)
LEFT JOIN {{ source('dbt_snapshots', 'productos_historico') }} AS ps
    ON detalle_o.producto_id = ps.producto_id
    AND o.fecha_orden::DATE BETWEEN ps.dbt_valid_from::DATE AND COALESCE(ps.dbt_valid_to::DATE, '9999-12-31'::DATE)

-- 2. LEFT JOIN al snapshot de categorías históricas (para el nombre en la fecha de la orden)
LEFT JOIN {{ source('dbt_snapshots', 'categorias_historico') }} AS cs
    ON ps.categoria_id = cs.categoria_id -- Unimos desde el producto histórico
    AND o.fecha_orden::DATE BETWEEN cs.dbt_valid_from::DATE AND COALESCE(cs.dbt_valid_to::DATE, '9999-12-31'::DATE)

-- 3. LEFT JOIN a la dimensión de productos actual (para el nombre actual como fallback)
LEFT JOIN {{ ref('dim_productos') }} AS dp_actual
    ON detalle_o.producto_id = dp_actual.producto_id

-- 4. Left join a la dimensión de categorias actual (para el nombre actual como fallback)
LEFT JOIN {{ ref('dim_categorias') }} AS dc_actual
    ON dp_actual.categoria_id = dc_actual.categoria_id

WHERE detalle_o.orden_id IS NOT NULL
  AND detalle_o.producto_id IS NOT NULL
  AND detalle_o.cantidad > 0
  AND detalle_o.precio_unitario >= 0
  AND TRIM(o.estado) IN ('Completado', 'Enviado')