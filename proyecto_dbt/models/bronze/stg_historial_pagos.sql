SELECT
    pago_id,
    orden_id,
    metodo_pago_id,
    monto,
    fecha_pago,
    estado_pago
FROM {{ source('ecommerce_db', 'historial_pagos') }}