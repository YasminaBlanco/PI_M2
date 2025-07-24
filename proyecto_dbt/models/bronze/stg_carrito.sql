SELECT
    carrito_id,
    usuario_id,
    producto_id,
    cantidad,
    fecha_agregado
FROM {{ source('ecommerce_db', 'carrito') }}