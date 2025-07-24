# Usar una imagen base de Python
FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /app/streamlit

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script de la aplicación Streamlit
COPY app.py .

# Exponer el puerto de Streamlit
EXPOSE 8501