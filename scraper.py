import requests
from bs4 import BeautifulSoup
import psycopg2
import logging
import time
import schedule
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class QuoteScraper:
    def __init__(self, db_config, base_url='https://quotes.toscrape.com'):
        self.base_url = base_url
        self.db_config = db_config
        self.conn = None
        self.cursor = None
        self.setup_logging()
    def setup_logging(self):
            logging.basicConfig(filename='scraper.log', level=logging.INFO,
                                format='%(asctime)s:%(levelname)s:%(message)s')

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            logging.info("Conexión exitosa a la base de datos.")
        except Exception as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            author VARCHAR(100) NOT NULL,
            tags TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def scrape_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            for quote in quotes:
                self.process_quote(quote)
            self.conn.commit()
            logging.info(f"Datos extraídos y guardados de la página: {url}")
            return self.get_next_page(soup)
        except Exception as e:
            logging.error(f"Error al scrapear la página {url}: {e}")
            return None

    def process_quote(self, quote):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        self.insert_quote(text, author, tags)

    def insert_quote(self, text, author, tags):
        insert_query = '''
        INSERT INTO quotes (text, author, tags)
        VALUES (%s, %s, %s)
        ON CONFLICT (text) DO NOTHING
        '''
        self.cursor.execute(insert_query, (text, author, tags))

    def get_next_page(self, soup):
        next_page = soup.find('li', class_='next')
        if next_page:
            return self.base_url + next_page.find('a')['href']
        return None

    def run(self):
        self.connect_to_db()
        self.create_table()
        url = self.base_url
        while url:
            url = self.scrape_page(url)
        self.close_connection()
        logging.info("Scraping completado. Conexión a la base de datos cerrada.")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

class AutomaticUpdater:
    def __init__(self, db_config, update_interval=24):
        self.db_config = db_config
        self.update_interval = update_interval
        self.scraper = QuoteScraper(db_config)

    def update_database(self):
        logging.info("Iniciando actualización automática de la base de datos.")
        self.scraper.run()
        logging.info("Actualización automática completada.")

    def schedule_updates(self):
        schedule.every(self.update_interval).hours.do(self.update_database)
        logging.info(f"Actualizaciones programadas cada {self.update_interval} horas.")

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    db_config = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }
    
update_interval = int(os.getenv("UPDATE_INTERVAL", 24))
    
    # Crear una instancia de QuoteScraper y ejecutar el scraping inmediatamente
scraper = QuoteScraper(db_config)
scraper.run()
    
    # Luego, configurar las actualizaciones automáticas
updater = AutomaticUpdater(db_config, update_interval)
updater.schedule_updates()