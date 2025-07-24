SELECT
    p.producto_id,                 
    TRIM(p.nombre) AS nombre_producto, 
    p.descripcion AS descripcion_producto,
    p.precio AS precio_unitario_actual,
    p.stock AS stock_actual,           
    p.categoria_id,                    
    c.nombre_categoria                 
FROM {{ ref('stg_productos') }} p     
LEFT JOIN {{ ref('dim_categorias') }} c ON p.categoria_id = c.categoria_id 
WHERE p.producto_id IS NOT NULL       
  AND p.precio IS NOT NULL            
  AND p.precio >= 0

  -- Selecciona el ID único del producto
-- Selecciona el nombre del producto y elimina espacios en blanco
-- Selecciona el precio actual de venta del producto
-- Selecciona el stock disponible del producto
-- Selecciona el ID de la categoría a la que pertenece el producto
-- Selecciona el nombre de la categoría, unida desde la tabla dim_categorias
-- Referencia al modelo staging (Bronze) de productos, aliased como 'p'
-- Une con la dimensión de categorías para obtener el nombre de la categoría
-- Filtra para asegurar que el producto_id no sea nulo
-- Asegura que el precio del producto no sea nulo
-- Asegura que el precio del producto sea un valor válido (no negativo)