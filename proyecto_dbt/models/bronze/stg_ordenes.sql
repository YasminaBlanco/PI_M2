SELECT
    orden_id,
    usuario_id,
    fecha_orden,
    total,
    estado
FROM {{ source('ecommerce_db', 'ordenes') }}