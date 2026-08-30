import os
import logging
import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_forecast(city):
    """Fetch 5-day weather forecast from OpenWeatherMap."""
    if not city or not isinstance(city, str):
        raise ValueError("City name must be provided")

    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        logger.error("WEATHER_API_KEY is not set")
        raise ValueError("API key missing")

    logger.info("Calling OpenWeatherMap API for: %s", city)
    res = requests.get(API_URL, params={"q": city, "appid": api_key, "units": "metric"}, timeout=5)
    res.raise_for_status()
    
    data = res.json()
    forecasts = [
        {
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"]
        }
        for item in data.get("list", [])
    ]
    return {"city": data.get("city", {}).get("name", city), "forecasts": forecasts}