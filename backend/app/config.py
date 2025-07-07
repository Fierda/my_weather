from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Loads .env for local development


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    WEATHER_API_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    class Config:
        env_file = ".env"  # optional: fallback if load_dotenv is removed

# Instantiate once
settings = Settings()
