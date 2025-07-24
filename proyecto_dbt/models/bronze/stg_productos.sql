SELECT
    producto_id,
    nombre,
    descripcion,
    precio,
    stock,
    categoria_id
FROM {{ source('ecommerce_db', 'productos') }}