from pydantic import BaseModel
from typing import Optional


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    feels_like: float
    icon: str


class LocationRequest(BaseModel):
    city: str
    country: Optional[str] = None
