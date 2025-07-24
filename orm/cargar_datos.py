import os
from db_conector import get_db_connection
from sqlalchemy import text

# Ruta a la carpeta donde tienes los archivos SQL
RUTA_SQL = os.path.join(os.path.dirname(__file__), 'sql')

# Archivos ordenados
archivos_sql = [
    '2.usuarios.sql',
    '3.categorias.sql',
    '4.productos.sql',
    '5.ordenes.sql',
    '6.detalle_ordenes.sql',
    '7.direcciones_envio.sql',
    '8.carrito.sql',
    '9.metodos_pago.sql',
    '10.ordenes_metodospago.sql',
    '11.resenas_productos.sql',
    '12.historial_pagos.sql'
]

def ejecutar_scripts_sql():
    conn = get_db_connection()
    trans = conn.begin()
    try:
        for archivo in archivos_sql:
            ruta_completa = os.path.join(RUTA_SQL, archivo)
            print(f"--> Ejecutando script: {archivo}")
            with open(ruta_completa, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                if sql_script.strip():
                    conn.execute(text(sql_script))
        trans.commit()
        print("\n✅ Todos los archivos .sql ejecutados correctamente.\n")
    except Exception as e:
        trans.rollback()
        print(f"❌ Error ejecutando {archivo}: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    ejecutar_scripts_sql()