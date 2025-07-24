-- Modelo de agregación para identificar la intención de compra de productos basada en el carrito y MES.
-- Ideal para responder al KPI "¿Qué producto muestra mayor intención de compra por mes?".
SELECT
    fc.producto_id,
    fc.nombre_producto_final AS nombre_producto, -- Usamos el nombre histórico del producto
    fc.nombre_categoria_final AS nombre_categoria, -- Usamos el nombre histórico de la categoría
    DATE_TRUNC('month', fc.fecha_agregado_carrito)::DATE AS mes_orden,

    COUNT(DISTINCT fc.carrito_id) AS veces_agregado_al_carrito,
    SUM(fc.cantidad_agregada_carrito) AS cantidad_total_agregada_carrito,
    COUNT(DISTINCT fc.usuario_id) AS usuarios_con_intencion
FROM {{ ref('fact_carritos') }} fc
GROUP BY
    fc.producto_id,
    fc.nombre_producto_final,
    fc.nombre_categoria_final,
    DATE_TRUNC('month', fc.fecha_agregado_carrito)::DATE
ORDER BY
    mes_orden DESC,
    veces_agregado_al_carrito DESC,
    cantidad_total_agregada_carrito DESC