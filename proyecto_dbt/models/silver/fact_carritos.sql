SELECT
    c.carrito_id,
    c.usuario_id,
    c.producto_id,
    c.cantidad AS cantidad_agregada_carrito,
    c.fecha_agregado::DATE AS fecha_agregado_carrito,
    -- Usa COALESCE para obtener el nombre histórico si existe, de lo contrario, el actual
    COALESCE(ps.nombre, dp_actual.nombre_producto) AS nombre_producto_final,
    COALESCE(cs.nombre, dc_actual.nombre_categoria) AS nombre_categoria_final
FROM {{ ref('stg_carrito') }} c

-- UNIÓN AL SNAPSHOT DE PRODUCTOS (SCD Tipo 2):**
LEFT JOIN {{ source('dbt_snapshots', 'productos_historico') }} AS ps
    ON c.producto_id = ps.producto_id
    -- La clave para SCD Tipo 2: unirse a la versión del producto que era válida en la fecha del carrito
    AND c.fecha_agregado::DATE BETWEEN ps.dbt_valid_from::DATE AND COALESCE(ps.dbt_valid_to::DATE, '9999-12-31'::DATE)

-- UNIÓN AL SNAPSHOT DE CATEGORÍAS (SCD Tipo 2):**
LEFT JOIN {{ source('dbt_snapshots', 'categorias_historico') }} AS cs
    ON ps.categoria_id = cs.categoria_id -- Usamos el categoria_id que viene del snapshot de productos (ps)
    -- La clave para SCD Tipo 2: unirse a la versión de la categoría que era válida en la fecha del carrito
    AND c.fecha_agregado::DATE BETWEEN cs.dbt_valid_from::DATE AND COALESCE(cs.dbt_valid_to::DATE, '9999-12-31'::DATE)

LEFT JOIN {{ ref('dim_productos') }} AS dp_actual
    ON c.producto_id = dp_actual.producto_id

LEFT JOIN {{ ref('dim_categorias') }} AS dc_actual
    ON dp_actual.categoria_id = dc_actual.categoria_id

WHERE c.carrito_id IS NOT NULL
  AND c.usuario_id IS NOT NULL
  AND c.producto_id IS NOT NULL
  AND c.cantidad > 0

-- ID único del registro del carrito
-- ID del usuario propietario del carrito
-- ID del producto agregado al carrito
-- Cantidad de este producto agregada al carrito
-- Fecha en que el producto fue agregado al carrito, convertida a tipo DATE
-- Nombre del producto, unido desde la dimensión de productos
-- Nombre de la categoría del producto, unido desde la dimensión de productos
-- Referencia al modelo staging (Bronze) de carrito, aliased como 'c'
-- Une con la dimensión de productos (Silver) para obtener el nombre y categoría
-- Asegura que el registro del carrito tenga un ID válido
-- Asegura que el registro del carrito esté asociado a un usuario válido
-- Asegura que el registro del carrito tenga un producto válido
-- Asegura que la cantidad agregada sea positiva
