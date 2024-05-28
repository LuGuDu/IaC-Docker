# Usa una imagen base con Python y OpenCV
FROM python:3.8-slim

# Instala las dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crea un directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

