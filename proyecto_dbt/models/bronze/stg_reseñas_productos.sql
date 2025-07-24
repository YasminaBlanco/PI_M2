SELECT
    reseña_id,
    usuario_id,
    producto_id,
    calificacion,
    comentario,
    fecha
FROM {{ source('ecommerce_db', 'reseñas_productos') }}