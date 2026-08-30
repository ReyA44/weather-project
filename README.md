# Weather Forecast App 🌤️

A weather forecast application built as part of the Software Development chapter in the Fullstack course.

## Features
- Add, view, and delete saved addresses
- Get 5-day weather forecast for any city
- Uses OpenWeatherMap free API

## Tech Stack
- Python 3.13, Flask, requests
- Testing: pytest + pytest-cov
- Containerization: Docker

## Setup
1. Clone the repo
2. Create virtual environment: `python3 -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set API key: `export WEATHER_API_KEY=your_key`
5. Run: `python app.py`