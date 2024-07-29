import unittest
from unittest.mock import patch, MagicMock
from app import app
import logging
from dotenv import load_dotenv
import os

load_dotenv()



class TestApp(unittest.TestCase):

    def setUp(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename='test.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        
        logging.info("Iniciando configuración del cliente de pruebas")

        self.app = app.test_client()
        self.app.testing = True 
        logging.info("Cliente de pruebas configurado correctamente")

        logging.info("Cargando configuración de la base de datos desde .env")
        self.db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }
        logging.info("Configuración de la base de datos cargada: %s", self.db_config)

    @patch('app.psycopg2.connect')
    def test_index_route(self, mock_connect):
        logging.info("Iniciando prueba de ruta index")
        # Simular una conexión a la base de datos
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = ("Test quote", "Test author", ["tag1", "tag2"])
        mock_connect.return_value.cursor.return_value = mock_cur

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test quote", response.data)
        self.assertIn(b"Test author", response.data)
        logging.info("Prueba de ruta index completada con éxito")

    @patch('app.psycopg2.connect')
    def test_search_quotes(self, mock_connect):
        logging.info("Iniciando prueba de búsqueda de citas")
        # Simular una conexión a la base de datos
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [("Test quote", "Test author", ["tag1", "tag2"])]
        mock_connect.return_value.cursor.return_value = mock_cur

        response = self.app.get('/search?search=test&author=Test&tags=tag1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], "Test quote")
        self.assertEqual(data[0]['author'], "Test author")
        logging.info("Prueba de búsqueda de citas completada con éxito")

if __name__ == '__main__':
    logging.info("Iniciando pruebas de TestApp")
    unittest.main()
    logging.info("Pruebas de TestApp completadas")