import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

# Leer variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Usar pg8000 como driver
DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
# Crear engine y sesión
    engine = create_engine(DATABASE_URL, echo=False, client_encoding='utf8')
    print("Motor de base de datos creado")
except Exception as e:
    print(f"Error al crear motor de base de datos: {e}")
    raise

Base = declarative_base()
DbSesion = sessionmaker(bind=engine)

def get_db_engine():
    return engine

def get_db_session():
    return DbSesion()

def get_db_connection():
    return engine.connect()
