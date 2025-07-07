import httpx
import logging
from fastapi import HTTPException
from typing import Optional

from app.models import WeatherResponse
from app.config import settings

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self):
        if not settings.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY environment variable is required")
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.WEATHER_API_BASE_URL

    async def get_weather(self, city: str, country: Optional[str] = None) -> WeatherResponse:
        location = f"{city},{country}" if country else city

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={"q": location, "appid": self.api_key, "units": "metric"},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return WeatherResponse(
                    location=f"{data['name']}, {data['sys']['country']}",
                    temperature=data['main']['temp'],
                    description=data['weather'][0]['description'].title(),
                    humidity=data['main']['humidity'],
                    wind_speed=data['wind']['speed'],
                    feels_like=data['main']['feels_like'],
                    icon=data['weather'][0]['icon']
                )

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail="City not found")
                raise HTTPException(status_code=500, detail="Weather service unavailable")
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Weather service timeout")
            except Exception as e:
                logger.error(f"Weather service error: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
