# Proyecto Integrador: 

Este proyecto es una solución integral para el análisis de Key Performance Indicators (KPIs) de productos de un e-commerce. Combina un pipeline de datos robusto con una aplicación interactiva para visualizar métricas clave y obtener insights sobre el rendimiento de los productos.

## 🎯 Objetivos del Proyecto

Este Proyecto Integrador (PI) se ha desarrollado con los siguientes objetivos clave:

* **Identificar los datos necesarios** para responder preguntas de negocio a partir de una sábana de datos a fin de cumplir los objetivos clave del negocio.
* **Utilizar SQL para realizar transformaciones de datos** utilizando la metodología de transformación por capas o arquitectura tipo medallón.
* **Modelar datos utilizando modelado dimensional** y siguiendo buenas prácticas de trabajo como recopilación de requisitos empresariales, definición de la granularidad, identificación de hechos e identificación de dimensiones.
* **Diseñar e implementar un modelo de datos dimensional** utilizando Slowly Changing Dimensions (SCDs) y gestionar las transformaciones con dbt.
* **Diseñar e implementar KPIs y métricas** para identificar patrones que ayuden a responder las preguntas de negocio.

## 🚀 Características Principales

* **Extracción y Carga de Datos:** Herramientas para cargar datos iniciales en la base de datos.
* **Transformación de Datos con dbt:** Modelos de datos definidos con dbt (Data Build Tool) para transformar datos crudos en métricas de negocio listas para el análisis.
* **Análisis de KPIs:** Cálculo y seguimiento de métricas como ingresos totales, crecimiento porcentual de ventas e intención de compra (productos agregados al carrito).
* **Dashboard Interactivo con Streamlit:** Una aplicación web intuitiva que permite a los usuarios explorar los KPIs, filtrar por mes y categoría, e identificar tendencias y oportunidades.
* **Conectividad con PostgreSQL:** Utiliza PostgreSQL como base de datos para almacenar y gestionar los datos.

## 🛠️ Tecnologías Utilizadas

* **Python:** Lenguaje principal para scripting, conectividad a la base de datos y la aplicación Streamlit.
* **Streamlit:** Framework para construir la aplicación interactiva del dashboard.
* **dbt (Data Build Tool):** Para la orquestación y transformación de datos en el almacén de datos.
* **PostgreSQL:** Sistema de gestión de bases de datos relacionales.
* **Pandas:** Biblioteca para manipulación y análisis de datos en Python.
* **Altair:** Biblioteca de visualización declarativa para Python, utilizada en Streamlit.
* **`.env`:** Para la gestión segura de variables de entorno (credenciales de base de datos).
* **Docker / Docker Compose:** Para la contenerización y orquestación de los servicios (base de datos, aplicación).

## 📂 Estructura del Proyecto

```
├── dbt_profiles/               # Configuración de perfiles de dbt
│    └── profiles.yml           # Perfil de dbt para la base de datos
├── proyecto_dbt/               # Scripts de dbt para la base de datos
│    └── models/
│           └── bronze/
│               └── sources.yml # Configuración de fuentes de datos
│               └── stg.sql     # Modelos stg en .sql   
│           └── silver/
│               └── dim_productos.sql     # Modelos dim en .sql
│               └── dim_categorias.sql     # Modelos dim en .sql
│               └── fact_carritos.sql # Modelo de datos de carritos
│               └── fact_ordenes.sql # Modelo de datos de ordenes
│               └── fact_productos.sql # Modelo de datos de productos
│           └── gold/
│               └── agg_crecimiento_ventas_productos.sql    # Modelo de agregación de KPIs
│               └── agg_ingresos_productos.sql              # Modelo de agregación de KPIs
│               └── agg_intencion_compra_productos.sql      # Modelo de agregación de KPIs
│               └── rpt_analisis_productos_kpis.sql         # Modelo principal de KPIs
│    └── macros/        # Macros de dbt para test
│    └── snapshots/     # Snapshots de historial de cambios
│    └── readme.md      # Archivo de documentación para dbt
├── init-scripts/               # Scripts SQL para inicialización de la base de datos
│   └── 01-EcommerceDB.sql      # Script de creación de esquema y tablas
├── orm/                        # Módulo de Object-Relational Mapping y scripts de datos
│   ├── cargar_datos.py         # Script para cargar datos en la DB
│   ├── crear_tablas.py         # Script para crear tablas (si no se usa init-scripts)
│   ├── db_conector.py          # Módulo de conexión a la base de datos
│   ├── exploracion_tablas.py   # Script para explorar las tablas de la base de datos
│   ├── modelo_tablas.py        # Definición de modelos de tablas
│   ├── readme.md               # Archivo de documentación para el orm
├── streamlit/                  # Aplicación Streamlit
│   ├── app.py                  # Código principal de la aplicación Streamlit
│   ├── Dockerfile              # Dockerfile para la aplicación Streamlit
│   └── requirements.txt        # Dependencias de Python para Streamlit
├── docker-compose.yml          # Configuración de Docker Compose
├── Dockerfile                  # Dockerfile para el proyecto
└── README.md                   # Este archivo
```

## ⚙️ Configuración y Ejecución (Orden de Pasos)

Para poner en marcha este proyecto, sigue los siguientes pasos en el orden indicado:

### 1. Creación de entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate # En Linux/macOS
.venv\Scripts\activate   # En Windows
```

Luego, instala las dependencias generales del proyecto que estan en el archivo `requirements.txt` en la raíz del proyecto, con los siguientes comandos:

```bash
pip install -r requirements.txt
```

### 2. Variables de Entorno

Copia el archivo `.env.example` a `.env` en la **raíz del proyecto**, en la carpeta **`orm/`** y en la carpeta de **`streamlit/`** . Edita ambos archivos `.env` con tus credenciales de base de datos y otras configuraciones necesarias. 

```
# Ejemplo de .env.example
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=your_db_port

PGADMIN_DEFAULT_EMAIL=your_pgadmin_email
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password

DBT_PROFILES_DIR=/root/.dbt
```

### 3. Levantamiento de la Base de Datos con Docker

Asegúrate de tener Docker y Docker Compose instalados. Desde la raíz del proyecto, levanta los contenedores definidos en `docker-compose.yml`. Esto iniciará tu base de datos PostgreSQL
y creará los contenedores de dbt (la carpeta `proyecto_dbt/`) y Streamlit.

```bash
docker-compose up --build -d
```
Verifica que el contenedor de la base de datos (`db`) esté en ejecución.

### 4 👉[Configuración y Carga de Datos Iniciales](orm/readme.md)👈 (hacer click para ir a la sección)

Esta sección se encarga de preparar la base de datos y cargar los datos iniciales.

* **Creación de Tablas:** Ejecutar el script `crear_tablas.py` para definir el esquema de tu base de datos.
    ```bash
    cd orm
    python crear_tablas.py
    ```
* **Carga de Datos:** Ejecuta el script `cargar_datos.py` para poblar la base de datos con los datos iniciales necesarios.
    ```bash
    python cargar_datos.py
    ```

### 5. 👉[Ejecución de Modelos dbt](proyecto_dbt/readme.md)👈 (hacer click para ir a la sección)

Una vez que la base de datos esté poblada, navega al contenedor desde la consola bash para transformar tus datos.
Con los siguientes comandos:
```bash
docker exec -it dbt_container bash
cd ecommerce
dbt init ecommerce_project
```
* Llenar las carpeta de models, macros, snapshots con los script propuestos en la carpeta `project_dbt/` luego de ejecutar los siguientes comandos:

```bash
dbt deps
dbt compile
dbt snapshot
dbt debug
dbt run --full-refresh
dbt test
dbt docs generate
dbt docs serve
```

### 6. Ejecución de la Aplicación Streamlit

La aplicación Streamlit se iniciará automáticamente como parte de la orquestación de contenedores. Podrás acceder al dashboard en tu navegador normalmente `http://localhost:8501`.
