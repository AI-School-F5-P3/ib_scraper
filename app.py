import logging
from flask import Flask, render_template, jsonify
import psycopg2
from scraper import QuoteScraper
from dotenv import load_dotenv
import os

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

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
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT text, author, tags FROM quotes ORDER BY RANDOM() LIMIT 1")
        quote = cur.fetchone()
        cur.close()
        conn.close()
        
        return render_template('index.html', quote=quote)
    except Exception as e:
        logging.error(f"Error en la ruta index: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/random_quote')
def random_quote():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT text, author, tags FROM quotes ORDER BY RANDOM() LIMIT 1")
        quote = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            "text": quote[0],
            "author": quote[1],
            "tags": quote[2]
        })
    except Exception as e:
        logging.error(f"Error al obtener cita aleatoria: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def create_table_if_not_exists():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL UNIQUE,
            author VARCHAR(100) NOT NULL,
            tags TEXT[],
            source VARCHAR(50)
        )
        """)
        conn.commit()
    except Exception as e:
        logging.error(f"Error creating table: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Llama a esta función antes de iniciar la aplicación
create_table_if_not_exists()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)