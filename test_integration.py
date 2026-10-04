"""
Integration Tests (Bonus 3b)
Sends real HTTP requests to a running server instance.
"""
import time
import threading
import unittest
import requests
from app import app


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start Flask server in a background thread."""
        cls.server = threading.Thread(
            target=lambda: app.run(
                host="127.0.0.1", port=5002,
                debug=False, use_reloader=False
            )
        )
        cls.server.daemon = True
        cls.server.start()
        time.sleep(0.5)
        cls.url = "http://127.0.0.1:5002"
        cls.auth = ("admin", "1234")

    def test_addresses_requires_auth(self):
        """Request without credentials returns 401."""
        res = requests.get(f"{self.url}/api/addresses", timeout=3)
        self.assertEqual(res.status_code, 401)

    def test_addresses_with_auth(self):
        """Request with correct credentials returns 200."""
        res = requests.get(
            f"{self.url}/api/addresses",
            auth=self.auth, timeout=3
        )
        self.assertEqual(res.status_code, 200)

    def test_stats_endpoint(self):
        """Monitoring endpoint returns usage statistics."""
        res = requests.get(
            f"{self.url}/api/stats",
            auth=self.auth, timeout=3
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_requests", data)
        self.assertIn("forecast_calls", data)


if __name__ == "__main__":
    unittest.main()
    