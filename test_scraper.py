import unittest
from unittest.mock import patch, MagicMock
from scraper import QuoteScraper
import logging

# Configuración del logging
logging.basicConfig(filename='test.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class TestQuoteScraper(unittest.TestCase):

    def setUp(self):
        self.db_config = {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "port": "test_port"
        }
        self.scraper = QuoteScraper(self.db_config)
        logging.info("Configurando TestQuoteScraper")

    @patch('scraper.psycopg2.connect')
    def test_connect_to_db(self, mock_connect):
        logging.info("Iniciando prueba de conexión a la base de datos")
        self.scraper.connect_to_db()
        mock_connect.assert_called_once_with(**self.db_config)
        logging.info("Prueba de conexión a la base de datos completada con éxito")

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_scrape_page(self, mock_bs, mock_get):
        logging.info("Iniciando prueba de raspado de página")
        mock_response = MagicMock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        mock_soup = MagicMock()
        mock_soup.find_all.return_value = []
        mock_bs.return_value = mock_soup

        self.scraper.conn = MagicMock()
        self.scraper.cursor = MagicMock()

        # Mock get_next_page para que devuelva None
        self.scraper.get_next_page = MagicMock(return_value=None)

        result = self.scraper.scrape_page("http://test.com")
        self.assertIsNone(result)

        # Verificar que get_next_page fue llamado
        self.scraper.get_next_page.assert_called_once_with(mock_soup)
        logging.info("Prueba de raspado de página completada con éxito")

    @patch('scraper.requests.get')
    def test_process_and_insert_author(self, mock_get):
        logging.info("Iniciando prueba de procesamiento e inserción de autor")
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <span class="author-born-date">Test Date</span>
            <span class="author-born-location">Test Location</span>
            <div class="author-description">Test Description</div>
        </html>
        """
        mock_get.return_value = mock_response

        self.scraper.conn = MagicMock()
        self.scraper.cursor = MagicMock()
        self.scraper.cursor.fetchone.return_value = (1,)

        author_id = self.scraper.process_and_insert_author("Test Author", "http://test.com")
        self.assertEqual(author_id, 1)
        logging.info("Prueba de procesamiento e inserción de autor completada con éxito")

if __name__ == '__main__':
    logging.info("Iniciando pruebas de TestQuoteScraper")
    unittest.main()
    logging.info("Pruebas de TestQuoteScraper completadas")