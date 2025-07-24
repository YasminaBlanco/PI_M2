SELECT
    orden_metodo_id,
    orden_id,
    metodo_pago_id,
    monto_pagado
FROM {{ source('ecommerce_db', 'ordenes_metodos_pago') }}