# backend/conftest.py
import pytest
import os

# Set environment variables for tests
os.environ.setdefault("OPENWEATHER_API_KEY", "local_test_key")
os.environ.setdefault("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    yield