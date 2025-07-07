import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file if present


class Settings:
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    WEATHER_API_BASE_URL: str = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5")


settings = Settings()
