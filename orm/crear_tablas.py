from db_conector import get_db_engine, Base
import modelo_tablas

def crear_tablas():
    engine = get_db_engine()

    try: 
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        raise

if __name__ == "__main__":
    crear_tablas()