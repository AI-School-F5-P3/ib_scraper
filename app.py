import logging
from flask import Flask, render_template, jsonify
import psycopg2
from scraper import QuoteScraper
from dotenv import load_dotenv
import os

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Crear una instancia de QuoteScraper
scraper = QuoteScraper(db_config)

@app.route('/')
def index():
    try:
        logging.info("Manejando solicitud a la ruta index.")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT text, author, tags FROM quotes ORDER BY RANDOM() LIMIT 1")
        quote = cur.fetchone()
        cur.close()
        conn.close()
        
        logging.info("Cita aleatoria obtenida exitosamente para la ruta index.")
        return render_template('index.html', quote=quote)
    except Exception as e:
        logging.error(f"Error en la ruta index: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/random_quote')
def random_quote():
    try:
        logging.info("Manejando solicitud a la ruta random_quote.")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT text, author, tags FROM quotes ORDER BY RANDOM() LIMIT 1")
        quote = cur.fetchone()
        cur.close()
        conn.close()
        
        logging.info("Cita aleatoria obtenida exitosamente para la API.")
        return jsonify({
            "text": quote[0],
            "author": quote[1],
            "tags": quote[2]
        })
    except Exception as e:
        logging.error(f"Error al obtener cita aleatoria: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting app on port {port}.")
    print(f" * Running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
    