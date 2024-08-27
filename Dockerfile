# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos requirements.txt si existen
COPY requirements.txt requirements.txt

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta actual a /app en el contenedor
COPY . .

# Ejecuta el script scraper.py para poblar la base de datos
RUN python scraper.py

# Comando por defecto para ejecutar la API
CMD ["python", "app.py"]
