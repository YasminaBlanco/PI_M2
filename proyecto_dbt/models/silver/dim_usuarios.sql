SELECT
    usuario_id,
    TRIM(nombre) AS nombre_usuario, 
    TRIM(apellido) AS apellido_usuario, 
    TRIM(email) AS email_usuario,     
    fecha_registro::DATE AS fecha_registro 
FROM {{ ref('stg_usuarios') }}     
WHERE usuario_id IS NOT NULL       
  AND email IS NOT NULL            

-- Selecciona el ID único del usuario
-- Selecciona el nombre del usuario y elimina espacios en blanco
-- Selecciona el apellido del usuario y elimina espacios en blanco
-- Selecciona el correo electrónico del usuario y elimina espacios en blanco
-- Selecciona la fecha de registro y la convierte explícitamente a tipo DATE
    -- La columna 'contraseña' de la fuente se omite aquí por seguridad y privacidad,     
    -- ya que no es relevante para el análisis de negocio y no debe almacenarse en texto plano.
-- Referencia al modelo staging (Bronze) de usuarios
-- Filtra para asegurar que el usuario_id no sea nulo
-- Asegura que el email del usuario no sea nulo, ya que es una clave importante
