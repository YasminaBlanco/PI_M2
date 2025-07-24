SELECT
    detalle_id,
    orden_id,
    producto_id,
    cantidad,
    precio_unitario
FROM {{ source('ecommerce_db', 'detalle_ordenes') }}