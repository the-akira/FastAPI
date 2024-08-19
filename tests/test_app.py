import unittest
import requests
from multiprocessing import Process
from app.main import app
import uvicorn

# Função para rodar o servidor FastAPI em segundo plano
def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8080)

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Inicia o servidor FastAPI em um processo separado
        cls.server_process = Process(target=start_server)
        cls.server_process.start()

    @classmethod
    def tearDownClass(cls):
        # Finaliza o servidor FastAPI após os testes
        cls.server_process.terminate()
        cls.server_process.join()

    def test_read_root(self):
        response = requests.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_create_song(self):
        new_song = {
            "name": "Test Song",
            "artist": "Test Artist",
            "year": 2024
        }
        response = requests.post("http://127.0.0.1:8000/songs/", json=new_song)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], new_song["name"])

    def test_read_songs(self):
        response = requests.get("http://127.0.0.1:8000/songs/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_send_email_endpoint(self):
        email_request = {
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "Test Message"
        }
        response = requests.post("http://127.0.0.1:8000/send-email/", json=email_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Email is being sent in the background"})

    def test_scrape_endpoint(self):
        scrape_request = {
            "url": "http://example.com"
        }
        response = requests.post("http://127.0.0.1:8000/scrape/", json=scrape_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Scraping started in the background"})

    def test_read_scraped_data(self):
        response = requests.get("http://127.0.0.1:8000/scraped-data/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == "__main__":
    unittest.main()