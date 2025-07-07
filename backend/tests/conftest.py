import pytest
import os

# Set up environment variables before any imports
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables before any tests run"""
    os.environ["OPENWEATHER_API_KEY"] = "test_api_key_12345"
    os.environ["WEATHER_API_BASE_URL"] = "https://api.openweathermap.org/data/2.5"
    yield