-- snapshots/productos_historico.sql
{% snapshot productos_historico %}

{{ 
    config(
        target_schema='dbt_snapshots',
        unique_key='producto_id',
        strategy='check',
        check_cols=['nombre', 'descripcion', 'precio', 'stock', 'categoria_id']
    )
}}

SELECT
    producto_id,
    nombre,
    descripcion,
    precio,
    stock,
    categoria_id
FROM {{ ref('stg_productos') }}

{% endsnapshot %}