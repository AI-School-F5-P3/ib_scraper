# Quote Scraper

Este proyecto es un scraper automatizado que extrae citas de la página web [https://quotes.toscrape.com](https://quotes.toscrape.com) y las almacena en una base de datos PostgreSQL. El scraper está diseñado para ejecutarse inicialmente y luego actualizarse automáticamente a intervalos regulares.

## Características

- Extrae citas, autores y etiquetas de [https://quotes.toscrape.com]
- Almacena los datos en una base de datos PostgreSQL
- Actualizaciones automáticas programadas
- Proporciona una API para obtener citas a través de solicitudes HTTP GET.

## Requisitos

- Python 3.12
- PostgreSQL

## Instalación

1. Clona este repositorio:
git clone [URL_DEL_REPOSITORIO]

2. Instala las dependencias:
`pip install -r requirements.txt`

3. Configura las variables de entorno en un archivo `.env`:

DB_NAME=nombre_de_tu_base_de_datos

DB_USER=tu_usuario

DB_PASSWORD=tu_contraseña

DB_HOST=localhost

DB_PORT=5432

UPDATE_INTERVAL=24


## Uso

- Ejecuta el script principal para realizar una extracción inicial y almacenar las citas obtenidas en una base de datos PostgreSQL. Además, se programará para realizar actualizaciones automáticas según el intervalo especificado en las variables de entorno:
`python scraper.py`

- Ejecuta el script para iniciar la aplicación Flask, que proporcionará una página web simple con una cita aleatoria y un botón "Nueva Cita" para cambiar a otra cita aleatoria:
`python app.py`


## Estructura del Proyecto

- `requirements.txt`: Lista de dependencias del proyecto.
- `scraper.py`: Contiene la lógica principal del scraper y la funcionalidad actualización automática.
- `scraper.log`: Archivo de registro que se genera durante la ejecución de `scraper.py`.
- `app.py`: Contiene la lógica de la API.
- `app.log`: Archivo de registro que se genera durante la ejecución de `app.py`.
- `consultas.txt`: Lista de ejemplos de comandos para realizar consultas con el scraper.