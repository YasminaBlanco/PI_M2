SELECT
    metodo_pago_id,
    nombre,
    descripcion
FROM {{ source('ecommerce_db', 'metodos_pago') }}