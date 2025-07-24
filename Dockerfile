# Imagen base de python
FROM python:3.10

# Instala dbt para PostgreSQL
RUN pip install dbt-postgres

# Establece el directorio de trabajo
WORKDIR /app
