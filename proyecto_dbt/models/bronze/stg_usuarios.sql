SELECT
    usuario_id,
    nombre,
    apellido,
    dni,
    email,
    contraseña,
    fecha_registro
FROM {{ source('ecommerce_db', 'usuarios') }}