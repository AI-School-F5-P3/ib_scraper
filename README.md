# Quote Scraper

Este proyecto es un scraper automatizado que extrae citas de la página web [https://quotes.toscrape.com](https://quotes.toscrape.com) y las almacena en una base de datos PostgreSQL. El scraper está diseñado para ejecutarse inicialmente y luego actualizarse automáticamente a intervalos regulares.

## Características

- Extrae citas, autores y etiquetas de [https://quotes.toscrape.com]
- Almacena los datos en una base de datos PostgreSQL
- Actualizaciones automáticas programadas
- Manejo de errores y registro de actividades

## Requisitos

- Python 3.x
- PostgreSQL

## Instalación

1. Clona este repositorio:
git clone [URL_DEL_REPOSITORIO]

2. Instala las dependencias:
pip install -r requirements.txt

3. Configura las variables de entorno en un archivo `.env`:
DB_NAME=nombre_de_tu_base_de_datos

DB_USER=tu_usuario

DB_PASSWORD=tu_contraseña

DB_HOST=localhost

DB_PORT=5432

UPDATE_INTERVAL=24


## Uso

Ejecuta el script principal:
python scraper.py

El scraper realizará una extracción inicial y luego se programará para actualizaciones automáticas según el intervalo especificado en las variables de entorno.

## Estructura del Proyecto

- `scraper.py`: Contiene la lógica principal del scraper y la actualización automática.
- `requirements.txt`: Lista de dependencias del proyecto.
- `scraper.log`: Archivo de registro que se genera durante la ejecución.