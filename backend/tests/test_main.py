# test_main.py
import os
# Set environment variables BEFORE importing the app
os.environ["OPENWEATHER_API_KEY"] = "test_api_key_12345"
os.environ["WEATHER_API_BASE_URL"] = "https://api.openweathermap.org/data/2.5"

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "weather-api"}

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Weather API is running" in response.json()["message"]