from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # For local .env loading, optional with pydantic-settings


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    WEATHER_API_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    class Config:
        env_file = ".env"  # Optional: fallback if load_dotenv() is removed


# Instantiate once
settings = Settings()
