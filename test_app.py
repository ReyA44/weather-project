import unittest
from unittest.mock import patch, Mock
from address_manager import AddressManager
from weather_service import get_forecast
from app import app
import base64

# Test class for the AddressManager — each method tests one behavior
class TestAddressManager(unittest.TestCase):
    def setUp(self):
        # Runs before each test: creating a fresh AddressManager instance
        # so tests don't affect each other
        self.mgr = AddressManager()

    def test_add_address_success(self):
        # Adding a valid city and checking it appears in the returned list
        result = self.mgr.add("Tel Aviv")
        self.assertIn("Tel Aviv", result)

    def test_add_address_empty_fails(self):
        # Verifying that adding an empty string raises a ValueError
        with self.assertRaises(ValueError):
            self.mgr.add("")

    def test_get_all(self):
        # Adding a city, then checking get_all() returns it
        self.mgr.add("London")
        self.assertEqual(self.mgr.get_all(), ["London"])

    def test_delete_address(self):
        self.mgr.add("Paris")
        # First delete should succeed (returns True)
        self.assertTrue(self.mgr.delete("Paris"))
        # Second delete should fail because "Paris" is already removed (returns False)
        self.assertFalse(self.mgr.delete("Paris"))


# Test class for the weather service — tests the get_forecast function
class TestWeatherService(unittest.TestCase):
    def test_missing_city_raises(self):
        # Passing an empty city name should raise a ValueError
        with self.assertRaises(ValueError):
            get_forecast("")

    # Temporarily clearing all environment variables so WEATHER_API_KEY is missing
    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_raises(self):
        # Without an API key set, calling get_forecast should raise a ValueError
        with self.assertRaises(ValueError):
            get_forecast("Rome")

    # Creating a mock for requests.get so we don't make a real HTTP call
    @patch("weather_service.requests.get")
    # Setting a fake API key in the environment for this test
    @patch.dict("os.environ", {"WEATHER_API_KEY": "dummy_key"})
    def test_successful_forecast(self, mock_get):
        # Creating a mock response object to simulate what the API would return
        mock_response = Mock()
        # Defining what mock_response.json() should return — fake weather data
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
        # Making raise_for_status() do nothing (simulating a successful HTTP response)
        mock_response.raise_for_status = Mock()
        # When requests.get() is called, return our fake response instead
        mock_get.return_value = mock_response

        # Calling the real function — but it will use our mock instead of the real API
        data = get_forecast("Haifa")
        # Verifying the function correctly extracted the city name
        self.assertEqual(data["city"], "Haifa")
        # Verifying we got exactly 1 forecast entry back
        self.assertEqual(len(data["forecasts"]), 1)



# (Keep TestAddressManager and TestWeatherService as they are)

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Create standard Basic Auth header (admin:1234)
        encoded_auth = base64.b64encode(b"admin:1234").decode("ascii")
        self.headers = {"Authorization": f"Basic {encoded_auth}"}

    def test_get_addresses_empty(self):
        response = self.client.get("/api/addresses", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_and_delete_address(self):
        res_post = self.client.post(
            "/api/addresses",
            json={"city": "Eilat"},
            headers=self.headers
        )
        self.assertEqual(res_post.status_code, 201)

        res_del = self.client.delete(
            "/api/addresses",
            json={"city": "Eilat"},
            headers=self.headers
        )
        self.assertEqual(res_del.status_code, 200)


# This block runs the tests when executing the file directly (python test_app.py)
if __name__ == "__main__":
    unittest.main()