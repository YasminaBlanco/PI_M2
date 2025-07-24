-- snapshots/categorias_historico.sql
{% snapshot categorias_historico %}

{{ 
    config(
        target_schema='dbt_snapshots',
        unique_key='categoria_id',
        strategy='check',
        check_cols=['nombre']
    )
}}

-- Selecciona los datos base de tu tabla staging de categorías
SELECT
    categoria_id,
    nombre
FROM {{ ref('stg_categorias') }}

{% endsnapshot %}