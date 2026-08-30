import unittest
from unittest.mock import patch, Mock
from address_manager import AddressManager
from weather_service import get_forecast
from app import app


class TestAddressManager(unittest.TestCase):
    def setUp(self):
        self.mgr = AddressManager()

    def test_add_address_success(self):
        result = self.mgr.add("Tel Aviv")
        self.assertIn("Tel Aviv", result)

    def test_add_address_empty_fails(self):
        with self.assertRaises(ValueError):
            self.mgr.add("")

    def test_get_all(self):
        self.mgr.add("London")
        self.assertEqual(self.mgr.get_all(), ["London"])

    def test_delete_address(self):
        self.mgr.add("Paris")
        self.assertTrue(self.mgr.delete("Paris"))
        self.assertFalse(self.mgr.delete("Paris"))


class TestWeatherService(unittest.TestCase):
    def test_missing_city_raises(self):
        with self.assertRaises(ValueError):
            get_forecast("")

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_raises(self):
        with self.assertRaises(ValueError):
            get_forecast("Rome")

    @patch("weather_service.requests.get")
    @patch.dict("os.environ", {"WEATHER_API_KEY": "dummy_key"})
    def test_successful_forecast(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "city": {"name": "Haifa"},
            "list": [
                {
                    "dt_txt": "2026-08-30 12:00:00",
                    "main": {"temp": 28.5},
                    "weather": [{"description": "clear sky"}]
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data = get_forecast("Haifa")
        self.assertEqual(data["city"], "Haifa")
        self.assertEqual(len(data["forecasts"]), 1)


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_addresses_empty(self):
        response = self.client.get("/api/addresses")
        self.assertEqual(response.status_code, 200)

    def test_post_and_delete_address(self):
        res_post = self.client.post("/api/addresses", json={"city": "Eilat"})
        self.assertEqual(res_post.status_code, 201)

        res_del = self.client.delete("/api/addresses", json={"city": "Eilat"})
        self.assertEqual(res_del.status_code, 200)


if __name__ == "__main__":
    unittest.main()