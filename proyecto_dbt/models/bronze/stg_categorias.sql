SELECT
    categoria_id,
    nombre,
    descripcion
FROM {{ source('ecommerce_db', 'categorias') }}