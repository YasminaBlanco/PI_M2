SELECT
    direccion_id,
    usuario_id,
    calle,
    ciudad,
    departamento,
    provincia,
    distrito,
    estado,
    codigo_postal,
    pais
FROM {{ source('ecommerce_db', 'direcciones_envio') }}