# Quote Scraper

Este proyecto es un scraper automatizado que extrae citas de la página web [https://quotes.toscrape.com](https://quotes.toscrape.com) y las almacena en una base de datos PostgreSQL. El scraper está diseñado para ejecutarse inicialmente y luego actualizarse automáticamente a intervalos regulares.

## Características

- Extrae citas, autores y etiquetas de [https://quotes.toscrape.com]
- Almacena los datos en una base de datos PostgreSQL
- Actualizaciones automáticas programadas
- Proporciona una API para obtener citas a través de solicitudes HTTP GET
- Interfaz web para visualizar citas aleatorias
- Función de búsqueda de citas por texto, autor y etiquetas
- Página web alojada en PythonAnywhere.

## Requisitos

- Python 3.1x
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

### O...

...simplemente abre la página https://mellorio.pythonanywhere.com/ en tu navegador!

## Uso

- Ejecuta el script principal para realizar una extracción inicial y almacenar las citas obtenidas en una base de datos PostgreSQL. Además, se programará para realizar actualizaciones automáticas según el intervalo especificado en las variables de entorno:
`python scraper.py`

- Ejecuta el script para iniciar la aplicación Flask, que proporcionará una página web simple con una cita aleatoria y un botón "Nueva Cita" para cambiar a otra cita aleatoria:
`python app.py`

- Accede a la aplicación web a través de tu navegador:
  - La página principal mostrará una cita aleatoria con un botón "Nueva Cita" para cambiar a otra cita aleatoria.
  - Utiliza el botón "Buscar Cita" para acceder a la página de búsqueda.

- En la página de búsqueda, puedes:
  - Buscar citas por texto
  - Filtrar por autor
  - Seleccionar una o varias etiquetas
  - Utilizar el botón "Limpiar selección de tags" para deseleccionar todas las etiquetas

- También puedes hacer consultas utilizando la funcionalidad integrada de herramientas de consulta. Los comandos para estas consultas están listados en el archivo `consultas.txt`. Asegúrate de seguir el formato correcto de los comandos para obtener resultados precisos.


## Estructura del Proyecto

- `requirements.txt`: Lista de dependencias del proyecto.
- `scraper.py`: Contiene la lógica principal del scraper y la funcionalidad actualización automática.
- `scraper.log`: Archivo de registro que se genera durante la ejecución de `scraper.py`.
- `app.py`: Contiene la lógica de la API.
- `app.log`: Archivo de registro que se genera durante la ejecución de `app.py`.
- `consultas.txt`: Lista de ejemplos de comandos para realizar consultas con el scraper.
- `templates/`: Directorio que contiene las plantillas HTML para la interfaz web.
  - `index.html`: Plantilla para la página principal con cita aleatoria.
  - `busqueda.html`: Plantilla para la página de búsqueda de citas.
- Página web alojada en PythonAnywhere.
- `test_app.py` y `test_scraper.py`: Incluyen pruebas de verificación de distintos métodos utilizados en la app.
- `test.log`: Archivo de registro que se genera durante la ejecución de `test_app.py` y `test_scraper.py`.