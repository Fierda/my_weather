from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # For local .env loading, optional with pydantic-settings


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    WEATHER_API_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    class Config:
        env_file = ".env"  # Optional: fallback if load_dotenv() is removed


# Instantiate once
settings = Settings()
