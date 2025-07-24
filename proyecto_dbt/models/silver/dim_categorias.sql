SELECT
    categoria_id,          
    TRIM(nombre) AS nombre_categoria, 
    descripcion            
FROM {{ ref('stg_categorias') }} 
WHERE categoria_id IS NOT NULL

-- Selecciona el ID único de la categoría
-- Selecciona el nombre de la categoría y elimina espacios en blanco al inicio/final
-- Selecciona la descripción de la categoría
-- Referencia al modelo staging (Bronze) de categorías
-- Filtra para asegurar que solo se incluyan categorías con un ID válido